import logging
import re
from struct import unpack
from time import sleep, time

from serial import Serial
from serial.tools.list_ports import comports


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

    def channels(self, count: int = 8) -> list[int]:
        return [
            self.channel(i)
            for i in range(count)
        ]

    @property
    def all_channels(self) -> tuple[int]:
        return self.channels()

    @property
    def marker(self) -> int:
        return self._aux[0]


CHANNELS_ON = ' !@#$%*'
ALL_CHANNELS = '12345678'


class CytonBoard:

    @staticmethod
    def list_ports() -> list[str]:
        filter_regex = 'OpenBCI'
        devices = [p.device for p in comports()]

        def _get_firmware_string(port, timeout=2):
            with Serial(port=port, baudrate=115200, timeout=timeout) as ser:
                ser.write(b'v')
                return ser.read_until(b'$$$').decode('utf-8', errors='ignore')

        ports = []
        for device in devices:
            msg = _get_firmware_string(device)
            if 'Device failed to poll Host' in msg:
                _log.error(
                    'Found USB dongle at "%s", '
                    'but it failed to poll message from a board; %s',
                    device, repr(msg)
                )
            elif re.search(filter_regex, msg):
                _log.info('Matched   [%s] %s "%s"', filter_regex, device, msg)
                ports.append(device)
            else:
                _log.info('Unmatched [%s] %s "%s"', filter_regex, device, msg)

        return ports

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

            return decoded_message

        return ''

    def create_sd_file(self) -> str:
        if self._use_sd:
            msg = self._command('A', wait=1, log=True)
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

    def reset(self):
        self._serial.write(b'v')
        sleep(0.2)
        self._serial.read_all()

    def marker(self, label: int):
        self._command(f'`{label}\'', wait=0, log=True)

    def read(self) -> list[list[int]]:
        buff = self._serial.read_all()

        if buff:
            start = 0
            while buff[start] != 0xA0:
                start += 1
                if start >= len(buff):
                    break

            if start > 0:
                buff = buff[start:]

        data = []
        if (samples := len(buff) // 33) > 0:
            for index in range(samples):
                offset = index * 33
                sample = Sample(buff[offset:offset + 33])
                if sample.is_ok:
                    channels = sample.all_channels + [sample.marker]
                    data.append(channels)

        return data
