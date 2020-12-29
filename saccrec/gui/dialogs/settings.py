from enum import Enum

from PySide2 import QtCore, QtGui, QtWidgets

from saccrec import settings
from saccrec.core.enums import Language
from saccrec.recording import CytonBoard
from saccrec.gui.widgets import ColorButton


class _GUISettingsPage(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(_GUISettingsPage, self).__init__(parent)

        self._initial_lang = None

        layout = QtWidgets.QFormLayout()

        self._languages_combo = QtWidgets.QComboBox()
        self._languages_combo.setDuplicatesEnabled(False)

        for lang in Language:
            self._languages_combo.addItem(lang.label, lang.value)

        layout.addRow(_('Language'), self._languages_combo)
        self.setLayout(layout)

        self.load()

    def load(self):
        self._initial_lang = settings.gui.lang
        self._languages_combo.setCurrentText(Language(self._initial_lang).label)

    def save(self):
        lang = str(self._languages_combo.currentData())

        if lang != self._initial_lang:
            settings.gui.lang = lang

            answer = QtWidgets.QMessageBox.question(
                self,
                _('Alert'),
                _('You need to restart the app in order to persist the changes. Do you really want to close the app?')
            )

            if answer == QtWidgets.QMessageBox.Yes:
                QtWidgets.QApplication.exit(0)

    @property
    def title(self) -> str:
        return _('User Interface')


class _OpenBCIChannelWidget(QtWidgets.QWidget):

    def __init__(self, channel_number: int, parent=None):
        super(_OpenBCIChannelWidget, self).__init__(parent)
        self._channel_number = channel_number
        self.setFixedSize(120, 100)

        self._activated_check = QtWidgets.QCheckBox()
        self._activated_check.stateChanged.connect(self._on_activated_changed)

        self._gain_label = QtWidgets.QLabel(_('Gain'))

        self._gain_edit = QtWidgets.QSpinBox()
        self._gain_edit.setFixedWidth(40)

        gain_layout = QtWidgets.QHBoxLayout()
        gain_layout.addWidget(self._gain_label)
        gain_layout.addWidget(self._gain_edit)

        layout = QtWidgets.QFormLayout()
        layout.addRow(
            '{channel} {number}    '.format(
                channel=_('Channel'),
                number=self._channel_number + 1
            ),
            self._activated_check
        )
        layout.addRow(gain_layout)
        layout.setSpacing(3)

        self.setLayout(layout)

    def _on_activated_changed(self):
        self._gain_edit.setVisible(self._activated_check.checkState())
        self._gain_label.setVisible(self._activated_check.checkState())

    def load(self):
        active = settings.hardware.channels[self._channel_number].active

        self._activated_check.setChecked(active)
        self._gain_label.setVisible(active)
        self._gain_edit.setVisible(active)
        self._gain_edit.setValue(settings.hardware.channels[self._channel_number].gain)

    def save(self):
        settings.hardware.channels[self._channel_number].active = self._activated_check.isChecked()
        settings.hardware.channels[self._channel_number].gain = self._gain_edit.value()


class _HardwarePage(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(_HardwarePage, self).__init__(parent)

        self._ports_combo = QtWidgets.QComboBox()
        self._ports_combo.setDuplicatesEnabled(False)
        for port in CytonBoard.list_ports():
            self._ports_combo.addItem(port, port)

        self._sample_rate_combo = QtWidgets.QComboBox()
        self._sample_rate_combo.setDuplicatesEnabled(False)
        for sr in (250, 500, 1000, 2000, 4000, 8000, 16000):
            self._sample_rate_combo.addItem(f'{sr} Hz', sr)

        channels_group = QtWidgets.QGroupBox(_('Channels'))
        self._channel_list = []
        top_layout = QtWidgets.QHBoxLayout()
        bottom_layout = QtWidgets.QHBoxLayout()
        for i in range(8):
            channel = _OpenBCIChannelWidget(i)
            self._channel_list.append(channel)
            if i < 4:
                top_layout.addWidget(channel)
            else:
                bottom_layout.addWidget(channel)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(_('Port'), self._ports_combo)
        form_layout.addRow(_('Sampling frequency'), self._sample_rate_combo)

        channels_layout = QtWidgets.QVBoxLayout()
        channels_layout.addLayout(top_layout)
        channels_layout.addLayout(bottom_layout)
        channels_group.setLayout(channels_layout)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(channels_group)
        layout.addStretch()
        self.setLayout(layout)

        self.load()

    def load(self):
        if (port := settings.hardware.port) != '':
            self._ports_combo.setCurrentText(port)
        else:
            self._ports_combo.setCurrentIndex(0)

        self._sample_rate_combo.setCurrentText(f'{settings.hardware.sampling_rate} Hz')

        for channel in self._channel_list:
            channel.load()

    def save(self):
        settings.hardware.port = str(self._ports_combo.currentData())
        settings.hardware.sampling_rate = int(self._sample_rate_combo.currentData())

        for channel in self._channel_list:
            channel.save()

    @property
    def title(self) -> str:
        return _('Hardware')


class _StimulusSettingsPage(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(_StimulusSettingsPage, self).__init__(parent)

        self._stimulus_screen_width_edit = QtWidgets.QDoubleSpinBox()
        self._stimulus_screen_width_edit.setRange(10.0, 200.0)
        self._stimulus_screen_width_edit.setFixedWidth(85)
        self._stimulus_screen_width_edit.setSuffix(' cm')

        self._stimulus_screen_height_edit = QtWidgets.QDoubleSpinBox()
        self._stimulus_screen_height_edit.setRange(10.0, 200.0)
        self._stimulus_screen_height_edit.setFixedWidth(85)
        self._stimulus_screen_height_edit.setSuffix(' cm')

        self._stimulus_saccadic_distance_edit = QtWidgets.QDoubleSpinBox()
        self._stimulus_saccadic_distance_edit.setFixedWidth(85)
        self._stimulus_saccadic_distance_edit.setRange(5.0, 198.0)
        self._stimulus_saccadic_distance_edit.setSuffix(' cm')

        self._stimulus_saccadic_ball_radius_edit = QtWidgets.QDoubleSpinBox()
        self._stimulus_saccadic_ball_radius_edit.setFixedWidth(85)
        self._stimulus_saccadic_ball_radius_edit.setRange(0.1, 1.0)
        self._stimulus_saccadic_ball_radius_edit.setSuffix(' cm')

        self._stimulus_saccadic_ball_color_select = ColorButton()

        self._stimulus_saccadic_background_color_select = ColorButton()

        screen_size_layout = QtWidgets.QHBoxLayout()
        screen_size_layout.addWidget(QtWidgets.QLabel(_('Width')))
        screen_size_layout.addWidget(self._stimulus_screen_width_edit)
        screen_size_layout.addWidget(QtWidgets.QLabel(_('Height')))
        screen_size_layout.addWidget(self._stimulus_screen_height_edit)
        screen_size_layout.addStretch()

        screen_size_group = QtWidgets.QGroupBox(_('Screen Size'))
        screen_size_group.setLayout(screen_size_layout)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(_('Maximum distance to saccadic stimulus *'), self._stimulus_saccadic_distance_edit)
        form_layout.addRow(_('Saccadic stimulus radius'), self._stimulus_saccadic_ball_radius_edit)
        form_layout.addRow(_('Stimulus color'), self._stimulus_saccadic_ball_color_select)
        form_layout.addRow(_('Background color'), self._stimulus_saccadic_background_color_select)
        form_layout.addRow('', QtWidgets.QLabel())
        form_layout.addRow('', QtWidgets.QLabel())
        form_layout.addRow(QtWidgets.QLabel(
            _('* Define the distance between the points of stimulus for the test with the greatest angle of stimulation'))
        )

        layout = QtWidgets.QVBoxLayout()
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
        return _('Stimuli')


class SettingsDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent=parent)

        self._contents_widget = QtWidgets.QListWidget()
        self._contents_widget.setFlow(QtWidgets.QListView.TopToBottom)
        self._contents_widget.setViewMode(QtWidgets.QListView.IconMode)
        self._contents_widget.setMovement(QtWidgets.QListView.Static)
        self._contents_widget.setFixedSize(90, 475)
        self._contents_widget.setSpacing(5)
        self._contents_widget.setIconSize(QtCore.QSize(60, 60))
        self.adjustSize()

        self._pages_widget = QtWidgets.QStackedWidget()
        self._pages_widget.addWidget(_GUISettingsPage())
        self._pages_widget.addWidget(_HardwarePage())
        self._pages_widget.addWidget(_StimulusSettingsPage())
        self._contents_widget.setCurrentRow(0)

        # MENUS
        gui_button = QtWidgets.QListWidgetItem(QtGui.QIcon(':/settings/gui.svg'), _('Interface'))
        self._contents_widget.addItem(gui_button)
        gui_button.setTextAlignment(QtCore.Qt.AlignHCenter)
        gui_button.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        openbci_button = QtWidgets.QListWidgetItem(QtGui.QIcon(':/settings/openbci.png'), _('OpenBCI'))
        self._contents_widget.addItem(openbci_button)
        openbci_button.setTextAlignment(QtCore.Qt.AlignHCenter)
        openbci_button.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        stimulus_button = QtWidgets.QListWidgetItem(QtGui.QIcon(':/settings/stimuli.svg'), _('Stimulus'))
        self._contents_widget.addItem(stimulus_button)
        stimulus_button.setTextAlignment(QtCore.Qt.AlignHCenter)
        stimulus_button.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        self._contents_widget.currentItemChanged.connect(self.change_page)

        dialog_buttons = QtWidgets.QDialogButtonBox()
        dialog_buttons.addButton(_('Apply'), QtWidgets.QDialogButtonBox.AcceptRole)
        dialog_buttons.addButton(_('Cancel'), QtWidgets.QDialogButtonBox.RejectRole)
        dialog_buttons.accepted.connect(self._on_accepted)
        dialog_buttons.rejected.connect(self._on_rejected)

        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addWidget(self._contents_widget)
        horizontal_layout.addWidget(self._pages_widget, 1)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(horizontal_layout)
        layout.addWidget(dialog_buttons)

        self.setLayout(layout)

    def change_page(self, current, previous):
        if not current:
            current = previous

        self._pages_widget.setCurrentIndex(self._contents_widget.row(current))
        self.setWindowTitle(self._pages_widget.currentWidget().title)

    def _on_accepted(self):
        for i in range(self._pages_widget.count()):
            self._pages_widget.widget(i).save()
        self.accept()

    def _on_rejected(self):
        self.reject()

    def open(self):
        for i in range(self._pages_widget.count()):
            self._pages_widget.widget(i).load()
        super(SettingsDialog, self).open()
