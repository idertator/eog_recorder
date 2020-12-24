from os.path import join, exists, dirname

from PySide6 import QtCore, QtWidgets

from eoglib.models import Subject, Protocol

from saccrec import settings
from saccrec.core.templating import render


class OutputWizardPage(QtWidgets.QWizardPage):
    outputPathChanged = QtCore.Signal(str)

    def __init__(self, subject: Subject, protocol: Protocol, parent=None):
        super(OutputWizardPage, self).__init__(parent=parent)

        self._subject = subject
        self._protocol = protocol
        self._output_path = ''

        self.setTitle(_('Output Setup'))

        self._output_path_edit = QtWidgets.QLineEdit(self)
        self._output_path_edit.textChanged.connect(self._on_output_path_changed)

        self._output_select_button = QtWidgets.QPushButton(_('Select'), self)
        self._output_select_button.pressed.connect(self._on_output_select_clicked)

        self._overview_webview = QtWidgets.QTextBrowser(self)
        self._overview_webview.viewport().setAutoFillBackground(False)
        self._overview_webview.setFrameStyle(QtWidgets.QFrame.NoFrame)

        output_layout = QtWidgets.QHBoxLayout()
        output_layout.addWidget(self._output_path_edit)
        output_layout.addWidget(self._output_select_button)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(output_layout)
        layout.addWidget(self._overview_webview)

        self.setLayout(layout)

    def isComplete(self) -> bool:
        filepath = self._output_path_edit.text()
        return exists(dirname(filepath)) and filepath.lower().endswith('.rec')

    def initializePage(self):
        self._output_path = join(settings.gui.records_path, self._subject.code) + '.rec'
        self._output_path_edit.setText(self._output_path)

        html = render(
            'overview',
            subject=self._subject,
            protocol=self._protocol,
            distance=self._protocol.distance_to_subject(settings.stimuli.saccadic_distance)
        )
        self._overview_webview.setHtml(html)

    def _on_output_path_changed(self):
        self.completeChanged.emit()
        self.outputPathChanged.emit(self._output_path)

    def _on_output_select_clicked(self):
        output = QtWidgets.QFileDialog.getSaveFileName(
            self,
            _('Select Output File'),
            self._output_path,
            filter=_('SaccRec File (*.rec)')
        )
        filepath = output[0]
        if not filepath.lower().endswith('.rec'):
            filepath += '.rec'

        self._output_path = filepath
        self._output_path_edit.setText(filepath)
