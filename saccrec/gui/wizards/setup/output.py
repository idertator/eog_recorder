from os.path import dirname, exists, join

from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets

from saccrec import settings
from saccrec.core import workspace


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
        self._overview_webview.setHtml(workspace.html_overview)

    def on_output_path_changed(self):
        self.completeChanged.emit()

    def on_output_select_clicked(self):
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
        self.completeChanged.emit()
