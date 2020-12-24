from enum import IntEnum, Enum


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
