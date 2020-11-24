from os.path import join

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import qApp, QMainWindow, QAction, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon

from saccrec import settings

import saccrec.gui.icons  # noqa: F401

from .about import AboutDialog
from .runner import Runner
from .settings import SettingsDialog
from .workspace import Workspace


class MainWindow(
    Runner,
    Workspace,
    QMainWindow
):

    def __init__(self):
        QMainWindow.__init__(self)
        Workspace.__init__(self)
        Runner.__init__(self)

        self._new_record_wizard = None

        self._about_dialog = AboutDialog()
        self._settings_dialog = SettingsDialog(self)

        # self._runner.stopped.connect(self.on_runner_stopped)
        # self._runner.finished.connect(self.on_runner_finished)

        self.setup_ui()

    def setup_ui(self):
        # Setting up top level menus
        menubar = self.menuBar()

        file_menu = menubar.addMenu(_('&Estudio'))
        help_menu = menubar.addMenu(_('&Ayuda'))

        # Setting up actions
        self._new_action = QAction(QIcon(':document.svg'), _('&Iniciar Prueba'), self)
        self._new_action.triggered.connect(self.on_new_test_wizard_clicked)

        self._exit_action = QAction(QIcon(':exit.svg'), _('&Salir'), self)
        self._exit_action.setShortcut('Ctrl+Q')
        self._exit_action.setStatusTip(_('Salir de la aplicación'))
        self._exit_action.triggered.connect(qApp.quit)

        self._settings_action = QAction(QIcon(':settings.svg'), _('&Configuración'), self)
        self._settings_action.setShortcut('Ctrl+P')
        self._settings_action.setStatusTip(_('Configurar aplicación'))
        self._settings_action.triggered.connect(self.open_settings_dialog)

        self._stop_action = QAction(QIcon(':stop-solid.svg'), _('&Detener'), self)
        self._stop_action.setShortcut('Ctrl+D')
        self._stop_action.setStatusTip(_('Detener grabación'))
        self._stop_action.triggered.connect(self._on_stop_clicked)

        self._about_action = QAction(QIcon(':help.svg'), _('&Acerca de ...'), self)
        self._about_action.triggered.connect(self.on_about_dialog_clicked)

        help_menu.addAction(self._about_action)

        # Setting up top menu
        file_menu.addAction(self._new_action)
        file_menu.addAction(self._settings_action)

        file_menu.addSeparator()

        file_menu.addAction(self._exit_action)

        # Setting up top toolbar
        main_toolbar = self.addToolBar('Main Toolbar')
        main_toolbar.addAction(self._new_action)
        main_toolbar.addAction(self._settings_action)
        main_toolbar.addSeparator()
        main_toolbar.addAction(self._stop_action)
        main_toolbar.addSeparator()
        main_toolbar.addAction(self._exit_action)

        # Setting up window
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('SaccRec')
        self.setWindowIcon(QIcon(':app.png'))

        self._setup_gui_for_non_recording()

        self.show()

    def _setup_gui_for_recording(self):
        self._new_action.setEnabled(False)
        self._exit_action.setEnabled(False)
        self._settings_action.setEnabled(False)
        self._about_action.setEnabled(False)

        self._stop_action.setEnabled(True)

    def _setup_gui_for_non_recording(self):
        self._new_action.setEnabled(True)
        self._exit_action.setEnabled(True)
        self._settings_action.setEnabled(True)
        self._about_action.setEnabled(True)

        self._stop_action.setEnabled(False)

    def on_new_test_wizard_clicked(self):
        if self._new_record_wizard is None:
            from .wizards import RecordSetupWizard

            self._new_record_wizard = RecordSetupWizard(parent=self)
            self._new_record_wizard.finished.connect(self.on_new_test_wizard_finished)

        self._new_record_wizard.show()

    def on_new_test_wizard_finished(self):
        self._new_action.setEnabled(False)
        self._settings_action.setEnabled(False)

        self.start()

        # self._runner.run(
        #     stimulus=wizard.stimulus,
        #     output=wizard.output_path,
        #     distance_to_subject=wizard.fixed_distance_to_subject,
        #     tests=wizard.tests
        # )

    def open_settings_dialog(self):
        self._settings_dialog.open()

    # def on_runner_stopped(self):
    #     self._new_action.setEnabled(True)
    #     self._settings_action.setEnabled(True)

    # def on_runner_finished(self):
    #     report = QMessageBox.question(
    #         self,
    #         _('Opción'),
    #         _('¿Desea generar un reporte sacádico?'),
    #         QMessageBox.Yes | QMessageBox.No
    #     )

    #     if report == QMessageBox.Yes:
    #         output = QFileDialog.getSaveFileName(
    #             self,
    #             _('Seleccione fichero de salida'),
    #             join(settings.gui.records_path, self.subject.code),
    #             filter='Microsoft Excel (*.xls)'
    #         )
    #         filepath = output[0]
    #         if not filepath.lower().endswith('.xls'):
    #             filepath += '.xls'

    #         if filepath:
    #             from saccrec.core import Study
    #             from saccrec.core.reports import excel_saccadic_report

    #             study = Study.open(self._new_record_wizard.output_path)
    #             excel_saccadic_report(study, filepath)

    #     self._new_action.setEnabled(True)
    #     self._settings_action.setEnabled(True)

    def on_about_dialog_clicked(self):
        self._about_dialog.open()

    def _on_stop_clicked(self):
        answer = QtWidgets.QMessageBox.critical(
            self,
            _('Confirmación de interrupción de prueba'),
            _('Está seguro que desea detener la prueba'),
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.No
        )
        if answer == QtWidgets.QMessageBox.Ok:
            self.stop()
