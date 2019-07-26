from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QWidget, QFormLayout, QCheckBox, QSpinBox, QVBoxLayout, QHBoxLayout

from saccrec.consts import SETTINGS_OPENBCI_DEFAULT_GAIN, SETTINGS_OPENBCI_DEFAULT_CHANNEL_NUMBER
from saccrec.core import Settings

class OpenBCIChannelWidget(QWidget):
    def __init__(self, channel_number: int, parent=None):
        super(OpenBCIChannelWidget, self).__init__(parent)
        self._channel_number = channel_number
        self._settings = QSettings('SaccRec', 'SaccRec', None)

        layout = QFormLayout()

        self._openbci_channel_activated_check = QCheckBox()
        self._openbci_channel_activated_check.setChecked(True)
        self._openbci_channel_activated_check.stateChanged.connect(self.on_activated_change)
        layout.addRow(f'Canal {self._channel_number + 1}', self._openbci_channel_activated_check)

        self._openbci_channel_gain_edit = QSpinBox()
        self._openbci_channel_gain_edit.setFixedWidth(40)
        layout.addRow('Ganancia', self._openbci_channel_gain_edit)

        self.setLayout(layout)

    def on_activated_change(self):
        self._openbci_channel_gain_edit.setEnabled(self._openbci_channel_activated_check.checkState())

    def load_settings(self):
        self._openbci_channel_activated_check.setChecked(
            int(self._settings.value(f'OpenBCIChannelActivated{self._channel_number}', 2)))
        self._openbci_channel_gain_edit.setValue(int(
            self._settings.value(f'OpenBCIChannelGain{self._channel_number}', SETTINGS_OPENBCI_DEFAULT_GAIN)))

    def save(self):
        self._settings.setValue(f'OpenBCIChannelActivated{self._channel_number}',
                                         self._openbci_channel_activated_check.checkState())
        self._settings.setValue(f'OpenBCIChannelGain{self._channel_number}',
                                         self._openbci_channel_gain_edit.value())


class OpenBCIChannelsSettingsPage(QWidget):
    def __init__(self, settings: Settings,parent=None):
        super(OpenBCIChannelsSettingsPage, self).__init__(parent)
        self.channel_list = list()

    def load_settings(self):
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        for i in range(SETTINGS_OPENBCI_DEFAULT_CHANNEL_NUMBER):
            channel = OpenBCIChannelWidget(i)
            channel.load_settings()
            self.channel_list.append(channel)
            if i < (SETTINGS_OPENBCI_DEFAULT_CHANNEL_NUMBER / 2):
                layout1.addWidget(channel)
            else:
                layout2.addWidget(channel)

        layout.addLayout(layout1)
        layout.addLayout(layout2)
        self.setLayout(layout)

    def save(self):
        for channel in self.channel_list:
            channel.save()

    @property
    def title(self) -> str:
        return 'Configuracion de los canales del OpenBCI'