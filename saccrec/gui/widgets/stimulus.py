from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QGroupBox, QLabel
from PyQt5.QtWidgets import QSpinBox, QDoubleSpinBox

from saccrec.consts import STIMULUS_DEFAULT_ANGLE, STIMULUS_MINIMUM_ANGLE, STIMULUS_MAXIMUM_ANGLE, DEFAULT_TEST
from saccrec.consts import STIMULUS_MINUMUM_SACCADES, STIMULUS_MAXIMUM_SACCADES


class StimulusWidget(QGroupBox):

    def __init__(self, data: dict, wizard_list: list = None, wizard_layout: QVBoxLayout = None, parent=None):
        super(StimulusWidget, self).__init__(parent=parent)

        self._data = data

        self._wizard_list = wizard_list
        self._wizard_layout = wizard_layout
        self.setTitle('')
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
        self._angle_edit.setToolTip(_('Ángulo'))
        element_layout = QVBoxLayout()
        element_layout.addWidget(QLabel(_('Ángulo')))
        element_layout.addWidget(self._angle_edit)
        layout.addLayout(element_layout)

        self._fixation_mean_duration_edit = QDoubleSpinBox(self)
        self._fixation_mean_duration_edit.setSingleStep(0.01)
        self._fixation_mean_duration_edit.setSuffix(_(' seg'))
        self._fixation_mean_duration_edit.setFixedWidth(80)
        self._fixation_mean_duration_edit.setToolTip(_('Duración de fijaciones'))
        element_layout = QVBoxLayout()
        element_layout.addWidget(QLabel(_('T. Fijación')))
        element_layout.addWidget(self._fixation_mean_duration_edit)
        layout.addLayout(element_layout)

        self._fixation_variability_edit = QDoubleSpinBox(self)
        self._fixation_variability_edit.setMinimum(0)
        self._fixation_variability_edit.setSingleStep(0.01)
        self._fixation_variability_edit.setSuffix(' %')
        self._fixation_variability_edit.setFixedWidth(80)
        self._fixation_variability_edit.setToolTip(_('Variabilidad de fijaciones'))
        element_layout = QVBoxLayout()
        element_layout.addWidget(QLabel(_('Variabilidad')))
        element_layout.addWidget(self._fixation_variability_edit)
        layout.addLayout(element_layout)

        self._saccades_count = QSpinBox(self)
        self._saccades_count.setMinimum(STIMULUS_MINUMUM_SACCADES)
        self._saccades_count.setMaximum(STIMULUS_MAXIMUM_SACCADES)
        self._saccades_count.setSingleStep(1)
        self._saccades_count.setFixedWidth(60)
        self._saccades_count.setToolTip(_('Cantidad de sácadas'))
        element_layout = QVBoxLayout()
        element_layout.addWidget(QLabel(_('Cantidad')))
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
        stimulus_widget = TestStimulusWidget(self._wizard_list, self._wizard_layout, 1)
        stimulus_widget.position = self.position + 1

        self._wizard_list.insert(stimulus_widget.position, stimulus_widget)
        for wizard_item in self._wizard_list:
            wizard_item.cancel_widget_button.setVisible(True)
            self._wizard_layout.addWidget(wizard_item)

    def reset(self):
        self._angle_edit.setValue(int(self._data.get('angle')))
        self._fixation_mean_duration_edit.setValue(self._data.get('fixation_duration'))
        self._fixation_variability_edit.setValue(self._data.get('fixation_variability'))
        self._saccades_count.setValue(self._data.get('saccades_count'))

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


class InitialStimulusWidget(StimulusWidget):
    def __init__(self, data: dict, wizard_list: list, wizard_layout: QVBoxLayout, parent=None):
        super(InitialStimulusWidget, self).__init__(data, wizard_list, wizard_layout, parent)
        self.setTitle(_('Prueba de Calibración Horizontal Inicial'))
        self.position = -1

    def reset(self):
        super(InitialStimulusWidget, self).reset()

        self.cancel_widget_button.setVisible(False)
        self._add_widget_button.setVisible(True)
        self._angle_edit.setEnabled(False)


class TestStimulusWidget(StimulusWidget):

    def __init__(self, wizard_list: list, wizard_layout: QVBoxLayout, position=0, data: dict = DEFAULT_TEST,parent=None):
        super(TestStimulusWidget, self).__init__(data, wizard_list, wizard_layout, parent)
        self.setTitle('{test_name} {angle} \u00B0'.format(
            test_name=_('Prueba sacádica a'),
            angle=STIMULUS_DEFAULT_ANGLE
        ))
        self.position = position
        self._angle_edit.valueChanged.connect(self.angle_edit_changed)

    def reset(self):
        super(TestStimulusWidget, self).reset()

        self.cancel_widget_button.setVisible(len(self._wizard_list) > 0)
        self._add_widget_button.setVisible(True)
        self._angle_edit.setEnabled(True)

    def angle_edit_changed(self):
        self.setTitle('{test_name} {angle} \u00B0'.format(
            test_name=_('Prueba sacádica a'),
            angle=str(self._angle_edit.value())
        ))


class FinalStimulusWidget(StimulusWidget):
    def __init__(self, data: dict, parent=None):
        super(FinalStimulusWidget, self).__init__(data, parent)
        self.setTitle(_('Prueba de Calibración Horizontal Final'))

    def reset(self):
        super(FinalStimulusWidget, self).reset()

        self.cancel_widget_button.setVisible(False)
        self._add_widget_button.setVisible(False)
        self._angle_edit.setEnabled(False)
