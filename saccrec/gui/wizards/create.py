from os.path import exists, dirname
from typing import List

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWizard, QWizardPage, QScrollArea, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QFileDialog, QPushButton

from saccrec.core import Settings, Screen
from saccrec.core import Subject, Gender
from saccrec.core.math import distance_to_subject
from saccrec.engine.stimulus import SaccadicStimuli
from saccrec.gui.widgets import SubjectWidget, StimulusWidget
from saccrec.gui.widgets.stimulus import TestStimulusWidget, InitialStimulusWidget, FinalStimulusWidget


class RecordSetupWizard(QWizard):
    finished = pyqtSignal()

    def __init__(self, settings: Settings, screen: Screen, parent=None):
        super(RecordSetupWizard, self).__init__(parent)
        self.setWizardStyle(QWizard.ClassicStyle)

        self._settings = settings
        self._screen = screen

        self._subject_page = SubjectWizardPage(self)
        self._stimulus_page = StimulusWizardPage(self._settings)
        self._output_page = OutputWizardPage(self._subject_page, settings=settings, parent=self)

        self._tests = None

        self.addPage(self._subject_page)
        self.addPage(self._stimulus_page)
        self.addPage(self._output_page)

        self.padre = parent

        self.setWindowTitle(_('Configuración de nuevo registro'))
        self.resize(640, 480)

        self.button(QWizard.FinishButton).clicked.connect(self.finish_wizard)

    @property
    def html(self) -> str:
        return '''<!DOCTYPE html>
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
        '''.format(
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

    @property
    def subject(self) -> Subject:
        return self._subject_page.subject

    @property
    def fixed_distance_to_subject(self) -> float:
        return distance_to_subject(
            self._settings.stimulus_saccadic_distance,
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
                    settings=self._settings,
                    screen=self._screen,
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

    def finish_wizard(self):
        self._stimulus_page.save()
        self.finished.emit()


class SubjectWizardPage(QWizardPage):

    def __init__(self, parent=None):
        super(SubjectWizardPage, self).__init__(parent)

        self.setTitle(_('Datos del sujeto'))

        layout = QVBoxLayout()
        self._subject_widget = SubjectWidget(self)
        self._subject_widget.fullnameChanged.connect(self.on_fullname_changed)
        layout.addWidget(self._subject_widget)

        self.setLayout(layout)

    def isComplete(self) -> bool:
        return self._subject_widget.full_name.strip() != ''

    def on_fullname_changed(self, value: str):
        self.completeChanged.emit()

    @property
    def html(self) -> str:
        gender = {
            Gender.Unknown: _('persona nacida el'),
            Gender.Male: _('hombre nacido el'),
            Gender.Female: _('mujer nacida el'),
        }[self._subject_widget.gender]
        borndate = self._subject_widget.borndate.strftime('%d/%m/%Y')
        status = self._subject_widget.status.label

        return '''<h4>{title}</h4>
            <p>fullname{}, {gender} {borndate} ({status})</p>
        '''.format(
            title=_('Sujeto'),
            fullname=self._subject_widget.full_name,
            gender=gender,
            borndate=borndate,
            status=status
        )

    @property
    def json(self) -> dict:
        return self._subject_widget.json

    @property
    def subject(self) -> Subject:
        return self._subject_widget.model

    @property
    def subject_code(self) -> str:
        def int_to_str(data: int) -> str:
            if int(data) < 10:
                return '0' + str(data)
            if len(str(data)) > 2:
                return str(data)[2:4]
            return str(data)

        full_name = self._subject_widget.full_name.upper().strip().split(' ')
        while len(full_name) > 3:
            full_name.remove(full_name[1])
        code = ''
        if len(full_name) == 1:
            code = full_name[0][0:3]
        else:
            for text in full_name:
                code += text[0]

        day = int_to_str(self._subject_widget.borndate.day)
        month = int_to_str(self._subject_widget.borndate.month)
        year = int_to_str(self._subject_widget.borndate.year)
        return code + day + month + year


class StimulusWizardPage(QWizardPage):

    def __init__(self, settings: Settings, parent=None):
        super(StimulusWizardPage, self).__init__(parent)

        self.setTitle(_('Configuración del estímulo'))
        self._settings = settings

        scroll_area = QScrollArea()
        scroll_area_widget = QWidget()
        scroll_area_layout = QVBoxLayout()

        layout = QVBoxLayout()
        self.test_widget_list = list()
        test_layout = QVBoxLayout()

        self.initial_calibration_test = InitialStimulusWidget(self._settings.tests.get('initial_calibration'), self.test_widget_list, test_layout)
        scroll_area_layout.addWidget(self.initial_calibration_test)

        test_list = self._settings.tests.get('tests')
        cont = 0
        for test in test_list:
            stimulus_widget = TestStimulusWidget(self.test_widget_list, test_layout, cont, test)
            test_layout.addWidget(stimulus_widget)
            self.test_widget_list.append(stimulus_widget)
            cont += 1

        scroll_area_layout.addLayout(test_layout)

        self.final_calibration_test = FinalStimulusWidget(self._settings.tests.get('final_calibration'))
        scroll_area_layout.addWidget(self.final_calibration_test)

        scroll_area.setWidgetResizable(True)
        scroll_area_widget.setLayout(scroll_area_layout)
        scroll_area.setWidget(scroll_area_widget)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    @property
    def html(self) -> str:
        text = '<h4>{title}</h4>'.format(
            title=_('Estímulos')
        )
        # angle = self._stimulus_widget.angle
        # count = self._stimulus_widget.saccades_count
        # duration = self._stimulus_widget.fixation_duration
        # variability = self._stimulus_widget.fixation_variability
        text += self.__test_to_html(self.initial_calibration_test)
        for test in self.test_widget_list:
            text += self.__test_to_html(test)
        text += self.__test_to_html(self.final_calibration_test)
        return text

    @staticmethod
    def __test_to_html(test: StimulusWidget) -> str:
        name = test.test_name
        if type(test) is TestStimulusWidget:
            name = _('Prueba sacádica')

        return '''<p>{name} {of_str} <b>{angle}&#176;</b> {with_str} <b>{saccades_count}</b> {saccades_str}.
        {duration_str} <b>{fixation_duration} {seconds_str}</b> {variability_str} <b>{fixation_variability}%</b>.</p>
        '''.format(
            name=name,
            of_str=_('a'),
            angle=test.angle,
            with_str=_('con'),
            saccades_count=test.saccades_count,
            saccades_str=_('sácadas'),
            duration_str=_('La duración media de las fijaciones es de'),
            fixation_duration=test.fixation_duration,
            seconds_str=_('segundos'),
            variability_str=_('con una variabilidad del'),
            fixation_variability=test.fixation_variability
        )

    @property
    def json(self) -> dict:
        json = {
            'initial_calibration': self.initial_calibration_test.json,
            'final_calibration': self.final_calibration_test.json,
        }
        test_list = list()
        for test in self.test_widget_list:
            test_list.append(test.json)
        json.setdefault('tests', test_list)
        return json

    @property
    def max_angle(self) -> float:
        return float(max(max(test.angle for test in self.test_widget_list), self.initial_calibration_test.angle,
                         self.final_calibration_test.angle))

    def save(self):
        self._settings.tests = self.json


class OutputWizardPage(QWizardPage):

    def __init__(self, subject_wizard_page: SubjectWizardPage, settings: Settings, parent=None):
        super(OutputWizardPage, self).__init__(parent=parent)
        self._settings = settings
        self._subject_wizard_page = subject_wizard_page

        self.setTitle(_('Configuración de la salida'))

        layout = QVBoxLayout()

        output_layout = QHBoxLayout()

        self._output_path_edit = QLineEdit(self)
        self._output_path_edit.textChanged.connect(self.on_output_path_changed)
        output_layout.addWidget(self._output_path_edit)

        self._output_select_button = QPushButton(_('Seleccionar'), self)
        self._output_select_button.pressed.connect(self.on_output_select_clicked)
        output_layout.addWidget(self._output_select_button)

        layout.addLayout(output_layout)

        self._overview_edit = QTextEdit(self)
        self._overview_edit.setReadOnly(True)
        self._overview_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        layout.addWidget(self._overview_edit)

        self.setLayout(layout)

    @property
    def json(self) -> str:
        return self._output_path_edit.text()

    def isComplete(self) -> bool:
        filepath = self._output_path_edit.text()
        return exists(dirname(filepath)) and filepath.lower().endswith('.rec')

    def initializePage(self):
        self._overview_edit.setHtml(self.wizard().html)

    def on_output_path_changed(self):
        self.completeChanged.emit()

    def on_output_select_clicked(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            _('Seleccione fichero de salida'),
            self._settings.output_dir + '/' + self._subject_wizard_page.subject_code,
            filter=_('Archivo de SaccRec (*.rec)')
        )
        if not filepath.lower().endswith('.rec'):
            filepath += '.rec'

        self._output_path_edit.setText(filepath)
        self.completeChanged.emit()
