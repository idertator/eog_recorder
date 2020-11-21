from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets

from saccrec.core.templating import render


class AboutDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent=parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(_('Acerca de DIATAX ...'))
        self.setFixedWidth(640)
        self.setFixedHeight(400)

        self._webview = QtWebEngineWidgets.QWebEngineView(self)
        self._webview.page().setBackgroundColor(QtCore.Qt.transparent)
        self._webview.setHtml(render('about'))

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addWidget(self._webview)

        self.setLayout(self._layout)
