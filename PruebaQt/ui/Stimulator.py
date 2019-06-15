from typing import Optional, Tuple

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
