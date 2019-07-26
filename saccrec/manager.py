from PyQt5.QtCore import QObject, pyqtSignal

from saccrec.core import Settings, Screen


class Manager(QObject):
    recordingStarted = pyqtSignal()
    recordingStopped = pyqtSignal()
    recordingFinished = pyqtSignal()

    def __init__(self, settings: Settings, screen: Screen, parent=None):
        super(Manager, self).__init__(parent=parent)

        self._settings = settings
        self._screen = screen

        self._subject = None
        self._stimulus = None
        self._output = None

    def start_recording(self, subject, stimulus, output, **kwargs):
        self._subject = subject
        self._stimulus = stimulus
        self._output = output

        self.recordingStarted.emit()
        
    def stop_recording(self):
        self.recordingStopped.emit()

    @property
    def current_stimuli(self):
        if self._stimulus is not None:
            from saccrec.engine.stimulus import SaccadicStimuli

            return SaccadicStimuli(
                settings=self._settings,
                screen=self._screen,
                angle=self._stimulus['angle'],
                fixation_duration=self._stimulus['fixation_duration'],
                fixation_variability=self._stimulus['fixation_variability'],
                saccades_count=self._stimulus['saccades_count']
            )
        return None
