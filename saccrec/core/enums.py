from enum import IntEnum


class Channel(IntEnum):
    Unknown = 0
    Stimulus = 1
    Horizontal = 2
    Vertical = 4
    Annotations = 8
