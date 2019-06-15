from datetime import date

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDialog

from .PersonDialogUI import Ui_PersonDialog


class PersonDialog(Ui_PersonDialog, QDialog):
    
    def __init__(self, settings, *args, **kwargs):
        super(PersonDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.saveButton.clicked.connect(self.onSaveButtonClicked)
        self.acceptButton.clicked.connect(self.onAcceptButtonClicked)

        self._settings = settings

    def open(self):
        self.nameEdit.setText(self._settings.initialName)
        self.lastNameEdit.setText('')
        self.borndate = date(1986, 9, 30)
        super(PersonDialog, self).open()

    @property
    def full_name(self) -> str:
        name = self.nameEdit.text()
        lastname = self.lastNameEdit.text()
        return f'{name} {lastname}'

    @property
    def borndate(self) -> date:
        return self.borndateDate.date().toPyDate()

    @borndate.setter
    def borndate(self, value: date):
        value = QDate(value.year, value.month, value.day)
        self.borndateDate.setDate(value)

    def onSaveButtonClicked(self, e):    
        print(self.borndate)

    def onAcceptButtonClicked(self, e):
        self.accept()