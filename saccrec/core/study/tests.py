from typing import Optional, Type

from numpy import ndarray

from saccrec.core.enums import Channel
from saccrec.engine.processing import differentiate


class Test:
    _TESTS = []
    _TESTS_FROM_KIND = {}
    
    def __init_subclass__(cls, kind, **kwargs):
        cls.kind = kind
        cls._TESTS.append(cls)
        cls._TESTS_FROM_KIND[kind] = cls

    @classmethod
    def from_kind(cls, kind: str) -> Type['Test']:
        return cls._TESTS_FROM_KIND[kind]

    def __init__(
        self,
        index: int,
        name: str,
        time: Optional[ndarray] = None,
        stimulus: Optional[ndarray] = None,
        horizontal: Optional[ndarray] = None,
        vertical: Optional[ndarray] = None,
        calibration: bool = False,
        **kwargs
    ):
        self._study = None
        if isinstance(index, int):
            self._index = index
        else:
            raise AttributeError('index must be of type int')

        if isinstance(name, str):
            self._name = name
        else:
            raise AttributeError('name must be of type str')

        if time is None or isinstance(time, ndarray):
            self._time = time
        else:
            raise AttributeError('time must be of type ndarray or None')

        if stimulus is None or isinstance(stimulus, ndarray):
            self._stimulus = stimulus
        else:
            raise AttributeError('stimulus must be of type ndarray or None')

        if horizontal is None or isinstance(horizontal, ndarray):
            self._horizontal = horizontal
        else:
            raise AttributeError('horizontal must be of type ndarray or None')        

        if vertical is None or isinstance(vertical, ndarray):
            self._vertical = vertical
        else:
            raise AttributeError('vertical must be of type ndarray or None')

        if isinstance(calibration, bool):
            self._calibration = calibration
        else:
            raise AttributeError('calibration must be of type bool')

        self._velocities = {}
        self._absolute_velocities = {}

    def __properties__(self) -> dict:
        return {}

    def __data__(self) -> Optional[dict]:
        return None

    def __json__(self) -> dict:
        properties = {
            'test_name': self._name,
            'calibration': self._calibration,
        }
        properties.update(self.__properties__())

        result = {
            'kind': type(self).kind,
            'properties': properties
        }
        if self._time is not None:
            result['time'] = f'{self._index:02}/time.npz'

        if self._stimulus is not None:
            result['stimulus'] = f'{self._index:02}/stimulus.npz'

        if self._horizontal is not None:
            result['horizontal'] = f'{self._index:02}/horizontal.npz'

        if self._vertical is not None:
            result['vertical'] = f'{self._index:02}/vertical.npz'

        data = self.__data__()
        if data is not None:
            result['data'] = data

        return result

    @property
    def study(self):
        return self._study

    @study.setter
    def study(self, value):
        from saccrec.core import Study
        assert(isinstance(value, Study))
        self._study = value

    @property
    def index(self) -> int:
        return self._index

    @property
    def name(self) -> str:
        return self._name

    @property
    def time(self) -> Optional[ndarray]:
        return self._time

    @property
    def stimulus(self) -> Optional[ndarray]:
        return self._stimulus

    @property
    def horizontal(self) -> Optional[ndarray]:
        return self._horizontal

    @property
    def vertical(self) -> Optional[ndarray]:
        return self._vertical

    @property
    def is_calibration(self) -> bool:
        return self._calibration

    def free_memory(self):
        self._velocities = {}
        self._absolute_velocities = {}

    def channel_samples(self, channel: Channel) -> Optional[ndarray]:
        if channel == Channel.Time:
            return self._time

        if channel == Channel.Stimulus:
            return self._stimulus

        if channel == Channel.Horizontal:
            return self._horizontal

        if channel == Channel.Vertical:
            return self._vertical

        return None

    def channel_velocities(self, channel: Channel) -> Optional[ndarray]:
        samples = self.channel_samples(channel)
        if samples is not None:
            if channel not in self._velocities:
                self._velocities[channel] = differentiate(samples, self._study.sampling_interval)
            return self._velocities[channel]
        return None

    def channel_absolute_velocities(self, channel: Channel) -> Optional[ndarray]:
        velocities = self.channel_velocities(channel)
        if velocities is not None:
            if channel not in self._absolute_velocities:
                self._absolute_velocities[channel] = velocities.abs()
            return self._absolute_velocities[channel]
        return None


class SaccadicTest(Test, kind='Saccadic'):

    def __init__(
        self, 
        angle: int, 
        fixation_duration: float,
        fixation_variability: float,
        saccades_count: int,
        **kwargs
    ):
        super(SaccadicTest, self).__init__(**kwargs)

        if isinstance(angle, int):
            self._angle = angle
        elif isinstance(angle, float):
            self._angle = int(angle)
        else:
            raise AttributeError('angle must be of type int or type float')

        if isinstance(fixation_duration, float):
            self._fixation_duration = fixation_duration
        else:
            raise AttributeError('fixation_duration must be of type float')

        if isinstance(fixation_variability, float):
            self._fixation_variability = fixation_variability
        else:
            raise AttributeError('fixation_variability must be of type float')

        if isinstance(saccades_count, int):
            self._saccades_count = saccades_count
        elif isinstance(saccades_count, float):
            self._saccades_count = int(saccades_count)
        else:
            raise AttributeError('saccades_count must be of type int or type float')

    def __properties__(self) -> dict:
        return {
            'angle': self._angle,
            'fixation_duration': self._fixation_duration,
            'fixation_variability': self._fixation_variability,
            'saccades_count': self._saccades_count,
        }

    @property
    def angle(self) -> int:
        return self._angle

    @property
    def fixation_duration(self) -> float:
        return self._fixation_duration

    @property
    def fixation_variability(self) -> float:
        return self._fixation_variability

    @property
    def saccades_count(self) -> int:
        return self._saccades_count
