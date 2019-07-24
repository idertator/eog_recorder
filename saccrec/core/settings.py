from PyQt5.QtCore import QSettings

from saccrec.consts import SETTINGS_STIMULUS_SCREEN_WIDTH_MINIMUM
from saccrec.consts import SETTINGS_STIMULUS_SCREEN_HEIGHT_MINIMUM
from saccrec.consts import SETTINGS_STIMULUS_SACCADIC_DISTANCE_MINIMUM

from saccrec.engine.recording import list_ports


class Settings(object):

    def __init__(self, parent=None):
        self._settings = QSettings('SaccRec', 'SaccRec', parent)

    @property
    def openbci_port(self) -> str:
        return self._settings.value('OpenBCI_Port', '')

    @openbci_port.setter
    def openbci_port(self, value: str):
        self._settings.setValue('OpenBCI_Port', value)

    @property
    def sampling_frequency(self) -> int:
        return int(self._settings.value('SamplingFrequency', 250))

    @sampling_frequency.setter
    def sampling_frequency(self, value: int):
        self._settings.setValue('SamplingFrequency', value)

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

    @property
    def stimulus_saccadic_distance(self) -> float:
        return float(self._settings.value('StimulusSaccadicDistance', SETTINGS_STIMULUS_SACCADIC_DISTANCE_MINIMUM))

    @stimulus_saccadic_distance.setter
    def stimulus_saccadic_distance(self, value: float):
        self._settings.setValue('StimulusSaccadicDistance', value)
