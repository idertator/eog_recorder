from serial import Serial
from struct import unpack
from time import sleep
from typing import Tuple, List

_COMMUNICATIONS_TIMEOUT_MSG = b'Failure: Communications timeout - Device failed to poll Host$$$'


def int32(data: bytes) -> int:
    out = (data[0] << 16) | (data[1] << 8) | data[2]
    return out | 0xFF000000 if (out & 0x00800000) > 0 else out & 0x00FFFFFF


class Sample:

    def __init__(self, data: bytes):
        if len(data) != 33:
            raise ValueError('Data frames must have 33 bytes')

        if data[0] != 0xA0:
            raise ValueError('Packet corrupted')

        unpacked = unpack('BB3s3s3s3s3s3s3s3s6sB', data)

        self._header = unpacked[0]
        self._sample = unpacked[1]
        self._channels = unpacked[2:10]
        self._aux = unpacked[10]
        self._footer = unpacked[11]

    @property
    def is_ok(self) -> bool:
        return self._header == 0xA0 and 0xC0 <= self._footer <= 0xCF

    @property
    def sample(self) -> int:
        return self._sample

    def channel(self, index: int) -> int:
        return int32(self._channels[index])

    def channels(self, count: int = 8) -> List[int]:
        return [self.channel(i) for i in range(count)]

    @property
    def all_channels(self) -> Tuple[int]:
        return self.channels()


CHANNELS_ON = ' !@#$%*'
ALL_CHANNELS = '12345678'


class CytonBoard:

    def __init__(
        self, port: str = '/dev/ttyUSB0',
        baudrate: int = 115200,
        channels: str = ALL_CHANNELS
    ):
        self._serial = Serial(
            port=port,
            baudrate=baudrate
        )
        self._buffer = bytes()

        self._serial.write(b'~6')
        self._serial.read_all()

        channel_set = ''.join(
            CHANNELS_ON[int(c)] if c in channels else c
            for c in ALL_CHANNELS
        ).encode('ASCII')

        self._serial.write(channel_set)
        sleep(0.2)
        self._serial.read_all()

        channel_settings = ''.join(
            f'x{c}060110X'
            for c in ALL_CHANNELS
            if c in channels
        ).encode('ASCII')

        self._serial.write(channel_settings)
        sleep(0.2)
        self._serial.read_all()


    def start(self):
        self._serial.write(b'b')

    def stop(self):
        self._serial.write(b's')
        self._buffer = bytes()

    def read(self) -> List[List[int]]:
        self._buffer += self._serial.read_all()

        if self._buffer:
            start = 0
            while self._buffer[start] != 0xA0:
                start += 1
                if start >= len(self._buffer):
                    break

            if start > 0:
                self._buffer = self._buffer[start:]

        samples = len(self._buffer) // 33

        data = []
        for index in range(samples):
            offset = index * 33
            sample = Sample(self._buffer[offset:offset + 33])
            if sample.is_ok:
                index = sample.sample
                channels = sample.all_channels
                data.append(channels)
                print(index, channels)

        self._buffer = self._buffer[samples * 33:]

        return data

if __name__ == '__main__':
    from datetime import datetime, timedelta

    board = CytonBoard(channels='1')
    board.start()

    start = datetime.now()

    count = 0
    while count < 500:
        count += len(board.read())
        sleep(0.002)

    board.stop()

    print((datetime.now() - start).microseconds / 1000)


