from datetime import datetime
from io import BytesIO
from json import load, dumps
from typing import Union, List, Type, Optional
from zipfile import ZipFile

from numpy import load as array_load, savez_compressed

from eoglib.models import Subject

from saccrec import settings
from saccrec.core.enums import Channel

from .hardware import Hardware
from .tests import Test


class Study:

    def __init__(
        self,
        path: str,
        version: int,
        recorded_at: Union[str, datetime],
        hardware: Hardware,
        subject: Subject,
        tests: List[Test],
        horizontal_calibration: float = 1.0,
        vertical_calibration: float = 1.0
    ):
        self._path = path

        if isinstance(version, int):
            self._version = version
        else:
            raise AttributeError('version must be of type int')

        if isinstance(recorded_at, str):
            self._recorded_at = datetime.strptime(recorded_at, settings.DATETIME_FORMAT)
        elif isinstance(recorded_at, datetime):
            self._recorded_at = recorded_at
        else:
            raise AttributeError('recorded_at must be of type str or type datetime')

        self._hardware = hardware
        self._subject = subject

        for test in tests:
            if not isinstance(test, Test):
                raise AttributeError('tests must only contains objects of type Test')
            test.study = self

        self._tests = tuple(tests)

        self._horizontal_calibration = horizontal_calibration
        self._vertical_calibration = vertical_calibration

    def __json__(self) -> dict:
        return {
            'version': self._version,
            'record': {
                'datetime': self._recorded_at.strftime(settings.DATETIME_FORMAT)
            },
            'hardware': self._hardware.__json__(),
            'processing': {
                'calibration': {
                    'horizontal': self._horizontal_calibration,
                    'vertical': self._vertical_calibration,
                }
            },
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
    def sampling_rate(self) -> int:
        return self._hardware.sample_rate.value

    @property
    def sampling_interval(self) -> float:
        return 1000.0 / float(self.sampling_rate)

    @property
    def hardware(self) -> Hardware:
        return self._hardware

    @property
    def subject(self) -> Subject:
        return self._subject

    @property
    def horizontal_calibration(self) -> float:
        return self._horizontal_calibration

    @horizontal_calibration.setter
    def horizontal_calibration(self, value) -> float:
        assert isinstance(value, float)
        self._horizontal_calibration = value

    @property
    def vertical_calibration(self) -> float:
        return self._vertical_calibration

    @vertical_calibration.setter
    def vertical_calibration(self, value) -> float:
        assert isinstance(value, float)
        self._vertical_calibration = value

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

                test = TestClass(
                    index=index,
                    name=name,
                    **properties,
                    **test_params
                )
                test.__parse_data__(test_dict.get('data', {}))
                tests.append(test)

            processing = manifest.get('processing', {
                'calibration': {
                    'horizontal': 1.0,
                    'vertical': 1.0,
                }
            })
            calibration = processing.get('calibration', {
                'horizontal': 1.0,
                'vertical': 1.0,
            })

            return cls(
                path=path,
                version=manifest['version'],
                recorded_at=manifest['record']['datetime'],
                hardware=Hardware(**manifest['hardware']),
                subject=Subject(**subject_dict),
                tests=tests,
                horizontal_calibration=calibration['horizontal'],
                vertical_calibration=calibration['vertical']
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

    def channel_calibration(self, channel: Channel) -> float:
        if channel == Channel.Horizontal:
            return self._horizontal_calibration
        if channel == Channel.Vertical:
            return self._vertical_calibration
        return 1.0
