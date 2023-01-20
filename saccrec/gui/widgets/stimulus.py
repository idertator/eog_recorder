from PySide6 import QtCore, QtWidgets

from eoglib.models import SaccadicStimulus


class SaccadicStimulusWidget(QtWidgets.QGroupBox):
    addPressed = QtCore.Signal(int)
    removePressed = QtCore.Signal(int)

    def __init__(
            self,
            index: int,
            stimulus: SaccadicStimulus,
            can_add: bool = False,
            can_remove: bool = False,
            enabled: bool = True,
            parent=None
    ):
        super(SaccadicStimulusWidget, self).__init__(parent=parent)

        self._index = index
        self._can_add = can_add
        self._can_remove = can_remove
        self._enabled = enabled

        self._stimulus = stimulus

        self.setTitle(self.title_processing(str(stimulus)))
        self.setFlat(True)
        self.setMinimumHeight(90)
        self.setFixedHeight(90)
        self.setAlignment(QtCore.Qt.AlignBottom)

        self._angle_edit = QtWidgets.QSpinBox(self)
        self._angle_edit.setValue(stimulus.angle)
        self._angle_edit.setRange(10, 60)
        self._angle_edit.setSingleStep(1)
        self._angle_edit.setSuffix(' \u00B0')
        self._angle_edit.setFixedWidth(60)
        self._angle_edit.setToolTip(_('Angle'))
        self._angle_edit.setEnabled(self._enabled)
        self._angle_edit.valueChanged.connect(self._on_angle_value_changed)

        angle_layout = QtWidgets.QVBoxLayout()
        angle_layout.addWidget(QtWidgets.QLabel(_('Angle')))
        angle_layout.addWidget(self._angle_edit)

        self._fixation_mean_duration_edit = QtWidgets.QDoubleSpinBox(self)
        self._fixation_mean_duration_edit.setValue(stimulus.fixation_duration)
        self._fixation_mean_duration_edit.setSingleStep(0.01)
        self._fixation_mean_duration_edit.setSuffix(_(' sec'))
        self._fixation_mean_duration_edit.setFixedWidth(80)
        self._fixation_mean_duration_edit.setToolTip(_('Fixation mean duration'))
        self._fixation_mean_duration_edit.setEnabled(self._enabled)
        self._fixation_mean_duration_edit.valueChanged.connect(self._on_fixation_duration_changed)

        duration_layout = QtWidgets.QVBoxLayout()
        duration_layout.addWidget(QtWidgets.QLabel(_('F. duration')))
        duration_layout.addWidget(self._fixation_mean_duration_edit)

        self._fixation_variability_edit = QtWidgets.QDoubleSpinBox(self)
        self._fixation_variability_edit.setValue(stimulus.fixation_variability)
        self._fixation_variability_edit.setMinimum(0)
        self._fixation_variability_edit.setSingleStep(0.01)
        self._fixation_variability_edit.setSuffix(' %')
        self._fixation_variability_edit.setFixedWidth(80)
        self._fixation_variability_edit.setToolTip(_('Fixation variability'))
        self._fixation_variability_edit.setEnabled(self._enabled)
        self._fixation_variability_edit.valueChanged.connect(self._on_fixation_variability_changed)

        variability_layout = QtWidgets.QVBoxLayout()
        variability_layout.addWidget(QtWidgets.QLabel(_('F. variability')))
        variability_layout.addWidget(self._fixation_variability_edit)

        self._saccades_count = QtWidgets.QSpinBox(self)
        self._saccades_count.setValue(stimulus.saccades_count)
        self._saccades_count.setRange(5, 100)
        self._saccades_count.setSingleStep(1)
        self._saccades_count.setFixedWidth(60)
        self._saccades_count.setToolTip(_('Saccades count'))
        self._saccades_count.setEnabled(self._enabled)
        self._saccades_count.valueChanged.connect(self._on_saccades_count_changed)

        count_layout = QtWidgets.QVBoxLayout()
        count_layout.addWidget(QtWidgets.QLabel(_('Quantity')))
        count_layout.addWidget(self._saccades_count)

        self._cancel_widget_button = QtWidgets.QPushButton('-')
        self._cancel_widget_button.setFixedSize(20, 20)
        self._cancel_widget_button.pressed.connect(self._on_remove_pressed)

        self._add_widget_button = QtWidgets.QPushButton('+')
        self._add_widget_button.setFixedSize(20, 20)
        self._add_widget_button.pressed.connect(self._on_add_pressed)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addLayout(angle_layout)
        layout.addLayout(duration_layout)
        layout.addLayout(variability_layout)
        layout.addLayout(count_layout)
        layout.addStretch()

        if self._can_remove:
            layout.addWidget(self._cancel_widget_button)

        if self._can_add:
            layout.addWidget(self._add_widget_button)

        self.setLayout(layout)

    def _on_remove_pressed(self):
        self.removePressed.emit(self._index)

    def _on_add_pressed(self):
        self.addPressed.emit(self._index)

    def _on_angle_value_changed(self, value: int):
        self._stimulus.angle = value
        self.title = str(self._stimulus)

    def _on_fixation_duration_changed(self, value: float):
        self._stimulus.fixation_duration = value

    def _on_fixation_variability_changed(self, value: float):
        self._stimulus.fixation_variability = value

    def _on_saccades_count_changed(self, value: int):
        self._stimulus.saccades_count = value

    @staticmethod
    def title_processing(title: str) -> str:
        start_text = title.split(' ')[0] + ' ' + title.split(' ')[1]
        match start_text:
            case 'Horizontal Calibration':
                return title.replace(start_text, _('Horizontal calibration'))
            case 'Horizontal Saccadic':
                return title.replace(start_text, _('Horizontal saccadic'))
            case 'Vertical Calibration':
                return title.replace(start_text, _('Vertical calibration'))
            case 'Vertical Saccadic':
                return title.replace(start_text, _('Vertical saccadic'))
            case 'Saccadic Calibration':
                return title.replace(start_text, _('Saccadic calibration'))
            case 'Unknown Saccadic':
                return title.replace('Unknown Saccadic Test', _('Unknown saccadic test'))
            case _:
                return title.replace('Saccadic', _('Saccadic'))

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int):
        self._index = value

    @property
    def can_add(self) -> bool:
        return self._can_add

    @property
    def can_remove(self) -> bool:
        return self._can_remove
