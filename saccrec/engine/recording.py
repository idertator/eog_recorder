from random import randrange
from multiprocessing import Process, Queue
from serial import Serial
from time import sleep
from typing import Optional, List, Tuple
from os.path import join

from numpy import array, savez_compressed, int32, float32

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
    return [
        '/dev/ttyUSB0',
        '/dev/ttyUSB1',
    ]


def initialize_board(settings: Settings) -> Optional[Cyton]:
    if not DEBUG:
        print('Serial Initialization')
        print(f'Port: {settings.openbci_port}, Baudrate: {settings.openbci_baudrate}, Timeout: {settings.openbci_timeout}')
        port = Serial(
            port=settings.openbci_port,
            baudrate=settings.openbci_baudrate,
            timeout=settings.openbci_timeout
        )

        board = Cyton(port)
        print('Board Initialization')
        print(f'Mode: {settings.openbci_board_mode}, Sample Rate: {settings.openbci_sample_rate}')

        board.set_board_mode('default')
        board.set_sample_rate(settings.openbci_sample_rate)

        board.configure_channel(1, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        board.configure_channel(2, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        board.configure_channel(3, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        board.configure_channel(4, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        board.configure_channel(5, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        board.configure_channel(6, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        board.configure_channel(7, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        board.configure_channel(8, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        board.configure_channel(9, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        board.configure_channel(10, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        board.configure_channel(11, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        board.configure_channel(12, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        board.configure_channel(13, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        board.configure_channel(14, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        board.configure_channel(15, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        board.configure_channel(16, power_down='ON', gain=24, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        board.disable_channel(5)
        board.disable_channel(6)
        board.disable_channel(7)
        board.disable_channel(8)
        board.disable_channel(9)
        board.disable_channel(10)
        board.disable_channel(11)
        board.disable_channel(12)    
        board.disable_channel(13)
        board.disable_channel(14)
        board.disable_channel(15)
        board.disable_channel(16)
        return board

    return None


def close_board(board: Cyton):
    if not DEBUG:
        board.terminate()


def textfile_to_array(filepath: str, dtype) -> array:
    result = []
    with open(filepath, 'rt') as f:
        for line in f:
            stripped = line.strip()
            if stripped:
                result.append(float(stripped))
    return array(result, dtype=dtype)


class OpenBCIRecorder(Process):

    def __init__(self, settings: Settings, tmp_folder: str = None):
        super(OpenBCIRecorder, self).__init__()
        self._settings = settings
        self._command_queue = Queue()
        self._data_queue = Queue()

        self._tmp_folder = tmp_folder


    def run(self):
        board = None
        if not DEBUG:
            board = initialize_board(self._settings)
            board.start_streaming()

        if self._tmp_folder is not None:
            ts_file = open(join(self._tmp_folder, 'time.tmp'), 'wt')
            hc_file = open(join(self._tmp_folder, 'horizontal.tmp'), 'wt')
            vc_file = open(join(self._tmp_folder, 'vertical.tmp'), 'wt')
        else:
            ts_file = None
            hc_file = None
            vc_file = None

        timestamp = 0
        while self._command_queue.empty() or self._command_queue.get() != 'stop':
            if not DEBUG:
                sample = board.read_sample()
                self._data_queue.put([
                    sample['timestamp'],
                    sample['eeg'][0],
                    sample['eeg'][1],
                ])
            else:
                sample = [timestamp, randrange(-300, 300), randrange(-300, 300)]
                timestamp += 1
                self._data_queue.put(sample)
                sleep(1.0 / 250)

            ts, hc, vc = sample

            if ts_file is not None:
                ts_file.write(f'{ts}\n')

            if hc_file is not None:
                hc_file.write(f'{hc}\n')

            if vc_file is not None:
                vc_file.write(f'{vc}\n')

        if not DEBUG:
            board.stop_streaming()            
            close_board(board)

        if ts_file is not None:
            ts_file.close()
            ts_array = textfile_to_array(join(self._tmp_folder, 'time.tmp'), int32)
            savez_compressed(join(self._tmp_folder, 'time.npz'), time=ts_array)

        if hc_file is not None:
            hc_file.close()
            hc_array = textfile_to_array(join(self._tmp_folder, 'horizontal.tmp'), int32)
            savez_compressed(join(self._tmp_folder, 'horizontal.npz'), horizontal=hc_array)

        if vc_file is not None:
            vc_file.close()
            vc_array = textfile_to_array(join(self._tmp_folder, 'vertical.tmp'), int32)
            savez_compressed(join(self._tmp_folder, 'vertical.npz'), vertical=vc_array)

    def start_streaming(self):
        self.start()

    def read_samples(self) -> List[Tuple[int, float, float]]:
        result = []

        while not self._data_queue.empty():
            result.append(self._data_queue.get())

        return result

    def stop_streaming(self):
        self._command_queue.put('stop')
        self.join()


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
