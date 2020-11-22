from os.path import join, exists, dirname

from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets

from saccrec import settings


class SubjectWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent):
        super(SubjectWizardPage, self).__init__(parent=parent)
        self.setup_ui()

    def setup_ui(self):
        self.setTitle(_('Datos del sujeto'))

        workspace = self.parent().parent()

        self._subject = workspace.subject
        self._subject.setParent(self)
        self._subject.nameChanged.connect(self.on_name_changed)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._subject)

        self.setLayout(layout)

    def isComplete(self) -> bool:
        return self._subject.name.strip() != ''

    def on_name_changed(self, value: str):
        self.completeChanged.emit()


class StimulusWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent):
        super(StimulusWizardPage, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setTitle(_('Configuración del estímulo'))

        workspace = self.parent().parent()

        self._protocol = workspace.protocol
        self._protocol.setParent(self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._protocol)

        self.setLayout(layout)

    @property
    def json(self) -> dict:
        return self._protocol.json


class OutputWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent):
        super(OutputWizardPage, self).__init__(parent=parent)

        self.setTitle(_('Configuración de la salida'))

        layout = QtWidgets.QVBoxLayout()

        output_layout = QtWidgets.QHBoxLayout()

        self._output_path_edit = QtWidgets.QLineEdit(self)
        self._output_path_edit.textChanged.connect(self.on_output_path_changed)
        output_layout.addWidget(self._output_path_edit)

        self._output_select_button = QtWidgets.QPushButton(_('Seleccionar'), self)
        self._output_select_button.pressed.connect(self.on_output_select_clicked)
        output_layout.addWidget(self._output_select_button)

        layout.addLayout(output_layout)

        self._overview_webview = QtWebEngineWidgets.QWebEngineView(self)
        self._overview_webview.page().setBackgroundColor(QtCore.Qt.transparent)
        layout.addWidget(self._overview_webview)

        self.setLayout(layout)

    def isComplete(self) -> bool:
        filepath = self._output_path_edit.text()
        return exists(dirname(filepath)) and filepath.lower().endswith('.rec')

    @property
    def json(self) -> str:
        return self._output_path_edit.text()

    def initializePage(self):
        workspace = self.parent().parent().parent().parent()
        self._overview_webview.setHtml(workspace.html_overview)

    def on_output_path_changed(self):
        self.completeChanged.emit()

    def on_output_select_clicked(self):
        workspace = self.parent().parent().parent().parent()
        subject = workspace.subject
        output = QtWidgets.QFileDialog.getSaveFileName(
            self,
            _('Seleccione fichero de salida'),
            join(settings.gui.records_path, subject.code),
            filter=_('Archivo de SaccRec (*.rec)')
        )
        filepath = output[0]
        if not filepath.lower().endswith('.rec'):
            filepath += '.rec'

        self._output_path_edit.setText(filepath)
        workspace.filepath = filepath
        self.completeChanged.emit()


class RecordSetupWizard(QtWidgets.QWizard):
    finished = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(RecordSetupWizard, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(_('Configuración de nuevo registro'))
        self.setWizardStyle(QtWidgets.QWizard.ClassicStyle)
        self.resize(640, 480)

        self._subject_page = SubjectWizardPage(self)
        self._stimulus_page = StimulusWizardPage(self)
        self._output_page = OutputWizardPage(self)

        self.addPage(self._subject_page)
        self.addPage(self._stimulus_page)
        self.addPage(self._output_page)

        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.finish_wizard)

    def finish_wizard(self):
        self._stimulus_page.save()
        self.finished.emit()

    @property
    def subject(self):
        return self.parent().subject

    @property
    def protocol(self):
        return self.parent().protocol
