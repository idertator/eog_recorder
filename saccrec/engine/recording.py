from random import randrange
from multiprocessing import Process, Queue
from serial import Serial
from tempfile import gettempdir
from time import sleep
from typing import Optional, List, Tuple
from os import remove
from os.path import join, exists

from numpy import array, savez_compressed, int32, float32

from openbci_interface import Cyton
from openbci_interface.util import list_devices

from saccrec.consts import DEBUG
from saccrec.core import Settings


def list_ports():
    if not DEBUG:
        return list_devices()
    return [
        '/dev/ttyUSB0',
        '/dev/ttyUSB1',
    ]


def initialize_board(settings: Settings) -> Optional[Cyton]:
    if not DEBUG:
        port = Serial(
            port=settings.openbci_port,
            baudrate=115200,
            timeout=2
        )

        board = Cyton(port)
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
        
        # for index in range(8):
        #     channel = index + 1
        #     active, gain = settings.openbci_channels[index]
        #     if active:
        #         board.configure_channel(channel * 2 - 1, power_down='ON', gain=gain, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        #         board.configure_channel(channel * 2, power_down='ON', gain=gain, input_type='NORMAL', bias=0, srb2=0, srb1=1)
        #     else:
        #         board.disable_channel(channel * 2 - 1)
        #         board.disable_channel(channel * 2)

        print('Board Config')
        print(board.get_config())
        print()
        print()
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
        super(OpenBCIRecorder, self).__init__(name='saccrec_recording')
        self._settings = settings
        self._command_queue = Queue()
        self._data_queue = Queue()

        self._tmp_folder = tmp_folder


    def run(self):
        pid_path = join(gettempdir(), 'saccrec.pid')
        with open(pid_path, 'wt') as f:
            f.write(f'{self.pid}')

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
                sample = [
                    timestamp,
                    sample['eeg'][0],
                    sample['eeg'][1],
                ]
                self._data_queue.put(sample)
            else:
                sample = [
                    timestamp, 
                    randrange(-300, 300), 
                    randrange(-300, 300)
                ]
                self._data_queue.put(sample)
                sleep(1.0 / 250)

            timestamp += 1
            
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

        if exists(pid_path):
            remove(pid_path)

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

    recorder = OpenBCIRecorder(settings)
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

# openbci_interface.exception.UnexpectedMessageFormat: Device returned a message not in OpenBCI format; 