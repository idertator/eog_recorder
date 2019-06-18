from enum import IntEnum

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtCore import QTimer

from .MainWindowUI import Ui_MainWindow
from .PersonDialog import PersonDialog
from .Settings import Settings
from .Stimulator import Stimulator
import random


class BallPosition(IntEnum):
    Left = 0
    Right = 1


class SaccadicStimulator:
    # duration: ms, fixation_mean_duration: ms, fixation_variation: ms
    def __init__(self, duration: int, fixation_mean_duration: int, fixation_variation: int):
        _min = fixation_mean_duration - fixation_variation
        _max = fixation_mean_duration + fixation_variation
        self.values = []
        _sum = 0
        while True:
            value = random.randrange(_min, _max)
            _sum = _sum + value
            self.values.append(_sum)
            if _sum  > duration:
                break
        
    def position(self, delta: int) -> BallPosition: # starts with right position
        for value in self.values:
            if value > delta:
                if self.values.index(value) % 2:
                    return BallPosition(False)
                else:
                    return BallPosition(True)


class MainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self._personDialog = None
        self._settings = Settings(self)

        self.actionAbrir.triggered.connect(self.onPersonDialogOpenClicked)
        self.actionIniciar.triggered.connect(self.onIniciarClicked)

        self._stimulator = Stimulator(self)
        self._stimulatorTimer = QTimer()
        self._stimulatorTimer.setInterval(60)
        self._stimulatorTimer.timeout.connect(self.onTimerTimeout)

        self.setCentralWidget(self._stimulator)

    @property
    def personDialog(self):
        if self._personDialog is None:
            self._personDialog = PersonDialog(self._settings, parent=self)
            self._personDialog.accepted.connect(self.onPersonAccepted)
        return self._personDialog

    def onTimerTimeout(self, *args):
        left = self.rect().center().x() - 700
        right = self.rect().center().x() + 700

        if self._stimulator.position is None:
            self._stimulator.position = left, self.rect().center().y()
        elif self._stimulator.position[0] == left:
            self._stimulator.position = right, self.rect().center().y()
        elif self._stimulator.position[0] == right:
            self._stimulator.position = left, self.rect().center().y()

    def onPersonDialogOpenClicked(self, e):
        self.personDialog.open()

    def onIniciarClicked(self, e):
        self._stimulatorTimer.start()

    def onPersonAccepted(self):
        print(self.personDialog.full_name)