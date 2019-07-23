from math import floor
from random import randint

from numpy import array, int8, zeros, ones, hstack

from saccrec.core import StimulusPosition


class SaccadicStimuli(object):
    
    def __init__(self, 
        sampling_rate: int,
        angle: int,
        fixation_duration: float,   
        fixation_variability: float,
        saccades_count: int
    ):
        """Constructor
    
        Args:
            sampling_rate (int): Sampling rate in Hz
            fixation_duration (float): Mean fixation duration in seconds
            fixation_variability (float): Variability of the fixation duration in percentage
            saccades_count (int): Amounts of saccades to generate
        """
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

    @property
    def channel(self) -> array:
        return self._channel

    def position(self, sample: int) -> StimulusPosition:
        if self._channel[sample] < 0:
            return StimulusPosition.Left
        if self._channel[sample] > 0:
            return StimulusPosition.Right
        return StimulusPosition.Center
