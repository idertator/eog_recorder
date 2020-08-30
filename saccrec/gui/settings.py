from enum import IntEnum

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QDialog, QListWidget, QListView, QStackedWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QDialogButtonBox, QColorDialog, QPushButton
from PyQt5.QtWidgets import QWidget, QFormLayout, QComboBox, QCheckBox, QSpinBox, QLabel, QDoubleSpinBox

from saccrec.core import Settings
from saccrec.engine.recording import list_ports


class _OpenBCISettingsPage(QWidget):

    SAMPLE_RATES = (250, 500, 1000, 2000, 4000, 8000, 16000)

    def __init__(self, settings: Settings, parent=None):
        super(_OpenBCISettingsPage, self).__init__(parent)
        self._settings = settings

        layout = QFormLayout()

        self._openbci_ports_combo = QComboBox()
        self._openbci_ports_combo.setDuplicatesEnabled(False)
        for port in list_ports():
            self._openbci_ports_combo.addItem(port, port)
        layout.addRow(_('Puerto'), self._openbci_ports_combo)

        self._openbci_sample_rate_combo = QComboBox()
        self._openbci_sample_rate_combo.setDuplicatesEnabled(False)
        for sr in self.SAMPLE_RATES:
            self._openbci_sample_rate_combo.addItem(str(sr), sr)
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


class _OpenBCIChannelWidget(QWidget):

    def __init__(self, channel_number: int, settings: Settings, parent=None):
        super(_OpenBCIChannelWidget, self).__init__(parent)
        self._channel_number = channel_number
        self._settings = settings
        self.setFixedHeight(100)
        self.setFixedWidth(120)

        layout = QFormLayout()
        gain_layout = QHBoxLayout()

        self._openbci_channel_activated_check = QCheckBox()
        self._openbci_channel_activated_check.stateChanged.connect(self.on_activated_change)
        layout.addRow(
            '{channel} {number}    '.format(
                channel=_('Canal'),
                number=self._channel_number + 1
            ),
            self._openbci_channel_activated_check
        )

        self._gain_label = QLabel(_('Ganancia'))
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
        self._openbci_channel_activated_check.setChecked(self._settings.openbci_channels[self._channel_number][0])
        self._gain_label.setVisible(self._openbci_channel_activated_check.isChecked())
        self._openbci_channel_gain_edit.setVisible(self._openbci_channel_activated_check.isChecked())
        self._openbci_channel_gain_edit.setValue(self._settings.openbci_channels[self._channel_number][1])

    def save(self):
        self._settings.openbci_channels[self._channel_number] = self._openbci_channel_activated_check.isChecked()
        self._settings.openbci_channels[self._channel_number] = self._openbci_channel_gain_edit.value()


class _OpenBCIChannelsSettingsPage(QWidget):

    def __init__(self, settings: Settings, parent=None):
        super(_OpenBCIChannelsSettingsPage, self).__init__(parent)
        self.channel_list = list()
        self._settings = settings

        layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()
        for i in range(8):
            channel = _OpenBCIChannelWidget(i, self._settings)
            self.channel_list.append(channel)
            if i < 4:
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
        return _('Configuración de los canales del OpenBCI')


class _ScreenSettingsPage(QWidget):

    def __init__(self, settings: Settings = Settings, parent=None):
        super(_ScreenSettingsPage, self).__init__(parent)
        self._settings = settings

        layout = QFormLayout()
        self.setWindowTitle(_('Pantalla de estímulo'))
        self._stimulus_screen_width_edit = QDoubleSpinBox()
        self._stimulus_screen_width_edit.setMinimum(10.0)
        self._stimulus_screen_width_edit.setMaximum(200.0)
        self._stimulus_screen_width_edit.setFixedWidth(85)
        self._stimulus_screen_width_edit.setSuffix(' cm')
        layout.addRow(_('Ancho'), self._stimulus_screen_width_edit)

        self._stimulus_screen_height_edit = QDoubleSpinBox()
        self._stimulus_screen_height_edit.setMinimum(10.0)
        self._stimulus_screen_height_edit.setMaximum(200.0)
        self._stimulus_screen_height_edit.setFixedWidth(85)
        self._stimulus_screen_height_edit.setSuffix(' cm')
        layout.addRow(_('Alto'), self._stimulus_screen_height_edit)

        self.setLayout(layout)

    def load_settings(self):
        self._stimulus_screen_width_edit.setValue(self._settings.stimulus_screen_width)
        self._stimulus_screen_height_edit.setValue(self._settings.stimulus_screen_height)

    def save(self):
        self._settings.stimulus_screen_width = self._stimulus_screen_width_edit.value()
        self._settings.stimulus_screen_height = self._stimulus_screen_height_edit.value()

    @property
    def title(self):
        return _('Configuración de pantalla')


class ColorButton(QPushButton):

    def __init__(self, color: QColor = None, *args, **kwargs):
        super(ColorButton, self).__init__(*args, **kwargs)

        self._color = color
        self.setFixedWidth(32)
        self.setFixedHeight(32)
        self.pressed.connect(self.onColorPicker)

    def value(self) -> QColor:
        return self._color

    def setColor(self, color: QColor):
        self._color = color
        if self._color:
            self.setStyleSheet(f'background-color: {self._color.name()};')
        else:
            self.setStyleSheet('')

    def onColorPicker(self):
        dlg = QColorDialog(self._color)
        if dlg.exec_():
            self.setColor(dlg.currentColor())


class _StimulusSettingsPage(QWidget):

    def __init__(self, settings: Settings, parent=None):
        super(_StimulusSettingsPage, self).__init__(parent)
        self._settings = settings
        layout = QFormLayout()

        self._stimulus_saccadic_distance_edit = QDoubleSpinBox()
        self._stimulus_saccadic_distance_edit.setFixedWidth(85)
        self._stimulus_saccadic_distance_edit.setMinimum(5.0)
        self._stimulus_saccadic_distance_edit.setMaximum(198.0)
        self._stimulus_saccadic_distance_edit.setSuffix(' cm')

        layout.addRow(_('Distancia máxima de estímulo sacádico *'), self._stimulus_saccadic_distance_edit)

        self._stimulus_saccadic_ball_radius_edit = QDoubleSpinBox()
        self._stimulus_saccadic_ball_radius_edit.setFixedWidth(85)
        self._stimulus_saccadic_ball_radius_edit.setMinimum(0.1)
        self._stimulus_saccadic_ball_radius_edit.setMaximum(1.0)
        self._stimulus_saccadic_ball_radius_edit.setSuffix(' cm')
        layout.addRow(_('Radio del estímulo sacádico'), self._stimulus_saccadic_ball_radius_edit)

        self._stimulus_saccadic_ball_color_select = ColorButton()
        layout.addRow(_('Color del estímulo'), self._stimulus_saccadic_ball_color_select)

        self._stimulus_saccadic_background_color_select = ColorButton()
        layout.addRow(_('Color de fondo'), self._stimulus_saccadic_background_color_select)

        layout.addRow('', QLabel())
        layout.addRow('', QLabel())
        layout.addRow(QLabel(_('* Define la distancia entre los puntos de estímulo para la prueba con mayor ángulo de estimulación')))

        self.setLayout(layout)

    def load_settings(self):
        self._stimulus_saccadic_distance_edit.setValue(self._settings.stimulus_saccadic_distance)
        self._stimulus_saccadic_ball_radius_edit.setValue(self._settings.stimulus_saccadic_ball_radius)
        self._stimulus_saccadic_ball_color_select.setColor(self._settings.stimulus_saccadic_ball_color)
        self._stimulus_saccadic_background_color_select.setColor(self._settings.stimulus_saccadic_background_color)

    def save(self):
        self._settings.stimulus_saccadic_distance = self._stimulus_saccadic_distance_edit.value()
        self._settings.stimulus_saccadic_ball_radius = self._stimulus_saccadic_ball_radius_edit.value()
        self._settings.stimulus_saccadic_ball_color = self._stimulus_saccadic_ball_color_select.value()
        self._settings.stimulus_saccadic_background_color = self._stimulus_saccadic_background_color_select.value()

    @property
    def title(self):
        return _('Configuración de estímulo')


class SettingsDialog(QDialog):

    def __init__(self, settings: Settings, parent=None):
        super(SettingsDialog, self).__init__(parent=parent)
        self._settings = settings

        self.contentsWidget = QListWidget()
        self.contentsWidget.setFlow(QListView.TopToBottom)
        self.contentsWidget.setViewMode(QListView.IconMode)
        self.contentsWidget.setMovement(QListView.Static)
        self.contentsWidget.setFixedWidth(90)
        self.contentsWidget.setFixedHeight(380)
        self.contentsWidget.setSpacing(5)
        self.contentsWidget.setIconSize(QSize(60, 60))
        self.adjustSize()

        self.pagesWidget = QStackedWidget()
        self.pagesWidget.addWidget(_OpenBCISettingsPage(self._settings))
        self.pagesWidget.addWidget(_OpenBCIChannelsSettingsPage(self._settings))
        self.pagesWidget.addWidget(_ScreenSettingsPage(self._settings))
        self.pagesWidget.addWidget(_StimulusSettingsPage(self._settings))
        self.contentsWidget.setCurrentRow(0)

        # MENUS
        openbci_button = QListWidgetItem(QIcon(':openbci.png'), 'OpenBCI')
        self.contentsWidget.addItem(openbci_button)
        openbci_button.setTextAlignment(Qt.AlignHCenter)
        openbci_button.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        channel_button = QListWidgetItem(QIcon(':channels.svg'), 'Canales')
        self.contentsWidget.addItem(channel_button)
        channel_button.setTextAlignment(Qt.AlignHCenter)
        channel_button.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        screen_button = QListWidgetItem(QIcon(':screen.svg'), 'Pantalla')
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
        dialog_buttons.addButton(_('Aplicar'), QDialogButtonBox.AcceptRole)
        dialog_buttons.addButton(_('Cancelar'), QDialogButtonBox.RejectRole)
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
