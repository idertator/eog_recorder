from os import makedirs
from os.path import expanduser, join, exists
from typing import List

from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QColor

from saccrec.consts import SETTINGS_OPENBCI_DEFAULT_SAMPLE_RATE, \
    SETTINGS_DEFAULT_STIMULUS_BALL_RADIUS, SETTINGS_DEFAULT_STIMULUS_BALL_COLOR, \
    SETTINGS_DEFAULT_STIMULUS_BACKGROUND_COLOR, SETTINGS_OPENBCI_DEFAULT_GAIN, SETTINGS_OPENBCI_DEFAULT_CHANNEL_NUMBER, \
    SETTINGS_STIMULUS_SCREEN_DEFAULT_WIDTH, SETTINGS_STIMULUS_SCREEN_DEFAULT_HEIGHT, STIMULUS_DEFAULT_ANGLE, \
    STIMULUS_DEFAULT_DURATION, STIMULUS_DEFAULT_VARIABILITY, STIMULUS_DEFAULT_SACCADES, DEFAULT_TESTS_COUNT, \
    DEFAULT_TEST, TESTS
from saccrec.consts import SETTINGS_STIMULUS_SACCADIC_DISTANCE_MINIMUM


class Channel(object):
    def __init__(self, settings: QSettings, parent=None):
        self._settings = settings
        self._channels = [
            (
                bool(int(self._settings.value(f'OpenBCIChannels/Activated{index}', 1))),
                int(self._settings.value(f'OpenBCIChannels/Gain{index}', SETTINGS_OPENBCI_DEFAULT_GAIN))
            ) for index in range(SETTINGS_OPENBCI_DEFAULT_CHANNEL_NUMBER)
        ]

    def __getitem__(self, index: int):
        return tuple(self._channels[index])

    def __setitem__(self, index, value):
        if isinstance(value, bool):
            self._channels[index] = (bool(value), int(self._channels[index][1]))
            self._settings.setValue(f'OpenBCIChannels/Activated{index}', int(bool(value)))
        if isinstance(value, int):
            self._channels[index] = (bool(self._channels[index][0]), int(value))
            self._settings.setValue(f'OpenBCIChannels/Gain{index}', int(value))
        if isinstance(value, tuple):
            self._channels[index] = value
            self._settings.setValue(f'OpenBCIChannels/Activated{index}', int(bool(value[0])))
            self._settings.setValue(f'OpenBCIChannels/Gain{index}', int(value[1]))

    @property
    def json(self) -> List[dict]:
        return [{
            'index': index,
            'active': active,
            'gain': gain,
        } for index, (active, gain) in enumerate(self._channels)]


class Settings(object):

    def __init__(self, parent=None):
        self._settings = QSettings('SaccRec', 'SaccRec', parent)
        self._channels = Channel(self._settings)

    @property
    def output_dir(self) -> str:
        homedir = expanduser('~')
        output_path = join(homedir, 'Recordings')
        if not exists(output_path):
            makedirs(output_path)
        return output_path

    # OPENBCI SETTINGS
    @property
    def openbci_port(self) -> str:
        return self._settings.value('OpenBCI/Port', '')

    @openbci_port.setter
    def openbci_port(self, value: str):
        self._settings.setValue('OpenBCI/Port', value)

    @property
    def openbci_sample_rate(self) -> int:
        return int(self._settings.value('OpenBCI/SampleRate', SETTINGS_OPENBCI_DEFAULT_SAMPLE_RATE))

    @openbci_sample_rate.setter
    def openbci_sample_rate(self, value: int):
        self._settings.setValue('OpenBCI/SampleRate', value)

    # SCREEN SETTINGS
    @property
    def stimulus_screen_width(self) -> float:
        return float(self._settings.value('Stimulus/ScreenWidth', SETTINGS_STIMULUS_SCREEN_DEFAULT_WIDTH))

    @stimulus_screen_width.setter
    def stimulus_screen_width(self, value: float):
        self._settings.setValue('Stimulus/ScreenWidth', value)

    @property
    def stimulus_screen_height(self) -> float:
        return float(self._settings.value('Stimulus/ScreenHeight', SETTINGS_STIMULUS_SCREEN_DEFAULT_HEIGHT))

    @stimulus_screen_height.setter
    def stimulus_screen_height(self, value: float):
        self._settings.setValue('Stimulus/ScreenHeight', value)

    # STIMULUS SETTINGS
    @property
    def stimulus_saccadic_distance(self) -> float:
        return float(self._settings.value('Stimulus/SaccadicDistance', SETTINGS_STIMULUS_SACCADIC_DISTANCE_MINIMUM))

    @stimulus_saccadic_distance.setter
    def stimulus_saccadic_distance(self, value: float):
        self._settings.setValue('Stimulus/SaccadicDistance', value)

    @property
    def stimulus_saccadic_ball_radius(self) -> float:
        return float(self._settings.value('Stimulus/SaccadicBallRadius', SETTINGS_DEFAULT_STIMULUS_BALL_RADIUS))

    @stimulus_saccadic_ball_radius.setter
    def stimulus_saccadic_ball_radius(self, value: float):
        self._settings.setValue('Stimulus/SaccadicBallRadius', value)

    @property
    def stimulus_saccadic_ball_color(self) -> QColor:
        return QColor(self._settings.value('Stimulus/SaccadicBallColor', SETTINGS_DEFAULT_STIMULUS_BALL_COLOR))

    @stimulus_saccadic_ball_color.setter
    def stimulus_saccadic_ball_color(self, value: QColor):
        self._settings.setValue('Stimulus/SaccadicBallColor', value)

    @property
    def stimulus_saccadic_background_color(self) -> QColor:
        return QColor(
            self._settings.value('Stimulus/SaccadicBackgroundColor', SETTINGS_DEFAULT_STIMULUS_BACKGROUND_COLOR))

    @stimulus_saccadic_background_color.setter
    def stimulus_saccadic_background_color(self, value: QColor):
        self._settings.setValue('Stimulus/SaccadicBackgroundColor', value)

    @property
    def openbci_channels(self) -> Channel:
        return self._channels

    @property
    def initial_calibration(self) -> dict:
        return dict(self._settings.value('Test/InitialCalibration', DEFAULT_TEST))

    @initial_calibration.setter
    def initial_calibration(self, value: dict):
        self._settings.setValue('Test/InitialCalibration', value)

    @property
    def test_stimulus(self) -> List[dict]:
        return list(self._settings.value('Test/TestStimulus', [DEFAULT_TEST]))

    @test_stimulus.setter
    def test_stimulus(self, value: List[dict]):
        return self._settings.setValue('Test/TestStimulus', value)

    @property
    def final_calibration(self) -> dict:
        return dict(self._settings.value('Test/FinalCalibration', DEFAULT_TEST))

    @final_calibration.setter
    def final_calibration(self, value: dict):
        return self._settings.setValue('Test/FinalCalibration', value)

    @property
    def tests(self) -> dict:
        return dict(self._settings.value('Test', TESTS))

    @tests.setter
    def tests(self, value: dict):
        self._settings.setValue('Test', value)

