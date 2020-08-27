from datetime import date
from typing import Union

from PyQt5.QtCore import pyqtSignal, QDate
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit, QComboBox, QDateEdit

from saccrec.core import Subject, Gender, SubjectStatus
from saccrec.i18n import _


INITIAL_DATE = QDate(2000, 1, 1)


class SubjectWidget(QWidget):
    fullnameChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SubjectWidget, self).__init__(parent=parent)

        layout = QFormLayout(self)

        self._full_name_edit = QLineEdit()
        self._full_name_edit.textChanged.connect(self.on_full_name_changed)
        layout.addRow(_('Nombre(s)'), self._full_name_edit)

        self._gender_combo = QComboBox()
        for gender in Gender:
            self._gender_combo.addItem(gender.label, gender.value)
        layout.addRow(_('Género'), self._gender_combo)

        self._borndate_edit = QDateEdit()
        self._borndate_edit.setCalendarPopup(True)
        layout.addRow(_('Fecha de nacimiento'), self._borndate_edit)

        self._status_combo = QComboBox()
        for status in SubjectStatus:
            self._status_combo.addItem(status.label, status.value)
        layout.addRow(_('Estado'), self._status_combo)

        self.setLayout(layout)

    def reset(self):
        self._full_name_edit.setText('')
        self._gender_combo.setCurrentIndex(0)
        self._borndate_edit.setDate(INITIAL_DATE)
        self._status_combo.setCurrentIndex(0)

    @property
    def full_name(self) -> str:
        return self._full_name_edit.text()

    @full_name.setter
    def full_name(self, value: str):
        initial_value = self._full_name_edit.text()
        if value != initial_value:
            self._full_name_edit.setText(value)
            self.fullnameChanged.emit(value)

    @property
    def gender(self) -> Gender:
        return Gender(self._gender_combo.currentData())

    @gender.setter
    def gender(self, value: Union[int, Gender]):
        if isinstance(value, int):
            self._gender_combo.setCurrentText(Gender(value).label)
        elif isinstance(value, SubjectStatus):
            self._gender_combo.setCurrentText(value.label)

    @property
    def borndate(self) -> date:
        return self._borndate_edit.date().toPyDate()

    @borndate.setter
    def borndate(self, value: date):
        qdate = QDate(value.year, value.month, value.day)
        self._borndate_edit.setDate(qdate)

    @property
    def status(self) -> SubjectStatus:
        return SubjectStatus(self._status_combo.currentData())

    @status.setter
    def status(self, value: Union[int, SubjectStatus]):
        if isinstance(value, int):
            self._status_combo.setCurrentText(SubjectStatus(value).label)
        elif isinstance(value, SubjectStatus):
            self._status_combo.setCurrentText(value.label)

    @property
    def json(self) -> dict:
        return {
            'full_name': self.full_name,
            'gender': self.gender,
            'borndate': self.borndate,
            'status': self.status,
        }

    @property
    def subject(self) -> Subject:
        return Subject(
            full_name=self.full_name,
            gender=self.gender,
            borndate=self.borndate,
            status=self.status
        )

    def on_full_name_changed(self):
        value = self._full_name_edit.text()
        self.fullnameChanged.emit(value)
