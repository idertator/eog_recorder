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


class Genre(IntEnum):
    Male = 0
    Female = 1


class SubjectStatus(IntEnum):
    Unknown = 0
    Control = 1
    Presymptomatic = 2
    SCA2 = 3
