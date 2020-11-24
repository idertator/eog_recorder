from .player import StimulusPlayer
from .signals import SignalsWidget


class Runner:

    def __init__(self):
        self._is_running = False

        self._signals_widget = SignalsWidget(self)
        self._signals_widget.setVisible(False)
        self.setCentralWidget(self._signals_widget)

        self._stimulus_player = StimulusPlayer(self)
        self._stimulus_player.started.connect(self._on_test_started)
        self._stimulus_player.stopped.connect(self._on_test_stopped)
        self._stimulus_player.finished.connect(self._on_test_finished)
        self._stimulus_player.moved.connect(self._on_test_moved)

        self._current_test = None

    def start(self):
        self._setup_gui_for_recording()

        self._current_test = 0
        stimulus = self.protocol[0]
        self._stimulus_player.start(stimulus)
        self._is_running = True

    def stop(self):
        self._setup_gui_for_non_recording()

        self._current_test = None
        self._is_running = False
        self._stimulus_player.close()
        self.reset_workspace()

    def finish(self):
        self._setup_gui_for_non_recording()

        self._current_test = 0
        self._is_running = False
        self._stimulus_player.close()

    def _on_test_started(self, timestamp):
        pass

    def _on_test_stopped(self):
        self._current_test = 0
        self._is_running = False
        self._stimulus_player.close()

    def _on_test_finished(self):
        self._current_test += 1
        if self._current_test < len(self.protocol):
            stimulus = self.protocol[self._current_test]
            self._stimulus_player.start(stimulus)
        else:
            self.finish()

    def _on_test_moved(self, value: int):
        pass


# from PyQt5.QtCore import pyqtSignal, QObject

# from saccrec.core import Record
# from saccrec.core.study import Hardware, Subject
# from saccrec.engine.recording import OpenBCIRecorder
# from saccrec.engine.stimulus import SaccadicStimuli
# from saccrec import settings

# from .player import StimulusPlayer
# from .signals import SignalsWidget


# class Runner(QObject):
#     started = pyqtSignal()
#     stopped = pyqtSignal()
#     finished = pyqtSignal()

#     def __init__(
#         self,
#         player: StimulusPlayer,
#         signals: SignalsWidget,
#         parent=None
#     ):
#         super(Runner, self).__init__(parent=parent)
#         self._player = player
#         self._signals = signals

#         self._recorder = OpenBCIRecorder(
#             port=settings.hardware.port,
#             sampling_rate=settings.hardware.sampling_rate
#         )

#         self._tests_stimuli = None
#         self._current_test = None

#         self._stimulus = None
#         self._output = None
#         self._distance_to_subject = None
#         self._tests_stimuli: list[SaccadicStimuli] = None
#         self._record = None

#         self._player.started.connect(self.on_player_started)
#         self._player.stopped.connect(self.on_player_stopped)
#         self._player.finished.connect(self.on_player_finished)
#         self._player.moved.connect(self.on_player_moved)

#     def run(
#         self,
#         stimulus: dict,
#         output: str,
#         distance_to_subject: float,
#         tests_stimuli: list[SaccadicStimuli],
#         **kwargs
#     ):
#         self._stimulus = stimulus
#         self._output = output
#         self._distance_to_subject = distance_to_subject
#         self._tests_stimuli = tests_stimuli

#         self._record = Record(
#             subject=self.parent().subject,
#             hardware=Hardware(
#                 sample_rate=settings.hardware.sampling_rate,
#                 channels=settings.hardware.channels.json
#             )
#         )

#         if not self._recorder.is_alive():
#             self._recorder.start()
#             self._recorder.wait_until_ready()

#         if not self._signals.isVisible():
#             self._signals.show()

#         tests_stimuli = self._tests_stimuli
#         self._current_test = 0
#         self._current_sd_file = None

#         self._signals.hide()
#         self._start_test()

#         self._player.showFullScreen()
#         self.started.emit()

#     def _start_test(self):
#         stimuli: SaccadicStimuli = self._tests_stimuli[self._current_test]

#         self._player.run_stimulus(
#             stimuli,
#             '\n'.join([str(stimuli), _('Presione espacio para continuar')])
#         )

#         self._player.move(
#             settings.screen.secondary_screen_rect.left(),
#             settings.screen.secondary_screen_rect.top()
#         )

#     def on_player_started(self):
#         if not self._signals.is_rendering:
#             self._signals.start(self._recorder)     # TODO: Change this to adding samples from here

#         self._current_sd_file = self._recorder.start_recording()
#         print(self._current_sd_file)  # TODO: Remove this later

#     def on_player_stopped(self):
#         self._signals.stop()
#         self._recorder.stop_recording()
#         self._recorder.close_recorder()

#         self.stopped.emit()

#     def on_player_finished(self):
#         self._signals.stop()
#         self._recorder.stop_recording()

#         current_stimulus = self._tests_stimuli[self._current_test]
#         self._record.add_test(
#             filename=self._current_sd_file,
#             angle=current_stimulus.angle,
#             fixation_duration=current_stimulus.fixation_duration,
#             fixation_variability=current_stimulus.fixation_variability,
#             saccades_count=current_stimulus.saccades_count,
#             test_name=current_stimulus.test_name
#         )

#         if self._current_test < len(self._tests_stimuli) - 1:
#             stimuli = self._tests_stimuli[self._current_test]
#             self._current_test += 1

#             self._player.run_stimulus(
#                 stimuli,
#                 '\n'.join([str(stimuli), _('Presione espacio para continuar')])
#             )
#         else:
#             self._player.close_player()
#             self._record.save(self._output)
#             self.finished.emit()

#     def on_player_moved(self, position: int):
#         self._recorder.put_marker(position)
