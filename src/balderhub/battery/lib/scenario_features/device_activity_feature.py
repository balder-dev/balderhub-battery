import logging
import time


import balder

logger = logging.getLogger(__name__)


class DeviceActivityFeature(balder.Feature):
    """
    Scenario Level feature that allows to check if a device is active or inactive.
    """

    def prepare(self) -> None:
        """
        Prepares the environment to be able to run the :meth:`DeviceActivityFeature.is_active` method.

        .. note::
            This method will not be called before EVERY ``is_active`` call, but when using this
            feature you need to make sure that the :meth:`DeviceActivityFeature.is_active` call is within the
            ``prepare()`` and ``cleanup`` call.
        """

    def is_active(self) -> bool:
        """
        :return: returns True if the device is active, False otherwise
        """
        raise NotImplementedError()

    def cleanup(self) -> None:
        """
        Cleans up the environment to be able to run the :meth:`DeviceActivityFeature.is_active` method.

        .. note::
            This method will not be called before EVERY ``is_active`` call, but when using this
            feature you need to make sure that the :meth:`DeviceActivityFeature.is_active` call is within the
            ``prepare()`` and ``cleanup`` call.
        """

    def wait_to_be_active(self, timeout_sec: float):
        """
        This method will wait up to ``timeout_sec`` seconds until the device should be shown ACTIVE. If it does not
        do that within the ``timeout_sec`` the method will raise a TimeoutError.

        .. note::
            When using this method please make sure that it is embedded within the ``prepare()`` and ``cleanup`` call.

        :param timeout_sec: maximum time to wait for a device to be ACTIVE
        """
        logger.debug(f'wait for maximal {timeout_sec} seconds that sensor is active')
        start_time = time.perf_counter()
        while (time.perf_counter() - start_time) < timeout_sec:
            if self.is_active():
                logger.debug(f'device is ACTIVE now (after {time.perf_counter() - start_time} seconds)')
                return
        raise TimeoutError(f'device is still not active while waiting for {timeout_sec} seconds')

    def wait_to_be_inactive(self, timeout_sec: float):
        """
        This method will wait up to ``timeout_sec`` seconds until the device should be shown INACTIVE. If it does not
        do that within the ``timeout_sec`` the method will raise a TimeoutError.

        .. note::
            When using this method please make sure that it is embedded within the ``prepare()`` and ``cleanup`` call.

        :param timeout_sec: maximum time to wait for a device to be INACTIVE
        """
        logger.debug(f'wait for maximal {timeout_sec} seconds that sensor is inactive')
        start_time = time.perf_counter()
        while (time.perf_counter() - start_time) < timeout_sec:
            if not self.is_active():
                logger.debug(f'device is INACTIVE now (after {time.perf_counter() - start_time} seconds)')
                return
        raise TimeoutError(f'device is still active after waiting for {timeout_sec} seconds')
