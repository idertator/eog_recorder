from math import floor, log10
from time import time

from eoglib.models import StimulusPosition
from numpy import (abs, arange, array, float32, hstack, int32, max, mean,
                   ndarray, ones)
from pyqtgraph import PlotCurveItem, PlotWidget, AxisItem
from PySide2 import QtWidgets


class SignalsWidget(QtWidgets.QWidget):

    def __init__(self, window_samples: int = 10000, parent=None):
        super(SignalsWidget, self).__init__(parent=parent)

        self._window_samples = window_samples

        self._horizontal_curve = PlotCurveItem(pen=(0, 0, 0))
        self._vertical_curve = PlotCurveItem(pen=(0, 0, 0))

        self._horizontal_plot = PlotWidget(name=_('Horizontal Channel'))
        self._horizontal_plot.setBackground(None)
        self._horizontal_plot.setMouseEnabled(x=False, y=False)
        self._horizontal_plot.enableAutoRange(x=True, y=True)
        self._horizontal_plot.setAutoVisible(x=True, y=True)
        self._horizontal_plot.setLabel('left', _('Horizontal Channel'), units='V')
        self._horizontal_plot.addItem(self._horizontal_curve)

        self._vertical_plot = PlotWidget(name=_('Vertical Channel'))
        self._vertical_plot.setBackground(None)
        self._vertical_plot.setMouseEnabled(x=False, y=False)
        self._vertical_plot.enableAutoRange(x=True, y=True)
        self._vertical_plot.setAutoVisible(x=True, y=True)
        self._vertical_plot.setLabel('left', _('Vertical Channel'), units='V')
        self._vertical_plot.addItem(self._vertical_curve)

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addWidget(self._horizontal_plot)
        self._layout.addWidget(self._vertical_plot)

        self.reset()

        self.setLayout(self._layout)

    def reset(self):
        self._empty = True
        self._horizontal_channel = None
        self._vertical_channel = None

        self._horizontal_curve.clear()
        self._vertical_curve.clear()

    def add_samples(self, horizontal: ndarray, vertical: ndarray):
        if self._horizontal_channel is None:
            self._horizontal_channel = ones(self._window_samples, dtype=float32) * mean(horizontal)
            self._vertical_channel = ones(self._window_samples, dtype=float32) * mean(vertical)

        self._horizontal_channel = hstack((self._horizontal_channel, horizontal))[-self._window_samples:]
        self._vertical_channel = hstack((self._vertical_channel, vertical))[-self._window_samples:]

        # Centering at Zero
        self._horizontal_channel -= int(mean(self._horizontal_channel))
        self._vertical_channel -= int(mean(self._vertical_channel))

        self._horizontal_curve.setData(y=self._horizontal_channel)
        self._vertical_curve.setData(y=self._vertical_channel)
