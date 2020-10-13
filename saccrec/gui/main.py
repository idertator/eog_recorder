from os.path import join

from PyQt5.QtWidgets import qApp, QMainWindow, QAction, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon

from saccrec import settings

import saccrec.gui.icons  # noqa: F401

from .about import AboutDialog
from .player import StimulusPlayerWidget
from .runner import Runner
from .settings import SettingsDialog
from .signals import SignalsWidget
from .wizards import RecordSetupWizard


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self._signals_widget = SignalsWidget(self)
        self._signals_widget.setVisible(False)

        self._new_record_wizard = RecordSetupWizard(parent=self)
        self._new_record_wizard.finished.connect(self.on_new_test_wizard_finished)

        self._settings_dialog = SettingsDialog(self)
        self._about_dialog = None
        self._stimulus_player = StimulusPlayerWidget(None)

        self._runner = Runner(
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

        file_menu = menubar.addMenu(_('&Estudio'))
        help_menu = menubar.addMenu(_('&Ayuda'))

        # Setting up actions
        self._new_action = QAction(QIcon(':document.svg'), _('&Iniciar Prueba'), self)
        self._new_action.triggered.connect(self.on_new_test_wizard_clicked)

        exit_action = QAction(QIcon(':exit.svg'), _('&Salir'), self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip(_('Salir de la aplicación'))
        exit_action.triggered.connect(qApp.quit)

        self._settings_action = QAction(QIcon(':settings.svg'), _('&Configuración'), self)
        self._settings_action.setShortcut('Ctrl+P')
        self._settings_action.setStatusTip(_('Configurar aplicación'))
        self._settings_action.triggered.connect(self.open_settings_dialog)

        self._about_action = QAction(QIcon(':help.svg'), _('&Acerca de ...'), self)
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
        self.setWindowTitle('SaccRec')
        self.setWindowIcon(QIcon(':app.png'))

        self.setCentralWidget(self._signals_widget)

        self.show()

    def on_new_test_wizard_clicked(self):
        self._new_record_wizard.show()

    def on_new_test_wizard_finished(self):
        self._new_action.setEnabled(False)
        self._settings_action.setEnabled(False)

        wizard = self._new_record_wizard

        self._runner.run(
            subject=wizard.subject,
            stimulus=wizard.stimulus,
            output=wizard.output_path,
            distance_to_subject=wizard.fixed_distance_to_subject,
            tests=wizard.tests
        )

        # self._runner.run(**self._new_record_wizard.json)

    def open_settings_dialog(self):
        self._settings_dialog.open()

    def on_runner_stopped(self):
        self._new_action.setEnabled(True)
        self._settings_action.setEnabled(True)

    def on_runner_finished(self):
        report = QMessageBox.question(
            self,
            _('Opción'),
            _('¿Desea generar un reporte sacádico?'),
            QMessageBox.Yes | QMessageBox.No
        )

        if report == QMessageBox.Yes:
            output = QFileDialog.getSaveFileName(
                self,
                _('Seleccione fichero de salida'),
                join(settings.gui.records_path, self._new_record_wizard.subject_page.subject_code),
                filter='Microsoft Excel (*.xls)'
            )
            filepath = output[0]
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
