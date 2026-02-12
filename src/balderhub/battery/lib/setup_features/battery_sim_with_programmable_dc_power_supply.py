import decimal

import balderhub.powersupply.lib.scenario_features

from ..scenario_features.removable_battery_sim_feature import RemovableBatterySimFeature


# TODO or should we move this in contrib of `balderhub-powersupply`?
class BatterySimWithProgrammableDcPowerSupply(RemovableBatterySimFeature):
    """
    Setup Level feature that can be used to simulate the battery behavior with programmable dc power supply instruments.

    .. note::
        Please note: This feature is for simple tests, because it does not use the full characteristic and simulates the
        different values by voltage change only.
    """

    power_supply = balderhub.powersupply.lib.scenario_features.DCPowerSupplyFeature()

    @property
    def min_allowed_voltage(self):
        """
        :return: security property to limit the minimal allowed voltage the whole feature is allowed to use
        """
        raise NotImplementedError

    @property
    def max_allowed_voltage(self):
        """
        :return: security property to limit the maximum allowed voltage the whole feature is allowed to use
        """
        raise NotImplementedError

    @property
    def battery_inserted(self) -> bool:
        return self.power_supply.is_enabled()

    def get_current_active_voltage(self) -> float:
        """
        :return: returns the current active voltage that is applied at the instrument
        """
        return float(self.power_supply.get_configured_voltage())

    def get_current_active_level(self) -> float:
        cur_voltage = self.get_current_active_voltage()
        return self.discharge_characteristic.reverse_get_level_for_voltage(cur_voltage)

    def _get_secured_voltage(self, for_percentage_of: float) -> float:
        voltage = self.discharge_characteristic.get_voltage_for(for_percentage_of)
        assert self.min_allowed_voltage <= voltage <= self.max_allowed_voltage, \
            (f"got invalid voltage of {voltage}V (min: {self.min_allowed_voltage} | max: {self.max_allowed_voltage}) "
             f"from {self.discharge_characteristic.__class__.__name__}")
        return voltage

    def insert_battery(self):
        current_voltage = self.get_current_active_voltage()
        if not self.min_allowed_voltage <= current_voltage <= self.max_allowed_voltage:
            raise ValueError(
                f'can not insert battery because current configured voltage of {current_voltage}V is not between '
                f'allowed voltage range ({self.min_allowed_voltage}V - {self.max_allowed_voltage}V)')
        self.power_supply.power_on()

    def set_to(self, battery_level: float):
        voltage_to_set = self._get_secured_voltage(battery_level)
        self.power_supply.set_configured_voltage(decimal.Decimal.from_float(voltage_to_set))

    def remove_battery(self):
        self.power_supply.power_off()
