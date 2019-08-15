from .manager import Manager


def debug():
    import pdb, PyQt5
    PyQt5.QtCore.pyqtRemoveInputHook()
    pdb.set_trace()
