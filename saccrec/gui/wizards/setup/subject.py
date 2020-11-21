from PyQt5 import QtWidgets

from saccrec.core import Gender, workspace


class SubjectWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent):
        super(SubjectWizardPage, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setTitle(_('Datos del sujeto'))

        self._subject = workspace.subject
        self._subject.setParent(self)
        self._subject.nameChanged.connect(self.on_name_changed)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._subject)

        self.setLayout(layout)

    def isComplete(self) -> bool:
        return self._subject.name.strip() != ''

    def on_name_changed(self, value: str):
        self.completeChanged.emit()
