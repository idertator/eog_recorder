import sys

from PyQt5.QtWidgets import qApp, QMainWindow, QAction, QApplication, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings

from saccrec import Manager
from saccrec.core import Settings, Screen

from saccrec.gui.dialogs import SettingsDialog
from saccrec.gui.widgets import SignalsWidget, StimulusPlayerWidget
from saccrec.gui.wizards import RecordSetupWizard

import saccrec.gui.icons


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self._settings = Settings(self)
        self._screen = Screen(self)

        self._manager = Manager(
            settings=self._settings,
            screen=self._screen,
            parent=self
        )
        self._manager.recordingStarted.connect(self.on_recording_started)
        self._manager.recordingStopped.connect(self.on_recording_stopped)
        self._manager.recordingFinished.connect(self.on_recording_finished)

        self.signals_widget = SignalsWidget(self)

        self._new_record_wizard = RecordSetupWizard(self)
        self._new_record_wizard.finished.connect(self.on_new_test_wizard_finished)

        self._settings_dialog = SettingsDialog(self._settings, self)
        self._stimulus_player = StimulusPlayerWidget(self._settings, None)

        self.initUI()

    def initUI(self):
        # Setting up top level menus
        menubar = self.menuBar()

        file_menu = menubar.addMenu('&Estudio')
        help_menu = menubar.addMenu('&Ayuda')

        # Setting up actions
        self._new_action = QAction(QIcon(':document.svg'), '&Iniciar Prueba', self)
        self._new_action.triggered.connect(self.on_new_test_wizard_clicked)

        exit_action = QAction(QIcon(':exit.svg'), '&Salir', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Salir de la aplicación')
        exit_action.triggered.connect(qApp.quit)

        self._settings_action = QAction(QIcon(':settings.svg'), '&Configuración', self)
        self._settings_action.setShortcut('Ctrl+P')
        self._settings_action.setStatusTip('Configurar aplicación')
        self._settings_action.triggered.connect(self.open_settings_dialog)

        about_action = QAction(QIcon(':help.svg'), '&Acerca de ...', self)

        help_menu.addAction(about_action)

        # Setting up top menu
        file_menu.addAction(self._new_action)
        file_menu.addAction(self._new_action)
        file_menu.addAction(self._settings_action)

        file_menu.addSeparator()

        file_menu.addAction(exit_action)

        # Setting up top toolbar
        main_toolbar = self.addToolBar('Main Toolbar')
        main_toolbar.addAction(self._new_action)
        main_toolbar.addAction(self._settings_action)

        main_toolbar.addSeparator()

        main_toolbar.addAction(exit_action)

        # Setting up window
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('EyeTracker OpenBCI')

        self.setCentralWidget(self.signals_widget)

        self.show()

    def on_new_test_wizard_clicked(self):
        self._new_record_wizard.show()

    def on_new_test_wizard_finished(self):
        self._manager.start_recording(**self._new_record_wizard.json)

    def open_settings_dialog(self):
        self._settings_dialog.open()

    def on_recording_started(self):
        self._new_action.setEnabled(False)
        self._settings_action.setEnabled(False)

        self._stimulus_player.move(
            self._screen.secondary_screen_rect.left(), 
            self._screen.secondary_screen_rect.top()
        )
        self._stimulus_player.showFullScreen()
        
        stimuli = self._manager.current_stimuli
        self._stimulus_player.run_stimulus(
            stimuli, 
            '\n'.join([str(stimuli), 'Presione espacio para continuar'])
        )

    def on_recording_stopped(self):
        self._new_action.setEnabled(True)
        self._settings_action.setEnabled(True)

    def on_recording_finished(self):
        self._new_action.setEnabled(True)
        self._settings_action.setEnabled(True)
