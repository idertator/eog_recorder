from os import makedirs
from os.path import expanduser, join, exists
from typing import List

from PyQt5.QtCore import QSettings

from saccrec.consts import DEFAULT_TEST, TESTS


class Channel(object):

    def __init__(self, settings: QSettings, parent=None):
        self._settings = settings
        self._channels = [
            (
                bool(int(self._settings.value(f'OpenBCIChannels/Activated{index}', 1))),
                int(self._settings.value(f'OpenBCIChannels/Gain{index}', 24))
            ) for index in range(8)
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

