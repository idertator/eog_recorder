import math
from os.path import exists, dirname

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtProperty, pyqtSignal, Qt, QDate
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QWizard, QWizardPage
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QFileDialog, QPushButton

from saccrec.core import Settings
from saccrec.core.math import distance_to_subject
from saccrec.core.models import Subject
from saccrec.gui.widgets import SubjectWidget, StimulusWidget


class RecordSetupWizard(QWizard):
    finished = pyqtSignal()

    def __init__(self, settings: Settings, parent=None):
        super(RecordSetupWizard, self).__init__(parent)
        self.setWizardStyle(QWizard.ClassicStyle)

        self._settings = settings

        self._subject_page = SubjectWizardPage(self)
        self._stimulus_page = StimulusWizardPage(self)
        self._output_page = OutputWizardPage(self)

        self.addPage(self._subject_page)
        self.addPage(self._stimulus_page)
        self.addPage(self._output_page)

        self.padre = parent
        
        self.setWindowTitle('Configuración de nuevo registro')
        self.resize(640, 480)

        self.button(QWizard.FinishButton).clicked.connect(self.finish_wizard)

    @property
    def html(self) -> str:
        return f'''<!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <h3>Resumen</h3>
                {self._subject_page.html}
                {self._stimulus_page.html}

                <h3>Important Notes</h3>
                <p>Distance to subject: <strong>{self.fixed_distance_to_subject:.2f} cm</strong></p>
            </body>
        </html>
        '''

    @property
    def json(self) -> dict:
        return {
            'subject': self._subject_page.json,
            'stimulus': self._stimulus_page.json,
            'output': self._output_page.json,
            'distance_to_subject': self.fixed_distance_to_subject,
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

    def finish_wizard(self):
        self.finished.emit()
        

class SubjectWizardPage(QWizardPage):

    def __init__(self, parent=None):
        super(SubjectWizardPage, self).__init__(parent)

        self.setTitle('Datos del sujeto')

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
        genre = 'hombre nacido el' if self._subject_widget.genre == 0 else 'mujer nacida el'
        borndate = self._subject_widget.borndate.strftime('%d/%m/%Y')
        status = self._subject_widget.status_label

        return f'''<h4>Sujeto</h4>
            <p>{self._subject_widget.full_name}, {genre} {borndate} ({status})</p>
        '''

    @property
    def json(self) -> dict:
        return self._subject_widget.json

    @property
    def subject(self) -> Subject:
        return self._subject_widget.model

class StimulusWizardPage(QWizardPage):

    def __init__(self, parent=None):
        super(StimulusWizardPage, self).__init__(parent)

        self.setTitle('Configuración del estímulo')
        
        layout = QVBoxLayout()
        self._stimulus_widget = StimulusWidget(self)
        layout.addWidget(self._stimulus_widget)

        self.setLayout(layout)

    @property
    def html(self) -> str:
        angle = self._stimulus_widget.angle
        count = self._stimulus_widget.saccades_count
        duration = self._stimulus_widget.fixation_duration
        variability = self._stimulus_widget.fixation_variability
        return f'''<h4>Estímulo</h4>
        <p>Prueba sacádica a <b>{angle}&#176;</b> con <b>{count}</b> sácadas.</p>
        <p>La duración media de las fijaciones es de <b>{duration} segundos</b> con una variabilidad del <b>{variability}%</b>.</p>
        '''

    @property
    def json(self) -> dict:
        return self._stimulus_widget.json

    @property
    def max_angle(self) -> float:
        return self._stimulus_widget.angle


class OutputWizardPage(QWizardPage):

    def __init__(self, parent=None):
        super(OutputWizardPage, self).__init__(parent)

        self.setTitle('Configuración de la salida')

        layout = QVBoxLayout()

        output_layout = QHBoxLayout()

        self._output_path_edit = QLineEdit(self)
        self._output_path_edit.textChanged.connect(self.on_output_path_changed)
        output_layout.addWidget(self._output_path_edit)

        self._output_select_button = QPushButton('Seleccionar', self)
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
            'Seleccione fichero de salida',
            filter='Archivo de SaccRec (*.rec)'
        )
        if not filepath.lower().endswith('.rec'):
            filepath += '.rec'

        self._output_path_edit.setText(filepath)
        self.completeChanged.emit()
