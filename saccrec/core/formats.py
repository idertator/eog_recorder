from datetime import datetime
from json import dump, dumps
from os import makedirs
from os.path import join
from shutil import rmtree
from tempfile import mkdtemp
from typing import List, Tuple, Optional
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
        horizontal: array,
        vertical: Optional[array] = None,
        annotations: Optional[List[Tuple[str, int, int]]] = None,
        **properties
    ):
        current_index = len(self._tests)

        data = {
            'properties': properties,
        }

        if stimulus is not None:
            path = f'{current_index:02}/stimulus.npz'
            full_path = join(self._folder, path)
            savez_compressed(full_path, stimulus)
            data['stimulus'] = path

        if horizontal is not None:
            path = f'{current_index:02}/horizontal.npz'
            full_path = join(self._folder, path)
            savez_compressed(full_path, horizontal)
            data['horizontal'] = path

        if vertical is not None:
            path = f'{current_index:02}/vertical.npz'
            full_path = join(self._folder, path)
            savez_compressed(full_path, vertical)
            data['vertical'] = path

        if annotations is not None:
            path = f'{current_index:02}/annotations.json'
            full_path = join(self._folder, path)
            with open(full_path, 'wt') as f:
                dump(annotations, f, indent=4)
            data['annotations'] = path

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

    def save(self, filepath: str):
        with ZipFile(filepath, mode='w') as out:
            manifest = dumps(self.manifest_json, indent=4)
            out.writestr('manifest.json', manifest)

            for test in self._tests:
                if 'stimulus' in test:
                    full_path = join(self._folder, test['stimulus']) 
                    out.write(full_path, test['stimulus'])

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
