from math import ceil, floor
from time import time

from PyQt5 import QtCore, QtGui, QtWidgets

from saccrec import settings
from saccrec.core.enums import StimulusPosition
from saccrec.core.study import Stimulus


class StimulusPlayer(QtWidgets.QWidget):
    started = QtCore.pyqtSignal(float)
    stopped = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()
    moved = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(StimulusPlayer, self).__init__()

        self._parent = parent

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._on_timeout)

        self._sampling_step = None

        self._timeout = None
        self._start_time = None
        self._stimulus = None

        self._message = None
        self._left_ball = None
        self._center_ball = None
        self._right_ball = None

        self._ball_position = None

    def _load_settings(self):
        # Timer interval computing based on refresh rate
        self._timeout = floor(1000.0 / screen.secondary_screen_refresh_rate / 2.0)
        self._timer.setInterval(self._timeout)

        # Sampling Step
        self._sampling_step = 1000 / settings.hardware.sampling_rate

        # Ball properties computing
        ball_radius = settings.stimuli.ball_radius

        if self._stimuli is None:
            self._ball_radius = ball_radius
        else:
            self._ball_radius = self._stimuli.cm_to_pixels_x(ball_radius)

        self._ball_color = settings.stimuli.ball_color
        self._background_color = settings.stimuli.back_color

        # Points Distance Computing
        distance = (tan(radians(self._stimulus.angle / 2.0)) * self._stimulus.distance_to_subject) * 2

        cm_width = settings.stimuli.screen_width
        cm_center, cm_delta = cm_width / 2, distance / 2
        self._cm_to_pixels_x = settings.screen.secondary_screen_rect.width() / cm_width

        left_x = (cm_center - cm_delta) * self._cm_to_pixels_x
        right_x = (cm_center + cm_delta) * self._cm_to_pixels_x
        center_x = (left_x + right_x) / 2

        y = settings.screen.secondary_screen_rect.center().y()

        self._left_ball = QtCore.QPoint(left_x, y)
        self._center_ball = QtCore.QPoint(center_x, y)
        self._right_ball = QtCore.QPoint(right_x, y)

    def _screen_position(self, sample: int) -> QtCore.QPoint:
        position = self._stimulus.position(sample)
        return {
            StimulusPosition.Left: self._left_ball,
            StimulusPosition.Right: self._right_ball,
            StimulusPosition.Center: self._center_ball,
        }.get(position, None)

    def start(self, stimulus: Stimulus):
        self._stimulus = stimulus

        self._load_settings()

        self._message = '\n'.join(
            self._stimulus.name,
            _('Presione espacio para continuar')
        )
        self.update()

    def stop(self):
        self._timer.stop()
        self.stopped.emit()

        self._stimulus = None

    def finished(self):
        self._timer.stop()
        self.finished.emit()

        self._stimulus = None

    def close(self):
        self.setParent(QtWidgets.qApp.topLevelWidgets()[0])
        self.close()
        self.setParent(None)

    def _start_test(self):
        self._message = None
        self._ball_position = self.screen_position(0)
        self._start_time = time()
        self.update()
        self._timer.start()
        self.started.emit(self._start_time)

    def _on_timeout(self):
        elapsed = (time() - self._start_time) * 1000.0
        current_sample = ceil(elapsed / self._sampling_step)

        previous_position = self._ball_position
        self._ball_position = self.screen_position(current_sample)

        if previous_position != self._ball_position:
            self.update()
            self.moved.emit(self._ball_position.value)

        if self._ball_position is None:
            self.finished()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)

        painter.setBackground(self._background_color)
        painter.fillRect(self.rect(), self._background_color)

        if self._message is not None:
            painter.save()
            painter.setPen(self._ball_color)

            font = painter.font()
            font.setPixelSize(48)
            painter.setFont(font)

            painter.drawText(
                self.rect(),
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                self._message
            )
            painter.restore()

        if self._ball_position is not None:
            painter.setPen(self._ball_color)
            painter.setBrush(self._ball_color)
            painter.drawEllipse(self._ball_position, self._ball_radius, self._ball_radius)

        painter.end()

    def keyPressEvent(self, event):
        if self._time.isActive():
            if (event.modifiers() & QtCore.Qt.ControlModifier) and event.key() == QtCore.Qt.Key_C:
                self.stop()
        else:
            if event.key() == QtCore.Qt.Key_Space:
                self._start_test()
