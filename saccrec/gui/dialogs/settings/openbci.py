from PyQt5.QtWidgets import QWidget, QFormLayout, QComboBox

from saccrec.consts import OPENBCI_SAMPLE_RATES
from saccrec.core import Settings
from saccrec.engine.recording import list_ports


class OpenBCISettingsPage(QWidget):
    def __init__(self, settings: Settings, parent=None):
        super(OpenBCISettingsPage, self).__init__(parent)
        self._settings = settings

        layout = QFormLayout()

        self._openbci_ports_combo = QComboBox()
        self._openbci_ports_combo.setDuplicatesEnabled(False)
        for port in list_ports():
            self._openbci_ports_combo.addItem(port, port)
        layout.addRow(_('Puerto'), self._openbci_ports_combo)

        self._openbci_sample_rate_combo = QComboBox()
        self._openbci_sample_rate_combo.setDuplicatesEnabled(False)
        for key, value in OPENBCI_SAMPLE_RATES:
            self._openbci_sample_rate_combo.addItem(value, key)
        layout.addRow(_('Frecuencia de muestreo'), self._openbci_sample_rate_combo)

        self.load_settings()
        self.setLayout(layout)

    def load_settings(self):
        # openbci_ports_combo
        if self._openbci_ports_combo.count() > 0 and self._settings.openbci_port != '':
            self._openbci_ports_combo.setCurrentIndex(self._openbci_ports_combo.findText(self._settings.openbci_port))
        else:
            self._openbci_ports_combo.setCurrentIndex(0)

        # openbci_sample_rate_combo
        if self._openbci_sample_rate_combo.count() > 0 and self._settings.openbci_sample_rate != '':
            self._openbci_sample_rate_combo.setCurrentIndex(
                self._openbci_sample_rate_combo.findText(str(self._settings.openbci_sample_rate)))
        else:
            self._openbci_sample_rate_combo.setCurrentIndex(0)

    def save(self):
        self._settings.openbci_port = self._openbci_ports_combo.currentData()
        self._settings.openbci_sample_rate = self._openbci_sample_rate_combo.currentData()

    @property
    def title(self) -> str:
        return _('Configuración del OpenBCI')
