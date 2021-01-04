from math import floor, log10
from time import time

from eoglib.models import StimulusPosition
from eoglib.filtering import notch_filter
from numpy import (abs, arange, array, float64, hstack, int32, max, mean,
                   ndarray, ones)
from numpy.random import random
# from pyqtgraph import PlotCurveItem, PlotWidget, AxisItem
from PySide6 import QtWidgets


class SignalsWidget(QtWidgets.QWidget):

    def __init__(self, window_samples: int = 10000, parent=None):
        super(SignalsWidget, self).__init__(parent=parent)

        # self._window_samples = window_samples

        # self._horizontal_curve = PlotCurveItem(pen=(0, 0, 0))
        # self._vertical_curve = PlotCurveItem(pen=(0, 0, 0))

        # self._horizontal_plot = PlotWidget(name=_('Horizontal Channel'))
        # self._horizontal_plot.setBackground(None)
        # self._horizontal_plot.setMouseEnabled(x=False, y=False)
        # self._horizontal_plot.enableAutoRange(x=True, y=True)
        # self._horizontal_plot.setAutoVisible(x=True, y=True)
        # self._horizontal_plot.setLabel('left', _('Horizontal Channel'), units='V')
        # self._horizontal_plot.addItem(self._horizontal_curve)

        # self._vertical_plot = PlotWidget(name=_('Vertical Channel'))
        # self._vertical_plot.setBackground(None)
        # self._vertical_plot.setMouseEnabled(x=False, y=False)
        # self._vertical_plot.enableAutoRange(x=True, y=True)
        # self._vertical_plot.setAutoVisible(x=True, y=True)
        # self._vertical_plot.setLabel('left', _('Vertical Channel'), units='V')
        # self._vertical_plot.addItem(self._vertical_curve)

        # self._layout = QtWidgets.QVBoxLayout()
        # self._layout.addWidget(self._horizontal_plot)
        # self._layout.addWidget(self._vertical_plot)

        # self.reset()

        # self.setLayout(self._layout)

    # def reset(self):
        # self._empty = True
        # self._horizontal_channel = None
        # self._vertical_channel = None

        # self._horizontal_curve.clear()
        # self._vertical_curve.clear()


    # def add_dropped(self, dropped: int):
        # sample_horizontal = self._horizontal_channel[-max(min(10, dropped), 5):]
        # sample_vertical = self._vertical_channel[-max(min(10, dropped), 5):]

        # horizontal_width = max(sample_horizontal) - min(sample_horizontal)
        # vertical_width = max(sample_vertical) - min(sample_vertical)

        # sample_horizontal = random(len(sample_horizontal), dtype=float64) * horizontal_width - horizontal_width / 2
        # sample_vertical = random(len(sample_vertical), dtype=float64) * vertical_width - vertical_width / 2

        # self._horizontal_channel = hstack((self._horizontal_channel, sample_horizontal))[-self._window_samples:]
        # self._vertical_channel = hstack((self._vertical_channel, sample_vertical))[-self._window_samples:]

    # def add_samples(self, horizontal: ndarray, vertical: ndarray):
        # if self._horizontal_channel is None:
        #     self._horizontal_channel = ones(self._window_samples, dtype=float64) * mean(horizontal)
        #     self._vertical_channel = ones(self._window_samples, dtype=float64) * mean(vertical)

        # self._horizontal_channel = hstack((self._horizontal_channel, horizontal))[-self._window_samples:]
        # self._vertical_channel = hstack((self._vertical_channel, vertical))[-self._window_samples:]

        # # Centering at Zero
        # self._horizontal_channel -= int(mean(self._horizontal_channel))
        # self._vertical_channel -= int(mean(self._vertical_channel))

        # self._horizontal_curve.setData(y=notch_filter(self._horizontal_channel, 250, 50))
        # self._vertical_curve.setData(y=notch_filter(self._vertical_channel, 250, 50))
