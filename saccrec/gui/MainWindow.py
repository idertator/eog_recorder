import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings

from qwt import tests

from saccrec.gui.TestWindow import MagicWizard
from saccrec.gui.ConfigWindow import ConfigWindow
from saccrec.core.Settings import Settings
from saccrec.core.Test import Test
from .Signals import SignalsWindow

from saccrec.gui.StimulatorWindow import StimulatorWindow

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

        self.test = Test()
        self.settings = Settings(self)

        self._newTest = MagicWizard(parent=self)
        self._configWindow = ConfigWindow(parent=self)
        self._signalsWindow = SignalsWindow(self)

        self._calibrationWindow1 = StimulatorWindow(parent=self, tipo='1')
        self._testStimulator = StimulatorWindow(parent=self, tipo='2')
        self._calibrationWindow2 = StimulatorWindow(parent=self, tipo='3')

    def newMenu(self, nombre):
        menubar = self.menuBar()
        menu = menubar.addMenu(nombre)
        return menu

    def initUI(self):
        exitAct = QAction(QIcon('saccrec/gui/images/exit.svg'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        signalsAct = QAction('Signals',self)
        signalsAct.triggered.connect(self.openSignalsWindow)

        testAct = QAction('Nuevo Test', self)
        testAct.triggered.connect(self.openNewTest)

        configAct = QAction('Configuracion', self)
        configAct.triggered.connect(self.openConfigWindow)

        aboutUs = QAction(QIcon('saccrec/gui/images/interrogacion.png'), '&About Us', self)

        self.statusBar()

        fileMenu = self.newMenu('&File')
        fileMenu.addAction(testAct)
        fileMenu.addAction(configAct)
        # fileMenu.addAction(signalsAct)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)

        helpMenu = self.newMenu('&Help')
        helpMenu.addAction(aboutUs)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('EyeTracker OpenBCI')
        self.show()

    def openNewTest(self):
        self._newTest.show()

    def openConfigWindow(self):
        self._configWindow.open()

    def openSignalsWindow(self):
        self._signalsWindow.show()
