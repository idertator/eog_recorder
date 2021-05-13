import atexit
import logging
import re
from struct import unpack
from time import sleep

from serial import Serial
from serial.tools.list_ports import comports

from saccrec.settings import hardware as conf

logger = logging.getLogger('saccrec')

_COM_ERROR = 'Failure: Communications timeout - Device failed to poll Host'
BUFFER_SIZE = 60


class CytonBoard:

    @staticmethod
    def list_ports() -> list[str]:
        filter_regex = 'EOG Soft Reset'
        devices = [p.device for p in comports()]

        def _get_firmware_string(port, timeout=0):
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
        self._command(conf.channels.activation_command)
        self._command(conf.eog_channels_command)

        for index, channel in enumerate(conf.channels):
            if channel.active:
                cmd = channel.settings_command
                if self._command(cmd) == 'Failure: too few chars$$$':
                    self._ready = False
                    logger.error(_('Error setting OpenEOG Channel {index}').format(
                        index=index + 1
                    ))

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
                is_error = False
                decoded_message = msg.decode('ASCII', errors='ignore')
                if '[MSG]' in decoded_message:
                    decoded_message = decoded_message.split('[MSG]')[1].strip()
                elif '[ERR]' in decoded_message:
                    is_error = True
                    decoded_message = decoded_message.split('[ERR]')[1].strip()

                if _COM_ERROR in decoded_message:
                    logger.error(f'<strong>[{cmd}]</strong>: {decoded_message}')
                    self._ready = False
                elif 'createfdContiguous failCorresponding' in decoded_message:
                    logger.error(f'<strong>[{cmd}]</strong>: {decoded_message}')
                    self._ready = False
                else:
                    if is_error:
                        logger.error(f'<strong>[{cmd}]</strong>: {decoded_message}')
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
            print(msg)
            self._ready = False

    def close_sd_file(self):
        self._command('j', wait=2)
        self._sd_open = False
        logger.info('SD File Closed')

    def start(self):
        sleep(1)
        self._serial.read_all()
        self._command('(', wait=2)
        self._recording = True

    def stop(self):
        self._serial.read_all()
        answer = self._command(')', wait=1).strip()
        while 'Test ended' not in answer:
            logger.error(f'Cannot close the test with the following answer: "{answer}". Trying again')
            answer = self._command(')', wait=1).strip()
        self._recording = False

    def read(self) -> tuple[int, int, int, int]:
        buff = self._serial.read(BUFFER_SIZE)

        result = []

        for i in range(BUFFER_SIZE // 10):
            sample = buff[i * 10:i * 10 + 10]

            header = sample[0]
            if header == 0:
                index, horizontal, vertical = unpack('>H3s3s', sample[1:-1])
                horizontal = unpack('>I', b'\00' + horizontal)[0]
                vertical = unpack('>I', b'\00' + vertical)[0]

                position = sample[-1]

                result.append((index, horizontal, vertical, position))

        return result

    def marker(self, label: str):
        self._command(f'O{label}', wait=0)


@atexit.register
def close_openbci():
    if (board := CytonBoard.board_instance) is not None:
        board.close()
