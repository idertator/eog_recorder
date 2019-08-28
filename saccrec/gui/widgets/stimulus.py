from PyQt5.QtCore import pyqtSignal, QDate, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QFrame, QGroupBox, QLabel
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QSpinBox, QDoubleSpinBox

from saccrec.consts import STIMULUS_DEFAULT_ANGLE, STIMULUS_MINIMUM_ANGLE, STIMULUS_MAXIMUM_ANGLE
from saccrec.consts import STIMULUS_DEFAULT_DURATION
from saccrec.consts import STIMULUS_DEFAULT_VARIABILITY
from saccrec.consts import STIMULUS_DEFAULT_SACCADES, STIMULUS_MINUMUM_SACCADES, STIMULUS_MAXIMUM_SACCADES


class StimulusWidget(QGroupBox):

    TEST_TYPE_SETTINGS = {
        # (name, position, angle_enabled)
        0: ('Prueba de Calibración Horizontal Inicial', -1, False),
        1: (f'Prueba sacádica a {STIMULUS_DEFAULT_ANGLE} \u00B0', 0, True),
        2: ('Prueba de Calibración Horizontal Final', -1, False)
    }

    def __init__(self, test_type, wizard_list: list = None, wizard_layout: QVBoxLayout = None, parent=None):
        super(StimulusWidget, self).__init__(parent=parent)

        self._test_type = test_type
        self._title = self.TEST_TYPE_SETTINGS[test_type][0]
        self.position = self.TEST_TYPE_SETTINGS[test_type][1]
        self._angle_enabled = self.TEST_TYPE_SETTINGS[test_type][2]

        self._wizard_list = wizard_list
        self._wizard_layout = wizard_layout
        self.setTitle(self._title)
        self.setFlat(True)
        self.setMinimumHeight(90)
        self.setFixedHeight(90)


        layout = QHBoxLayout(self)

        self._angle_edit = QSpinBox(self)
        self._angle_edit.setMinimum(STIMULUS_MINIMUM_ANGLE)
        self._angle_edit.setMaximum(STIMULUS_MAXIMUM_ANGLE)
        self._angle_edit.setSingleStep(1)
        self._angle_edit.setSuffix(' \u00B0')
        self._angle_edit.setFixedWidth(60)
        self._angle_edit.setToolTip('Ángulo')
        self._angle_edit.valueChanged.connect(self.angle_edit_changed)
        element_layout = QVBoxLayout()
        element_layout.addWidget(QLabel('Ángulo'))
        element_layout.addWidget(self._angle_edit)
        layout.addLayout(element_layout)

        self._fixation_mean_duration_edit = QDoubleSpinBox(self)
        self._fixation_mean_duration_edit.setSingleStep(0.01)
        self._fixation_mean_duration_edit.setSuffix(' seg')
        self._fixation_mean_duration_edit.setFixedWidth(80)
        self._fixation_mean_duration_edit.setToolTip('Duración de fijaciones')
        element_layout = QVBoxLayout()
        element_layout.addWidget(QLabel('Duración'))
        element_layout.addWidget(self._fixation_mean_duration_edit)
        layout.addLayout(element_layout)

        self._fixation_variability_edit = QDoubleSpinBox(self)
        self._fixation_variability_edit.setMinimum(0)
        self._fixation_variability_edit.setSingleStep(0.01)
        self._fixation_variability_edit.setSuffix(' %')
        self._fixation_variability_edit.setFixedWidth(80)
        self._fixation_variability_edit.setToolTip('Variabilidad de fijaciones')
        element_layout = QVBoxLayout()
        element_layout.addWidget(QLabel('Variabilidad'))
        element_layout.addWidget(self._fixation_variability_edit)
        layout.addLayout(element_layout)

        self._saccades_count = QSpinBox(self)
        self._saccades_count.setMinimum(STIMULUS_MINUMUM_SACCADES)
        self._saccades_count.setMaximum(STIMULUS_MAXIMUM_SACCADES)
        self._saccades_count.setSingleStep(1)
        self._saccades_count.setFixedWidth(60)
        self._saccades_count.setToolTip('Cantidad de sácadas')
        element_layout = QVBoxLayout()
        element_layout.addWidget(QLabel('Cantidad'))
        element_layout.addWidget(self._saccades_count)
        layout.addLayout(element_layout)

        layout.addStretch()

        self.cancel_widget_button = QPushButton('-')
        self.cancel_widget_button.setFixedWidth(20)
        self.cancel_widget_button.setFixedHeight(20)
        self.cancel_widget_button.pressed.connect(self.cancel_widget_button_pressed)
        layout.addWidget(self.cancel_widget_button)

        self._add_widget_button = QPushButton('+')
        self._add_widget_button.setFixedWidth(20)
        self._add_widget_button.setFixedHeight(20)
        self._add_widget_button.pressed.connect(self.add_widget_button_pressed)
        layout.addWidget(self._add_widget_button)

        self.setAlignment(Qt.AlignBottom)

        self.setLayout(layout)
        self.reset()

    def cancel_widget_button_pressed(self):
        self._wizard_list.remove(self)
        count = 0
        for wizard_item in self._wizard_list:
            wizard_item.position = count
            count += 1
        self._wizard_list[0].cancel_widget_button.setVisible(len(self._wizard_list) > 1)
        self.deleteLater()

    def add_widget_button_pressed(self):
        # ELIMINAR TODOS LOS ELEMENTOS DEL LAYOUT
        for wizard_item in self._wizard_list:
            self._wizard_layout.removeWidget(wizard_item)
        stimulus_widget = StimulusWidget(1, self._wizard_list, self._wizard_layout)
        stimulus_widget.position = self.position + 1

        self._wizard_list.insert(stimulus_widget.position, stimulus_widget)
        for wizard_item in self._wizard_list:
            wizard_item.cancel_widget_button.setVisible(True)
            self._wizard_layout.addWidget(wizard_item)

    def angle_edit_changed(self):
        if self._test_type != 1:
            return
        self.setTitle(f'Prueba sacádica a {str(self._angle_edit.value())} \u00B0')

    def reset(self):
        self._angle_edit.setValue(STIMULUS_DEFAULT_ANGLE)
        self._fixation_mean_duration_edit.setValue(STIMULUS_DEFAULT_DURATION)
        self._fixation_variability_edit.setValue(STIMULUS_DEFAULT_VARIABILITY)
        self._saccades_count.setValue(STIMULUS_DEFAULT_SACCADES)

        self.cancel_widget_button.setVisible(self._wizard_layout is not None and len(self._wizard_list) > 0)
        self._add_widget_button.setVisible(self._wizard_layout is not None)
        self._angle_edit.setEnabled(self._angle_enabled)

    @property
    def angle(self) -> int:
        return self._angle_edit.value()

    @angle.setter
    def angle(self, value: int):
        self._angle_edit.setValue(value)

    @property
    def fixation_duration(self) -> float:
        return self._fixation_mean_duration_edit.value()

    @fixation_duration.setter
    def fixation_duration(self, value: float):
        self._fixation_mean_duration_edit.setValue(value)

    @property
    def fixation_variability(self) -> float:
        return self._fixation_variability_edit.value()

    @fixation_variability.setter
    def fixation_variability(self, value: float):
        self._fixation_variability_edit.setValue(value)

    @property
    def saccades_count(self) -> int:
        return self._saccades_count.value()

    @saccades_count.setter
    def saccades_count(self, value: int):
        self._saccades_count.setValue(value)

    @property
    def test_name(self) -> str:
        return self.title()

    @property
    def test_type(self) -> int:
        return self._test_type

    @property
    def json(self) -> dict:
        return {
            'angle': self.angle,
            'fixation_duration': self.fixation_duration,
            'fixation_variability': self.fixation_variability,
            'saccades_count': self.saccades_count,
        }
