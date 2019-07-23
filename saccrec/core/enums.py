from enum import IntEnum


class Channel(IntEnum):
    Unknown = 0
    Stimulus = 1
    Horizontal = 2
    Vertical = 4
    Annotations = 8


class StimulusPosition(IntEnum):
    Left = -1
    Center = 0
    Right = 1
