from math import log10

from numpy import arange, array, float32, hstack, int32, ones, zeros
from pyqtgraph import PlotCurveItem, PlotWidget, setConfigOption
from PySide6 import QtGui, QtWidgets

SAMPLING_STEP = 4
WINDOW_LENGTH = 3000


class SignalsWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(SignalsWidget, self).__init__(parent=parent)

        background_color = self.palette().color(QtGui.QPalette.Window)

        self._first = True

        self._time = None
        self._horizontal = None
        self._vertical = None
        self._positions = None

        setConfigOption('background', background_color)
        setConfigOption('foreground', 'k')

        self._horizontal_plot = PlotCurveItem()
        self._horizontal_positions_plot = PlotCurveItem()

        self._horizontal_widget = PlotWidget()
        self._horizontal_widget.setTitle(_('Horizontal Channel'))
        self._horizontal_widget.setMouseEnabled(False, False)
        self._horizontal_widget.enableAutoRange(True, True)
        self._horizontal_widget.addItem(self._horizontal_plot)
        self._horizontal_widget.addItem(self._horizontal_positions_plot)

        self._vertical_plot = PlotCurveItem()
        self._vertical_positions_plot = PlotCurveItem()

        self._vertical_widget = PlotWidget()
        self._vertical_widget.setTitle(_('Vertical Channel'))
        self._vertical_widget.setMouseEnabled(False, False)
        self._vertical_widget.enableAutoRange(True, True)
        self._vertical_widget.addItem(self._vertical_plot)
        self._vertical_widget.addItem(self._vertical_positions_plot)

        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(self._horizontal_widget)
        layout.addWidget(self._vertical_widget)

        self.setLayout(layout)

        self.reset_data()

    def reset_data(self):
        self._first = True

        self._time = arange(WINDOW_LENGTH, dtype=int32) * SAMPLING_STEP
        self._horizontal = ones(WINDOW_LENGTH, dtype=float32)
        self._vertical = ones(WINDOW_LENGTH, dtype=float32)
        self._positions = zeros(WINDOW_LENGTH, dtype=int32)

        self._horizontal_plot.setData(self._time, self._horizontal)
        self._horizontal_positions_plot.setData(self._time, self._positions)
        self._vertical_plot.setData(self._time, self._vertical)
        self._vertical_positions_plot.setData(self._time, self._positions)

    def plot(self, horizontal: array, vertical: array, positions: array):
        if self._horizontal.size > 0 and self._first:
            self._horizontal = self._horizontal * horizontal.mean()
            self._vertical = self._vertical * vertical.mean()
            self._first = False

        time = (arange(1, len(horizontal) + 1, dtype=int32) * SAMPLING_STEP) + self._time[-1]

        self._time = hstack((self._time, time))[-WINDOW_LENGTH:]
        self._horizontal = hstack((self._horizontal, horizontal))[-WINDOW_LENGTH:]
        self._vertical = hstack((self._vertical, vertical))[-WINDOW_LENGTH:]
        self._positions = hstack((self._positions, positions))[-WINDOW_LENGTH:]

        horizontal_mean, horizontal_std = self._horizontal.mean(), self._horizontal.std()
        horizontal_scale = 10 ** log10(horizontal_std * 4)

        vertical_mean, vertical_std = self._vertical.mean(), self._vertical.std()
        self._vertical -= vertical_mean
        vertical_scale = 10 ** log10(vertical_std * 4)

        self._horizontal_plot.setData(
            self._time, self._horizontal - horizontal_mean,
            pen='b',
            antialias=True
        )
        self._horizontal_positions_plot.setData(
            self._time, self._positions * horizontal_scale,
            pen='r'
        )

        self._vertical_plot.setData(
            self._time, self._vertical - vertical_mean,
            pen='b',
            antialias=True
        )

        self._vertical_positions_plot.setData(
            self._time, self._positions * vertical_scale,
            pen='r'
        )
