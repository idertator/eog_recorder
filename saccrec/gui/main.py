import logging

from eoglib.models import Protocol, StimulusPosition, Subject
from numpy import array, float32
from PySide6 import QtCore, QtGui, QtWidgets

from saccrec import settings
from saccrec.core.formats import create_study
from saccrec.gui import icons  # noqa: F401
from saccrec.gui.dialogs import AboutDialog, SDCardImport, SettingsDialog
from saccrec.gui.widgets import LoggerWidget, SignalsWidget, StimulusPlayer
from saccrec.gui.wizards import RecordSetupWizard
from saccrec.recording import CytonBoard

logger = logging.getLogger('saccrec')
logger.setLevel(logging.INFO)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        # Local State
        self._current_test = 0

        self._subject: Subject = None
        self._protocol: Protocol = None
        self._output_path: str = ''
        self._light_intensity: int = 0
        self._filename: str = None
        self._studies: list[str] = []
        self._current_file = None
        self._board = None

        # Setting signals
        self._signals_widget = SignalsWidget()
        self._signals_widget.setVisible(False)

        # Setting logger
        self._logger = LoggerWidget()

        logger.addHandler(self._logger)

        # Related Widgets
        self._new_record_wizard: RecordSetupWizard = None
        self._sd_import_dialog: SDCardImport = None
        self._about_dialog: AboutDialog = None
        self._settings_dialog = SettingsDialog(self)

        # Setting Splitter
        self._splitter = QtWidgets.QSplitter()
        self._splitter.setOrientation(QtCore.Qt.Vertical)
        self._splitter.addWidget(self._signals_widget)
        self._splitter.addWidget(self._logger)
        self._splitter.setCollapsible(0, True)

        # Local Widgets
        self.setCentralWidget(self._splitter)

        self._stimulus_player = StimulusPlayer(self, self._on_read_data)
        self._stimulus_player.aboutToStart.connect(self._on_test_about_to_start)
        self._stimulus_player.started.connect(self._on_test_started)
        self._stimulus_player.stopped.connect(self._on_test_stopped)
        self._stimulus_player.finished.connect(self._on_test_finished)
        self._stimulus_player.refreshed.connect(self._on_stimulus_refreshed)

        # Setting up top level menus
        menubar = self.menuBar()

        file_menu = menubar.addMenu(_('&Study'))
        help_menu = menubar.addMenu(_('&Help'))

        # Setting up actions
        self._connect_action = QtGui.QAction(QtGui.QIcon(':/actions/plug.svg'), _('&Connect'), self)
        self._connect_action.triggered.connect(self._on_connect_clicked)

        self._new_action = QtGui.QAction(QtGui.QIcon(':/actions/file.svg'), _('&New Recording'), self)
        self._new_action.triggered.connect(self._on_new_action_clicked)
        self._new_action.setEnabled(False)

        self._import_sd_action = QtGui.QAction(QtGui.QIcon(':/actions/sd-card.svg'), _('&Import SD Data'), self)
        self._import_sd_action.triggered.connect(self._on_import_sd_action_clicked)

        self._exit_action = QtGui.QAction(QtGui.QIcon(':/actions/door-open.svg'), _('&Exit'), self)
        self._exit_action.setShortcut('Ctrl+Q')
        self._exit_action.setStatusTip(_('Exit the app'))
        self._exit_action.triggered.connect(QtWidgets.QApplication.instance().quit)

        self._settings_action = QtGui.QAction(QtGui.QIcon(':/actions/cog.svg'), _('&Settings'), self)
        self._settings_action.setShortcut('Ctrl+P')
        self._settings_action.setStatusTip(_('Configure the application'))
        self._settings_action.triggered.connect(self._on_settings_action_clicked)

        self._stop_action = QtGui.QAction(QtGui.QIcon(':/actions/stop-circle.svg'), _('&Stop'), self)
        self._stop_action.setShortcut('Ctrl+D')
        self._stop_action.setStatusTip(_('Stop recording'))
        self._stop_action.triggered.connect(self._on_stop_clicked)

        self._about_action = QtGui.QAction(QtGui.QIcon(':/actions/info-circle.svg'), _('&About ...'), self)
        self._about_action.triggered.connect(self._on_about_action_clicked)

        help_menu.addAction(self._about_action)

        # Setting up top menu
        file_menu.addAction(self._new_action)
        file_menu.addAction(self._settings_action)

        file_menu.addSeparator()

        file_menu.addAction(self._exit_action)

        # Setting up top toolbar
        main_toolbar = self.addToolBar('Main Toolbar')
        main_toolbar.addAction(self._connect_action)
        main_toolbar.addAction(self._new_action)
        main_toolbar.addAction(self._import_sd_action)
        main_toolbar.addAction(self._settings_action)
        main_toolbar.addSeparator()
        main_toolbar.addAction(self._stop_action)
        main_toolbar.addSeparator()
        main_toolbar.addAction(self._exit_action)

        # Setting up window
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('SaccRec')
        self.setWindowIcon(QtGui.QIcon(':/brand/app.png'))

        self._setup_gui_for_non_recording()

    # ======================================
    #         GUI State Management
    # ======================================

    def _setup_gui_for_recording(self):
        self._new_action.setEnabled(False)
        self._import_sd_action.setEnabled(False)
        self._exit_action.setEnabled(False)
        self._settings_action.setEnabled(False)
        self._about_action.setEnabled(False)

        self._stop_action.setEnabled(True)

    def _setup_gui_for_non_recording(self):
        self._new_action.setEnabled(True)
        self._import_sd_action.setEnabled(True)
        self._exit_action.setEnabled(True)
        self._settings_action.setEnabled(True)
        self._about_action.setEnabled(True)

        self._stop_action.setEnabled(False)

    # ======================================
    #       Actions Events Handlers
    # ======================================

    def _on_connect_clicked(self):
        self._board = CytonBoard.reset(port=settings.hardware.port)

        # Check for OpenBCI Connection
        if self._board.ready:
            self._new_action.setEnabled(True)
        else:
            self._new_action.setEnabled(False)

    def _on_new_action_clicked(self):
        if self._new_record_wizard is None:
            self._new_record_wizard = RecordSetupWizard(parent=self)
            self._new_record_wizard.finished.connect(self._on_wizard_finished)
        self._new_record_wizard.open()

    def _on_import_sd_action_clicked(self):
        if self._sd_import_dialog is None:
            self._sd_import_dialog = SDCardImport(self)
        self._sd_import_dialog.open(self._studies)
        self._studies = []

    def _on_settings_action_clicked(self):
        self._settings_dialog.open()

    def _on_about_action_clicked(self):
        if self._about_dialog is None:
            self._about_dialog = AboutDialog(self)
        self._about_dialog.open()

    def _on_stop_clicked(self):
        answer = QtWidgets.QMessageBox.critical(
            self,
            _('Test Interruption Confirmation'),
            _('Are you sure to interrupt the test?'),
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.No
        )
        if answer == QtWidgets.QMessageBox.Ok:
            self._setup_gui_for_non_recording()

            self._current_test = 0
            self._stimulus_player.close()

    # ======================================
    #        App Flow Event Handlers
    # ======================================

    def _on_wizard_finished(self, record_setup: dict):
        if self._board.ready:
            self._filename = self._board.create_sd_file()

        if self._board.ready:
            self._current_file = open(f'/tmp/{self._filename}.dat', 'wb')

            self._setup_gui_for_recording()
            self._signals_widget.setVisible(True)

            self._new_record_wizard.finished.disconnect(self._on_wizard_finished)
            self._new_record_wizard.destroy()
            self._new_record_wizard = None

            self._subject = record_setup['subject']
            self._protocol = record_setup['protocol']
            self._output_path = record_setup['output_path']
            self._light_intensity = record_setup['light_intensity']

            sampling_rate = settings.hardware.sampling_rate

            # Generating stimulus signals
            for stimulus in self._protocol:
                stimulus.generate_channel(sampling_rate)

            # Initialize Recorder
            self._current_test = 0
            stimulus = self._protocol[0]
            saccadic_distance = settings.stimuli.saccadic_distance
            distance_to_subject = self._protocol.distance_to_subject(saccadic_distance)
            self._stimulus_player.start(stimulus, distance_to_subject)

    def _on_test_about_to_start(self):
        self._signals_widget.reset_data()

        if self._board.ready:
            self._board.marker(StimulusPosition.Center.marker)

    def _on_test_started(self, timestamp):
        if self._board.ready:
            self._board.start()

    def _on_test_stopped(self):
        self._current_test = 0
        self._stimulus_player.stop()
        self._stimulus_player.close()
        self._board.stop()

    def _on_test_finished(self):
        self._current_test += 1
        self._board.stop()
        if self._current_test < len(self._protocol):
            stimulus = self._protocol[self._current_test]
            saccadic_distance = settings.stimuli.saccadic_distance
            distance_to_subject = self._protocol.distance_to_subject(saccadic_distance)
            self._stimulus_player.start(stimulus, distance_to_subject)
        else:
            if self._current_file is not None:
                self._current_file.close()
                self._current_file = None

            if self._board.ready:
                self._board.close_sd_file()

                self._setup_gui_for_non_recording()

                self._current_test = 0
                self._stimulus_player.close()

                if create_study(
                    subject=self._subject,
                    protocol=self._protocol,
                    light_intensity=self._light_intensity,
                    output_path=self._output_path,
                    source_filename=self._filename
                ) is not None:
                    self._studies.append(self._output_path)
                    QtWidgets.QMessageBox.information(
                        self,
                        _('Success'),
                        _('Your study was successfully writed to {path}').format(
                            path=self._output_path
                        )
                    )

    def _on_stimulus_refreshed(self, value: int):
        self._board.marker(StimulusPosition(value).marker)

    def _on_read_data(self):
        horizontal_list, vertical_list, position_list = [], [], []
        for index, horizontal, vertical, position in self._board.read():
            horizontal_list.append(horizontal)
            vertical_list.append(vertical)
            position_list.append({
                0x01: -1,
                0x02: 1,
                0x10: 0,
            }[position])

        horizontal = array(horizontal_list, dtype=float32)
        vertical = array(vertical_list, dtype=float32)
        positions = array(position_list, dtype=float32)

        self._signals_widget.plot(horizontal, vertical, positions)
