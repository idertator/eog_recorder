from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDoubleSpinBox, QWidget, QColorDialog, QPushButton
from PyQt5.QtWidgets import QFormLayout
from saccrec.consts import SETTINGS_STIMULUS_SACCADIC_DISTANCE_MINIMUM, \
    SETTINGS_STIMULUS_SACCADIC_DISTANCE_MAXIMUM, SETTINGS_DEFAULT_STIMULUS_BALL_RADIUS_MINIMUM, \
    SETTINGS_DEFAULT_STIMULUS_BALL_RADIUS_MAXIMUM

from saccrec.core.settings import Settings


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
            self.setStyleSheet("")

    def onColorPicker(self):
        dlg = QColorDialog(self._color)
        if dlg.exec_():
            self.setColor(dlg.currentColor())


class StimulusSettingsPage(QWidget):
    def __init__(self, settings: Settings, parent=None):
        super(StimulusSettingsPage, self).__init__(parent)
        self._settings = settings
        layout = QFormLayout()

        self._stimulus_saccadic_distance_edit = QDoubleSpinBox()
        self._stimulus_saccadic_distance_edit.setMinimum(SETTINGS_STIMULUS_SACCADIC_DISTANCE_MINIMUM)
        self._stimulus_saccadic_distance_edit.setMaximum(SETTINGS_STIMULUS_SACCADIC_DISTANCE_MAXIMUM)
        self._stimulus_saccadic_distance_edit.setSuffix(' cm')
        layout.addRow('Distancia de estímulo sacádico', self._stimulus_saccadic_distance_edit)

        self._stimulus_saccadic_ball_radius_edit = QDoubleSpinBox()
        self._stimulus_saccadic_ball_radius_edit.setMinimum(SETTINGS_DEFAULT_STIMULUS_BALL_RADIUS_MINIMUM)
        self._stimulus_saccadic_ball_radius_edit.setMaximum(SETTINGS_DEFAULT_STIMULUS_BALL_RADIUS_MAXIMUM)
        self._stimulus_saccadic_ball_radius_edit.setSuffix(' cm')
        layout.addRow('Radio de la estimulo sacadica', self._stimulus_saccadic_ball_radius_edit)

        self._stimulus_saccadic_ball_color_select = ColorButton()
        layout.addRow('Color del estimulo', self._stimulus_saccadic_ball_color_select)

        self._stimulus_saccadic_background_color_select = ColorButton()
        layout.addRow('Color de fondo', self._stimulus_saccadic_background_color_select)

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
        return 'Configuracion de estimulo'
