import atexit
import logging
import re
from struct import unpack
from time import sleep

from serial import Serial
from serial.tools.list_ports import comports

from saccrec.settings import hardware as conf

logger = logging.getLogger("saccrec")

_COM_ERROR = "Communications timeout - Device failed to poll Host"
BUFFER_SIZE = 60


class CytonBoard:
    @staticmethod
    def list_ports() -> list[str]:
        filter_regex = "OpenEOG"
        devices = [p.device for p in comports()]

        def _get_firmware_string(port, timeout=0):
            with Serial(port=port, baudrate=115200, timeout=timeout) as ser:
                ser.write(b"v")
                sleep(1)
                return ser.read_all().decode("utf-8", errors="ignore")

        ports = []
        for device in devices:
            msg = _get_firmware_string(device)
            if re.search(filter_regex, msg):
                ports.append(device)

        return ports

    def __init__(self, port: str):
        logger.info("Initializing Cyton Board")

        self._port = port
        self._recording = False

        self._processed_samples = 0
        self._ready = True
        self._buffer = b""

        self._serial = Serial(port=port, baudrate=115200, timeout=0)

        sleep(2)

        self._command("v", wait=1)
        self._command(conf.eog_channels_command)

        for index, channel in enumerate(conf.channels):
            if channel.active:
                cmd = channel.settings_command
                if "too few chars" in self._command(cmd):
                    self._ready = False
                    logger.error(
                        _("Error setting OpenEOG Channel {index}").format(
                            index=index + 1
                        )
                    )

        sleep(1)
        if msg := self._serial.read_all():
            logger.warn(f"Hanged data: {msg}")

    board_instance = None

    @classmethod
    def reset(cls, port: str):
        if cls.board_instance is not None:
            cls.board_instance.close()
        cls.board_instance = CytonBoard(port=port)
        return cls.board_instance

    def _command(self, cmd: str, wait: float = 0.2) -> str:
        self._serial.write(cmd.encode("ASCII"))

        if wait > 0:
            sleep(wait)

            msg = self._serial.read_all()
            if b"$$$" in msg:
                is_error = False
                decoded_message = msg.decode("ASCII", errors="ignore")
                if "[MSG]" in decoded_message:
                    decoded_message = decoded_message.split("[MSG]")[1].strip()
                elif "[ERR]" in decoded_message:
                    is_error = True
                    decoded_message = decoded_message.split("[ERR]")[1].strip()

                if _COM_ERROR in decoded_message:
                    logger.error(f"<strong>[{cmd}]</strong>: {decoded_message}")
                    self._ready = False
                elif "createfdContiguous failCorresponding" in decoded_message:
                    logger.error(f"<strong>[{cmd}]</strong>: {decoded_message}")
                    self._ready = False
                else:
                    if is_error:
                        logger.error(f"<strong>[{cmd}]</strong>: {decoded_message}")
                    else:
                        logger.info(f"<strong>[{cmd}]</strong>: {decoded_message}")
                return decoded_message
            else:
                logger.info(f"<strong>[{cmd}]</strong>")

        return ""

    @property
    def ready(self) -> bool:
        return self._ready

    def close(self):
        if self._recording:
            self.stop()

        self._serial.close()

        logger.info("Closing Cyton Board")

    def start(self):
        self._buffer = b""
        self._serial.reset_input_buffer()
        sleep(1)
        try:
            self._command("(", wait=2)
            self._recording = True
        except ValueError:
            self._recording = True

    def stop(self):
        self._serial.reset_input_buffer()
        sleep(1)
        while self._serial.in_waiting == 0:
            sleep(1)
        self._command(")", wait=2).strip()
        self._recording = False
        self._serial.reset_input_buffer()
        sleep(1)
        self._buffer = b""

    def read(self) -> tuple[int, int, int, int]:
        buff = self._serial.read(self._serial.in_waiting)

        self._buffer += buff
        index = 0
        while index < len(self._buffer) and self._buffer[index] != 0:
            index += 1

        if index > 0:
            self._buffer = self._buffer[index:]

        if len(self._buffer) >= BUFFER_SIZE:
            buff = self._buffer[:BUFFER_SIZE]
            self._buffer = self._buffer[BUFFER_SIZE:]

        result = []

        if len(buff) == BUFFER_SIZE:
            for i in range(BUFFER_SIZE // 10):
                if sample := buff[i * 10 : i * 10 + 10]:
                    header = sample[0]
                    if header == 0:
                        if (position := sample[-1]) in {0x01, 0x02, 0x04, 0x08, 0x10}:
                            index, horizontal, vertical = unpack(">H3s3s", sample[1:-1])
                            horizontal = unpack(">I", b"\00" + horizontal)[0]
                            vertical = unpack(">I", b"\00" + vertical)[0]

                            result.append((index, horizontal, vertical, position))

        return result

    def marker(self, label: str):
        self._command(f"O{label}", wait=0)


@atexit.register
def close_openbci():
    if (board := CytonBoard.board_instance) is not None:
        board.close()
