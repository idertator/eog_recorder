import atexit
import logging
import re
from struct import unpack
from time import sleep, time

from numpy import array, int32, uint8, ndarray
from serial import Serial
from serial.tools.list_ports import comports

logger = logging.getLogger('saccrec')

_COM_ERROR = b'Failure: Communications timeout - Device failed to poll Host$$$'


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
        logger.info('Initializing Cyton Board')

        self._recording = False
        self._sd_open = False

        self._processed_samples = 0
        self._ready = True

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
            self._ready = False
            logger.error('Error setting Cyton Channel 1')

        if self._command('x2060110X') == 'Failure: too few chars$$$':
            self._ready = False
            logger.error('Error setting Cyton Channel 2')

        if self._command('x3160110X') == 'Failure: too few chars$$$':
            self._ready = False
            logger.error('Error setting Cyton Channel 3')

        if self._command('x4160110X') == 'Failure: too few chars$$$':
            self._ready = False
            logger.error('Error setting Cyton Channel 4')

        if self._command('x5160110X') == 'Failure: too few chars$$$':
            self._ready = False
            logger.error('Error setting Cyton Channel 5')

        if self._command('x6160110X') == 'Failure: too few chars$$$':
            self._ready = False
            logger.error('Error setting Cyton Channel 6')

        if self._command('x7160110X') == 'Failure: too few chars$$$':
            self._ready = False
            logger.error('Error setting Cyton Channel 7')

        if self._command('x8160110X') == 'Failure: too few chars$$$':
            self._ready = False
            logger.error('Error setting Cyton Channel 8')

        sleep(1)
        if msg := self._serial.read_all():
            logger.warn(f'Hanged data: {msg}')

    board_instance = None

    @classmethod
    def instance(cls, port: str = '/dev/ttyUSB0'):
        if cls.board_instance is None:
            cls.board_instance = CytonBoard(port=port)
        return cls.board_instance

    @classmethod
    def reset(cls, port: str = '/dev/ttyUSB0'):
        if cls.board_instance is not None:
            cls.board_instance.close()
        cls.board_instance = CytonBoard(port=port)
        return cls.board_instance

    def _command(self, cmd: str, wait: float = 0.2) -> str:
        self._serial.write(cmd.encode('ASCII'))

        if wait > 0:
            sleep(wait)

            msg = self._serial.read_all()
            if b'$$$' in msg:
                decoded_message = msg.decode('ASCII', errors='ignore')
                if msg == _COM_ERROR:
                    logger.error(f'<strong>[{cmd}]</strong>: {decoded_message}')
                    self._ready = False
                elif b'createfdContiguous failCorresponding' in msg:
                    logger.error(f'<strong>[{cmd}]</strong>: {decoded_message}')
                    self._ready = False
                else:
                    logger.info(f'<strong>[{cmd}]</strong>: {decoded_message}')
                return decoded_message

        return ''

    @property
    def ready(self) -> bool:
        return self._ready

    def close(self):
        if self._recording:
            self.stop()

        if self._sd_open:
            self.close_sd_file()

        self._serial.close()

        logger.info('Closing Cyton Board')

    def create_sd_file(self) -> str:
        msg = self._command('S', wait=2)
        try:
            result = re.search('OBCI_[0-9A-F]{2}.TXT', msg)[0]
            self._sd_open = True
            return result
        except TypeError:
            logger.error_('The recorder is not working properly. Please check the batteries and restart the app.')
            self._ready = False

    def close_sd_file(self):
        self._command('j', wait=0)
        self._sd_open = False
        logger.info(f'SD File Closed')

    def start(self):
        self._command('b', wait=0)
        self._recording = True

    def stop(self):
        self._command('s', wait=0)
        self._recording = False

    def marker(self, label: str):
        self._command(f'`{label}', wait=0)

    def read(self) -> bytes:
        return self._serial.read_all()


@atexit.register
def close_openbci():
    if (board := CytonBoard.board_instance) is not None:
        board.close()
