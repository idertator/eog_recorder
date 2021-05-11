import atexit
import logging
import re
from struct import unpack
from time import sleep, time

from numpy import array, int32, ndarray, uint8
from serial import Serial
from serial.tools.list_ports import comports

from saccrec.settings import hardware as conf

logger = logging.getLogger('saccrec')

_COM_ERROR = b'Failure: Communications timeout - Device failed to poll Host$$$'


class CytonBoard:

    @staticmethod
    def list_ports() -> list[str]:
        filter_regex = 'EOG Soft Reset'
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

    def __init__(self, port: str):
        logger.info('Initializing Cyton Board')

        self._port = port
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
        # self._command('!@345678')        # Activate first 2 channels
        self._command(conf.channels.activation_command)
        self._command(conf.eog_channels_command)
        # self._command('N12')

        for index, channel in enumerate(conf.channels):
            if channel.active:
                cmd = channel.settings_command
                if self._command(cmd) == 'Failure: too few chars$$$':
                    self._ready = False
                    logger.error(_('Error setting OpenEOG Channel {index}').format(
                        index=index+1
                    ))

        # if self._command('x1060110X') == 'Failure: too few chars$$$':
        #     self._ready = False
        #     logger.error('Error setting Cyton Channel 1')

        # if self._command('x2060110X') == 'Failure: too few chars$$$':
        #     self._ready = False
        #     logger.error('Error setting Cyton Channel 2')

        sleep(1)
        if msg := self._serial.read_all():
            logger.warn(f'Hanged data: {msg}')

    board_instance = None

    @classmethod
    def reset(cls, port: str):
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
            else:
                logger.info(f'<strong>[{cmd}]</strong>')

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
            result = re.search('[0-9A-F]{6}.EOG', msg)[0]
            self._sd_open = True
            return result
        except TypeError:
            logger.error(msg)
            self._ready = False

    def close_sd_file(self):
        self._command('j', wait=2)
        self._sd_open = False
        logger.info(f'SD File Closed')

    def start(self):
        self._command('(', wait=2)
        self._recording = True

    def stop(self):
        answer = self._command(')', wait=1).strip()
        while answer != '[MSG] Test ended$$$':
            logger.error(f'Cannot close the test with the following answer: "{answer}". Trying again')
            answer = self._command(')', wait=1).strip()
        self._recording = False

    def marker(self, label: str):
        self._command(f'O{label}', wait=0)


@atexit.register
def close_openbci():
    if (board := CytonBoard.board_instance) is not None:
        board.close()
