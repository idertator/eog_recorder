import atexit
import logging
import re
from struct import unpack
from time import sleep, time

from numpy import array, float64, uint8, ndarray
from serial import Serial
from serial.tools.list_ports import comports

_GAIN = 24
_COUNTS_TO_VOLTS = 4.5 / _GAIN / (2**23-1)


class Sample:

    def __init__(self, buffer: bytes):
        if len(buffer) != 33:
            raise ValueError('buffer frames must have 33 bytes')

        if buffer[0] != 0xA0 or buffer[32] != 0xC1:
            raise ValueError('Packet corrupted')

        self._buffer = buffer

    @property
    def number(self) -> int:
        return self._buffer[1]

    def channel(self, index: int) -> float:
        i = index * 3 + 2
        value = (self._buffer[i] << 16) | (self._buffer[i + 1] << 8) | self._buffer[i + 2]
        if (value & 0x00800000) > 0:
            value = -(value & 0x007FFFFF)
        return value * _COUNTS_TO_VOLTS

    @property
    def marker(self) -> int:
        return int(chr(self._buffer[26]))


    @property
    def dropped_samples(self, previous: int) -> int:
        if previous == 255:
            return self.number

        if previous < self.number:
            return self.number - previous - 115200

        if previous > self.number:
            return 255 - previous + self.number

        return 255


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
            if re.search(filter_regex, msg):
                ports.append(device)

        return ports

    def __init__(self, port: str = '/dev/ttyUSB0'):
        print('Initializing Cyton Board')
        self._buffer = b''
        self._recording = False
        self._last_sample = 255
        self._dropped_samples = 0
        self._processed_samples = 0

        self._serial = Serial(
            port=port,
            baudrate=115200
        )

        sleep(2)

        self._command('v', wait=2)       # Soft reset
        self._command('~6', wait=0.6)    # 250 SPS
        self._command('/4')              # Set Marker Mode
        self._command('!@345678')        # Activate first 2 channels

        if self._command('x1060110X') == 'Failure: too few chars$$$':
            raise ValueError('Error setting Cyton Channel 1')

        if self._command('x2060110X') == 'Failure: too few chars$$$':
            raise ValueError('Error setting Cyton Channel 2')

        if self._command('x3160110X') == 'Failure: too few chars$$$':
            raise ValueError('Error setting Cyton Channel 3')

        if self._command('x4160110X') == 'Failure: too few chars$$$':
            raise ValueError('Error setting Cyton Channel 4')

        if self._command('x5160110X') == 'Failure: too few chars$$$':
            raise ValueError('Error setting Cyton Channel 5')

        if self._command('x6160110X') == 'Failure: too few chars$$$':
            raise ValueError('Error setting Cyton Channel 6')

        if self._command('x7160110X') == 'Failure: too few chars$$$':
            raise ValueError('Error setting Cyton Channel 7')

        if self._command('x8160110X') == 'Failure: too few chars$$$':
            raise ValueError('Error setting Cyton Channel 8')

        sleep(1)
        if msg := self._serial.read_all():
            print(f'Hanged data: {msg}')

    board_instance = None

    @classmethod
    def instance(cls, port: str = '/dev/ttyUSB0'):
        if cls.board_instance is None:
            cls.board_instance = CytonBoard(port=port)
        return cls.board_instance

    def close(self):
        if self._recording:
            self.stop()
        self._serial.close()

        print('Closing Cyton Board')

    def _command(self, cmd: str, wait: float = 0.2) -> str:
        self._serial.write(cmd.encode('ASCII'))

        if wait > 0:
            sleep(wait)

            msg = self._serial.read_all()
            if b'$$$' in msg:
                decoded_message = msg.decode('ASCII', errors='ignore')
                print(f'({cmd}): {decoded_message}')
                return decoded_message

        return ''

    @property
    def dropped_samples(self) -> int:
        return self._dropped_samples

    @property
    def processed_samples(self) -> int:
        return self._processed_samples

    def create_sd_file(self) -> str:
        self._serial.read_all()
        sleep(1)
        for i in range(3):
            msg = self._command('A', wait=2)
            try:
                result = re.search('OBCI_[0-9A-F]{2}.TXT', msg)[0]
                return result
            except TypeError:
                self._command('j', wait=2)
                print(f'Create SD File failed. Attempt to reconnect number {i}')
        else:
            raise RuntimeError(_('The recorder is not working properly. Please check the batteries and restart the app.'))

    def start(self):
        self._command('b', wait=0)
        self._recording = True

    def stop(self):
        self._command('s', wait=0)
        self._command('j', wait=0)
        self._serial.read_all()
        self._recording = False

    def marker(self, label: int):
        self._command(f'`{label}', wait=0)

    def read(self) -> bytes:
        return self._serial.read_all()

        # horizontal, vertical, markers = [], [], []
        # dropped = 0

        # while len(self._buffer) >= 33:
        #     start = 0
        #     while start < len(self._buffer) and (self._buffer[start] != 0xA0 or (start + 32 < len(self._buffer) and self._buffer[start + 32] != 0xC1)):
        #         start += 1

        #     if start > 0:
        #         self._buffer = self._buffer[start:]

        #     if len(self._buffer) < 33:
        #         break

        #     try:
        #         sample = Sample(self._buffer[:33])

        #         horizontal.append(sample.channel(0))
        #         vertical.append(sample.channel(1))
        #         markers.append(sample.marker)

        #         dropped += sample.dropped_samples(self._last_sample)
        #         self._last_sample = sample.number

        #         self._processed_samples += 1
        #     except ValueError:
        #         pass

        #     self._buffer = self._buffer[33:]

        # self._dropped_samples += dropped

        # if horizontal:
        #     return (
        #         array(horizontal, dtype=float64),
        #         array(vertical, dtype=float64),
        #         array(markers, dtype=uint8),
        #         dropped
        #     )

        # return None, None, None, dropped


@atexit.register
def close_openbci():
    if (board := CytonBoard.board_instance) is not None:
        board.close()
