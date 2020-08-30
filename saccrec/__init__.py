import pdb

import PyQt5


def debug():
    PyQt5.QtCore.pyqtRemoveInputHook()
    pdb.set_trace()
