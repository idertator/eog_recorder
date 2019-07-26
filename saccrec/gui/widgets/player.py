from math import ceil
from time import time

from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import qApp, QWidget

from saccrec.core import Settings
from saccrec.engine.stimulus import SaccadicStimuli


STIMULUS_TIMEOUT = 7    # TODO: Calculate this from the refresh rate of the monitor
BACKGROUND_COLOR = QColor(0, 0, 0)
BALL_RADIUS = 10
BALL_COLOR = QColor(255, 255, 255)


class StimulusPlayerWidget(QWidget):
    stimuliStarted = pyqtSignal(float)
    stimuliFinished = pyqtSignal()
    
    def __init__(self, settings: Settings, parent=None):
        super(StimulusPlayerWidget, self).__init__(parent=parent)
        self._settings = settings
        
        self._sampling_step = 1000 / int(self._settings.openbci_sample_rate)

        self._stimuli = None
        self._ball_position = None

        self._timer = QTimer()
        self._timer.setInterval(STIMULUS_TIMEOUT)
        self._timer.timeout.connect(self.on_timeout)

        self._start_time = 0

    def run_stimulus(self, stimuli: SaccadicStimuli):
        self._stimuli = stimuli
        self._ball_position = stimuli.screen_position(0)
        self.update()
        self._start_time = time()
        self._timer.start()
        self.stimuliStarted.emit(self._start_time)

    def on_timeout(self):
        elapsed = (time() - self._start_time) * 1000.0
        current_sample = ceil(elapsed / self._sampling_step)
        self._ball_position = self._stimuli.screen_position(current_sample)
        self.update()

        if self._ball_position is None:
            self._timer.stop()
            self.close_player()
            self.stimuliFinished.emit()
            
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        painter.setBackground(BACKGROUND_COLOR)
        painter.fillRect(self.rect(), BACKGROUND_COLOR)

        painter.setBrush(BALL_COLOR)

        if self._ball_position is not None:
            painter.drawEllipse(self._ball_position, BALL_RADIUS, BALL_RADIUS)

        painter.end()

    def close_player(self):
        self.setParent(qApp.topLevelWidgets()[0])
        self.close()
        self.setParent(None)


# class StimulusPlayerWidget1(QWidget):
    
#     def __init__(self, tipo=None, parent=None):
#         super(StimulusPlayerWidget1, self).__init__()

#         self.padre = parent

#         self.tipo = tipo

#         self.contador = 0
#         self.isRight = True

#         self.initUI()

#         self._stimulator = Stimulator(self)
#         self._ballposition = BallPosition(self.padre.test.test_duration, self.padre.test.mean_duration, self.padre.test.variation)
#         self._stimulatorTimer = QTimer()
#         self._stimulatorTimer.setInterval(16)
#         self._stimulatorTimer.timeout.connect(self.onTimerTimeout)

#         layout = QVBoxLayout()
#         layout.addWidget(self._stimulator)
        
#         self.setLayout(layout)
    
#     @property
#     def screenpixels(self):
#         app = QGuiApplication.instance()
#         size = app.primaryScreen().size()
#         return size.width(), size.height()

#     def initUI(self):
#         self.resize(self.screenpixels[0], self.screenpixels[1])

#     def runStimulator(self):
#         self.show()
#         self.initialTimeStamp = datetime.now()
#         print('Initial timestamp: '+str(self.initialTimeStamp))
#         self._stimulatorTimer.start()

#     @property
#     def stimulator(self):
#         return self._stimulator

#     @property
#     def screensize(self):
#         return self.padre.settings.screensize

#     @property
#     def distancePoints(self):
#         return float(self.padre.settings.distanceBetweenPoints)

    
#     @property
#     def distanceFromPatient(self):
#         if self.padre.test.stimulation_angle > 30:
#             angulo_maximo = self.padre.test.stimulation_angle
#         else:
#             angulo_maximo = 30
#         distance_from_mid = self.distancePoints / 2

#         distance_from_patient = distance_from_mid * (math.sin(math.radians(90 - angulo_maximo)) / math.sin(math.radians(angulo_maximo)))

#         return distance_from_patient


#     @property
#     def distanceFromCenter(self):
#         if(self.tipo == '1' or self.tipo == '3'):
#             angulo_vision = 30
#         else:
#             angulo_vision = self.padre.test.stimulation_angle 

#         pantalla_horizontal = self.screensize[0]

#         densidad_pixeles = self.screenpixels[0] / self.screensize[0]

#         distance_from_mid = self.distanceFromPatient * (math.sin(math.radians(angulo_vision)) / math.sin(math.radians(90 - angulo_vision)))

#         return math.floor(distance_from_mid * densidad_pixeles)


#     @property
#     def deltatime(self):
#         difference = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f") - datetime.strptime(str(self.initialTimeStamp), "%Y-%m-%d %H:%M:%S.%f")
#         delta = difference.seconds * 1000 + int(difference.microseconds/1000)
#         return delta

    
#     def onTimerTimeout(self, *args):
#         left = self.rect().center().x() - self.distanceFromCenter
#         right = self.rect().center().x() + self.distanceFromCenter


#         if self._ballposition.isRight(self.deltatime):
#             self._stimulator.position = right, self.rect().center().y()
#             if self.isRight == False:
#                 self.isRight = True
#                 self.contador = self.contador + 1
#         else:
#             self._stimulator.position = left, self.rect().center().y()
#             if self.isRight:
#                 self.isRight = False
#                 self.contador = self.contador + 1

#         if(self.tipo == '1' or self.tipo == '3'):
#             if(self.contador == 10):
#                 self._stimulatorTimer.stop()
#                 self.hide()
#                 if(self.tipo == '1'):
#                     QMessageBox.question(self,'Aviso','A continuación será el test. Presione Ok para continuar.',QMessageBox.Ok)
#                     self.padre._testStimulator.runStimulator()
#                 else:
#                     QMessageBox.question(self,'Aviso','Ha terminado la calibración. Presione Ok para finalizar.',QMessageBox.Ok)
        
#         if(self.deltatime / 1000 > self.padre.test._test_duration and self.tipo == '2'):
#             self._stimulatorTimer.stop()
#             self.hide()
#             QMessageBox.question(self,'Aviso','A continuación será la calibración. Presione Ok para continuar.',QMessageBox.Ok)
#             self.padre._calibrationWindow2.runStimulator()
