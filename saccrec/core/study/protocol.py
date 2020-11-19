from json import load, dump
from os import makedirs
from os.path import join, exists

from PyQt5 import QtWidgets

from saccrec import settings

from .stimulus import Stimulus


class Protocol(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(Protocol, self).__init__(parent=parent)

        from saccrec.settings import gui
        if (path := gui.current_protocol) is not None:
            self._stimuli = self._load_stimuli(path)
        else:
            self._stimuli = self._default_stimuli()

        self.setup_ui()

    def __len__(self):
        return len(self._stimuli)

    def __getitem__(self, index: int) -> Stimulus:
        return self._stimuli[index]

    def _default_stimuli(self) -> list[Stimulus]:
        stimuli = [
            Stimulus(
                index=0,
                name=_('Prueba de calibración horizontal inicial'),
                angle=30,
                fixation_duration=3.0,
                fixation_variability=50.0,
                saccades_count=10,
                can_add=True,
                can_remove=False,
                enabled=False,
                parent=self
            ),
            Stimulus(
                index=1,
                name=_('Prueba sacádica a 30\u00B0'),
                angle=30,
                fixation_duration=3.0,
                fixation_variability=50.0,
                saccades_count=20,
                can_add=True,
                can_remove=True,
                enabled=True,
                parent=self
            ),
            Stimulus(
                index=2,
                name=_('Prueba de calibración horizontal final'),
                angle=30,
                fixation_duration=3.0,
                fixation_variability=50.0,
                saccades_count=10,
                can_add=False,
                can_remove=False,
                enabled=False,
                parent=self
            ),
        ]

        for stimulus in stimuli:
            if stimulus.can_add:
                stimulus.addPressed.connect(self._on_stimulus_add_pressed)

            if stimulus.can_remove:
                stimulus.removePressed.connect(self._on_stimulus_remove_pressed)

        return stimuli

    def _load_stimuli(self, filename: str) -> list[Stimulus]:
        if exists(filename):
            result = []

            with open(filename, 'rt') as f:
                stimuli = load(f)

                for index, stimulus in enumerate(stimuli):
                    can_add = index < len(stimuli) - 1
                    can_remove = index > 0 and index < len(stimuli) - 1
                    enabled = index > 0 and index < len(stimuli) - 1

                    stimulus_widget = Stimulus(
                        index=index,
                        name=stimulus['name'],
                        angle=stimulus['angle'],
                        fixation_duration=stimulus['fixation_duration'],
                        fixation_variability=stimulus['fixation_variability'],
                        saccades_count=stimulus['saccades_count'],
                        can_add=can_add,
                        can_remove=can_remove,
                        enabled=enabled,
                        parent=self
                    )

                    if can_add:
                        stimulus_widget.addPressed.connect(self._on_stimulus_add_pressed)

                    if can_remove:
                        stimulus_widget.removePressed.connect(self._on_stimulus_remove_pressed)

                    result.append(stimulus_widget)

            return result

        settings.gui.current_protocol = None
        return self._default_stimuli()

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

    def setup_ui(self):
        self._load_button = QtWidgets.QPushButton()
        self._load_button.setText(_('Abrir'))
        self._load_button.pressed.connect(self._on_load_pressed)

        self._save_button = QtWidgets.QPushButton()
        self._save_button.setText(_('Guardar'))
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

        self._main_layout = QtWidgets.QVBoxLayout()
        self._main_layout.addLayout(self._top_buttons_layout)
        self._main_layout.addWidget(self._scroll_area)
        self.setLayout(self._main_layout)

    def _on_load_pressed(self):
        default_path = settings.gui.protocols_path
        if not exists(default_path):
            makedirs(default_path)

        filename, selected_filter = QtWidgets.QFileDialog.getOpenFileName(
            self,
            _('Abrir fichero de protocolo'),
            default_path,
            filter=_('Archivo de Protocolo (*.json)')
        )
        if filename:
            self._clear_stimulus_widgets(disconnect=True)
            self._stimuli = self._load_stimuli(filename)
            self._populate_stimulus_widgets()

    def _on_save_pressed(self):
        if settings.gui.current_protocol is not None:
            default_path = settings.gui.current_protocol
        else:
            default_path = settings.gui.protocols_path
            if not exists(default_path):
                makedirs(default_path)
            default_path = join(default_path, _('SinNombre.json'))

        filename, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
            self,
            _('Guardar fichero de protocolo'),
            default_path,
            filter=_('Archivo de Protocolo (*.json)')
        )
        if filename:
            with open(filename, 'wt') as f:
                dump([
                    stimulus.json
                    for stimulus in self._stimuli
                ], f, indent=4)
            settings.gui.current_protocol = filename

    def _on_stimulus_add_pressed(self, index: int):
        self._clear_stimulus_widgets()

        current = self._stimuli[index]

        stimulus_widget = Stimulus(
            index=index + 1,
            name=current.name,
            angle=current.angle,
            fixation_duration=current.fixation_duration,
            fixation_variability=current.fixation_variability,
            saccades_count=current.saccades_count,
            can_add=True,
            can_remove=True,
            enabled=True,
            parent=self
        )

        stimulus_widget.addPressed.connect(self._on_stimulus_add_pressed)
        stimulus_widget.removePressed.connect(self._on_stimulus_remove_pressed)

        self._stimuli.insert(index + 1, stimulus_widget)

        for i in range(index + 2, len(self._stimuli)):
            self._stimuli[i].index = i

        self._populate_stimulus_widgets()

    def _on_stimulus_remove_pressed(self, index: int):
        self._clear_stimulus_widgets()

        stimulus = self._stimuli[index]
        stimulus.setParent(None)

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
    def max_angle(self) -> float:
        return float(
            max(
                test.angle
                for test in self._stimuli
            )
        )
