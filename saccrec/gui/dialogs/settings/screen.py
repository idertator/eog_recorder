from PyQt5.QtWidgets import QWidget, QFormLayout, QDoubleSpinBox

from saccrec.consts import SETTINGS_STIMULUS_SCREEN_DEFAULT_WIDTH_MINIMUM, \
    SETTINGS_STIMULUS_SCREEN_DEFAULT_WIDTH_MAXIMUM, \
    SETTINGS_STIMULUS_SCREEN_DEFAULT_HEIGHT_MINIMUM, SETTINGS_STIMULUS_SCREEN_DEFAULT_HEIGHT_MAXIMUM
from saccrec.core import Settings


class ScreenSettingsPage(QWidget):
    def __init__(self, settings: Settings = Settings, parent=None):
        super(ScreenSettingsPage, self).__init__(parent)
        self._settings = settings

        layout = QFormLayout()
        self.setWindowTitle("Pantalla de estimulo")
        self._stimulus_screen_width_edit = QDoubleSpinBox()
        self._stimulus_screen_width_edit.setMinimum(SETTINGS_STIMULUS_SCREEN_DEFAULT_WIDTH_MINIMUM)
        self._stimulus_screen_width_edit.setMaximum(SETTINGS_STIMULUS_SCREEN_DEFAULT_WIDTH_MAXIMUM)
        self._stimulus_screen_width_edit.setFixedWidth(85)
        self._stimulus_screen_width_edit.setSuffix(' cm')
        layout.addRow('Ancho', self._stimulus_screen_width_edit)

        self._stimulus_screen_height_edit = QDoubleSpinBox()
        self._stimulus_screen_height_edit.setMinimum(SETTINGS_STIMULUS_SCREEN_DEFAULT_HEIGHT_MINIMUM)
        self._stimulus_screen_height_edit.setMaximum(SETTINGS_STIMULUS_SCREEN_DEFAULT_HEIGHT_MAXIMUM)
        self._stimulus_screen_height_edit.setFixedWidth(85)
        self._stimulus_screen_height_edit.setSuffix(' cm')
        layout.addRow('Alto', self._stimulus_screen_height_edit)

        self.setLayout(layout)

    def load_settings(self):
        self._stimulus_screen_width_edit.setValue(self._settings.stimulus_screen_width)
        self._stimulus_screen_height_edit.setValue(self._settings.stimulus_screen_height)

    def save(self):
        self._settings.stimulus_screen_width = self._stimulus_screen_width_edit.value()
        self._settings.stimulus_screen_height = self._stimulus_screen_height_edit.value()

    @property
    def title(self):
        return 'Configuracion de pantalla'
