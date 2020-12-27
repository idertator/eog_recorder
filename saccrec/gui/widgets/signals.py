from math import floor, log10

from eoglib.models import StimulusPosition
from numpy import array, int32, hstack

from PySide6 import QtWidgets, QtCore, QtGui


SIGNALS_PADDING = 1.5
WINDOWS_WIDTH = 4000


class SignalsManager:

    def __init__(self, window_width: int = WINDOWS_WIDTH):
        self._window_width = window_width
        self._current_stimulus_position = 0

        self._hc_window = array([], dtype=int32)
        self._hc_max = 0
        self._vc_window = array([], dtype=int32)
        self._vc_max = 0
        self._sc_window = array([], dtype=int32)
        self._sc_max = 0
        self._x_offset = 0

    def _samples_to_lines(self, samples: array) -> list[QtCore.QLineF]:
        lines = []

        last = None
        for index, sample in enumerate(samples):
            current = QtCore.QPointF(index + self._x_offset, sample)
            if last is not None:
                lines.append(QtCore.QLineF(last, current))
            last = current

        return lines

    def add_samples(self, samples: list[tuple[int, int, int]]):
        horizontal = []
        vertical = []
        stimulus = []
        for  h, v, c in samples:
            if c != 0:
                position = StimulusPosition(c)
                if position == StimulusPosition.Left:
                    self._current_stimulus_position = -1
                elif position == StimulusPosition.Right:
                    self._current_stimulus_position = 1
                elif position == StimulusPosition.Center:
                    self._current_stimulus_position = 0

            horizontal.append(h)
            vertical.append(v)
            stimulus.append(self._current_stimulus_position)

        horizontal = array(horizontal, dtype=int32)
        vertical = array(vertical, dtype=int32)
        stimulus = array(stimulus, dtype=int32)

        self._hc_window = hstack((self._hc_window, horizontal))
        self._vc_window = hstack((self._vc_window, vertical))
        self._sc_window = hstack((self._sc_window, stimulus))

        length = len(self._hc_window)
        if length > self._window_width:
            self._x_offset += length - self._window_width
            self._hc_window = self._hc_window[length - self._window_width:]
            self._vc_window = self._vc_window[length - self._window_width:]
            self._sc_window = self._sc_window[length - self._window_width:]

    @property
    def horizontal_lines(self) -> list[QtCore.QLineF]:
        if self._hc_window.any():
            channel = self._hc_window - self._hc_window.mean()
            self._hc_max = max(abs(channel.min()), abs(channel.max()))
            return self._samples_to_lines(channel)
        return []

    @property
    def vertical_lines(self) -> list[QtCore.QLineF]:
        if self._vc_window.any():
            channel = self._vc_window - self._vc_window.mean()
            self._vc_max = max(abs(channel.min()), abs(channel.max()))
            return self._samples_to_lines(channel)
        return []

    @property
    def stimulus_lines(self) -> list[QtCore.QLineF]:
        if self._sc_window.any():
            channel = self._sc_window * (10 ** floor(log10(self._hc_max)))
            return self._samples_to_lines(channel)
        return []

    @property
    def horizontal_window(self) -> QtCore.QRect:
        return QtCore.QRect(
            QtCore.QPoint(self._x_offset, self._hc_max * SIGNALS_PADDING),
            QtCore.QPoint(self._x_offset + WINDOWS_WIDTH, -self._hc_max * SIGNALS_PADDING)
        )

    @property
    def vertical_window(self) -> QtCore.QRect:
        return QtCore.QRect(
            QtCore.QPoint(self._x_offset, self._vc_max * SIGNALS_PADDING),
            QtCore.QPoint(self._x_offset + WINDOWS_WIDTH, -self._vc_max * SIGNALS_PADDING)
        )


class SignalsWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(SignalsWidget, self).__init__(parent=parent)

        self._channel_padding = 10
        self._left_padding = 100

        self._background = QtGui.QColor(255, 255, 255)
        self._channels_outline_width = 2
        self._channels_outline = QtGui.QColor(150, 150, 150)
        self._signals_color = QtGui.QColor(30, 30, 100)

        self._manager = SignalsManager(window_width=WINDOWS_WIDTH)

    def add_samples(self, samples: list[tuple[int, int, int]]):
        self._manager.add_samples(samples)
        self.update()

    @property
    def channel_height(self) -> int:
        padding_total = 3 * self._channel_padding
        return floor((self.size().height() - padding_total) / 2)

    @property
    def channel_width(self) -> int:
        return self.size().width() - (self._left_padding + self._channel_padding)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(self.rect(), self._background)

        # Horizontal Channel
        painter.save()
        channel_rect = QtCore.QRect(
            self._left_padding, self._channel_padding,
            self.channel_width, self.channel_height
        )
        painter.setPen(QtGui.QPen(self._channels_outline, self._channels_outline_width))
        painter.drawRect(channel_rect)

        painter.save()
        viewport = channel_rect.adjusted(1, 1, -1, -1)
        painter.setClipRect(viewport)
        painter.setViewport(viewport)
        painter.setWindow(self._manager.horizontal_window)

        pen = QtGui.QPen(self._signals_color, 2.0)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLines(self._manager.stimulus_lines)
        painter.drawLines(self._manager.horizontal_lines)

        painter.restore()

        painter.drawText(channel_rect.topLeft() + QtCore.QPoint(10, 20), _('Horizontal Channel'))

        painter.restore()

        # Vertical Channel
        painter.save()
        channel_rect = QtCore.QRect(
            self._left_padding, self._channel_padding + self.channel_height + self._channel_padding,
            self.channel_width, self.channel_height
        )
        painter.setPen(QtGui.QPen(self._channels_outline, self._channels_outline_width))
        painter.drawRect(channel_rect)

        painter.save()
        viewport = channel_rect.adjusted(1, 1, -1, -1)
        painter.setClipRect(viewport)
        painter.setViewport(viewport)
        painter.setWindow(self._manager.vertical_window)

        pen = QtGui.QPen(self._signals_color, 3.0)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLines(self._manager.vertical_lines)

        painter.restore()

        painter.drawText(channel_rect.topLeft() + QtCore.QPoint(10, 20), _('Vertical Channel'))

        painter.restore()

        painter.end()
