from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QColor

from saccrec.consts import SETTINGS_STIMULUS_SCREEN_WIDTH_MINIMUM, SETTINGS_OPENBCI_DEFAULT_BOARD_TYPE, \
    SETTINGS_OPENBCI_DEFAULT_SAMPLE_RATE, SETTINGS_OPENBCI_DEFAULT_BOARD_MODE, SETTINGS_OPENBCI_DEFAULT_BAUDRATE, \
    SETTINGS_OPENBCI_DEFAULT_TIMEOUT, SETTINGS_DEFAULT_STIMULUS_BALL_RADIUS, SETTINGS_DEFAULT_STIMULUS_BALL_COLOR, \
    SETTINGS_DEFAULT_STIMULUS_BACKGROUND_COLOR
from saccrec.consts import SETTINGS_STIMULUS_SCREEN_HEIGHT_MINIMUM
from saccrec.consts import SETTINGS_STIMULUS_SACCADIC_DISTANCE_MINIMUM


class Settings(object):

    def __init__(self, parent=None):
        self._settings = QSettings('SaccRec', 'SaccRec', parent)

    # OPENBCI SETTINGS
    @property
    def openbci_port(self) -> str:
        return self._settings.value('OpenBCIPort', '')

    @openbci_port.setter
    def openbci_port(self, value: str):
        self._settings.setValue('OpenBCIPort', value)

    @property
    def openbci_board_type(self) -> str:
        return self._settings.value('OpenBCIBoardType', SETTINGS_OPENBCI_DEFAULT_BOARD_TYPE)

    @openbci_board_type.setter
    def openbci_board_type(self, value: str):
        self._settings.setValue('OpenBCIBoardType', value)

    @property
    def openbci_sample_rate(self) -> int:
        return self._settings.value('OpenBCISampleRate', SETTINGS_OPENBCI_DEFAULT_SAMPLE_RATE)

    @openbci_sample_rate.setter
    def openbci_sample_rate(self, value: int):
        self._settings.setValue('OpenBCISampleRate', value)

    @property
    def openbci_board_mode(self) -> str:
        return self._settings.value('OpenBCIBoardMode', SETTINGS_OPENBCI_DEFAULT_BOARD_MODE)

    @openbci_board_mode.setter
    def openbci_board_mode(self, value: str):
        self._settings.setValue('OpenBCIBoardMode', value)

    @property
    def openbci_baudrate(self) -> int:
        return self._settings.value('OpenBCIBaudrate', SETTINGS_OPENBCI_DEFAULT_BAUDRATE)

    @openbci_baudrate.setter
    def openbci_baudrate(self, value: int):
        self._settings.setValue('OpenBCIBaudrate', value)

    @property
    def openbci_timeout(self) -> int:
        return self._settings.value('OpenBCITimeout', SETTINGS_OPENBCI_DEFAULT_TIMEOUT)

    @openbci_timeout.setter
    def openbci_timeout(self, value: int):
        self._settings.setValue('OpenBCITimeout', value)

    # SCREEN SETTINGS
    @property
    def stimulus_screen_width(self) -> float:
        return float(self._settings.value('StimulusScreenWidth', SETTINGS_STIMULUS_SCREEN_WIDTH_MINIMUM))

    @stimulus_screen_width.setter
    def stimulus_screen_width(self, value: float):
        self._settings.setValue('StimulusScreenWidth', value)

    @property
    def stimulus_screen_height(self) -> float:
        return float(self._settings.value('StimulusScreenHeight', SETTINGS_STIMULUS_SCREEN_HEIGHT_MINIMUM))

    @stimulus_screen_height.setter
    def stimulus_screen_height(self, value: float):
        self._settings.setValue('StimulusScreenHeight', value)

    # STIMULUS SETTINGS
    @property
    def stimulus_saccadic_distance(self) -> float:
        return float(self._settings.value('StimulusSaccadicDistance', SETTINGS_STIMULUS_SACCADIC_DISTANCE_MINIMUM))

    @stimulus_saccadic_distance.setter
    def stimulus_saccadic_distance(self, value: float):
        self._settings.setValue('StimulusSaccadicDistance', value)

    @property
    def stimulus_saccadic_ball_radius(self) -> float:
        return self._settings.value('StimulusSaccadicBallRadius', SETTINGS_DEFAULT_STIMULUS_BALL_RADIUS)

    @stimulus_saccadic_ball_radius.setter
    def stimulus_saccadic_ball_radius(self, value: float):
        self._settings.setValue('StimulusSaccadicBallRadius', value)

    @property
    def stimulus_saccadic_ball_color(self) -> QColor:
        return QColor(self._settings.value('StimulusSaccadicBallColor', SETTINGS_DEFAULT_STIMULUS_BALL_COLOR))

    @stimulus_saccadic_ball_color.setter
    def stimulus_saccadic_ball_color(self, value: str):
        self._settings.setValue('StimulusSaccadicBallColor', value)

    @property
    def stimulus_saccadic_background_color(self) -> QColor:
        return QColor(self._settings.value('StimulusSaccadicBackgroundColor', SETTINGS_DEFAULT_STIMULUS_BACKGROUND_COLOR))

    @stimulus_saccadic_background_color.setter
    def stimulus_saccadic_background_color(self, value: str):
        self._settings.setValue('StimulusSaccadicBackgroundColor', value)
