from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QListWidget, QListView, QStackedWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout, \
    QDialogButtonBox

from saccrec.core import Settings
from saccrec.gui.dialogs.settings.openbci_channels import OpenBCIChannelsSettingsPage
from saccrec.gui.dialogs.settings.openbci import OpenBCISettingsPage
from saccrec.gui.dialogs.settings.screen import ScreenSettingsPage
from saccrec.gui.dialogs.settings.stimulus import StimulusSettingsPage


class SettingsDialog(QDialog):
    def __init__(self, settings: Settings, parent=None):
        super(SettingsDialog, self).__init__(parent=parent)
        self._settings = settings

        self.contentsWidget = QListWidget()
        self.contentsWidget.setFlow(QListView.TopToBottom)
        self.contentsWidget.setViewMode(QListView.IconMode)
        self.contentsWidget.setMovement(QListView.Static)
        self.contentsWidget.setFixedWidth(150)
        self.contentsWidget.setFixedHeight(260)
        self.contentsWidget.setSpacing(5)
        self.contentsWidget.setIconSize(QSize(25, 25))

        self.pagesWidget = QStackedWidget()
        self.pagesWidget.addWidget(OpenBCISettingsPage(self._settings))
        self.pagesWidget.addWidget(OpenBCIChannelsSettingsPage(self._settings))
        self.pagesWidget.addWidget(ScreenSettingsPage(self._settings))
        self.pagesWidget.addWidget(StimulusSettingsPage(self._settings))
        self.contentsWidget.setCurrentRow(0)

        openbci_button = QListWidgetItem(QIcon(':openbci.png'), 'OpenBCI')
        self.contentsWidget.addItem(openbci_button)
        openbci_button.setTextAlignment(Qt.AlignHCenter)
        openbci_button.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        channel_button = QListWidgetItem(QIcon(':channels.svg'), 'Canales')
        self.contentsWidget.addItem(channel_button)
        channel_button.setTextAlignment(Qt.AlignHCenter)
        channel_button.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        screen_button = QListWidgetItem(QIcon(':screen.svg'), 'Pantalla de estimulo')
        self.contentsWidget.addItem(screen_button)
        screen_button.setTextAlignment(Qt.AlignHCenter)
        screen_button.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        stimulus_button = QListWidgetItem(QIcon(':stimuli.svg'), 'Estimulo')
        self.contentsWidget.addItem(stimulus_button)
        stimulus_button.setTextAlignment(Qt.AlignHCenter)
        stimulus_button.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        screen_button.setTextAlignment(Qt.AlignHCenter)
        openbci_button.setTextAlignment(Qt.AlignHCenter)
        channel_button.setTextAlignment(Qt.AlignHCenter)
        screen_button.setTextAlignment(Qt.AlignHCenter)
        stimulus_button.setTextAlignment(Qt.AlignHCenter)
        self.contentsWidget.currentItemChanged.connect(self.change_page)

        layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.contentsWidget)
        horizontal_layout.addWidget(self.pagesWidget, 1)

        dialog_buttons = QDialogButtonBox()
        dialog_buttons.addButton('Aplicar', QDialogButtonBox.AcceptRole)
        dialog_buttons.addButton('Cancelar', QDialogButtonBox.RejectRole)
        dialog_buttons.accepted.connect(self.on_accepted)
        dialog_buttons.rejected.connect(self.on_rejected)
        layout.addLayout(horizontal_layout)
        layout.addWidget(dialog_buttons)

        self.setLayout(layout)

    def change_page(self, current, previous):
        if not current:
            current = previous

        self.pagesWidget.setCurrentIndex(self.contentsWidget.row(current))
        self.setWindowTitle(self.pagesWidget.currentWidget().title)

    def on_accepted(self):
        for i in range(self.pagesWidget.count()):
            self.pagesWidget.widget(i).save()
        self.accept()

    def on_rejected(self):
        self.reject()

    def open(self):
        for i in range(self.pagesWidget.count()):
            self.pagesWidget.widget(i).load_settings()
        super(SettingsDialog, self).open()