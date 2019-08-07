from math import floor
from typing import List, Dict

from numpy import sin, cos, linspace, pi, array
from numpy.random import randint, random

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import QRect, QPoint, QLineF, QPointF, QTimer

HORIZONTAL_CHANNEL = 'Horizontal Channel'
VERTICAL_CHANNEL = 'Vertical Channel'
CHANNELS = [HORIZONTAL_CHANNEL, VERTICAL_CHANNEL]


class SignalsManager:

    def __init__(self, channels: List[str] = CHANNELS, window_width: int = 500):
        self._channels = channels
        self._window_width = window_width
        self._lines = {channel: [] for channel in channels}

    @staticmethod
    def samples_to_lines(samples: array, x_offset: int):
        lines = []

        last = None
        for index, sample in enumerate(samples):
            current = QPointF(index + x_offset, sample)
            if last is not None:
                lines.append(QLineF(last, current))
            last = current

        return lines

    @staticmethod
    def merge_lines(first: List[QLineF], last: List[QLineF], max_samples: int) -> List[QLineF]:
        total = len(first) + len(last) + 1

        if total > max_samples:
            result = first + last
            return result[len(result) - max_samples:]

        if first:
            first.append(QLineF(first[-1].p2(), last[0].p1()))
            return first + last
        return last

    def add_samples(self, samples: Dict[str, array]):
        for channel, samples in samples.items():
            first = self._lines[channel]
            x = first[-1].p2().x() + 1 if first else 0
            last = SignalsManager.samples_to_lines(samples, x)

            self._lines[channel] = SignalsManager.merge_lines(first, last, self._window_width)

    def add_random_samples(self, samples_count: int = 50, abs_max: float = 300.0):
        samples = {}
        for channel in self._lines.keys():
            samples[channel] = (random(samples_count) - 0.5) * abs_max * 2

        self.add_samples(samples)

    def lines(self, channel: str) -> List[QLineF]:
        return self._lines.get(channel, [])

    @property
    def window(self) -> QRect:
        for channel, lines in self._lines.items():
            min_x = 0
            max_x = self._window_width
            if lines:
                min_x = lines[0].p1().x()
                max_x = max(self._window_width, lines[-1].p2().x())

            return QRect(QPoint(min_x, 500), QPoint(max_x, -500))


class SignalsWidget(QWidget):

    def __init__(self, parent=None):
        super(SignalsWidget, self).__init__(parent=parent)

        self._channels = CHANNELS
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

    def start(self):
        self._rendering = True
        self._refresh_timer.start()

    def stop(self):
        self._refresh_timer.stop()
        self._rendering = False

    def fetch_signals(self):
        self._manager.add_random_samples()
        self.update()

    @property
    def is_rendering(self) -> bool:
        return self._rendering

    @property
    def channel_height(self) -> int:
        channels = len(self._channels)
        padding_total = (channels + 1) * self._channel_padding
        return floor((self.size().height() - padding_total) / channels)

    @property
    def channel_width(self) -> int:
        return self.size().width() - (self._left_padding + self._channel_padding)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self._background)

        channels = len(self._channels)
        for channel, channel_title in enumerate(self._channels):
            painter.save()

            channel_rect = QRect(
                self._left_padding, self._channel_padding + (channel * (self.channel_height + self._channel_padding)),
                self.channel_width, self.channel_height
            )
            painter.setPen(QPen(self._channels_outline, self._channels_outline_width))
            painter.drawRect(channel_rect)

            painter.save()
            viewport = channel_rect.adjusted(1, 1, -1, -1)
            painter.setClipRect(viewport)
            painter.setViewport(viewport)
            window = self._manager.window
            painter.setWindow(window)

            painter.setPen(QPen(self._signals_color, 0.8))
            lines = self._manager.lines(channel_title)
            painter.drawLines(lines)

            painter.restore()

            painter.drawText(channel_rect.topLeft() + QPoint(10, 20), channel_title)

            painter.restore()

        painter.end()
