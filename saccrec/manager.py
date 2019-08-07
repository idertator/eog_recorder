from typing import List

from PyQt5.QtCore import QObject, pyqtSignal

from saccrec.core import Settings, Screen


class Manager(QObject):
    started = pyqtSignal()
    stopped = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, settings: Settings, screen: Screen, parent=None):
        super(Manager, self).__init__(parent=parent)

        self._settings = settings
        self._screen = screen

        self._subject = None
        self._stimulus = None
        self._output = None

        self._tests = None

    def start_recording(self, subject, stimulus, output, **kwargs):
        self._subject = subject
        self._stimulus = stimulus
        self._output = output

        self.started.emit()
        
    def stop_recording(self):
        self.stopped.emit()

    @property
    def tests(self) -> List['SaccadicStimuli']:
        if self._tests is None:
            from saccrec.engine.stimulus import SaccadicStimuli

            self._tests = [
                SaccadicStimuli(
                    settings=self._settings,
                    screen=self._screen,
                    angle=30,
                    fixation_duration=self._stimulus['fixation_duration'],
                    fixation_variability=self._stimulus['fixation_variability'],
                    saccades_count=5,
                    test_name='Prueba de Calibración Horizontal Inicial'
                ),
                SaccadicStimuli(
                    settings=self._settings,
                    screen=self._screen,
                    angle=self._stimulus['angle'],
                    fixation_duration=self._stimulus['fixation_duration'],
                    fixation_variability=self._stimulus['fixation_variability'],
                    saccades_count=self._stimulus['saccades_count']
                ),
                SaccadicStimuli(
                    settings=self._settings,
                    screen=self._screen,
                    angle=30,
                    fixation_duration=self._stimulus['fixation_duration'],
                    fixation_variability=self._stimulus['fixation_variability'],
                    saccades_count=5,
                    test_name='Prueba de Calibración Horizontal Final'
                ),
            ]

        return self._tests
