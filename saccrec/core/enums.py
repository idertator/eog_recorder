from enum import IntEnum, Enum


class Channel(Enum):
    Unknown = 'Unknown'
    Stimulus = 'Stimulus'
    Horizontal = 'Horizontal'
    Vertical = 'Vertical'
    Annotations = 'Annotations'


class StimulusPosition(IntEnum):
    Left = -1
    Center = 0
    Right = 1


class Genre(Enum):
    Unknown = 'Unknown'
    Male = 'Male'
    Female = 'Female'


class SubjectStatus(Enum):
    Unknown = 'Unknown'
    Control = 'Control'
    Presymptomatic = 'Presymptomatic'
    SCA2 = 'SCA2'


class BoardTypes(Enum):
    Cyton = 'cyton'
    Ganglion = 'ganglion'
    Daisy = 'daisy'


class BoardModes(Enum):
    Default = 'default'
    Debug = 'debug'
    Analog = 'analog'
    Digital = 'digital'
    Marker = 'marker'


class SampleRates(IntEnum):
    SR250 = 250
    SR500 = 500
    SR1000 = 1000
    SR2000 = 2000
    SR4000 = 4000
    SR8000 = 8000
    SR16000 = 16000
