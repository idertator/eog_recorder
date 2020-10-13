from typing import List

from PyQt5 import QtCore, QtWidgets

from saccrec import settings
from saccrec.core import Subject
from saccrec.core.math import distance_to_subject
from saccrec.engine.stimulus import SaccadicStimuli

from .output import OutputWizardPage
from .stimulus import StimulusWizardPage
from .subject import SubjectWizardPage


_SUMMARY_HTML = '''<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
    </head>
    <body>
        <h2>{title}</h2>
        {subject}
        {stimulus}

        <h2>{notes}</h2>
        <p>{distance_title}: <strong>{distance} cm</strong></p>
    </body>
</html>
'''


class RecordSetupWizard(QtWidgets.QWizard):
    finished = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(RecordSetupWizard, self).__init__(parent)
        self.setWizardStyle(QtWidgets.QWizard.ClassicStyle)

        self._subject_page = SubjectWizardPage(self)
        self._stimulus_page = StimulusWizardPage(self)
        self._output_page = OutputWizardPage(self)

        self._tests = None

        self.addPage(self._subject_page)
        self.addPage(self._stimulus_page)
        self.addPage(self._output_page)

        self.setWindowTitle(_('Configuración de nuevo registro'))
        self.resize(640, 480)

        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.finish_wizard)

    @property
    def subject_code(self) -> str:
        return self._subject_page.subject_code

    @property
    def subject(self) -> Subject:
        return self._subject_page.subject

    @property
    def stimulus(self) -> dict:
        return self._stimulus_page.json

    @property
    def fixed_distance_to_subject(self) -> float:
        return distance_to_subject(
            settings.stimuli.saccadic_distance,
            self._stimulus_page.max_angle
        )

    @property
    def tests(self) -> List[SaccadicStimuli]:
        distance_to_subject = self.fixed_distance_to_subject
        if self._tests is None:
            # HACER UNA LISTA CON TODAS LAS PRUEBAS INCLUIDA LA INICIAL Y LA FINAL
            auxiliar_list = list()
            auxiliar_list.append(self._stimulus_page.initial_calibration_test)
            for test in self._stimulus_page.test_widget_list:
                auxiliar_list.append(test)
            auxiliar_list.append(self._stimulus_page.final_calibration_test)

            self._tests = [
                SaccadicStimuli(
                    distance_to_subject=distance_to_subject,
                    angle=test.angle,
                    fixation_duration=test.fixation_duration,
                    fixation_variability=test.fixation_variability,
                    saccades_count=test.saccades_count,
                    test_name=test.test_name,
                )
                for test in auxiliar_list
            ]
        return self._tests

    @property
    def output_path(self) -> str:
        return self._output_page.json

    @property
    def subject_page(self):
        return self._subject_page

    @property
    def html(self) -> str:
        return _SUMMARY_HTML.format(
            title=_('Resumen'),
            subject=self._subject_page.html,
            stimulus=self._stimulus_page.html,
            notes=_('Notas importantes'),
            distance_title=_('Distancia del sujeto a la pantalla'),
            distance=f'{self.fixed_distance_to_subject:.2f}'
        )

    @property
    def json(self) -> dict:
        return {
            'subject': self._subject_page.json,
            'stimulus': self._stimulus_page.json,
            'output': self._output_page.json,
            'distance_to_subject': self.fixed_distance_to_subject,
            'tests': self.tests,
        }

    def finish_wizard(self):
        self._stimulus_page.save()
        self.finished.emit()
