from datetime import date

from PyQt5.QtCore import pyqtSignal, QDate
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit, QComboBox, QDateEdit

from saccrec.settings import GENRES, GENRES_DICT, SUBJECT_STATUSES, SUBJECT_STATUSES_DICT

INITIAL_DATE = QDate(2000, 1, 1)

class SubjectWidget(QWidget):
    fullnameChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SubjectWidget, self).__init__(parent=parent)

        layout = QFormLayout(self)

        self._full_name_edit = QLineEdit()
        self._full_name_edit.textChanged.connect(self.on_full_name_changed)
        layout.addRow('Nombre(s)', self._full_name_edit)

        self._genre_combo = QComboBox()
        for genre_value, genre_label in GENRES:
            self._genre_combo.addItem(genre_label, genre_value)
        layout.addRow('Género', self._genre_combo)

        self._borndate_edit = QDateEdit()
        self._borndate_edit.setCalendarPopup(True)
        layout.addRow('Fecha de nacimiento', self._borndate_edit)

        self._status_combo = QComboBox()
        for status_value, status_label in SUBJECT_STATUSES:
            self._status_combo.addItem(status_label, status_value)
        layout.addRow('Estado', self._status_combo)

        self.setLayout(layout)

    def reset(self):
        self._full_name_edit.setText('')
        self._genre_combo.setCurrentIndex(0)
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
    def genre(self) -> int:
        return self._genre_combo.currentData()

    @genre.setter
    def genre(self, value: int):
        self._genre_combo.setCurrentIndex(GENRES_DICT[value])

    @property
    def borndate(self) -> date:
        return self._borndate_edit.date().toPyDate()

    @borndate.setter
    def borndate(self, value: date):
        qdate = QDate(value.year, value.month, value.day)
        self._borndate_edit.setDate(qdate)

    @property
    def status(self) -> int:
        return self._status_combo.currentData()

    @status.setter
    def status(self, value: int):
        self._status_combo.setCurrentIndex(SUBJECT_STATUSES_DICT[value])

    def on_full_name_changed(self):
        value = self._full_name_edit.text()
        self.fullnameChanged.emit(value)
