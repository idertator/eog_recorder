from os import makedirs
from os.path import expanduser, join, exists
from typing import List

from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QColor

from saccrec.consts import SETTINGS_OPENBCI_DEFAULT_SAMPLE_RATE, \
    SETTINGS_DEFAULT_STIMULUS_BALL_RADIUS, SETTINGS_DEFAULT_STIMULUS_BALL_COLOR, \
    SETTINGS_DEFAULT_STIMULUS_BACKGROUND_COLOR, SETTINGS_OPENBCI_DEFAULT_GAIN, SETTINGS_OPENBCI_DEFAULT_CHANNEL_NUMBER, \
    SETTINGS_STIMULUS_SCREEN_DEFAULT_WIDTH, SETTINGS_STIMULUS_SCREEN_DEFAULT_HEIGHT, STIMULUS_DEFAULT_ANGLE, \
    STIMULUS_DEFAULT_DURATION, STIMULUS_DEFAULT_VARIABILITY, STIMULUS_DEFAULT_SACCADES, DEFAULT_TESTS_COUNT
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


class TestSet(object):
    def __init__(self, settings: QSettings, parent=None):
        self._settings = settings
        self._test = []
        for i in range(self.test_count):
            self._test.append(
                (
                    int(self._settings.value(f'CalibrationTests/Test{i}/Angle', STIMULUS_DEFAULT_ANGLE)),
                    float(
                        self._settings.value(f'CalibrationTests/Test{i}/FixationDuration', STIMULUS_DEFAULT_DURATION)),
                    float(self._settings.value(f'CalibrationTests/Test{i}/FixationVariability',
                                               STIMULUS_DEFAULT_VARIABILITY)),
                    int(self._settings.value(f'CalibrationTests/Test{i}/SaccadesCount', STIMULUS_DEFAULT_SACCADES))
                )
            )

    def __getitem__(self, item: int) -> tuple:
        return self._test[item]

    def __setitem__(self, index: int, value: tuple):
        self._test[index] = (
            self._settings.setValue(f'CalibrationTests/Test{item}/Angle', value[0]),
            self._settings.setValue(f'CalibrationTests/Test{item}/FixationDuration', value[1]),
            self._settings.setValue(f'CalibrationTests/Test{item}/FixationVariability', value[2]),
            self._settings.setValue(f'CalibrationTests/Test{item}/SaccadesCount', value[3]),
        )

    @property
    def test_count(self) -> int:
        return int(self._settings.value('CalibrationTests/TestCount', DEFAULT_TESTS_COUNT))

    @test_count.setter
    def test_count(self, value: int):
        self._settings.setValue('CalibrationTests/TestCount', value)

    @property
    def initial(self) -> tuple:
        return (
            int(self._settings.value('CalibrationTests/Initial/Angle',
                                     STIMULUS_DEFAULT_ANGLE)),
            float(self._settings.value('CalibrationTests/Initial/FixationDuration',
                                       STIMULUS_DEFAULT_DURATION)),
            float(self._settings.value('CalibrationTests/Initial/FixationVariability',
                                       STIMULUS_DEFAULT_VARIABILITY)),
            int(self._settings.value(f'CalibrationTests/Initial/SaccadesCount',
                                     STIMULUS_DEFAULT_SACCADES))
        )

    @initial.setter
    def initial(self, value: tuple):
        self._settings.setValue('CalibrationTests/Initial/Angle', value[0])
        self._settings.setValue('CalibrationTests/Initial/FixationDuration', value[1])
        self._settings.setValue('CalibrationTests/Initial/FixationVariability', value[2])
        self._settings.setValue('CalibrationTests/Initial/SaccadesCount', value[3])

    @property
    def final(self) -> tuple:
        return (
            int(self._settings.value('CalibrationTests/Final/Angle',
                                     STIMULUS_DEFAULT_ANGLE)),
            float(self._settings.value('CalibrationTests/Final/FixationDuration',
                                       STIMULUS_DEFAULT_DURATION)),
            float(self._settings.value('CalibrationTests/Final/FixationVariability',
                                       STIMULUS_DEFAULT_VARIABILITY)),
            int(self._settings.value(f'CalibrationTests/Final/SaccadesCount',
                                     STIMULUS_DEFAULT_SACCADES))
        )

    @final.setter
    def final(self, value: tuple):
        self._settings.setValue('CalibrationTests/Final/Angle', value[0])
        self._settings.setValue('CalibrationTests/Final/FixationDuration', value[1])
        self._settings.setValue('CalibrationTests/Final/FixationVariability', value[2])
        self._settings.setValue('CalibrationTests/Final/SaccadesCount', value[3])


class Settings(object):

    def __init__(self, parent=None):
        self._settings = QSettings('SaccRec', 'SaccRec', parent)
        self._channels = Channel(self._settings)
        self._calibration_tests = TestSet(self._settings)

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
    def calibration_tests(self) -> TestSet:
        return self._calibration_tests
