from math import floor
from typing import List, Tuple

from numpy import array, float32, hstack

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import QRect, QPoint, QLineF, QPointF, QTimer

from saccrec.engine.recording import OpenBCIRecorder


SIGNALS_PADDING = 1.5
WINDOWS_WIDTH = 4000


class SignalsManager:

    def __init__(self, window_width: int = WINDOWS_WIDTH):
        self._window_width = window_width

        self._hc_window = array([], dtype=float32)
        self._hc_max = 0
        self._vc_window = array([], dtype=float32)
        self._vc_max = 0
        self._x_offset = 0

    def _samples_to_lines(self, samples: array) -> List[QLineF]:
        lines = []

        last = None
        for index, sample in enumerate(samples):
            current = QPointF(index + self._x_offset, sample)
            if last is not None:
                lines.append(QLineF(last, current))
            last = current

        return lines

    def add_samples(self, samples: List[Tuple[int, float, float]]):
        horizontal = []
        vertical = []
        for _, timestamp, h, v in samples:
            horizontal.append(h)
            vertical.append(v)

        horizontal = array(horizontal, dtype=float32)
        vertical = array(vertical, dtype=float32)

        self._hc_window = hstack((self._hc_window, horizontal))
        self._vc_window = hstack((self._vc_window, vertical))

        length = len(self._hc_window)
        if length > self._window_width:
            self._x_offset += length - self._window_width
            self._hc_window = self._hc_window[length - self._window_width:]
            self._vc_window = self._vc_window[length - self._window_width:]

    @property
    def horizontal_lines(self) -> List[QLineF]:
        if self._hc_window.any():
            channel = self._hc_window - self._hc_window.mean()
            self._hc_max = max(abs(channel.min()), abs(channel.max()))
            return self._samples_to_lines(channel)
        return []

    @property
    def vertical_lines(self) -> List[QLineF]:
        if self._vc_window.any():
            channel = self._vc_window - self._vc_window.mean()
            self._vc_max = max(abs(channel.min()), abs(channel.max()))
            return self._samples_to_lines(channel)
        return []

    @property
    def horizontal_window(self) -> QRect:
        return QRect(
            QPoint(self._x_offset, self._hc_max * SIGNALS_PADDING),
            QPoint(self._x_offset + WINDOWS_WIDTH, -self._hc_max * SIGNALS_PADDING)
        )

    @property
    def vertical_window(self) -> QRect:
        return QRect(
            QPoint(self._x_offset, self._vc_max * SIGNALS_PADDING),
            QPoint(self._x_offset + WINDOWS_WIDTH, -self._vc_max * SIGNALS_PADDING)
        )


class SignalsWidget(QWidget):

    def __init__(self, parent=None):
        super(SignalsWidget, self).__init__(parent=parent)

        self._channel_padding = 10
        self._left_padding = 100

        self._background = QColor(255, 255, 255)
        self._channels_outline_width = 2
        self._channels_outline = QColor(150, 150, 150)
        self._signals_color = QColor(30, 30, 100)

        self._manager = SignalsManager(window_width=WINDOWS_WIDTH)

        self._refresh_timer = QTimer()
        self._refresh_timer.setInterval(200)
        self._refresh_timer.timeout.connect(self.fetch_signals)
        self._rendering = False

        self._recorder = None

    def start(self, recorder: OpenBCIRecorder):
        self._rendering = True
        self._recorder = recorder
        self._refresh_timer.start()

    def stop(self):
        self._refresh_timer.stop()
        self._rendering = False

    def fetch_signals(self):
        samples = self._recorder.read_samples()
        if samples:
            self._manager.add_samples(samples)
            self.update()

    @property
    def is_rendering(self) -> bool:
        return self._rendering

    @property
    def channel_height(self) -> int:
        padding_total = 3 * self._channel_padding
        return floor((self.size().height() - padding_total) / 2)

    @property
    def channel_width(self) -> int:
        return self.size().width() - (self._left_padding + self._channel_padding)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), self._background)

        # Horizontal Channel
        painter.save()
        channel_rect = QRect(
            self._left_padding, self._channel_padding,
            self.channel_width, self.channel_height
        )
        painter.setPen(QPen(self._channels_outline, self._channels_outline_width))
        painter.drawRect(channel_rect)

        painter.save()
        viewport = channel_rect.adjusted(1, 1, -1, -1)
        painter.setClipRect(viewport)
        painter.setViewport(viewport)
        lines = self._manager.horizontal_lines
        painter.setWindow(self._manager.horizontal_window)

        pen = QPen(self._signals_color, 2.0)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLines(lines)

        painter.restore()

        painter.drawText(channel_rect.topLeft() + QPoint(10, 20), _('Canal Horizontal'))

        painter.restore()

        # Vertical Channel
        painter.save()
        channel_rect = QRect(
            self._left_padding, self._channel_padding + self.channel_height + self._channel_padding,
            self.channel_width, self.channel_height
        )
        painter.setPen(QPen(self._channels_outline, self._channels_outline_width))
        painter.drawRect(channel_rect)

        painter.save()
        viewport = channel_rect.adjusted(1, 1, -1, -1)
        painter.setClipRect(viewport)
        painter.setViewport(viewport)
        lines = self._manager.vertical_lines
        painter.setWindow(self._manager.vertical_window)

        pen = QPen(self._signals_color, 3.0)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLines(lines)

        painter.restore()

        painter.drawText(channel_rect.topLeft() + QPoint(10, 20), _('Canal Vertical'))

        painter.restore()

        painter.end()
