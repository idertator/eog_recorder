from os.path import join

from eoglib.models import Protocol, StimulusPosition, Subject
from PySide6 import QtCore, QtGui, QtWidgets

from saccrec import settings
from saccrec.core.formats import create_study
from saccrec.gui import icons  # noqa: F401
from saccrec.gui.dialogs import AboutDialog, SettingsDialog, SDCardImport
from saccrec.gui.widgets import SignalsWidget, StimulusPlayer
from saccrec.gui.wizards import RecordSetupWizard
from saccrec.recording import CytonBoard


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        # Local State
        self._current_test = None

        self._subject: Subject = None
        self._protocol: Protocol = None
        self._output_path: str = ''
        self._light_intensity: int = 0
        self._filenames: list[str] = []
        self._studies: list[str] = []

        self._board: CytonBoard = None
        self._corrupt_packets = 0

        # Related Widgets
        self._new_record_wizard: RecordSetupWizard = None
        self._sd_import_dialog: SDCardImport = None
        self._about_dialog: AboutDialog = None
        self._settings_dialog = SettingsDialog(self)

        # Local Widgets
        self._signals_widget = SignalsWidget(self)
        self._signals_widget.setVisible(False)
        self.setCentralWidget(self._signals_widget)

        self._stimulus_player = StimulusPlayer(self)
        self._stimulus_player.started.connect(self._on_test_started)
        self._stimulus_player.stopped.connect(self._on_test_stopped)
        self._stimulus_player.finished.connect(self._on_test_finished)
        self._stimulus_player.moved.connect(self._on_stimulus_moved)
        self._stimulus_player.refreshed.connect(self._on_stimulus_refreshed)

        # Setting up top level menus
        menubar = self.menuBar()

        file_menu = menubar.addMenu(_('&Study'))
        help_menu = menubar.addMenu(_('&Help'))

        # Setting up actions
        self._new_action = QtGui.QAction(QtGui.QIcon(':/actions/file.svg'), _('&New Recording'), self)
        self._new_action.triggered.connect(self._on_new_action_clicked)

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

        self.show()

        # Check for OpenBCI Connection
        ports = CytonBoard.list_ports()
        if not ports:
            self._new_action.setEnabled(False)
            QtWidgets.QMessageBox.critical(
                self,
                _('OpenBCI Cyton Not Detected'),
                _('Please connect the recording device and restart this application')
            )

        if settings.hardware.port in {'None', None}:
            settings.hardware.port = ports[0]

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

            self._current_test = None
            self._stimulus_player.close()

    # ======================================
    #        App Flow Event Handlers
    # ======================================

    def _on_wizard_finished(self, record_setup: dict):
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
        self._filenames = []
        self._board = CytonBoard(
            port=settings.hardware.port,
            sampling_rate=settings.hardware.sampling_rate,
            channels='12',
            use_sd=True
        )
        self._board.initialize()

        self._current_test = 0
        stimulus = self._protocol[0]
        saccadic_distance = settings.stimuli.saccadic_distance
        distance_to_subject = self._protocol.distance_to_subject(saccadic_distance)
        self._stimulus_player.start(stimulus, distance_to_subject)

    def _on_test_started(self, timestamp):
        sd_filename = self._board.create_sd_file()
        self._board.start()
        self._board.marker(StimulusPosition.Center.value)
        self._filenames.append(sd_filename)

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
            self._setup_gui_for_non_recording()

            self._current_test = 0
            self._stimulus_player.close()

            if (study := create_study(
                subject=self._subject,
                protocol=self._protocol,
                light_intensity=self._light_intensity,
                output_path=self.output_path,
                filenames=self.filenames
            )) is not None:
                QtWidgets.QMessageBox.information(
                    self,
                    _('Success'),
                    _('Your study was successfully writed to {path}').format(
                        path=output_path
                    )
                )

    def _on_stimulus_moved(self, value: int):
        self._board.marker(value)

    def _on_stimulus_refreshed(self):
        try:
            all_samples = self._board.read()
            if all_samples:
                samples = [
                    (sample[0], sample[1], sample[8])
                    for sample in all_samples
                ]
                self._signals_widget.add_samples(samples)
        except ValueError:
            self._corrupt_packets += 1
