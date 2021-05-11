from datetime import datetime
from os.path import join, exists, dirname

from PySide6 import QtCore, QtWidgets

from eoglib.models import Subject, Protocol

from saccrec import settings
from saccrec.core.templating import render


class OutputWizardPage(QtWidgets.QWizardPage):
    outputPathChanged = QtCore.Signal(str)
    lightIntensityChanged = QtCore.Signal(int)

    def __init__(self, subject: Subject, protocol: Protocol, parent=None):
        super(OutputWizardPage, self).__init__(parent=parent)

        self._subject = subject
        self._protocol = protocol
        self._output_path = ''

        self.setTitle(_('Output Setup'))

        self._light_intensity_label = QtWidgets.QLabel(_('Light Intensity'))

        self._light_intensity_spinner = QtWidgets.QSpinBox()
        self._light_intensity_spinner.setRange(0, 200)
        self._light_intensity_spinner.setSuffix(' lux')
        self._light_intensity_spinner.setSingleStep(1)
        self._light_intensity_spinner.setValue(0)
        self._light_intensity_spinner.setFocusPolicy(QtCore.Qt.StrongFocus)
        self._light_intensity_spinner.valueChanged.connect(self._on_light_intensity_changed)

        self._output_path_edit = QtWidgets.QLineEdit(self)
        self._output_path_edit.textChanged.connect(self._on_output_path_changed)

        self._output_select_button = QtWidgets.QPushButton(_('Select'), self)
        self._output_select_button.pressed.connect(self._on_output_select_clicked)

        self._overview_webview = QtWidgets.QTextBrowser(self)
        self._overview_webview.viewport().setAutoFillBackground(False)
        self._overview_webview.setFrameStyle(QtWidgets.QFrame.NoFrame)

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self._light_intensity_label)
        top_layout.addWidget(self._light_intensity_spinner)
        top_layout.addWidget(self._output_path_edit)
        top_layout.addWidget(self._output_select_button)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self._overview_webview)

        self.setLayout(layout)

    def isComplete(self) -> bool:
        filepath = self._output_path_edit.text()
        return exists(dirname(filepath)) and filepath.lower().endswith('.eog')

    def setProtocol(self, protocol: Protocol):
        self._protocol = protocol

    def initializePage(self):
        filename = self._subject.initials + datetime.now().strftime('%d%m%Y%H%M') + '.eog'
        self._output_path = join(settings.gui.records_path, filename)
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

    def _on_light_intensity_changed(self, value: int):
        self.lightIntensityChanged.emit(value)

    def _on_output_select_clicked(self):
        output = QtWidgets.QFileDialog.getSaveFileName(
            self,
            _('Select Output File'),
            self._output_path,
            filter=_('SaccRec File (*.eog)')
        )
        filepath = output[0]
        if not filepath.lower().endswith('.eog'):
            filepath += '.eog'

        self._output_path = filepath
        self._output_path_edit.setText(filepath)
