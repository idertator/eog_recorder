from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
import sys
import time
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class SignalsWindow(QMainWindow):

    def __init__(self, parent=None):

        QMainWindow.__init__(self,parent)
        self.parent = parent

        title = "Signals"
        top = 400
        left = 400
        width = 900
        height = 500

        self.setWindowTitle(title)
        self.setGeometry(top,left,width,height)

        self.MyUI()
    
    def MyUI(self):

        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)

        layout = QtWidgets.QVBoxLayout(self._main)

        signals = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(signals)

        self._dynamic_ax = signals.figure.subplots()
        self._timer = signals.new_timer(
            100, [(self._update_signals, (), {})])
        self._timer.start()

    def _update_signals(self):
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._dynamic_ax.figure.canvas.draw()