from abc import ABC, abstractmethod


class BaseBatteryDischargeCharacteristic(ABC):
    """
    Base Battery Discharge Characteristic that describes the discharge characteristic of a custom battery.
    """

    @abstractmethod
    def get_voltage_for(self, remaining_capacity_percent: float, with_load_ohm: float = 15_000) -> float:
        """
        This method returns the current battery voltage
        :param remaining_capacity_percent: the remaining capacity of the battery in percent (0..1)
        :param with_load_ohm: the load resistance that is expected under that voltage # TODO
        :return: the expected battery voltage in ohm
        """

    @abstractmethod
    def reverse_get_level_for_voltage(self, voltage: float, with_load_ohm: float = 15_000) -> float:
        """
        This method is the reverse method of the :meth:`BaseBatteryDischargeCharacteristic.get_voltage_for` method.
        It returns the expected level for the given voltage.

        :param voltage: the voltage the expected level should be returned
        :param with_load_ohm: the load resistance that is expected under that voltage # TODO
        :return: the expected battery level (0..1)
        """


    @abstractmethod
    def get_inner_resistance_for(self, remaining_capacity_percent: float, with_load_ohm: float = 15_000) -> float:
        """
        This method returns the current battery inner resistance value in Ohm.

        :param remaining_capacity_percent: the remaining capacity of the battery in percent (0..1)
        :param with_load_ohm: the load resistance that is expected under that voltage
        :return:
        """
