from math import floor
from typing import List, Dict, Tuple

from numpy import sin, cos, linspace, pi, array, float32, hstack, mean
from numpy.random import randint, random

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import QRect, QPoint, QLineF, QPointF, QTimer

from saccrec.engine.recording import OpenBCIRecorder


SIGNALS_PADDING = 1.5


class SignalsManager:

    def __init__(self, window_width: int = 500):
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
        for timestamp, h, v in samples:
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

        hc_max, hc_min = float(self._hc_window.max()), float(self._hc_window.min())
        hc_center = (hc_max + hc_min) / 2
        vc_max, vc_min = float(self._vc_window.max()), float(self._vc_window.min())
        vc_center = (vc_max + vc_min) / 2

        self._hc_window -= hc_center
        self._vc_window -= vc_center

        self._hc_max = max(abs(hc_max - hc_center), abs(hc_min - hc_center))
        self._vc_max = max(abs(vc_max - hc_center), abs(vc_min - hc_center))

    @property
    def horizontal_lines(self) -> List[QLineF]:
        return self._samples_to_lines(self._hc_window)

    @property
    def vertical_lines(self) -> List[QLineF]:
        return self._samples_to_lines(self._vc_window)
        
    @property
    def horizontal_window(self) -> QRect:
        return QRect(
            QPoint(self._x_offset, self._hc_max * SIGNALS_PADDING), 
            QPoint(self._x_offset + 500, -self._hc_max * SIGNALS_PADDING)
        )

    @property
    def vertical_window(self) -> QRect:
        return QRect(
            QPoint(self._x_offset, self._vc_max * SIGNALS_PADDING), 
            QPoint(self._x_offset + 500, -self._vc_max * SIGNALS_PADDING)
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

        self._manager = SignalsManager(window_width=500)

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
        painter.setWindow(self._manager.horizontal_window)

        painter.setPen(QPen(self._signals_color, 2.0))
        painter.drawLines(self._manager.horizontal_lines)

        painter.restore()

        painter.drawText(channel_rect.topLeft() + QPoint(10, 20), 'Horizontal Channel')

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
        painter.setWindow(self._manager.vertical_window)

        painter.setPen(QPen(self._signals_color, 2.0))
        painter.drawLines(self._manager.vertical_lines)

        painter.restore()

        painter.drawText(channel_rect.topLeft() + QPoint(10, 20), 'Vertical Channel')

        painter.restore()

        painter.end()
