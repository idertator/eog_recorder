from math import floor, ceil
from random import randint

from numpy import array, int8, zeros, ones, hstack

from PyQt5.QtCore import QPoint

from saccrec.core import Settings, Screen, StimulusPosition


class SaccadicStimuli(object):
    
    def __init__(self,
        settings: Settings,
        screen: Screen,
        angle: int,
        fixation_duration: float,   
        fixation_variability: float,
        saccades_count: int,
        test_name: str = 'Prueba Sacádica'
    ):
        """Constructor
    
        Args:
            settings (saccrec.core.Settings): Settings object
            screen: (saccrec.core.Screen): Screen object
            angle (int): Stimuli angle
            fixation_duration (float): Mean fixation duration in seconds
            fixation_variability (float): Variability of the fixation duration in percentage
            saccades_count (int): Amounts of saccades to generate
            test_name (str): Name of the stimulation pattern
        """
        self._settings = settings
        self._screen = screen

        self._angle = angle
        self._test_name = test_name

        self._left_ball = None
        self._center_ball = None
        self._right_ball = None
        self._cm_to_pixels_x = 1.0

        sampling_rate = settings.openbci_sample_rate

        samples = floor(fixation_duration * sampling_rate)
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
        return f'{self._test_name} {self._angle}\u00B0'

    def _update_positions(self):
        cm_width = self._settings.stimulus_screen_width
        cm_center = cm_width / 2
        cm_delta = self._settings.stimulus_saccadic_distance / 2
        self._cm_to_pixels_x = self._screen.secondary_screen_rect.width() / cm_width

        left_x = (cm_center - cm_delta) * self._cm_to_pixels_x
        right_x = (cm_center + cm_delta) * self._cm_to_pixels_x
        center_x = self._screen.secondary_screen_rect.center().x()

        y = self._screen.secondary_screen_rect.center().y()

        self._left_ball = QPoint(left_x, y)
        self._center_ball = QPoint(center_x, y)
        self._right_ball = QPoint(right_x, y)

    def reset_settings(self):
        self._update_positions()

    def position(self, sample: int) -> StimulusPosition:
        if self._channel[sample] < 0:
            return StimulusPosition.Left
        if self._channel[sample] > 0:
            return StimulusPosition.Right
        return StimulusPosition.Center

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
    def channel(self) -> array:
        return self._channel
