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
