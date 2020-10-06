from enum import IntEnum, Enum


class Gender(IntEnum):
    Unknown = 0
    Male = 1
    Female = 2

    @property
    def label(self) -> str:
        return {
            Gender.Unknown: _('Desconocido'),
            Gender.Male: _('Masculino'),
            Gender.Female: _('Femenino'),
        }[self]


class SubjectStatus(IntEnum):
    Unknown = 0
    Control = 1
    Presymptomatic = 2
    SCA2 = 3

    @property
    def label(self) -> str:
        return {
            SubjectStatus.Unknown: _('Desconocido'),
            SubjectStatus.Control: _('Control'),
            SubjectStatus.Presymptomatic: _('Presintomático'),
            SubjectStatus.SCA2: _('SCA2'),
        }[self]


class Channel(Enum):
    Unknown = 'Unknown'
    Timestamps = 'Timestamps'
    Time = 'Time'
    Stimulus = 'Stimulus'
    Horizontal = 'Horizontal'
    Vertical = 'Vertical'
    Annotations = 'Annotations'


class StimulusPosition(IntEnum):
    Left = -1
    Center = 0
    Right = 1


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
