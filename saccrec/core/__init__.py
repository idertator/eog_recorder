from PyQt5 import QtWidgets

from .enums import Gender, SubjectStatus
from .enums import Channel, StimulusPosition, BoardTypes, BoardModes, SampleRates
from .formats import Record

from .screen import Screen
from .study import Study, Test, SaccadicTest, Saccade

from .workspace import Workspace


workspace = None

def initialize_workspace(main_window: QtWidgets.QMainWindow) -> Workspace:
    global workspace
    workspace = Workspace(main_window)
    return workspace

__all__ = [
    'Gender',
    'SubjectStatus',
    'Channel',
    'StimulusPosition',
    'BoardTypes',
    'BoardModes',
    'SampleRates',
    'Record',
    'Screen',
    'Study',
    'Subject',
    'Test',
    'SaccadicTest',
    'Saccade',

    'workspace',
]
