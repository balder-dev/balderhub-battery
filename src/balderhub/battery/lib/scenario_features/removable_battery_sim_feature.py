import logging
from typing import Union, Generator

from .battery_sim_feature import BatterySimFeature

logger = logging.getLogger(__name__)


class RemovableBatterySimFeature(BatterySimFeature):
    """
    Scenario Level feature implementation of :class:`balderhub.battery.lib.scenario_features.BatterySimFeature` that
    can be used for removable batteries.
    """

    @property
    def battery_inserted(self) -> bool:
        """
        :return: returns True if the battery is inserted at the moment, otherwise False
        """
        raise NotImplementedError

    def insert_battery(self) -> None:
        """
        This callback simulates the inserting of the battery into the device.
        """
        raise NotImplementedError()

    def remove_battery(self):
        """
        This callback simulates the removement of the battery into the device.
        """
        raise NotImplementedError

    def _fixture_teardown(self, level_before: Union[float, None]):
        if level_before is not None:
            # device was powered on before entering this fixture
            current_level = self.get_current_active_level()
            if current_level == level_before:
                logger.info(f"battery has the same battery level of {current_level} before entering this fixture "
                            f"like it has now -> do not change it")
            else:
                logger.info(f"battery has a different battery level (currently {current_level}) like it has before "
                            f"entering this fixture -> reset battery level back to {level_before}")
                self.set_to(level_before)

            if not self.battery_inserted:
                self.insert_battery()
        else:
            if self.battery_inserted:
                logger.info('battery is still inserted but was not inserted before entering this fixture -> remove it')
                self.remove_battery()
            else:
                logger.info(
                    'battery is not inserted and was not inserted before entering this fixture too -> do nothing'
                )

    def fixt_make_sure_device_is_powered_on(
            self,
            with_level: float = 1,
            restart_in_construct: bool = False,
            restore_entry_state: bool = True
    ) -> Generator[None, None, None]:
        """
        This is a fixture that ensures that the device is powered one. It will set the battery to the provided level.

        .. note::
            You can directly use this fixture within balder like:

            .. code-block:: python

                @balder.fixture(...)
                def my_fixture(...):
                    yield from feat.fixt_make_sure_device_is_powered_on(...)

        :param with_level: the level the battery should be set to
        :param restart_in_construct: if True, the fixtures will definitely restart the device (power-off and re power
                                     on), even if the device was already powered on before entering this fixture
        :param restore_entry_state: if Ture, the fixture will restore the state of the battery like it was before
                                    entering this fixture within the teardown code
        :return: the generator object to use directly as balder fixture
        """
        # TODO also within higher version of feature

        level_before = None
        if self.battery_inserted:
            logger.info('Battery is still inserted -> check battery level')
            level_before = self.get_current_active_level()
            if level_before != with_level:
                logger.info(f'- current level is {level_before}, but should be {with_level} -> adjust')
                self.set_to(with_level)
            else:
                logger.info('- current level is the expected level -> do not change level')
            if restart_in_construct:
                logger.info('- restarting is required -> so remove battery and insert it again')
                self.remove_battery()
                self.insert_battery()
        else:
            logger.info(f'no battery is inserted -> adjust level to {with_level} and insert battery')
            self.set_to(with_level)
            self.insert_battery()
        yield
        if not restore_entry_state:
            return
        self._fixture_teardown(level_before=level_before)


    def fixt_make_sure_device_is_powered_off(self, restore_entry_state: bool = True) -> Generator[None, None, None]:
        """
        This is a fixture that ensures that the device is powered off. It will remove the battery if this is not
        already done before entering this fixture.

        .. note::
            You can directly use this fixture within balder like:

            .. code-block:: python

                @balder.fixture(...)
                def my_fixture(...):
                    yield from feat.fixt_make_sure_device_is_powered_off(...)

        :param restore_entry_state: if Ture, the fixture will restore the state of the battery like it was before
                                    entering this fixture within the teardown code
        :return: the generator object to use directly as balder fixture
        """
        level_before = None
        if self.battery_inserted:
            logger.info('Battery is still inserted -> remove it')
            level_before = self.get_current_active_level()
            self.remove_battery()
        else:
            logger.info('Battery was already removed -> nothing to do')
        yield
        if not restore_entry_state:
            return
        self._fixture_teardown(level_before=level_before)
