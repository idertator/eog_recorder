from typing import Optional

from numpy import ndarray

from saccrec.core.enums import Channel


class Saccade:

    def __init__(
        self,
        onset: int, offset: int,
        test: 'Test', channel: Channel,
        ignore_calibration: bool = False
    ):
        self._onset = onset
        self._offset = offset
        self._test = test
        self._channel = channel
        self._ignore_calibration = ignore_calibration

        self._amplitude = None
        self._duration = None
        self._max_velocity = None

        self._sampling_interval = test.study.sampling_interval

    def __str__(self) -> str:
        return _('Sácada: {onset} -> {offset}').format(
            onset=self.onset,
            offset=self.offset
        )

    def __json__(self) -> dict:
        return (self._onset, self._offset)

    @property
    def onset(self) -> int:
        return self._onset

    @property
    def offset(self) -> int:
        return self._offset

    @property
    def _calibration(self) -> float:
        if not self._ignore_calibration:
            return self._test.study.channel_calibration(self._channel)
        return 1.0

    @property
    def amplitude(self) -> float:
        samples = self._test.channel_samples(self._channel)
        return abs(samples[self._offset] - samples[self._onset]) * self._calibration

    @property
    def duration(self) -> float:
        return (self._offset - self._onset) * self._sampling_interval

    @property
    def max_velocity(self) -> float:
        abs_velocities = self._test.channel_absolute_velocities(self._channel)
        max_velocity = abs_velocities[self._onset:self._offset].max()
        scale = self._test.study.channel_calibration(self._channel) * 1000.0
        return max_velocity * scale
