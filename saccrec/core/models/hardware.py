from typing import Optional, Union, List

from saccrec.core import SampleRates


_BOARD_FIELD = 'board'
_SAMPLE_RATE_FIELD = 'sample_rate'
_CHANNELS_FIELDS = 'channels'


class Hardware:

    def __init__(
        self,
        sample_rate: Optional[Union[SampleRates, str]] = None,
        channels: List[dict] = list()
    ):
        if isinstance(sample_rate, int):
            self._sample_rate = SampleRates(sample_rate)
        else:
            self._sample_rate = sample_rate

        self._channels = channels

    @property
    def sample_rate(self) -> Optional[SampleRates]:
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, value: Optional[Union[SampleRates, int]]):
        if isinstance(value, int):
            self._sample_rate = SampleRates(value)
        else:
            self._sample_rate = value

    @property
    def channels(self) -> List[dict]:
        return self._channels

    @channels.setter
    def channels(self, value: List[dict]):
        self._channels = value

    @property
    def json(self) -> dict:
        return {
            _SAMPLE_RATE_FIELD: self._sample_rate.value if self._sample_rate is not None else None,
            _CHANNELS_FIELDS: self._channels,
        }

    @classmethod
    def from_json(cls, json: dict) -> 'Hardware':
        return Hardware(
            sample_rate=json.get(_SAMPLE_RATE_FIELD, None),
            channels=json.get(_CHANNELS_FIELDS, [])
        )
