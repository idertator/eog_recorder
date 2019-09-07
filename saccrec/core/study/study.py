from datetime import datetime
from io import BytesIO
from json import load, dumps
from typing import Union, List, Type, Optional
from zipfile import ZipFile

from numpy import load as array_load, savez_compressed

from saccrec.consts import DATETIME_FORMAT

from .hardware import Hardware
from .subject import Subject
from .tests import Test, SaccadicTest


class Study:

    def __init__(
        self, 
        path: str,
        version: int,
        recorded_at: Union[str, datetime], 
        hardware: Hardware,
        subject: Subject,
        tests: List[Test]
    ):
        self._path = path

        if isinstance(version, int):
            self._version = version
        else:
            raise AttributeError('version must be of type int')

        if isinstance(recorded_at, str):
            self._recorded_at = datetime.strptime(recorded_at, DATETIME_FORMAT)
        elif isinstance(recorded_at, datetime):
            self._recorded_at = recorded_at
        else:
            raise AttributeError('recorded_at must be of type str or type datetime')

        self._hardware = hardware
        self._subject = subject

        for test in tests:
            if not isinstance(test, Test):
                raise AttributeError('tests must only contains objects of type Test')

        self._tests = tuple(tests)

    def __json__(self) -> dict:
        return {
            'version': self._version,
            'record': {
                'datetime': self._recorded_at.strftime(DATETIME_FORMAT)
            },
            'hardware': self._hardware.__json__(),
            'subject': self._subject.__json__(),
            'tests': [test.__json__() for test in self._tests]
        }

    def __len__(self) -> int:
        return len(self._tests)

    def __getitem__(self, index) -> Test:
        return self._tests[index]

    @property
    def version(self) -> int:
        return self._version

    @property
    def recorded_at(self) -> datetime:
        return self._recorded_at

    @property
    def sample_rate(self) -> int:
        return self._hardware.sample_rate.value

    @property
    def hardware(self) -> Hardware:
        return self._hardware

    @property
    def subject(self) -> Subject:
        return self._subject

    @classmethod
    def open(cls, path: str) -> 'Study':
        with ZipFile(path, mode='r') as fin:
            with fin.open('manifest.json', 'r') as manifest_file:
                manifest = load(manifest_file)

            subject_dict = manifest['subject']
            subject_dict['name'] = subject_dict.pop('full_name')

            tests = []
            for index, test_dict in enumerate(manifest['tests']):
                test_params = {}
                for channel in 'time', 'stimulus', 'horizontal', 'vertical':
                    if channel in test_dict:
                        with fin.open(test_dict[channel], 'r') as farray:
                            test_params[channel] = array_load(farray)[channel]

                kind = test_dict.get('kind', 'Saccadic')

                properties = test_dict['properties']
                name = properties.pop('test_name')
                properties['calibration'] = properties.get('calibration', 'calibración' in name.lower())

                TestClass = Test.from_kind(kind)

                tests.append(
                    TestClass(
                        index=index,
                        name=name,
                        **properties, 
                        **test_params
                    )
                )
                    
            return cls(
                path=path,
                version=manifest['version'],
                recorded_at=manifest['record']['datetime'],
                hardware=Hardware(**manifest['hardware']),
                subject=Subject(**subject_dict),
                tests=tests
            )

    def save(self, path: Optional[str] = None):
        path = path if path is not None else self._path

        with ZipFile(path, mode='w') as out:
            manifest = dumps(self.__json__(), indent=4)
            out.writestr('manifest.json', manifest)

            for test in self:
                for channel in 'time', 'stimulus', 'horizontal', 'vertical':
                    channel_array = getattr(test, channel, None)
                    if channel_array is not None:
                        buffer = BytesIO()
                        savez_compressed(buffer, **{
                            channel: channel_array
                        })
                        buffer.seek(0)
                        out.writestr(f'{test.index:02}/{channel}.npz', buffer.read())

    def filter(self, test_cls: Optional[Type[Test]] = None, calibration: Optional[bool] = None) -> List[Test]:
        if calibration is None:
            if test_cls is not None:
                return [test for test in self._tests if isinstance(test, test_cls)]
            return [test for test in self._tests]

        if test_cls is not None:
            return [test for test in self._tests if isinstance(test, test_cls) and test.is_calibration == calibration]

        return [test for test in self._tests if test.is_calibration == calibration]
