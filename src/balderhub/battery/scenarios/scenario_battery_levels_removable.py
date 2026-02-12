import balder
from balder import connections

from balderhub.battery.lib.scenario_features import BatteryTestCriteriaConfig
from balderhub.battery.lib.scenario_features.battery_level_reader import BatteryLevelReader
from balderhub.battery.lib.scenario_features.removable_battery_sim_feature import RemovableBatterySimFeature


class ScenarioBatteryLevelRemovable(balder.Scenario):
    """
    Basic Test scenario that validates the correctness for reading battery levels within the device-under-test. It uses
    the :class:`balderhub.battery.lib.scenario_features.RemovableBatterySimFeature` to emulate the battery and reads
    back the battery level from the DUT and validates that they are the same.
    """

    class BatterySim(balder.Device):
        """the battery simulation device"""
        sim = RemovableBatterySimFeature() # TODO use different one for Non-Removable to

    @balder.connect(BatterySim, over_connection=connections.DCPowerConnection)  # pylint: disable=undefined-variable
    class DeviceUnderTest(balder.Device):
        """the device under test"""
        test_config = BatteryTestCriteriaConfig()

    @balder.connect(DeviceUnderTest, over_connection=balder.Connection)  # pylint: disable=undefined-variable
    class ReaderDevice(balder.Device):
        """a device that can read the battery level from the DUT"""
        display = BatteryLevelReader()

    @balder.fixture('variation')
    def power_off_and_restore(self):
        """
        variation level feature that makes sure that the device is powered off before entering the variation and
        restores it within the teardown part
        """
        yield from self.BatterySim.sim.fixt_make_sure_device_is_powered_off()

    @balder.fixture('testcase')
    def device_is_powered_off(self):
        """testcase level feature that makes sure that the device is powered off before entering the test"""
        yield from self.BatterySim.sim.fixt_make_sure_device_is_powered_off(restore_entry_state=False)

    @balder.parametrize_by_feature(
        'battery_level', (DeviceUnderTest, 'test_config', 'validation_with_battery_levels')
    )
    def test_battery_level_detection(self, battery_level: float):
        """
        This test inserts the battery and then tries to read the battery level. It validates that both are equal.

        :param battery_level: feature-parametrization for all battery levels that should be validated (defined by
                              :meth:`BatteryTestCriteriaConfig.validation_with_battery_levels`
        """
        # TODO we need alternative that allows reading while system is powered on

        assert self.ReaderDevice.display.read_current_battery_level() is None, \
            "was able to read Battery level before setting the battery level"

        self.BatterySim.sim.set_to(battery_level)

        try:
            self.BatterySim.sim.insert_battery()

            # TODO what is with start up time?
            read_battery_level = self.ReaderDevice.display.read_current_battery_level()
            assert read_battery_level is not None, \
                'device was unable to read the battery level after battery was inserted'

            expected_min_level = max((0, battery_level - self.ReaderDevice.display.expected_accuracy_plusminus_percent))
            expected_max_level = min((1, battery_level + self.ReaderDevice.display.expected_accuracy_plusminus_percent))
            assert expected_min_level <= read_battery_level <= expected_max_level, \
                (f"received unexpected value {read_battery_level} - "
                 f"expected {battery_level} (min: {expected_min_level} | max: {expected_max_level})")
        finally:
            self.BatterySim.sim.remove_battery()
