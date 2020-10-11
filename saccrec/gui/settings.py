from enum import Enum

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog, QListWidget, QListView, QStackedWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QDialogButtonBox, QColorDialog, QPushButton, QMessageBox, QGroupBox
from PyQt5.QtWidgets import QWidget, QFormLayout, QComboBox, QCheckBox, QSpinBox, QLabel, QDoubleSpinBox

from saccrec import settings
from saccrec.engine.openbci import list_ports


class _Language(Enum):
    English = 'en'
    Spanish = 'es'

    @property
    def label(self) -> str:
        return {
            _Language.English: _('Inglés'),
            _Language.Spanish: _('Español'),
        }[self]


class _GUISettingsPage(QWidget):

    def __init__(self, parent=None):
        super(_GUISettingsPage, self).__init__(parent)

        self._initial_lang = None

        layout = QFormLayout()

        self._languages_combo = QComboBox()
        self._languages_combo.setDuplicatesEnabled(False)

        for lang in _Language:
            self._languages_combo.addItem(lang.label, lang.value)

        layout.addRow(_('Idioma'), self._languages_combo)
        self.setLayout(layout)

        self.load()

    def load(self):
        self._initial_lang = settings.gui.lang
        self._languages_combo.setCurrentText(_Language(self._initial_lang).label)

    def save(self):
        lang = str(self._languages_combo.currentData())

        if lang != self._initial_lang:
            settings.gui.lang = lang

            answer = QMessageBox.question(
                self,
                _('Alerta'),
                _('Para establecer los cambios se necesita reiniciar la aplicación. ¿Desea cerrar la aplicación?')
            )

            if answer == QMessageBox.Yes:
                QApplication.exit(0)

    @property
    def title(self) -> str:
        return _('Interfaz de Usuario')


class _OpenBCIChannelWidget(QWidget):

    def __init__(self, channel_number: int, parent=None):
        super(_OpenBCIChannelWidget, self).__init__(parent)
        self._channel_number = channel_number
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

    def load(self):
        active = settings.hardware.channels[self._channel_number].active

        self._openbci_channel_activated_check.setChecked(active)
        self._gain_label.setVisible(active)
        self._openbci_channel_gain_edit.setVisible(active)
        self._openbci_channel_gain_edit.setValue(settings.hardware.channels[self._channel_number].gain)

    def save(self):
        settings.hardware.channels[self._channel_number].active = self._openbci_channel_activated_check.isChecked()
        settings.hardware.channels[self._channel_number].gain = self._openbci_channel_gain_edit.value()


class _HardwarePage(QWidget):

    def __init__(self, parent=None):
        super(_HardwarePage, self).__init__(parent)

        form_layout = QFormLayout()
        self._openbci_ports_combo = QComboBox()
        self._openbci_ports_combo.setDuplicatesEnabled(False)
        for port in list_ports():
            self._openbci_ports_combo.addItem(port, port)
        form_layout.addRow(_('Puerto'), self._openbci_ports_combo)

        self._openbci_sample_rate_combo = QComboBox()
        self._openbci_sample_rate_combo.setDuplicatesEnabled(False)
        for sr in (250, 500, 1000, 2000, 4000, 8000, 16000):
            self._openbci_sample_rate_combo.addItem(f'{sr} Hz', sr)
        form_layout.addRow(_('Frecuencia de muestreo'), self._openbci_sample_rate_combo)

        channels_group = QGroupBox(_('Canales'))
        self._channel_list = []
        channels_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()
        for i in range(8):
            channel = _OpenBCIChannelWidget(i)
            self._channel_list.append(channel)
            if i < 4:
                top_layout.addWidget(channel)
            else:
                bottom_layout.addWidget(channel)

        channels_layout.addLayout(top_layout)
        channels_layout.addLayout(bottom_layout)
        channels_group.setLayout(channels_layout)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(channels_group)

        layout.addStretch()

        self.load()
        self.setLayout(layout)

    def load(self):
        if (port := settings.hardware.port) != '':
            self._openbci_ports_combo.setCurrentText(port)
        else:
            self._openbci_ports_combo.setCurrentIndex(0)

        self._openbci_sample_rate_combo.setCurrentText(f'{settings.hardware.sampling_rate} Hz')

        for channel in self._channel_list:
            channel.load()

    def save(self):
        settings.hardware.port = str(self._openbci_ports_combo.currentData())
        settings.hardware.sampling_rate = int(self._openbci_sample_rate_combo.currentData())

        for channel in self._channel_list:
            channel.save()

    @property
    def title(self) -> str:
        return _('Configuración del Hardware')


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

    def __init__(self, parent=None):
        super(_StimulusSettingsPage, self).__init__(parent)

        screen_size_group = QGroupBox(_('Tamaño Pantalla'))
        screen_size_layout = QHBoxLayout()

        screen_size_layout.addWidget(QLabel(_('Ancho')))

        self._stimulus_screen_width_edit = QDoubleSpinBox()
        self._stimulus_screen_width_edit.setMinimum(10.0)
        self._stimulus_screen_width_edit.setMaximum(200.0)
        self._stimulus_screen_width_edit.setFixedWidth(85)
        self._stimulus_screen_width_edit.setSuffix(' cm')
        screen_size_layout.addWidget(self._stimulus_screen_width_edit)

        screen_size_layout.addWidget(QLabel(_('Alto')))

        self._stimulus_screen_height_edit = QDoubleSpinBox()
        self._stimulus_screen_height_edit.setMinimum(10.0)
        self._stimulus_screen_height_edit.setMaximum(200.0)
        self._stimulus_screen_height_edit.setFixedWidth(85)
        self._stimulus_screen_height_edit.setSuffix(' cm')
        screen_size_layout.addWidget(self._stimulus_screen_height_edit)

        screen_size_layout.addStretch()

        screen_size_group.setLayout(screen_size_layout)

        form_layout = QFormLayout()

        self._stimulus_saccadic_distance_edit = QDoubleSpinBox()
        self._stimulus_saccadic_distance_edit.setFixedWidth(85)
        self._stimulus_saccadic_distance_edit.setMinimum(5.0)
        self._stimulus_saccadic_distance_edit.setMaximum(198.0)
        self._stimulus_saccadic_distance_edit.setSuffix(' cm')

        form_layout.addRow(_('Distancia máxima de estímulo sacádico *'), self._stimulus_saccadic_distance_edit)

        self._stimulus_saccadic_ball_radius_edit = QDoubleSpinBox()
        self._stimulus_saccadic_ball_radius_edit.setFixedWidth(85)
        self._stimulus_saccadic_ball_radius_edit.setMinimum(0.1)
        self._stimulus_saccadic_ball_radius_edit.setMaximum(1.0)
        self._stimulus_saccadic_ball_radius_edit.setSuffix(' cm')
        form_layout.addRow(_('Radio del estímulo sacádico'), self._stimulus_saccadic_ball_radius_edit)

        self._stimulus_saccadic_ball_color_select = ColorButton()
        form_layout.addRow(_('Color del estímulo'), self._stimulus_saccadic_ball_color_select)

        self._stimulus_saccadic_background_color_select = ColorButton()
        form_layout.addRow(_('Color de fondo'), self._stimulus_saccadic_background_color_select)

        form_layout.addRow('', QLabel())
        form_layout.addRow('', QLabel())
        form_layout.addRow(QLabel(_('* Define la distancia entre los puntos de estímulo para la prueba con mayor ángulo de estimulación')))

        layout = QVBoxLayout()
        layout.addWidget(screen_size_group)
        layout.addLayout(form_layout)
        layout.addStretch()

        self.setLayout(layout)

    def load(self):
        self._stimulus_screen_width_edit.setValue(settings.stimuli.screen_width)
        self._stimulus_screen_height_edit.setValue(settings.stimuli.screen_height)
        self._stimulus_saccadic_distance_edit.setValue(settings.stimuli.saccadic_distance)
        self._stimulus_saccadic_ball_radius_edit.setValue(settings.stimuli.ball_radius)
        self._stimulus_saccadic_ball_color_select.setColor(settings.stimuli.ball_color)
        self._stimulus_saccadic_background_color_select.setColor(settings.stimuli.back_color)

    def save(self):
        settings.stimuli.screen_width = self._stimulus_screen_width_edit.value()
        settings.stimuli.screen_height = self._stimulus_screen_height_edit.value()
        settings.stimuli.saccadic_distance = self._stimulus_saccadic_distance_edit.value()
        settings.stimuli.ball_radius = self._stimulus_saccadic_ball_radius_edit.value()
        settings.stimuli.ball_color = self._stimulus_saccadic_ball_color_select.value()
        settings.stimuli.back_color = self._stimulus_saccadic_background_color_select.value()

    @property
    def title(self):
        return _('Configuración de estímulo')


class SettingsDialog(QDialog):

    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent=parent)

        self.contentsWidget = QListWidget()
        self.contentsWidget.setFlow(QListView.TopToBottom)
        self.contentsWidget.setViewMode(QListView.IconMode)
        self.contentsWidget.setMovement(QListView.Static)
        self.contentsWidget.setFixedWidth(90)
        self.contentsWidget.setFixedHeight(475)
        self.contentsWidget.setSpacing(5)
        self.contentsWidget.setIconSize(QSize(60, 60))
        self.adjustSize()

        self.pagesWidget = QStackedWidget()
        self.pagesWidget.addWidget(_GUISettingsPage())
        self.pagesWidget.addWidget(_HardwarePage())
        self.pagesWidget.addWidget(_StimulusSettingsPage())
        self.contentsWidget.setCurrentRow(0)

        # MENUS
        gui_button = QListWidgetItem(QIcon(':gui.svg'), _('Interfaz'))
        self.contentsWidget.addItem(gui_button)
        gui_button.setTextAlignment(Qt.AlignHCenter)
        gui_button.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        openbci_button = QListWidgetItem(QIcon(':openbci.png'), _('OpenBCI'))
        self.contentsWidget.addItem(openbci_button)
        openbci_button.setTextAlignment(Qt.AlignHCenter)
        openbci_button.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        stimulus_button = QListWidgetItem(QIcon(':stimuli.svg'), _('Estímulo'))
        self.contentsWidget.addItem(stimulus_button)
        stimulus_button.setTextAlignment(Qt.AlignHCenter)
        stimulus_button.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

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
            self.pagesWidget.widget(i).load()
        super(SettingsDialog, self).open()
