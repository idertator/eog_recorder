from PyQt5 import QtWidgets

from saccrec.core import Subject, Gender
from saccrec.gui.subject import SubjectWidget


class SubjectWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent):
        super(SubjectWizardPage, self).__init__(parent)

        self.setTitle(_('Datos del sujeto'))

        layout = QtWidgets.QVBoxLayout()
        self._subject_widget = SubjectWidget(self)
        self._subject_widget.fullnameChanged.connect(self.on_fullname_changed)
        layout.addWidget(self._subject_widget)

        self.setLayout(layout)

    def isComplete(self) -> bool:
        return self._subject_widget.full_name.strip() != ''

    def on_fullname_changed(self, value: str):
        self.completeChanged.emit()

    @property
    def html(self) -> str:
        gender = {
            Gender.Unknown: _('persona nacida el'),
            Gender.Male: _('hombre nacido el'),
            Gender.Female: _('mujer nacida el'),
        }[self._subject_widget.gender]
        borndate = self._subject_widget.borndate.strftime('%d/%m/%Y')
        status = self._subject_widget.status.label

        return '''<h4>{title}</h4>
            <p>{fullname}, {gender} {borndate} ({status})</p>
        '''.format(
            title=_('Sujeto'),
            fullname=self._subject_widget.full_name,
            gender=gender,
            borndate=borndate,
            status=status
        )

    @property
    def json(self) -> dict:
        return self._subject_widget.json

    @property
    def subject(self) -> Subject:
        return self._subject_widget.model

    @property
    def subject_code(self) -> str:
        def int_to_str(data: int) -> str:
            if int(data) < 10:
                return '0' + str(data)
            if len(str(data)) > 2:
                return str(data)[2:4]
            return str(data)

        full_name = self._subject_widget.full_name.upper().strip().split(' ')
        while len(full_name) > 3:
            full_name.remove(full_name[1])
        code = ''
        if len(full_name) == 1:
            code = full_name[0][0:3]
        else:
            for text in full_name:
                code += text[0]

        day = int_to_str(self._subject_widget.borndate.day)
        month = int_to_str(self._subject_widget.borndate.month)
        year = int_to_str(self._subject_widget.borndate.year)
        return code + day + month + year
