import pdb

import PySide6


def debug():
    PySide6.QtCore.pyqtRemoveInputHook()
    pdb.set_trace()
