from typing import Union, List

from saccrec.core.enums import SampleRates


class _Channel:

    def __init__(self, index: int, active: bool, gain: int = 24):
        if isinstance(index, int):
            self._index = index
        else:
            raise AttributeError('index must be of type int')

        if isinstance(active, bool):
            self._active = active
        else:
            raise AttributeError('active must be of type bool')

        if isinstance(gain, int):
            self._gain = gain
        else:
            raise AttributeError('gain must be of type int')

    def __json__(self) -> dict:
        return {
            'index': self._index,
            'active': self._active,
            'gain': self._gain,
        }

    @property
    def index(self) -> int:
        return self._index

    @property
    def active(self) -> bool:
        return self._active

    @property
    def gain(self) -> int:
        return self._gain


class Channels:

    def __init__(self, channels: List[dict]):
        self._channels = [_Channel(**channel) for channel in channels]

    def __len__(self) -> int:
        return len(self._chanels)

    def __getitem__(self, index) -> _Channel:
        return self._channels[index]

    def __json__(self) -> List[dict]:
        return [channel.__json__() for channel in self._channels]


class Hardware:

    def __init__(self, sample_rate: Union[int, SampleRates], channels: List[dict]):
        if isinstance(sample_rate, int):
            self._sample_rate = SampleRates(sample_rate)
        elif isinstance(sample_rate, SampleRates):
            self._sample_rate = sample_rate
        else:
            raise AttributeError('sample_rate must be of type int or type SampleRates')

        self._channels = Channels(channels)

    def __json__(self) -> dict:
        return {
            'sample_rate': self._sample_rate.value,
            'channels': self._channels.__json__()
        }

    @property
    def sample_rate(self) -> SampleRates:
        return self._sample_rate

    @property
    def channels(self) -> Channels:
        return self._channels



