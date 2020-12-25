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


class Language(Enum):
    English = 'en'
    Spanish = 'es'

    @property
    def label(self) -> str:
        return {
            Language.English: _('English'),
            Language.Spanish: _('Spanish'),
        }[self]
