import subprocess
import math
from datetime import datetime
from time import time

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PyQt5.QtCore import QTimer

from saccrec.core import Settings, StimulusPosition
from saccrec.engine.stimulus import SaccadicStimuli


STIMULUS_TIMEOUT = 7    # TODO: Calculate this from the refresh rate of the monitor


class StimulusPlayerWidget(QWidget):
    
    def __init__(self, settings: Settings, parent=None):
        super(StimulusPlayerWidget, self).__init__(parent=parent)
        self._settings = settings
        self._stimuli = None
        self._ball_position = StimulusPosition.Center

        self._timer = QTimer()
        self._timer.setInterval(STIMULUS_TIMEOUT)
        self._timer.timeout.connect(self.on_timeout)

        self._start_time = 0

    def run_stimulus(self, stimuli: SaccadicStimuli):
        self._stimuli = stimuli
        self._start_time = time()
        self._ball_position = stimuli.position(0)
        # TODO: Setup ball positions
        # TODO: Start timer

    def on_timeout(self):
        elapsed = time() - self._start_time
        # TODO: Check if elapsed (time position) needs for a stimuli change


from saccrec.core.Stimulator import Stimulator
from saccrec.core.Stimulator import BallPosition


class StimulusPlayerWidget1(QWidget):
    
    def __init__(self, tipo=None, parent=None):
        super(StimulusPlayerWidget1, self).__init__()

        self.padre = parent

        self.tipo = tipo

        self.contador = 0
        self.isRight = True

        self.initUI()

        self._stimulator = Stimulator(self)
        self._ballposition = BallPosition(self.padre.test.test_duration, self.padre.test.mean_duration, self.padre.test.variation)
        self._stimulatorTimer = QTimer()
        self._stimulatorTimer.setInterval(16)
        self._stimulatorTimer.timeout.connect(self.onTimerTimeout)

        layout = QVBoxLayout()
        layout.addWidget(self._stimulator)
        
        self.setLayout(layout)
    
    @property
    def screenpixels(self):
        app = QGuiApplication.instance()
        size = app.primaryScreen().size()
        return size.width(), size.height()

    def initUI(self):
        self.resize(self.screenpixels[0], self.screenpixels[1])

    def runStimulator(self):
        self.show()
        self.initialTimeStamp = datetime.now()
        print('Initial timestamp: '+str(self.initialTimeStamp))
        self._stimulatorTimer.start()

    @property
    def stimulator(self):
        return self._stimulator

    @property
    def screensize(self):
        return self.padre.settings.screensize

    @property
    def distancePoints(self):
        return float(self.padre.settings.distanceBetweenPoints)

    
    @property
    def distanceFromPatient(self):
        if self.padre.test.stimulation_angle > 30:
            angulo_maximo = self.padre.test.stimulation_angle
        else:
            angulo_maximo = 30
        distance_from_mid = self.distancePoints / 2

        distance_from_patient = distance_from_mid * (math.sin(math.radians(90 - angulo_maximo)) / math.sin(math.radians(angulo_maximo)))

        return distance_from_patient


    @property
    def distanceFromCenter(self):
        if(self.tipo == '1' or self.tipo == '3'):
            angulo_vision = 30
        else:
            angulo_vision = self.padre.test.stimulation_angle 

        pantalla_horizontal = self.screensize[0]

        densidad_pixeles = self.screenpixels[0] / self.screensize[0]

        distance_from_mid = self.distanceFromPatient * (math.sin(math.radians(angulo_vision)) / math.sin(math.radians(90 - angulo_vision)))

        return math.floor(distance_from_mid * densidad_pixeles)


    @property
    def deltatime(self):
        difference = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f") - datetime.strptime(str(self.initialTimeStamp), "%Y-%m-%d %H:%M:%S.%f")
        delta = difference.seconds * 1000 + int(difference.microseconds/1000)
        return delta

    
    def onTimerTimeout(self, *args):
        left = self.rect().center().x() - self.distanceFromCenter
        right = self.rect().center().x() + self.distanceFromCenter


        if self._ballposition.isRight(self.deltatime):
            self._stimulator.position = right, self.rect().center().y()
            if self.isRight == False:
                self.isRight = True
                self.contador = self.contador + 1
        else:
            self._stimulator.position = left, self.rect().center().y()
            if self.isRight:
                self.isRight = False
                self.contador = self.contador + 1

        if(self.tipo == '1' or self.tipo == '3'):
            if(self.contador == 10):
                self._stimulatorTimer.stop()
                self.hide()
                if(self.tipo == '1'):
                    QMessageBox.question(self,'Aviso','A continuación será el test. Presione Ok para continuar.',QMessageBox.Ok)
                    self.padre._testStimulator.runStimulator()
                else:
                    QMessageBox.question(self,'Aviso','Ha terminado la calibración. Presione Ok para finalizar.',QMessageBox.Ok)
        
        if(self.deltatime / 1000 > self.padre.test._test_duration and self.tipo == '2'):
            self._stimulatorTimer.stop()
            self.hide()
            QMessageBox.question(self,'Aviso','A continuación será la calibración. Presione Ok para continuar.',QMessageBox.Ok)
            self.padre._calibrationWindow2.runStimulator()

    