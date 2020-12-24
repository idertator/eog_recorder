from PySide6 import QtCore, QtWidgets

from saccrec.core.templating import render


class AboutDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent=parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(_('About DIATAX ...'))
        self.setFixedWidth(640)
        self.setFixedHeight(400)

        self._webview = QtWidgets.QTextBrowser(self)
        self._webview.viewport().setAutoFillBackground(False)
        self._webview.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self._webview.setHtml(render('about'))

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addWidget(self._webview)

        self.setLayout(self._layout)
