from PyQt5.QtCore import pyqtSignal, QObject, QSettings

from saccrec.core import Settings, Screen, Record
from saccrec.core.models import Subject, Hardware
from saccrec.engine.recording import OpenBCIRecorder
from saccrec import settings as SETTINGS

from .player import StimulusPlayerWidget
from .signals import SignalsWidget

_settings = QSettings()


class Runner(QObject):
    started = pyqtSignal()
    stopped = pyqtSignal()
    finished = pyqtSignal()

    def __init__(
        self,
        settings: Settings,
        screen: Screen,
        player: StimulusPlayerWidget,
        signals: SignalsWidget,
        parent=None
    ):
        super(Runner, self).__init__(parent=parent)
        self._settings = settings
        self._screen = screen
        self._player = player
        self._signals = signals

        port = _settings.value(SETTINGS.OPENBCI_PORT)
        sampling_rate = _settings.value(SETTINGS.OPENBCI_SAMPLING_RATE, 1000)

        self._recorder = OpenBCIRecorder(port=port, sampling_rate=sampling_rate)

        self._tests = None
        self._next_test = None

        self._subject = None
        self._stimulus = None
        self._output = None
        self._distance_to_subject = None
        self._tests = None
        self._record = None

        self._player.started.connect(self.on_player_started)
        self._player.stopped.connect(self.on_player_stopped)
        self._player.finished.connect(self.on_player_finished)
        self._player.moved.connect(self.on_player_moved)

    def run(self, subject, stimulus, output, distance_to_subject, tests, **kwargs):
        self._subject = subject
        self._stimulus = stimulus
        self._output = output
        self._distance_to_subject = distance_to_subject
        self._tests = tests

        subject = Subject.from_json(subject)

        sampling_rate = int(_settings.value(SETTINGS.OPENBCI_SAMPLING_RATE, 250))

        hardware = Hardware(
            sample_rate=sampling_rate,
            channels=self._settings.openbci_channels.json
        )

        self._record = Record(
            subject=subject,
            hardware=hardware
        )

        tests = self._tests
        self._next_test = 1

        self._signals.hide()

        stimuli = tests[0]
        self._player.run_stimulus(
            stimuli,
            '\n'.join([str(stimuli), _('Presione espacio para continuar')])
        )
        self._player.move(
            self._screen.secondary_screen_rect.left(),
            self._screen.secondary_screen_rect.top()
        )

        self._player.showFullScreen()
        self.started.emit()

    def on_player_started(self):
        if not self._signals.isVisible():
            self._signals.show()

        if not self._recorder.is_alive():
            self._recorder.start()
            self._recorder.wait_until_ready()

        if not self._signals.is_rendering:
            self._signals.start(self._recorder)

        test_filename = self._recorder.start_recording()
        print(test_filename)

    def on_player_stopped(self):
        self._signals.stop()
        self._recorder.stop_recording()

        self.stopped.emit()

    def on_player_finished(self):
        self._signals.stop()
        self._recorder.stop_recording()

        current_test = self._tests[self._next_test - 1]
        self._record.add_test(
            stimulus=current_test.channel,
            angle=current_test.angle,
            fixation_duration=current_test.fixation_duration,
            fixation_variability=current_test.fixation_variability,
            saccades_count=current_test.saccades_count,
            test_name=current_test.test_name
        )

        if self._next_test < len(self._tests):
            stimuli = self._tests[self._next_test]
            self._next_test += 1

            self._player.run_stimulus(
                stimuli,
                '\n'.join([str(stimuli), _('Presione espacio para continuar')])
            )
        else:
            self._player.close_player()
            self._record.save(self._output)
            self.finished.emit()

    def on_player_moved(self, position: int):
        self._recorder.put_marker(position)
