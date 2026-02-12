from abc import ABC, abstractmethod

import bisect

from .base_battery_discharge_characteristic import BaseBatteryDischargeCharacteristic


class BaseDiscreteBatteryDischargeCharacteristic(BaseBatteryDischargeCharacteristic, ABC):
    """
    Base discrete Battery Discharge Characteristic; needs to be overwritten and can be used for battery level tests
    without defining a full discharge characteristic model
    """

    @property
    @abstractmethod
    def voltage_max(self) -> float:
        """
        :return: returns the maximum voltage the battery can have (f.e. without any load)
        """

    @property
    @abstractmethod
    def voltage_cut_off(self) -> float:
        """
        :return: returns the CUT-OFF voltage at which the device should not work anymore
        """

    @property
    @abstractmethod
    def edges(self) -> dict[float, tuple[float, float]]:
        """
        :return: returns a dictionary with the battery level as key (0..1) and a tuple with the voltage and the inner
                 resistance in Ohm as value
        """

    def _validate_edges(self, edges: dict[float, tuple[float, float]]) -> None:
        value_before = max(v[0] for v in edges.values())
        for key in sorted(edges.keys(), reverse=True):

            if key > 1 or key < 0:
                raise ValueError(f'edge key {key} is out of range (needs to be between 0 and 1)')
            if not isinstance(edges[key], tuple):
                raise TypeError('values in edges needs to be tuples')

            voltage = edges[key][0]
            resistance = edges[key][1]

            if not isinstance(voltage, float):
                raise TypeError('values in edges needs to be tuples with two floats (voltage, resistance)')
            if not isinstance(resistance, float):
                raise TypeError('values in edges needs to be tuples with two floats (voltage, resistance)')
            if resistance < 0:
                raise ValueError('the resistance value needs to be higher than 0')
            if voltage > self.voltage_max:
                raise ValueError('calculation returns {voltage}V but max-voltage is set to {self.voltage_max}V')
            if voltage < self.voltage_cut_off:
                raise ValueError(
                    f'calculation returns {voltage}V but cut-off-voltage is set to {self.voltage_cut_off}V')
            if edges[key][0] > value_before:
                raise ValueError('the values in `edges` must also decrease or remain the same as the battery level '
                                 'decreases')

    def get_voltage_for(self, remaining_capacity_percent: float, with_load_ohm: float = 15_000) -> float:
        edges = self.edges
        self._validate_edges(edges)

        sorted_keys = sorted(edges.keys())
        idx = bisect.bisect_right(sorted_keys, remaining_capacity_percent) - 1
        relevant_key = sorted_keys[idx] if idx >= 0 else sorted_keys[0]  # Fallback to lowest

        result = edges[relevant_key][0]

        if result > self.voltage_max:
            raise ValueError(f'calculation returns {result}V but max-voltage is set to {self.voltage_max}V')
        if result < self.voltage_cut_off:
            raise ValueError(f'calculation resturns {result}V but cut-off-voltage is set to {self.voltage_cut_off}V')
        return result

    def reverse_get_level_for_voltage(self, voltage: float, with_load_ohm: float = 15_000) -> float:
        reverse_dict = {v[0]: k for k, v in self.edges.items()}
        sorted_keys = sorted(reverse_dict.keys())
        idx = bisect.bisect_right(sorted_keys, voltage) - 1
        relevant_key = sorted_keys[idx] if idx >= 0 else sorted_keys[0]  # Fallback to lowest

        result = reverse_dict[relevant_key]
        if result < 0 or result > 1:
            raise ValueError('result needs to be between 0 and 1')
        return result

    def get_inner_resistance_for(self, remaining_capacity_percent: float, with_load_ohm: float = 15_000) -> float:
        edges = self.edges
        self._validate_edges(edges)

        sorted_keys = sorted(edges.keys())
        idx = bisect.bisect_right(sorted_keys, remaining_capacity_percent) - 1
        relevant_key = sorted_keys[idx] if idx >= 0 else sorted_keys[0]  # Fallback to lowest

        return edges[relevant_key][1]
