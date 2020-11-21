from PyQt5 import QtWidgets

from saccrec import settings
from saccrec.core import workspace
from saccrec.core.study import Stimulus


class StimulusWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent):
        super(StimulusWizardPage, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setTitle(_('Configuración del estímulo'))

        self._protocol = workspace.protocol
        self._protocol.setParent(self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._protocol)

        self.setLayout(layout)

    @property
    def json(self) -> dict:
        return self._protocol.json
