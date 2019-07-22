import sys

from PyQt5.QtWidgets import qApp, QMainWindow, QAction, QApplication, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings

from saccrec.gui.create import RecordSetupWizard
from saccrec.gui.ConfigWindow import ConfigWindow
from saccrec.core.Settings import Settings
from saccrec.core.Test import Test

from saccrec.gui.StimulatorWindow import StimulatorWindow
from saccrec.gui.SignalsWidget import SignalsWidget

import saccrec.gui.icons


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.test = Test()
        self.settings = Settings(self)

        self.signals_widget = SignalsWidget(self)

        self._newTest = RecordSetupWizard(parent=self)
        self._configWindow = ConfigWindow(parent=self)

        self._calibrationWindow1 = StimulatorWindow('1', self)
        self._testStimulator = StimulatorWindow('2', self)
        self._calibrationWindow2 = StimulatorWindow('3', self)

        self.initUI()

    def initUI(self):
        # Setting up top level menus
        menubar = self.menuBar()

        file_menu = menubar.addMenu('&Estudio')
        help_menu = menubar.addMenu('&Ayuda')

        # Setting up actions
        new_action = QAction(QIcon(':document.svg'), '&Iniciar Prueba', self)
        new_action.triggered.connect(self.open_new_test_wizard)

        exit_action = QAction(QIcon(':exit.svg'), '&Salir', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Salir de la aplicación')
        exit_action.triggered.connect(qApp.quit)

        settings_action = QAction(QIcon(':settings.svg'), '&Configuración', self)
        settings_action.setShortcut('Ctrl+P')
        settings_action.setStatusTip('Configurar aplicación')
        settings_action.triggered.connect(self.open_settings_dialog)

        about_action = QAction(QIcon(':help.svg'), '&Acerca de ...', self)

        help_menu.addAction(about_action)

        # Setting up top menu
        file_menu.addAction(new_action)
        file_menu.addAction(new_action)
        file_menu.addAction(settings_action)

        file_menu.addSeparator()

        file_menu.addAction(exit_action)

        # Setting up top toolbar
        main_toolbar = self.addToolBar('Main Toolbar')
        main_toolbar.addAction(new_action)
        main_toolbar.addAction(settings_action)

        main_toolbar.addSeparator()

        main_toolbar.addAction(exit_action)

        # Setting up window
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('EyeTracker OpenBCI')

        self.setCentralWidget(self.signals_widget)

        self.show()

    def open_new_test_wizard(self):
        self._newTest.show()

    def open_settings_dialog(self):
        self._configWindow.open()
