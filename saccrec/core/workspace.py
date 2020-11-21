from typing import Optional

from PyQt5 import QtCore, QtWidgets

from saccrec.core.study import Subject, Protocol


class Workspace(QtCore.QObject):

    def __init__(self, main_window: QtWidgets.QMainWindow):
        super(Workspace, self).__init__(parent=main_window)

        self._main_window = main_window

        self._subject = Subject()
        self._protocol = Protocol()
        self._filepath = None

    @property
    def subject(self) -> Subject:
        return self._subject

    @property
    def protocol(self) -> Protocol:
        return self._protocol

    @property
    def filepath(self) -> Optional[str]:
        return self._filepath

    @filepath.setter
    def filepath(self, value: str):
        self._filepath = value

    @property
    def html_overview(self) -> str:
        from saccrec.core.templating import render
        return render(
            'overview',
            subject=self._subject,
            protocol=self._protocol
        )
