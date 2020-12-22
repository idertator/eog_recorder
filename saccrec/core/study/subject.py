from datetime import date
from typing import Union, Optional

from PySide6 import QtCore, QtWidgets

from saccrec import settings
from saccrec.core import Gender, SubjectStatus


class Subject(QtWidgets.QWidget):
    nameChanged = QtCore.Signal(str)

    def __init__(
        self,
        name: str = '',
        gender: Union[int, Gender] = Gender.Unknown,
        status: Union[int, SubjectStatus] = SubjectStatus.Unknown,
        borndate: Optional[Union[str, date]] = None,
        parent=None
    ):
        super(Subject, self).__init__(parent=parent)

        self._setup_ui()

        self.name = name
        self.gender = gender
        self.status = status

    def _setup_ui(self):
        layout = QtWidgets.QFormLayout(self)

        self._name_edit = QtWidgets.QLineEdit()
        self._name_edit.textChanged.connect(self._on_name_changed)
        layout.addRow(_('Nombre(s)'), self._name_edit)

        self._gender_combo = QtWidgets.QComboBox()
        for gender in Gender:
            self._gender_combo.addItem(gender.label, gender.value)
        layout.addRow(_('Género'), self._gender_combo)

        self._borndate_edit = QtWidgets.QDateEdit()
        self._borndate_edit.setCalendarPopup(True)
        self._borndate_edit.setDisplayFormat('dd/MM/yyyy')
        layout.addRow(_('Fecha de nacimiento'), self._borndate_edit)

        self._status_combo = QtWidgets.QComboBox()
        for status in SubjectStatus:
            self._status_combo.addItem(status.label, status.value)
        layout.addRow(_('Estado'), self._status_combo)

        self.setLayout(layout)

    def reset(self):
        self._name_edit.setText('')
        self._gender_combo.setCurrentIndex(0)
        self._borndate_edit.setDate(QtCore.QDate(2000, 1, 1))
        self._status_combo.setCurrentIndex(0)

    @property
    def name(self) -> str:
        return self._name_edit.text()

    @name.setter
    def name(self, value: str):
        initial_value = self._name_edit.text()
        if value != initial_value:
            self._name_edit.setText(value)
            self.nameChanged.emit(value)

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
    def status(self) -> SubjectStatus:
        return SubjectStatus(self._status_combo.currentData())

    @status.setter
    def status(self, value: Union[int, SubjectStatus]):
        if isinstance(value, int):
            self._status_combo.setCurrentText(SubjectStatus(value).label)
        elif isinstance(value, SubjectStatus):
            self._status_combo.setCurrentText(value.label)

    @property
    def borndate(self) -> date:
        return self._borndate_edit.date().toPython()

    @borndate.setter
    def borndate(self, value: Union[str, date]):
        if isinstance(borndate, str):
            value = datetime.strptime(borndate, settings.DATE_FORMAT).date()

        if value is not None:
            qdate = QtCore.QDate(value.year, value.month, value.day)
        else:
            qdate = QtCore.QDate(2000, 1, 1)

        self._borndate_edit.setDate(qdate)

    @property
    def json(self) -> dict:
        return {
            'name': self.name,
            'gender': self.gender.value,
            'status': self.status.value,
            'borndate': self.borndate.strftime(settings.DATE_FORMAT),
        }

    @property
    def age(self) -> int:
        today = date.today()
        if self.borndate is not None:
            years = today.year - self.borndate.year
            if today.month > self.borndate.month:
                return years + 1
            if today.month < self.borndate.year:
                return years
            if today.day >= self.borndate.day:
                return years + 1
            return years
        return 0

    @property
    def code(self) -> str:
        def int_to_str(data: int) -> str:
            if int(data) < 10:
                return '0' + str(data)
            if len(str(data)) > 2:
                return str(data)[2:4]
            return str(data)

        name = self.name.upper().strip().split(' ')
        while len(name) > 3:
            name.remove(name[1])
        initials = ''
        if len(name) == 1:
            initials = name[0][0:3]
        else:
            for text in name:
                initials += text[0]

        borndate = self.borndate

        day = int_to_str(borndate.day)
        month = int_to_str(borndate.month)
        year = int_to_str(borndate.year)
        return initials + day + month + year

    def _on_name_changed(self):
        value = self._name_edit.text()
        self.nameChanged.emit(value)

