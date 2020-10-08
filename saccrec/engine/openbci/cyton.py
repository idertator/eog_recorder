import logging
import re

from serial import Serial
from struct import unpack
from time import sleep
from typing import Tuple, List


_COMMUNICATIONS_TIMEOUT_MSG = b'Failure: Communications timeout - Device failed to poll Host$$$'
_log = logging.getLogger(__name__)


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
        data = self._channels[index]
        return (data[0] << 16) | (data[1] << 8) | data[2]

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
        channels: str = ALL_CHANNELS,
        sampling_rate: int = 1000,
        use_sd: bool = False
    ):
        self._serial = Serial(
            port=port,
            baudrate=baudrate
        )
        self._buffer = bytes()
        self._channels = channels
        self._sampling_rate = sampling_rate
        self._use_sd = use_sd

    def _command(self, cmd: str, wait: float = 0.3, log: bool = False) -> str:
        self._serial.write(cmd.encode('ASCII'))

        if wait > 0:
            sleep(wait)

        msg = self._serial.read_all()
        if b'$$$' in msg:
            decoded_message = msg.decode('ASCII', errors='ignore')
            output = f'({cmd}): {decoded_message}'

            if log:
                _log.info(output)
                print(output)
                print()

            return decoded_message

        return ''

    def create_sd_file(self) -> str:
        if self._use_sd:
            msg = self._command('A', wait=0.5, log=True)
            return re.search('OBCI_[0-9A-F]{2}.TXT', msg)[0]
        return None

    def initialize(self):
        rate = {
            16000: 0,
            8000: 1,
            4000: 2,
            2000: 3,
            1000: 4,
            500: 5,
            250: 6,
        }.get(self._sampling_rate, 6)
        self._command(f'~{rate}', log=True)

        # Set active channels
        self._command(
            ''.join(
                CHANNELS_ON[int(c)] if c in self._channels else c
                for c in ALL_CHANNELS
            ),
            log=True
        )

        # Configure channels
        self._command(
            ''.join(
                f'x{c}060110X'
                for c in ALL_CHANNELS
                if c in self._channels
            ),
            log=True
        )

        # Set board mode to Marker mode
        self._command('/4', log=True)

    def start(self):
        self._serial.write(b'b')

    def stop(self):
        self._serial.write(b's')
        if self._use_sd:
            self._serial.write(b'j')
        self._buffer = bytes()

    def reset(self):
        self._serial.write(b'v')
        sleep(0.2)
        self._serial.read_all()

    def marker(self, label: int):
        self._command(f'`{label}\'', log=True)

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
                data.append((index, channels))

        self._buffer = self._buffer[samples * 33:]

        return data
