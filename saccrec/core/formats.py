from datetime import datetime
from json import dumps
from os import makedirs
from os.path import join, exists, dirname
from shutil import rmtree
from tempfile import mkdtemp
from zipfile import ZipFile

from numpy import array, savez_compressed

from saccrec.consts import DATETIME_FORMAT
from saccrec.core.models import Subject, Hardware


_CURRENT_VERSION = 1


class Record:

    def __init__(
        self,
        subject: Subject,
        hardware: Hardware
    ):
        self._datetime = datetime.now()
        self._subject = subject
        self._hardware = hardware

        self._tests = []

        self._folder = mkdtemp(prefix='saccrec-')

    def add_test(
        self,
        stimulus: array,
        **properties
    ):
        current_index = len(self._tests)

        data = {
            'properties': properties,
        }

        if stimulus is not None:
            path = f'{current_index:02}/stimulus.npz'
            full_path = join(self._folder, path)
            if not exists(dirname(full_path)):
                makedirs(dirname(full_path))
            savez_compressed(full_path, stimulus=stimulus)
            data['stimulus'] = path

        path = f'{current_index:02}/time.npz'
        full_path = join(self._folder, path)
        if exists(full_path):
            data['time'] = path

        path = f'{current_index:02}/horizontal.npz'
        full_path = join(self._folder, path)
        if exists(full_path):
            data['horizontal'] = path

        path = f'{current_index:02}/vertical.npz'
        full_path = join(self._folder, path)
        if exists(full_path):
            data['vertical'] = path

        self._tests.append(data)

    @property
    def manifest_json(self) -> dict:
        return {
            'version': _CURRENT_VERSION,
            'record': {
                'datetime': self._datetime.strftime(DATETIME_FORMAT)
            },
            'subject': self._subject.json,
            'hardware': self._hardware.json,
            'tests': self._tests,
        }

    def folder_for_test(self, test_index: int) -> str:
        path = join(self._folder, f'{test_index:02}')
        if not exists(path):
            makedirs(path)
        return path

    def save(self, filepath: str):
        with ZipFile(filepath, mode='w') as out:
            manifest = dumps(self.manifest_json, indent=4)
            out.writestr('manifest.json', manifest)

            for test in self._tests:
                if 'stimulus' in test:
                    full_path = join(self._folder, test['stimulus'])
                    out.write(full_path, test['stimulus'])

                if 'time' in test:
                    full_path = join(self._folder, test['time'])
                    out.write(full_path, test['time'])

                if 'horizontal' in test:
                    full_path = join(self._folder, test['horizontal'])
                    out.write(full_path, test['horizontal'])

                if 'vertical' in test:
                    full_path = join(self._folder, test['vertical'])
                    out.write(full_path, test['vertical'])

                if 'annotations' in test:
                    full_path = join(self._folder, test['annotations'])
                    out.write(full_path, test['annotations'])

    def close(self):
        rmtree(self._folder, ignore_errors=True)
