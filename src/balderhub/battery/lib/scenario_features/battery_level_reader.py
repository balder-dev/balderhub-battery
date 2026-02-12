from typing import Union

import balder


class BatteryLevelReader(balder.Feature):
    """
    Scenario level feature that provides a interface for reading the battery level
    """

    @property
    def expected_accuracy_plusminus_percent(self) -> float:
        """
        :return: returns the expected accuracy in percent (+/- from expected value)
        """
        # TODO maybe we need jitter and percent?
        return 0.01

    def read_current_battery_level(self) -> Union[float, None]:
        """reads the current battery level (return None if the device is powered off)"""
        raise NotImplementedError()
