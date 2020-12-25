from PySide6 import QtCore, QtWidgets, QtSvgWidgets

from saccrec.core.templating import render


class AboutDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent=parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(_('About DIATAX ...'))
        self.setFixedSize(640, 350)

        self._diatax_logo = QtSvgWidgets.QSvgWidget(':diatax.svg')
        self._eyestracker_logo = QtSvgWidgets.QSvgWidget(':eyestracker.svg')

        self._webview = QtWidgets.QTextBrowser(self)
        self._webview.viewport().setAutoFillBackground(False)
        self._webview.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self._webview.setHtml(render('about'))
        # self._webview.setFixedHeight(200)

        self._diatax_layout = QtWidgets.QHBoxLayout()
        self._diatax_layout.addStretch()
        self._diatax_layout.addWidget(self._diatax_logo)
        self._diatax_layout.addStretch()

        self._eyestracker_layout = QtWidgets.QHBoxLayout()
        self._eyestracker_layout.addStretch()
        self._eyestracker_layout.addWidget(self._eyestracker_logo)
        self._eyestracker_layout.addStretch()

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addLayout(self._eyestracker_layout)
        self._layout.addWidget(self._webview)
        self._layout.addLayout(self._diatax_layout)

        self.setLayout(self._layout)
