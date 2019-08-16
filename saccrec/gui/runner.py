from typing import List

from PyQt5.QtCore import pyqtSignal, QObject

from saccrec.core import Settings, Screen, Record
from saccrec.core.models import Subject, Hardware
from saccrec.engine.stimulus import SaccadicStimuli
from saccrec.gui.widgets import StimulusPlayerWidget, SignalsWidget


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

    @property
    def tests(self) -> List[SaccadicStimuli]:
        if self._tests is None:
            self._tests = [
                SaccadicStimuli(
                    settings=self._settings,
                    screen=self._screen,
                    distance_to_subject=self._distance_to_subject,
                    angle=30,
                    fixation_duration=self._stimulus['fixation_duration'],
                    fixation_variability=self._stimulus['fixation_variability'],
                    saccades_count=5,
                    test_name='Prueba de Calibración Horizontal Inicial'
                ),
                SaccadicStimuli(
                    settings=self._settings,
                    screen=self._screen,
                    distance_to_subject=self._distance_to_subject,
                    angle=self._stimulus['angle'],
                    fixation_duration=self._stimulus['fixation_duration'],
                    fixation_variability=self._stimulus['fixation_variability'],
                    saccades_count=self._stimulus['saccades_count']
                ),
                SaccadicStimuli(
                    settings=self._settings,
                    screen=self._screen,
                    distance_to_subject=self._distance_to_subject,
                    angle=30,
                    fixation_duration=self._stimulus['fixation_duration'],
                    fixation_variability=self._stimulus['fixation_variability'],
                    saccades_count=5,
                    test_name='Prueba de Calibración Horizontal Final'
                ),
            ]

        return self._tests

    def run(self, subject, stimulus, output, distance_to_subject, **kwargs):
        self._subject = subject
        self._stimulus = stimulus
        self._output = output
        self._distance_to_subject = distance_to_subject

        subject = Subject.from_json(subject)
        hardware = Hardware(
            board=self._settings.openbci_board_type,
            mode=self._settings.openbci_board_mode,
            sample_rate=self._settings.openbci_sample_rate,
            channels=self._settings.openbci_channels.json
        )

        self._record = Record(
            subject=subject,
            hardware=hardware
        )

        tests = self.tests
        self._next_test = 1

        self._signals.hide()

        stimuli = tests[0]
        self._player.run_stimulus(
            stimuli, 
            '\n'.join([str(stimuli), 'Presione espacio para continuar'])
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

        if not self._signals.is_rendering:
            self._signals.start()

    def on_player_stopped(self):
        self._signals.stop()
        self._player.close_player()
        self.stopped.emit()
    
    def on_player_finished(self):
        self._signals.stop()

        current_test = self._tests[self._next_test - 1]
        self._record.add_test(
            stimulus=current_test.channel,
            horizontal=None,
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
                '\n'.join([str(stimuli), 'Presione espacio para continuar'])
            )
        else:
            self._player.close_player()
            self._record.save(self._output)
            self.finished.emit()
