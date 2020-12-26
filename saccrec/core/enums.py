from enum import IntEnum, Enum


class Language(Enum):
    English = 'en'
    Spanish = 'es'

    @property
    def label(self) -> str:
        return {
            Language.English: _('English'),
            Language.Spanish: _('Spanish'),
        }[self]
