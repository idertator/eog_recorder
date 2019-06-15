from PyQt5.QtWidgets import QMainWindow

from .MainWindowUI import Ui_MainWindow
from .PersonDialog import PersonDialog
from .Settings import Settings


class MainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self._personDialog = None
        self._settings = Settings(self)

        self.actionAbrir.triggered.connect(self.onPersonDialogOpenClicked)

        # self._name = ''
        # self._lastName = ''

    @property
    def personDialog(self):
        if self._personDialog is None:
            self._personDialog = PersonDialog(self._settings, parent=self)
            self._personDialog.accepted.connect(self.onPersonAccepted)
        return self._personDialog

    def onPersonDialogOpenClicked(self, e):
        self.personDialog.open()

    def onPersonAccepted(self):
        print(self.personDialog.full_name)