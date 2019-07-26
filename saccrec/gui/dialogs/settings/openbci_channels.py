from PyQt5.QtWidgets import QWidget, QFormLayout, QCheckBox, QSpinBox, QVBoxLayout, QHBoxLayout, QLabel

from saccrec.consts import SETTINGS_OPENBCI_DEFAULT_CHANNEL_NUMBER
from saccrec.core import Settings


class OpenBCIChannelWidget(QWidget):
    def __init__(self, channel_number: int, settings: Settings, parent=None):
        super(OpenBCIChannelWidget, self).__init__(parent)
        self._channel_number = channel_number
        self._settings = settings
        self.setFixedHeight(100)
        self.setFixedWidth(120)

        layout = QFormLayout()
        gain_layout = QHBoxLayout()

        self._openbci_channel_activated_check = QCheckBox()
        self._openbci_channel_activated_check.stateChanged.connect(self.on_activated_change)
        layout.addRow(f'Canal {self._channel_number + 1}    ', self._openbci_channel_activated_check)

        self._gain_label = QLabel('Ganancia')
        gain_layout.addWidget(self._gain_label)

        self._openbci_channel_gain_edit = QSpinBox()
        self._openbci_channel_gain_edit.setFixedWidth(40)
        gain_layout.addWidget(self._openbci_channel_gain_edit)

        layout.addRow(gain_layout)
        self.setLayout(layout)

    def on_activated_change(self):
        self._openbci_channel_gain_edit.setVisible(self._openbci_channel_activated_check.checkState())
        self._gain_label.setVisible(self._openbci_channel_activated_check.checkState())

    def load_settings(self):
        self._openbci_channel_activated_check.setChecked(bool(int(self._settings.openbci_channels[self._channel_number][0])))
        self._gain_label.setVisible(self._openbci_channel_activated_check.isChecked())
        self._openbci_channel_gain_edit.setVisible(self._openbci_channel_activated_check.isChecked())
        self._openbci_channel_gain_edit.setValue(int(self._settings.openbci_channels[self._channel_number][1]))

    def save(self):
        self._settings.openbci_channels[self._channel_number] = self._openbci_channel_activated_check.isChecked()
        self._settings.openbci_channels[self._channel_number] = self._openbci_channel_gain_edit.value()


class OpenBCIChannelsSettingsPage(QWidget):
    def __init__(self, settings: Settings, parent=None):
        super(OpenBCIChannelsSettingsPage, self).__init__(parent)
        self.channel_list = list()
        self._settings = settings

        layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()
        for i in range(SETTINGS_OPENBCI_DEFAULT_CHANNEL_NUMBER):
            channel = OpenBCIChannelWidget(i, self._settings)
            self.channel_list.append(channel)
            if i < (SETTINGS_OPENBCI_DEFAULT_CHANNEL_NUMBER / 2):
                top_layout.addWidget(channel)
            else:
                bottom_layout.addWidget(channel)

        layout.addLayout(top_layout)
        layout.addLayout(bottom_layout)
        self.setLayout(layout)

    def load_settings(self):
        for channel in self.channel_list:
            channel.load_settings()

    def save(self):
        for channel in self.channel_list:
            channel.save()

    @property
    def title(self) -> str:
        return 'Configuracion de los canales del OpenBCI'
