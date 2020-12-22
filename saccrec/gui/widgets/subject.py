from PySide6 import QtCore, QtWidgets

from eoglib.models import Subject, Gender, Status


class SubjectWidget(QtWidgets.QWidget):
    nameChanged = QtCore.Signal(str)

    def __init__(self, subject: Subject = Subject(), parent=None):
        super(SubjectWidget, self).__init__(parent=parent)

        self._subject = subject

        self._name_edit = QtWidgets.QLineEdit()
        self._name_edit.text = self._subject.name
        self._name_edit.textChanged.connect(self._on_name_changed)

        self._gender_combo = QtWidgets.QComboBox()
        for gender in Gender:
            self._gender_combo.addItem(gender.label, gender.value)
        self._gender_combo.current_data = self._subject.gender
        self._gender_combo.currentIndexChanged.connect(self._on_gender_changed)

        bd = self._subject.borndate

        self._borndate_edit = QtWidgets.QDateEdit()
        self._borndate_edit.date = QtCore.QDate(bd.year, bd.month, bd.day)
        self._borndate_edit.calendar_popup = True
        self._borndate_edit.display_format = 'dd/MM/yyyy'
        self._borndate_edit.dateChanged.connect(self._on_borndate_changed)

        self._status_combo = QtWidgets.QComboBox()
        for status in Status:
            self._status_combo.addItem(status.label, status.value)
        self._status_combo.current_data = self._subject.status
        self._status_combo.currentIndexChanged.connect(self._on_status_changed)

        layout = QtWidgets.QFormLayout(self)
        layout.addRow(_('Nombre(s)'), self._name_edit)
        layout.addRow(_('Género'), self._gender_combo)
        layout.addRow(_('Fecha de nacimiento'), self._borndate_edit)
        layout.addRow(_('Estado'), self._status_combo)
        self.layout = layout

    def _on_name_changed(self):
        value = self._name_edit.text
        self._subject.name = value
        self.nameChanged.emit(value)

    def _on_gender_changed(self, index):
        self._subject.gender = Gender(self._gender_combo.current_data)

    def _on_borndate_changed(self, value):
        self._subject.borndate = value.toPython()

    def _on_status_changed(self, index):
        self._subject.status = Status(self._status_combo.current_data)

    def reset(self):
        self._name_edit.text = ''
        self._borndate_edit.date = QtCore.QDate(2000, 1, 1)
        self._gender_combo.current_index = 0
        self._status_combo.current_index = 0

    @property
    def subject(self) -> Subject:
        return self._subject
