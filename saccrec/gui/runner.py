from typing import List, Tuple

from PyQt5.QtCore import pyqtSignal, QObject

from saccrec.engine.stimulus import SaccadicStimuli
from saccrec.gui.widgets import StimulusPlayerWidget


class Runner(QObject):
    started = pyqtSignal()
    finished = pyqtSignal()
    testStarted = pyqtSignal()
    testFinished = pyqtSignal()

    def __init__(self, player: StimulusPlayerWidget, parent=None):
        super(Runner, self).__init__(parent=parent)
        self._player = player

    def run(self, tests: List[Tuple[SaccadicStimuli, str]]):
        """Run a set of stimulus grouping them into a recording
        
        Args:
            tests (List[Tuple[SaccadicStimuli, str]]): List of tuples of two elements
                First element - Stimuli signal to run
                Second element - Initial message to show

        TODO: Implement this
        """
        pass