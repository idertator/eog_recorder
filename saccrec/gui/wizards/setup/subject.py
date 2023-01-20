from PySide6 import QtWidgets

from eoglib.models import Subject

from saccrec.gui.widgets import SubjectWidget


class SubjectWizardPage(QtWidgets.QWizardPage):

    def __init__(self, subject: Subject, parent=None):
        super(SubjectWizardPage, self).__init__(parent=parent)
        self._subject = subject

        self.setTitle(_('Subject info'))

        self._subject_widget = SubjectWidget(
            subject=subject,
            parent=self
        )
        self._subject_widget.nameChanged.connect(self._on_name_changed)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self._subject_widget)

    def isComplete(self) -> bool:
        return self._subject.name.strip() != ''

    def _on_name_changed(self, value: str):
        self.completeChanged.emit()
