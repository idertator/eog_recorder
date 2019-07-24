from math import floor
from random import randint

from numpy import array, int8, zeros, ones, hstack

from saccrec.core import Settings, StimulusPosition


class SaccadicStimuli(object):
    
    def __init__(self,
        settings: Settings,
        angle: int,
        fixation_duration: float,   
        fixation_variability: float,
        saccades_count: int,
        test_name: str = 'Saccadic'
    ):
        """Constructor
    
        Args:
            settings (saccrec.core.Settings): Settings object
            angle (int): Stimuli angle
            fixation_duration (float): Mean fixation duration in seconds
            fixation_variability (float): Variability of the fixation duration in percentage
            saccades_count (int): Amounts of saccades to generate
            test_name (str): Name of the stimulation pattern
        """
        self._angle = angle
        self._settings = settings
        self._test_name = test_name

        sampling_rate = settings.sampling_frequency

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

    def __str__(self):
        return f'{self._test_name} {self._angle}\u00B0'

    @property
    def channel(self) -> array:
        return self._channel

    def position(self, sample: int) -> StimulusPosition:
        if self._channel[sample] < 0:
            return StimulusPosition.Left
        if self._channel[sample] > 0:
            return StimulusPosition.Right
        return StimulusPosition.Center

    def screen_position(self, sample: int) -> int:
        pass

    @property
    def angle(self) -> int:
        return self._angle
