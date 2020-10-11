from math import floor, ceil
from random import randint

from numpy import array, int8, zeros, ones, hstack

from PyQt5.QtCore import QPoint

from saccrec.core import Screen, StimulusPosition
from saccrec.core.math import points_distance
from saccrec import settings


class SaccadicStimuli(object):

    def __init__(
        self,
        screen: Screen,
        distance_to_subject: float,
        angle: int,
        fixation_duration: float,
        fixation_variability: float,
        saccades_count: int,
        test_name: str = 'Prueba Sacádica'
    ):
        """Constructor

        Args:
            screen: (saccrec.core.Screen): Screen object
            distance_to_subject (float): Distance to the subject in cm
            angle (int): Stimuli angle
            fixation_duration (float): Mean fixation duration in seconds
            fixation_variability (float): Variability of the fixation duration in percentage
            saccades_count (int): Amounts of saccades to generate
            test_name (str): Name of the stimulation pattern
        """
        self._screen = screen
        self._distance_to_subject = distance_to_subject

        self._angle = angle
        self._fixation_duration = fixation_duration
        self._fixation_variability = fixation_variability
        self._saccades_count = saccades_count
        self._test_name = test_name

        self._left_ball = None
        self._center_ball = None
        self._right_ball = None
        self._cm_to_pixels_x = 1.0

        samples = floor(fixation_duration * settings.hardware.sampling_rate)
        delta = floor(((fixation_variability / 100.0) * samples) / 2)

        durations = [randint(samples - delta, samples + delta) for _ in range(saccades_count + 2)]

        first, *main, last = durations

        chunks = [zeros(first, dtype=int8)]
        current_angle = -floor(angle / 2)
        for duration in main:
            chunks.append(ones(duration, dtype=int8) * current_angle)
            current_angle *= -1
        chunks.append(zeros(last, dtype=int8))

        self._channel = hstack(chunks)

        self.reset_settings()

    def __str__(self):
        return f'{self._test_name}'

    def _update_positions(self):
        distance = points_distance(self._distance_to_subject, self._angle)

        cm_width = settings.stimuli.screen_width
        cm_center = cm_width / 2
        cm_delta = distance / 2
        self._cm_to_pixels_x = self._screen.secondary_screen_rect.width() / cm_width

        left_x = (cm_center - cm_delta) * self._cm_to_pixels_x
        right_x = (cm_center + cm_delta) * self._cm_to_pixels_x
        center_x = (left_x + right_x) / 2

        y = self._screen.secondary_screen_rect.center().y()

        self._left_ball = QPoint(left_x, y)
        self._center_ball = QPoint(center_x, y)
        self._right_ball = QPoint(right_x, y)

    def reset_settings(self):
        self._update_positions()

    def position(self, sample: int) -> StimulusPosition:
        if sample < len(self._channel):
            if self._channel[sample] < 0:
                return StimulusPosition.Left
            if self._channel[sample] > 0:
                return StimulusPosition.Right
            return StimulusPosition.Center
        return None

    def screen_position(self, sample: int) -> QPoint:
        if self._left_ball is None or self._right_ball is None or self._center_ball is None:
            self._update_positions()

        if sample < len(self._channel):
            value = self._channel[sample]
            if value < 0:
                return self._left_ball
            if value > 0:
                return self._right_ball
            return self._center_ball

        return None

    def cm_to_pixels_x(self, value: float) -> int:
        return ceil(value * self._cm_to_pixels_x)

    @property
    def angle(self) -> int:
        return self._angle

    @property
    def fixation_duration(self) -> float:
        return self._fixation_duration

    @property
    def fixation_variability(self) -> float:
        return self._fixation_variability

    @property
    def saccades_count(self) -> int:
        return self._saccades_count

    @property
    def test_name(self) -> str:
        return self._test_name

    @property
    def channel(self) -> array:
        return self._channel
