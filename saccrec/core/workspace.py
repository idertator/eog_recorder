from PyQt5 import QtCore, QtWidgets

from saccrec.core.study import Subject, Protocol


class Workspace(QtCore.QObject):

    def __init__(self, main_window: QtWidgets.QMainWindow):
        super(Workspace, self).__init__(parent=main_window)

        self._main_window = main_window

        self._subject = Subject()
        self._protocol = Protocol()

    @property
    def subject(self) -> Subject:
        return self._subject

    @property
    def protocol(self) -> Protocol:
        return self._protocol
