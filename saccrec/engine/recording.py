import logging

from multiprocessing import Process, Queue
from tempfile import gettempdir
from time import sleep
from os import remove
from os.path import join, exists

from .commands import CMD_START, CMD_STOP, CMD_FINISH, CMD_MARKER, CMD_READY
from .openbci import CytonBoard


_log = logging.getLogger(__name__)


class OpenBCIRecorder(Process):

    def __init__(
        self,
        port: str,
        sampling_rate: int = 1000
    ):
        super(OpenBCIRecorder, self).__init__(name='saccrec_recording')
        self._port = port
        self._sampling_rate = sampling_rate

        self._command_queue = Queue()
        self._command_output = Queue()
        self._data_queue = Queue()

    def run(self):
        pid_path = join(gettempdir(), 'saccrec.pid')
        with open(pid_path, 'wt') as f:
            f.write(f'{self.pid}')

        board = CytonBoard(
            port=self._port,
            sampling_rate=self._sampling_rate,
            channels='12',
            use_sd=True
        )
        board.initialize()

        timestamp = 0
        recording = False

        self._command_output.put(CMD_READY)
        print('Running')
        while True:
            if not self._command_queue.empty():
                command = self._command_queue.get()
                print(f'COMMAND: "{command}"')

                if command == CMD_START:
                    print('Before')
                    filename = board.create_sd_file()
                    print(f'FILENAME: {filename}')
                    self._command_output.put(filename)
                    board.start()
                    recording = True

                if command == CMD_STOP:
                    recording = False
                    board.stop()

                if command == CMD_FINISH:
                    break

                if command.startswith(CMD_MARKER):
                    label = command[-1]
                    board.marker(label)

            if recording:
                sample = board.read()

                if len(sample) > 0:
                    for index, s in sample:
                        sample = [
                            index,
                            timestamp,
                            s[0],
                            s[1],
                        ]
                        if timestamp > 0:
                            self._data_queue.put(sample)
                        timestamp += 1

            sleep(1.0 / 500.0)

        if exists(pid_path):
            remove(pid_path)

    def wait_until_ready(self) -> bool:
        while self._command_output.empty():
            sleep(0.1)
        return self._command_output.get() == CMD_READY

    def start_recording(self) -> str:
        self._command_queue.put(CMD_START)
        while self._command_output.empty():
            sleep(0.1)
        filename = self._command_output.get()
        return filename

    def stop_recording(self):
        self._command_queue.put(CMD_STOP)

    def close_recorder(self):
        self._command_queue.put(CMD_FINISH)
        sleep(0.3)
        self.join()

    def read_samples(self) -> list[tuple[int, int, float, float]]:
        result = []
        while not self._data_queue.empty():
            result.append(self._data_queue.get())
        return result

    def put_marker(self, label: int):
        self._command_queue.put(f'{CMD_MARKER}{label}')

