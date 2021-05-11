from os.path import exists

from PySide6 import QtCore, QtWidgets

from eoglib.io import load_protocol
from eoglib.models import Subject, Protocol, SaccadicStimulus, StimulusOrientation

from saccrec import settings

from .output import OutputWizardPage
from .stimulus import StimulusWizardPage
from .subject import SubjectWizardPage


class RecordSetupWizard(QtWidgets.QWizard):
    finished = QtCore.Signal(dict)

    def __init__(self, parent):
        super(RecordSetupWizard, self).__init__(parent)

        self.setWindowTitle(_('New Record Wizard'))
        self.setWizardStyle(QtWidgets.QWizard.ClassicStyle)
        self.resize(640, 480)

        self._subject = Subject()

        if (path := settings.gui.current_protocol) is not None:
            if exists(path):
                self._protocol = load_protocol(path)
            else:
                self._protocol = self._default_protocol()
        else:
            self._protocol = self._default_protocol()

        self._light_intensity = 0
        self._output_path = ''

        self._subject_page = SubjectWizardPage(
            subject=self._subject,
            parent=self
        )

        self._stimulus_page = StimulusWizardPage(
            protocol=self._protocol,
            parent=self
        )
        self._stimulus_page.protocolLoaded.connect(self._on_protocol_loaded)

        self._output_page = OutputWizardPage(
            subject=self._subject,
            protocol=self._protocol,
            parent=self
        )
        self._output_page.outputPathChanged.connect(self._on_output_path_changed)
        self._output_page.lightIntensityChanged.connect(self._on_light_intensity_changed)

        self.addPage(self._subject_page)
        self.addPage(self._stimulus_page)
        self.addPage(self._output_page)

        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.finish_wizard)

    def finish_wizard(self):
        self.finished.emit({
            'subject': self._subject,
            'protocol': self._protocol,
            'output_path': self._output_path,
            'light_intensity': self._light_intensity,
        })

    def _default_protocol(self) -> Protocol:
        return Protocol(
            stimuli=[
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

    def _on_protocol_loaded(self, protocol: Protocol):
        self._protocol = protocol

    def _on_output_path_changed(self, output_path: str):
        self._output_path = output_path

    def _on_light_intensity_changed(self, value: int):
        self._light_intensity = value
