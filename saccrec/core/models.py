from collections import defaultdict
from typing import Dict

from numpy import array, float32, hstack

from saccrec.core import Channel

from .errors import NotEnoughDataError


class ChannelsBuffer:

    def __init__(self):
        self._buffer: Dict[Channel, array] = defaultdict(lambda: array([], dtype=float32))

    def push(self, channels: Dict[Channel, array]):
        for channel, data in channels.items():
            current = self._buffer[channel]
            self._buffer[channel] = hstack((current, data))

    def pop(self, count: int, wait_for_count: bool = False) -> Dict[Channel, array]:
        result: Dict[Channel, array] = {}

        for channel, data in self._buffer.items():
            current = self._buffer[channel]
            if len(current) < count and wait_for_count:
                raise NotEnoughDataError(self, count)

            result[channel] = data[:count]
            self._buffer[channel] = data[count:]

        return result

    @property
    def __len__(self) -> int:
        return min(len(x) for x in self._buffer.values())
