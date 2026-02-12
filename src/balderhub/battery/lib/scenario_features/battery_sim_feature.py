import balder

from balderhub.battery.lib.utils.battery_discharge_characteristic.base_battery_discharge_characteristic import \
    BaseBatteryDischargeCharacteristic


class BatterySimFeature(balder.Feature):
    """Base scenario level feature that provides bindings to a device that can simulate batteries"""

    @property
    def discharge_characteristic(self) -> BaseBatteryDischargeCharacteristic:
        """
        :return: returns a specific Battery Characteristic that describes the behavior of the battery discharge
        """
        raise NotImplementedError()

    def set_to(self, battery_level: float):
        """
        This method sets the battery level to the provided value (needs to be between 0 and 1)
        :param battery_level:
        :return:
        """
        raise NotImplementedError

    def get_current_active_level(self) -> float:
        """
        This method returns the current setted battery level.
        :return: the current setted battery level
        """
        raise NotImplementedError
