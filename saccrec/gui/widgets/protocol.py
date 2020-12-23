from os import makedirs
from os.path import join, exists

from PySide6 import QtWidgets

from saccrec import settings

from eoglib.io import load_protocol, save_protocol
from eoglib.models import Protocol, SaccadicStimulus, StimulusOrientation

from .stimulus import SaccadicStimulusWidget


class ProtocolWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ProtocolWidget, self).__init__(parent=parent)

        if (path := settings.gui.current_protocol) is not None:
            self._protocol = load_protocol(path)
        else:
            self._protocol = self._default_protocol()
        self._stimuli = self._protocol_widgets(self._protocol)

        self._load_button = QtWidgets.QPushButton()
        self._load_button.setText(_('Open'))
        self._load_button.pressed.connect(self._on_load_pressed)

        self._save_button = QtWidgets.QPushButton()
        self._save_button.setText(_('Save'))
        self._save_button.pressed.connect(self._on_save_pressed)

        self._top_buttons_layout = QtWidgets.QHBoxLayout()
        self._top_buttons_layout.addStretch()
        self._top_buttons_layout.addWidget(self._load_button)
        self._top_buttons_layout.addWidget(self._save_button)

        self._scroll_area_layout = QtWidgets.QVBoxLayout()
        self._populate_stimulus_widgets()

        self._scroll_area_widget = QtWidgets.QWidget()
        self._scroll_area_widget.setLayout(self._scroll_area_layout)

        self._scroll_area = QtWidgets.QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setWidget(self._scroll_area_widget)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self._top_buttons_layout)
        self.layout.addWidget(self._scroll_area)

    def _default_protocol(self) -> Protocol:
        return Protocol(
            stimuli = [
                SaccadicStimulus(
                    calibration=True,
                    angle=30,
                    fixation_duration=3.0,
                    fixation_variability=50.0,
                    saccades_count=10,
                    orientation=StimulusOrientation.Horizontal
                ),
                SaccadicStimulus(
                    calibration=False,
                    angle=30,
                    fixation_duration=3.0,
                    fixation_variability=50.0,
                    saccades_count=20,
                    orientation=StimulusOrientation.Horizontal
                ),
                SaccadicStimulus(
                    calibration=True,
                    angle=30,
                    fixation_duration=3.0,
                    fixation_variability=50.0,
                    saccades_count=10,
                    orientation=StimulusOrientation.Horizontal
                ),
            ]
        )

    def _protocol_widgets(self, protocol: Protocol) -> list[SaccadicStimulusWidget]:
        widgets = []
        for index, stimulus in enumerate(protocol):
            if isinstance(stimulus, SaccadicStimulus):
                widget = SaccadicStimulusWidget(
                    index=index,
                    stimulus=stimulus,
                    can_add=index < len(protocol) - 1,
                    can_remove=not stimulus.calibration,
                    enabled=not stimulus.calibration,
                    parent=self
                )

                if widget.can_add:
                    widget.addPressed.connect(self._on_stimulus_add_pressed)

                if widget.can_remove:
                    widget.removePressed.connect(self._on_stimulus_remove_pressed)

                widgets.append(widget)
        return widgets

    def _clear_stimulus_widgets(self, disconnect: bool = False):
        for widget in self._stimuli:
            if disconnect:
                if widget.can_add:
                    widget.addPressed.disconnect(self._on_stimulus_add_pressed)
                if widget.can_remove:
                    widget.removePressed.disconnect(self._on_stimulus_remove_pressed)

            self._scroll_area_layout.removeWidget(widget)

    def _populate_stimulus_widgets(self):
        for index, stimulus in enumerate(self._stimuli):
            self._scroll_area_layout.addWidget(stimulus)

    def _on_load_pressed(self):
        default_path = settings.gui.protocols_path
        if not exists(default_path):
            makedirs(default_path)

        filename, selected_filter = QtWidgets.QFileDialog.getOpenFileName(
            self,
            _('Open Protocol File'),
            default_path,
            filter=_('Protocol File (*.json)')
        )
        if filename:
            self._clear_stimulus_widgets(disconnect=True)
            self._protocol = load_protocol(filename)
            self._stimuli = self._protocol_widgets(self._protocol)
            self._populate_stimulus_widgets()

    def _on_save_pressed(self):
        if settings.gui.current_protocol is not None:
            default_path = settings.gui.current_protocol
        else:
            default_path = settings.gui.protocols_path
            if not exists(default_path):
                makedirs(default_path)
            default_path = join(default_path, _('Unknown.json'))

        filename, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
            self,
            _('Save Protocol File'),
            default_path,
            filter=_('Protocol File (*.json)')
        )
        if filename:
            save_protocol(filename, self._protocol)
            settings.gui.current_protocol = filename

    def _on_stimulus_add_pressed(self, index: int):
        self._clear_stimulus_widgets()

        current_stimulus = self._protocol[index]
        stimulus = SaccadicStimulus(
            calibration=False,
            angle=current_stimulus.angle,
            fixation_duration=current_stimulus.fixation_duration,
            fixation_variability=current_stimulus.fixation_variability,
            saccades_count=current_stimulus.saccades_count,
            orientation=current_stimulus.orientation
        )

        stimulus_widget = SaccadicStimulusWidget(
            index=index + 1,
            stimulus=stimulus,
            can_add=True,
            can_remove=True,
            enabled=True,
            parent=self
        )

        stimulus_widget.addPressed.connect(self._on_stimulus_add_pressed)
        stimulus_widget.removePressed.connect(self._on_stimulus_remove_pressed)

        self._protocol.insert(index + 1, stimulus)
        self._stimuli.insert(index + 1, stimulus_widget)

        for i in range(index + 2, len(self._stimuli)):
            self._stimuli[i].index = i

        self._populate_stimulus_widgets()

    def _on_stimulus_remove_pressed(self, index: int):
        self._clear_stimulus_widgets()

        stimulus = self._stimuli[index]
        stimulus.parent = None

        if stimulus.can_add:
            stimulus.addPressed.disconnect(self._on_stimulus_add_pressed)
        if stimulus.can_remove:
            stimulus.removePressed.disconnect(self._on_stimulus_remove_pressed)

        del self._stimuli[index]
        stimulus = None

        for i in range(index, len(self._stimuli)):
            self._stimuli[i].index = i

        self._populate_stimulus_widgets()

    @property
    def protocol(self) -> Protocol:
        return self._protocol
