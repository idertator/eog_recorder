from typing import List

from PyQt5.QtCore import pyqtSignal, QObject

from saccrec.core import Settings, Screen
from saccrec.engine.stimulus import SaccadicStimuli
from saccrec.gui.widgets import StimulusPlayerWidget


class Runner(QObject):
    started = pyqtSignal()
    stopped = pyqtSignal()
    finished = pyqtSignal()

    def __init__(
        self, 
        settings: Settings,
        screen: Screen,
        player: StimulusPlayerWidget, 
        parent=None
    ):
        super(Runner, self).__init__(parent=parent)
        self._settings = settings
        self._screen = screen
        self._player = player

        self._tests = None
        self._next_test = None

        self._player.stopped.connect(self.on_player_stopped)
        self._player.finished.connect(self.on_player_finished)

    def run(self, tests: List[SaccadicStimuli]):
        """Run a set of stimulus grouping them into a recording
        
        Args:
            tests (List[SaccadicStimuli]): List of stimuli to show
        """
        self._tests = tests
        self._next_test = 1

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

    def on_player_stopped(self):
        self._player.close_player()
        self.stopped.emit()
    
    def on_player_finished(self):
        if self._next_test < len(self._tests):
            stimuli = self._tests[self._next_test]
            self._next_test += 1

            self._player.run_stimulus(
                stimuli, 
                '\n'.join([str(stimuli), 'Presione espacio para continuar'])
            )
        else:
            self._player.close_player()
            self.finished.emit()
