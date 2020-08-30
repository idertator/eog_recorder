from enum import Enum

DEBUG = True

DATE_FORMAT = '%d/%m/%Y'
DATETIME_FORMAT = '%d/%m/%Y %H:%M'


class Language(Enum):
    English = 'en'
    Spanish = 'es'

    @property
    def label(self) -> str:
        return {
            Language.English: _('Inglés'),
            Language.Spanish: _('Español'),
        }[self]


DEFAULT_TEST = {
    'angle': 30,
    'fixation_duration': 3.0,
    'fixation_variability': 50.0,
    'saccades_count': 10,
}

TESTS = {
    'initial_calibration': DEFAULT_TEST,
    'tests': [DEFAULT_TEST],
    'final_calibration': DEFAULT_TEST,
}
