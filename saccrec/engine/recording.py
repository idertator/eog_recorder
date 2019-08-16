from multiprocessing import Process, Queue
from serial import Serial
from time import sleep
from typing import Optional

from openbci_interface import Cyton
from openbci_interface.util import list_devices

from saccrec.consts import DEBUG
from saccrec.core import Settings


_DEFAULT_CHANNEL_SETTINGS = {
    'power_down': 'ON',
    'input_type': 'NORMAL',
    'bias': 0,
    'srb2': 0,
    'srb1': 1,
}


def list_ports():
    if DEBUG:
        return [
            '/dev/ttyUSB0',
            '/dev/ttyUSB1',
        ]
    return [port for port in list_devices()]


def initialize_board(settings: Settings) -> Optional[Cyton]:
    if not DEBUG:
        port = Serial(
            port=settings.openbci_port,
            baudrate=settings.openbci_baudrate,
            timeout=settings.openbci_timeout
        )

        board = Cyton(port)

        board.set_board_mode(settings.openbci_board_mode)
        board.set_sample_rate(settings.openbci_sample_rate)

        for index in range(8):
            channel = index + 1
            active, gain = settings.openbci_channels[index]
            if active:
                board.configure_channel(channel, gain=gain, **_DEFAULT_CHANNEL_SETTINGS)
            else:
                board.disable_channel(channel)

        return board

    return None


def close_board(board: Cyton):
    board.terminate()


class OpenBCIRecorder(Process):

    def __init__(self, input_queue: Queue, output_queue: Queue, board: Cyton):
        self._input_queue = Queue()
        self._output_queue = Queue()

        self._board = board

    def run(self):
        self._board.start_streaming()

        while self._input_queue.empty() or self._input_queue.get() != 'stop':
            if not DEBUG:
                sample = self._board.read_sample()
                self._output_queue.put(sample)
            else:
                sample = [1, 2]
                self._output_queue.put(sample)
                sleep(1.0 / self._board.get_sample_rate())
            
        self._board.stop_streaming()            
