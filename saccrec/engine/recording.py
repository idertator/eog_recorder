from random import randrange
from multiprocessing import Process, Queue
from serial import Serial
from time import sleep
from typing import Optional, List, Tuple

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
    if not DEBUG:
        board.terminate()


class OpenBCIRecorder(Process):

    def __init__(self, board: Cyton):
        super(OpenBCIRecorder, self).__init__()
        self._command_queue = Queue()
        self._data_queue = Queue()

        self._board = board

    def run(self):
        if not DEBUG:
            self._board.start_streaming()

        timestamp = 0
        while self._command_queue.empty() or self._command_queue.get() != 'stop':
            if not DEBUG:
                sample = self._board.read_sample()
                self._data_queue.put(sample)
            else:
                sample = [timestamp, randrange(-300, 300), randrange(-300, 300)]
                timestamp += 1
                self._data_queue.put(sample)
                sleep(1.0 / 250)

        if not DEBUG:
            self._board.stop_streaming()            

    def start_streaming(self):
        self.start()

    def read_samples(self) -> List[Tuple[int, float, float]]:
        result = []

        while not self._data_queue.empty():
            result.append(self._data_queue.get())

        return result

    def stop_streaming(self):
        self._command_queue.put('stop')
        recorder.join()


if __name__ == '__main__':
    command_queue = Queue()
    queue = Queue()

    settings = Settings()
    
    if not DEBUG:
        board = initialize_board(settings)
    else:
        board = None

    recorder = OpenBCIRecorder(board=board)
    recorder.start_streaming()

    count = 0
    stop = 1000

    while count < stop:
        samples = recorder.read_samples()
        if samples:
            print(samples)
            count += len(samples)
        sleep(0.001)

    recorder.stop_streaming()
    close_board(board)
