from PyQt5.QtWidgets import QWidget, QFormLayout, QComboBox, QSpinBox

from saccrec.consts import OPENBCI_BOARD_TYPES, OPENBCI_SAMPLE_RATES, OPENBCI_BOARD_MODES, \
    SETTINGS_OPENBCI_DEFAULT_BAUDRATE_MAXIMUM, SETTINGS_OPENBCI_DEFAULT_BAUDRATE_MINIMUM, \
    SETTINGS_OPENBCI_DEFAULT_TIMEOUT_MINIMUM, SETTINGS_OPENBCI_DEFAULT_TIMEOUT_MAXIMUM
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
        layout.addRow('Puerto', self._openbci_ports_combo)

        self._openbci_board_type_combo = QComboBox()
        self._openbci_board_type_combo.setDuplicatesEnabled(False)
        for key, value in OPENBCI_BOARD_TYPES:
            self._openbci_board_type_combo.addItem(value, key)
        layout.addRow('Tipo de placa', self._openbci_board_type_combo)

        self._openbci_sample_rate_combo = QComboBox()
        self._openbci_sample_rate_combo.setDuplicatesEnabled(False)
        for key, value in OPENBCI_SAMPLE_RATES:
            self._openbci_sample_rate_combo.addItem(value, key)
        layout.addRow('Frecuencia de muestreo', self._openbci_sample_rate_combo)

        self._openbci_board_mode_combo = QComboBox()
        self._openbci_board_mode_combo.setDuplicatesEnabled(False)
        for key, value in OPENBCI_BOARD_MODES:
            self._openbci_board_mode_combo.addItem(value, key)
        layout.addRow('Modo de placa', self._openbci_board_mode_combo)

        self._openbci_baudrate_edit = QSpinBox()
        self._openbci_baudrate_edit.setMaximum(SETTINGS_OPENBCI_DEFAULT_BAUDRATE_MAXIMUM)
        self._openbci_baudrate_edit.setMinimum(SETTINGS_OPENBCI_DEFAULT_BAUDRATE_MINIMUM)
        layout.addRow('Baudrate', self._openbci_baudrate_edit)

        self._openbci_timeout_edit = QSpinBox()
        self._openbci_timeout_edit.setSuffix(' ms')
        self._openbci_timeout_edit.setMinimum(SETTINGS_OPENBCI_DEFAULT_TIMEOUT_MINIMUM)
        self._openbci_timeout_edit.setMaximum(SETTINGS_OPENBCI_DEFAULT_TIMEOUT_MAXIMUM)
        layout.addRow('Timeout', self._openbci_timeout_edit)


        self.load_settings()
        self.setLayout(layout)

    def load_settings(self):
        # openbci_ports_combo
        if self._openbci_ports_combo.count() > 0 and self._settings.openbci_port != '':
            self._openbci_ports_combo.setCurrentIndex(self._openbci_ports_combo.findText(self._settings.openbci_port))
        else:
            self._openbci_ports_combo.setCurrentIndex(0)

        # openbci_board_type_combo
        if self._openbci_board_type_combo.count() > 0 and self._settings.openbci_board_type != '':
            self._openbci_board_type_combo.setCurrentIndex(
                self._openbci_board_type_combo.findText(self._settings.openbci_board_type))
        else:
            self._openbci_board_type_combo.setCurrentIndex(0)

        # openbci_sample_rate_combo
        if self._openbci_sample_rate_combo.count() > 0 and self._settings.openbci_sample_rate != '':
            self._openbci_sample_rate_combo.setCurrentIndex(
                self._openbci_sample_rate_combo.findText(str(self._settings.openbci_sample_rate)))
        else:
            self._openbci_sample_rate_combo.setCurrentIndex(0)

        # openbci_board_mode
        if self._openbci_board_mode_combo.count() > 0 and self._settings.openbci_board_mode != '':
            self._openbci_board_mode_combo.setCurrentIndex(
                self._openbci_board_mode_combo.findText(self._settings.openbci_board_mode))
        else:
            self._openbci_board_mode_combo.setCurrentIndex(0)

        # openbci_baudrate_edit
        self._openbci_baudrate_edit.setValue(int(self._settings.openbci_baudrate))

        # openbci_timeout_edit
        self._openbci_timeout_edit.setValue(int(self._settings.openbci_timeout))

    def save(self):
        self._settings.openbci_port = self._openbci_ports_combo.currentData()
        self._settings.openbci_board_type = self._openbci_board_type_combo.currentData()
        self._settings.openbci_sample_rate = self._openbci_sample_rate_combo.currentData()
        self._settings.openbci_board_mode = self._openbci_board_mode_combo.currentData()
        self._settings.openbci_baudrate = self._openbci_baudrate_edit.value()
        self._settings.openbci_timeout = self._openbci_timeout_edit.value()


    @property
    def title(self) -> str:
        return 'Configuracion del OpenBCI'