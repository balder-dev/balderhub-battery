import balder

class BatteryTestCriteriaConfig(balder.Feature):
    """Test Criteria Configuration object to define criteria the test should use"""

    @property
    def validation_with_battery_levels(self) -> list[float]:
        """
        :return: returns a list of battery levels the test should use
        """
        return [1.0, 0.8, 0.6, 0.4, 0.2, 0.1, 0]
