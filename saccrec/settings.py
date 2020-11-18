from typing import List
from json import loads
from os.path import expanduser, join
from typing import Optional

from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow

from saccrec.core.screen import Screen


_settings: QSettings = QSettings()


DATE_FORMAT = '%d/%m/%Y'
DATETIME_FORMAT = '%d/%m/%Y %H:%M'

screen: Screen = None


def initialize_screen(main_window: QMainWindow):
    global screen
    screen = Screen(main_window)


class _GUISettings:

    @property
    def lang(self) -> str:
        return _settings.value('GUI/Lang', 'en')

    @lang.setter
    def lang(self, value: str):
        _settings.setValue('GUI/Lang', value)

    @property
    def records_path(self) -> str:
        homedir = expanduser('~')
        default_path = join(homedir, 'Recordings')
        return _settings.value('GUI/RecordsPath', default_path)

    @records_path.setter
    def records_path(self, value: str):
        _settings.setValue('GUI/RecordsPath', value)

    @property
    def current_protocol(self) -> Optional[str]:
        return _settings.value('GUI/CurrentProtocol', None)

    @current_protocol.setter
    def current_protocol(self, value: str):
        _settings.setValue('GUI/CurrentProtocol', value)


gui = _GUISettings()


class _Channel:

    def __init__(self, index: int):
        self._index = index

    @property
    def index(self) -> int:
        return self._index

    @property
    def active(self) -> bool:
        return _settings.value(f'Hardware/Channels/{self._index}/Active', '1') == '1'

    @active.setter
    def active(self, value: bool):
        _settings.setValue(f'Hardware/Channels/{self._index}/Active', '1' if value else '0')

    @property
    def gain(self) -> int:
        return int(_settings.value(f'Hardware/Channels/{self._index}/Gain', 24))

    @gain.setter
    def gain(self, value: int):
        _settings.setValue(f'Hardware/Channels/{self._index}/Gain', value)

    @property
    def json(self) -> dict:
        return {
            'index': self._index,
            'active': self.active,
            'gain': self.gain,
        }


class _Channels:

    def __init__(self, count: int = 8):
        self._channels = [_Channel(index) for index in range(count)]

    def __getitem__(self, index: int) -> _Channel:
        return self._channels[index]

    def __len__(self) -> int:
        return len(self._channels)

    @property
    def json(self) -> List[dict]:
        return [channel.json for channel in self._channels]


class _HardwareSettings:

    def __init__(self):
        self._channels = _Channels()

    @property
    def port(self) -> str:
        return str(_settings.value('Hardware/Port', ''))

    @port.setter
    def port(self, value: str):
        _settings.setValue('Hardware/Port', value)

    @property
    def sampling_rate(self) -> int:
        return int(_settings.value('Hardware/SamplingRate', 1000))

    @sampling_rate.setter
    def sampling_rate(self, value: int):
        _settings.setValue('Hardware/SamplingRate', value)

    @property
    def channels(self) -> _Channels:
        return self._channels


hardware = _HardwareSettings()


class _StimuliSettings:

    @property
    def saccadic_distance(self) -> float:
        return float(_settings.value('Stimuli/SaccadicDistance', 40.0))

    @saccadic_distance.setter
    def saccadic_distance(self, value: float):
        _settings.setValue('Stimuli/SaccadicDistance', value)

    @property
    def ball_radius(self) -> float:
        return float(_settings.value('Stimuli/BallRadius', 0.5))

    @ball_radius.setter
    def ball_radius(self, value: float):
        _settings.setValue('Stimuli/BallRadius', value)

    @property
    def ball_color(self) -> QColor:
        return _settings.value('Stimuli/BallColor', QColor(255, 255, 255))

    @ball_color.setter
    def ball_color(self, value: QColor):
        _settings.setValue('Stimuli/BallColor', value)

    @property
    def back_color(self) -> QColor:
        return _settings.value('Stimuli/BackColor', QColor(0, 0, 0))

    @back_color.setter
    def back_color(self, value: QColor):
        _settings.setValue('Stimuli/BackColor', value)

    @property
    def screen_width(self) -> float:
        return float(_settings.value('Stimuli/ScreenWidth', 47.5))

    @screen_width.setter
    def screen_width(self, value: float):
        _settings.setValue('Stimuli/ScreenWidth', value)

    @property
    def screen_height(self) -> float:
        return float(_settings.value('Stimuli/ScreenHeight', 30.0))

    @screen_height.setter
    def screen_height(self, value: float):
        _settings.value('Stimuli/ScreenHeight', value)


stimuli = _StimuliSettings()

DEFAULT_TEST = {
    'angle': 30,
    'fixation_duration': 3.0,
    'fixation_variability': 50.0,
    'saccades_count': 10,
}

_TESTS = {
    'initial_calibration': DEFAULT_TEST,
    'tests': [DEFAULT_TEST],
    'final_calibration': DEFAULT_TEST,
}


class _TestsSettings:

    @property
    def initial_calibration(self) -> dict:
        if (json := _settings.value('Test/InitialCalibration', None)) is not None:
            return loads(json)
        return DEFAULT_TEST

    @initial_calibration.setter
    def initial_calibration(self, value: dict):
        _settings.setValue('Test/InitialCalibration', value)

    @property
    def test_stimulus(self) -> List[dict]:
        if (json := _settings.value('Test/TestStimulus', None)) is not None:
            return loads(json)
        return [DEFAULT_TEST]

    @test_stimulus.setter
    def test_stimulus(self, value: List[dict]):
        return _settings.setValue('Test/TestStimulus', value)

    @property
    def final_calibration(self) -> dict:
        if (json := _settings.value('Test/FinalCalibration', None)) is not None:
            return loads(json)
        return DEFAULT_TEST

    @final_calibration.setter
    def final_calibration(self, value: dict):
        return _settings.setValue('Test/FinalCalibration', value)

    @property
    def tests(self) -> dict:
        return dict(_settings.value('Test', _TESTS))

    @tests.setter
    def tests(self, value: dict):
        _settings.setValue('Test', value)


tests = _TestsSettings()
