from typing import Optional, Tuple
from enum import IntEnum

from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtGui import QPainter, QColor, QPen


class Stimulator(QWidget):

    def __init__(self, parent=None):
        super(Stimulator, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.backgroundColor = QColor(0, 0, 0)
        self.objectColor = QColor(255, 255, 255)
        self.objectSize = 30
        self._position = None

    @property
    def position(self) -> Optional[Tuple[int, int]]:
        return self._position

    @position.setter
    def position(self, value: Optional[Tuple[int, int]]):
        self._position = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        painter.setBackground(self.backgroundColor)
        painter.fillRect(self.rect(), self.backgroundColor)

        painter.setBrush(self.objectColor)

        if self._position is not None:
            x, y = self._position

            print(x, y)
            painter.drawEllipse(x, y, self.objectSize, self.objectSize)

        painter.end()

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
