from PyQt5 import QtWidgets

from saccrec.core import Gender, workspace


class SubjectWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent):
        super(SubjectWizardPage, self).__init__(parent)

        self.setTitle(_('Datos del sujeto'))

        layout = QtWidgets.QVBoxLayout()

        self._subject = workspace.subject
        self._subject.setParent(self)
        self._subject.nameChanged.connect(self.on_name_changed)
        layout.addWidget(self._subject)

        self.setLayout(layout)

    def isComplete(self) -> bool:
        return self._subject.name.strip() != ''

    def on_name_changed(self, value: str):
        self.completeChanged.emit()

    @property
    def html(self) -> str:
        gender = {
            Gender.Unknown: _('persona nacida el'),
            Gender.Male: _('hombre nacido el'),
            Gender.Female: _('mujer nacida el'),
        }[self._subject.gender]
        borndate = self._subject.borndate.strftime('%d/%m/%Y')
        status = self._subject.status.label

        return '''<h4>{title}</h4>
            <p>{name}, {gender} {borndate} ({status})</p>
        '''.format(
            title=_('Sujeto'),
            name=self._subject.name,
            gender=gender,
            borndate=borndate,
            status=status
        )
