from PyQt5.QtCore import pyqtSignal, QDate
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QSpinBox, QDoubleSpinBox

from saccrec.consts import STIMULUS_DEFAULT_ANGLE, STIMULUS_MINIMUM_ANGLE, STIMULUS_MAXIMUM_ANGLE
from saccrec.consts import STIMULUS_DEFAULT_DURATION
from saccrec.consts import STIMULUS_DEFAULT_VARIABILITY
from saccrec.consts import STIMULUS_DEFAULT_SACCADES, STIMULUS_MINUMUM_SACCADES, STIMULUS_MAXIMUM_SACCADES


class StimulusWidget(QWidget):
    
    def __init__(self, parent=None):
        super(StimulusWidget, self).__init__(parent=parent)

        layout = QFormLayout(self)

        self._angle_edit = QSpinBox(self)
        self._angle_edit.setMinimum(STIMULUS_MINIMUM_ANGLE)
        self._angle_edit.setMaximum(STIMULUS_MAXIMUM_ANGLE)
        self._angle_edit.setSingleStep(1)
        self._angle_edit.setSuffix(' grados')
        layout.addRow('Ángulo', self._angle_edit)

        self._fixation_mean_duration_edit = QDoubleSpinBox(self)
        self._fixation_mean_duration_edit.setSingleStep(0.01)
        self._fixation_mean_duration_edit.setSuffix(' segundos')
        layout.addRow('Duración de fijaciones', self._fixation_mean_duration_edit)

        self._fixation_variability_edit = QDoubleSpinBox(self)
        self._fixation_variability_edit.setMinimum(0)
        self._fixation_variability_edit.setSingleStep(0.01)
        self._fixation_variability_edit.setSuffix(' %')
        layout.addRow('Variabilidad de las fijaciones', self._fixation_variability_edit)

        self._saccades_count = QSpinBox(self)
        self._saccades_count.setMinimum(STIMULUS_MINUMUM_SACCADES)
        self._saccades_count.setMaximum(STIMULUS_MAXIMUM_SACCADES)
        self._saccades_count.setSingleStep(1)
        layout.addRow('Cantidad de Sácadas', self._saccades_count)

        self.setLayout(layout)
        self.reset()

    def reset(self):
        self._angle_edit.setValue(STIMULUS_DEFAULT_ANGLE)
        self._fixation_mean_duration_edit.setValue(STIMULUS_DEFAULT_DURATION)
        self._fixation_variability_edit.setValue(STIMULUS_DEFAULT_VARIABILITY)
        self._saccades_count.setValue(STIMULUS_DEFAULT_SACCADES)

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
    def json(self) -> dict:
        return {
            'angle': self.angle,
            'fixation_duration': self.fixation_duration,
            'fixation_variability': self.fixation_variability,
            'saccades_count': self.saccades_count,
        }