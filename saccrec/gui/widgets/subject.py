from datetime import date

from PySide6 import QtCore, QtWidgets

from eoglib.models import Subject, Gender, Status


class SubjectWidget(QtWidgets.QWidget):
    nameChanged = QtCore.Signal(str)

    def __init__(self, subject: Subject, parent=None):
        super(SubjectWidget, self).__init__(parent=parent)

        self._subject = subject

        self._name_edit = QtWidgets.QLineEdit()
        self._name_edit.setText(self._subject.name)
        self._name_edit.textChanged.connect(self._on_name_changed)

        self._gender_combo = QtWidgets.QComboBox()
        for gender in Gender:
            match gender.label:
                case 'Desconocido':
                    self._gender_combo.addItem(_('Unknown'), gender.value)
                case 'Masculino':
                    self._gender_combo.addItem(_('Male'), gender.value)
                case 'Femenino':
                    self._gender_combo.addItem(_('Female'), gender.value)
                case _:
                    self._gender_combo.addItem(gender.label, gender.value)
        self._gender_combo.setCurrentIndex(self._subject.gender.index)
        self._gender_combo.currentIndexChanged.connect(self._on_gender_changed)

        bd = self._subject.borndate

        self._borndate_edit = QtWidgets.QDateEdit()
        self._borndate_edit.setDate(QtCore.QDate(bd.year, bd.month, bd.day))
        self._borndate_edit.setCalendarPopup(True)
        self._borndate_edit.setDisplayFormat('dd/MM/yyyy')
        self._borndate_edit.dateChanged.connect(self._on_borndate_changed)

        self._status_combo = QtWidgets.QComboBox()
        for status in Status:
            match status.label:
                case 'Desconocido':
                    self._status_combo.addItem(_('Unknown'), status.value)
                case 'Control':
                    self._status_combo.addItem(_('Control'), status.value)
                case 'Presintomático':
                    self._status_combo.addItem(_('Presymptomatic'), status.value)
                case 'Enfermo':
                    self._status_combo.addItem(_('Sick'), status.value)
                case _:
                    self._status_combo.addItem(status.label, status.value)
        self._status_combo.setCurrentIndex(self._subject.status.index)
        self._status_combo.currentIndexChanged.connect(self._on_status_changed)

        layout = QtWidgets.QFormLayout(self)
        layout.addRow(_('Name'), self._name_edit)
        layout.addRow(_('Gender'), self._gender_combo)
        layout.addRow(_('Born date'), self._borndate_edit)
        layout.addRow(_('Status'), self._status_combo)
        self.layout = layout

    def _on_name_changed(self, value: str):
        self._subject.name = value
        self.nameChanged.emit(value)

    def _on_gender_changed(self, index):
        self._subject.gender = Gender(self._gender_combo.currentData())

    def _on_borndate_changed(self, value):
        self._subject.borndate = date(value.year(), value.month(), value.day())

    def _on_status_changed(self, index):
        self._subject.status = Status(self._status_combo.currentData())

    def reset(self):
        self._name_edit.setText('')
        self._borndate_edit.setDate(QtCore.QDate(2000, 1, 1))
        self._gender_combo.setCurrentIndex(0)
        self._status_combo.setCurrentIndex(0)

    @property
    def subject(self) -> Subject:
        return self._subject
