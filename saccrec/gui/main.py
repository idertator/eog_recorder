import sys

from PyQt5.QtWidgets import qApp, QMainWindow, QAction, QApplication, QDialog, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings

from saccrec.core import Settings, Screen

from saccrec.gui.dialogs import SettingsDialog, AboutDialog
from saccrec.gui.widgets import SignalsWidget, StimulusPlayerWidget
from saccrec.gui.wizards import RecordSetupWizard

import saccrec.gui.icons

from .runner import Runner


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self._settings = Settings(self)
        self._screen = Screen(self)

        self._signals_widget = SignalsWidget(self)
        self._signals_widget.setVisible(False)

        self._new_record_wizard = RecordSetupWizard(
            settings=self._settings,
            screen=self._screen,
            parent=self
        )
        self._new_record_wizard.finished.connect(self.on_new_test_wizard_finished)

        self._settings_dialog = SettingsDialog(self._settings, self)
        self._about_dialog = None
        self._stimulus_player = StimulusPlayerWidget(self._settings, None)

        self._runner = Runner(
            settings=self._settings,
            screen=self._screen,
            player=self._stimulus_player,
            signals=self._signals_widget,
            parent=self
        )

        self._runner.stopped.connect(self.on_runner_stopped)
        self._runner.finished.connect(self.on_runner_finished)

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

        self._about_action = QAction(QIcon(':help.svg'), '&Acerca de ...', self)
        self._about_action.triggered.connect(self.on_about_dialog_clicked)

        help_menu.addAction(self._about_action)

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
        self.setWindowIcon(QIcon(':app.png'))

        self.setCentralWidget(self._signals_widget)

        self.show()

    def on_new_test_wizard_clicked(self):
        self._new_record_wizard.show()

    def on_new_test_wizard_finished(self):
        self._new_action.setEnabled(False)
        self._settings_action.setEnabled(False)

        self._runner.run(**self._new_record_wizard.json)

    def open_settings_dialog(self):
        self._settings_dialog.open()
        
    def on_runner_stopped(self):
        self._new_action.setEnabled(True)
        self._settings_action.setEnabled(True)

    def on_runner_finished(self):
        report = QMessageBox.question(
            self, 
            'Opción',
            '¿Desea generar un reporte sacádico?',
            QMessageBox.Yes | QMessageBox.No
        )

        if report == QMessageBox.Yes:
            filepath, _ = QFileDialog.getSaveFileName(
                self,
                'Seleccione fichero de salida',
                self._settings.output_dir + '/' + self._new_record_wizard.subject_page.subject_code,
                filter='Microsoft Excel (*.xls)'
            )
            if not filepath.lower().endswith('.xls'):
                filepath += '.xls'

            if filepath:
                from saccrec.core import Study
                from saccrec.core.reports import excel_saccadic_report

                study = Study.open(self._new_record_wizard.output_path)
                excel_saccadic_report(study, filepath)

        self._new_action.setEnabled(True)
        self._settings_action.setEnabled(True)

    def on_about_dialog_clicked(self):
        if self._about_dialog is None:
            self._about_dialog = AboutDialog(parent=self)
    
        self._about_dialog.open()
