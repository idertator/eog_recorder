from PySide6 import QtCore, QtWidgets

from eoglib.models import Protocol

from saccrec.gui.widgets import ProtocolWidget


class StimulusWizardPage(QtWidgets.QWizardPage):
    protocolLoaded = QtCore.Signal(Protocol)

    def __init__(self, protocol: Protocol, parent=None):
        super(StimulusWizardPage, self).__init__(parent=parent)
        self._protocol = protocol

        self.setTitle(_("Stimuli Setup"))

        self._protocol_widget = ProtocolWidget(protocol=self._protocol, parent=self)
        self._protocol_widget.protocolNameChanged.connect(
            self._on_protocol_name_changed
        )
        self._protocol_widget.protocolLoaded.connect(self._on_protocol_loaded)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self._protocol_widget)

    def isComplete(self) -> bool:
        return self._protocol.name.strip() != ""

    def _on_protocol_name_changed(self, value: str):
        self.completeChanged.emit()

    def _on_protocol_loaded(self, protocol: Protocol):
        self._protocol = protocol
        self.protocolLoaded.emit(protocol)
