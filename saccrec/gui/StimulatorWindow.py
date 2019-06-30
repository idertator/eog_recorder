import subprocess
import math
from datetime import datetime

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer

from saccrec.core.Stimulator import Stimulator
from saccrec.core.Stimulator import BallPosition

class StimulatorWindow(QMainWindow):
    
    def __init__(self, tipo = None, parent=None):
        super(StimulatorWindow, self).__init__(parent)

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

        self.setCentralWidget(self._stimulator)
    

    def initUI(self):
        self.resize(self.screenpixels[0],self.screenpixels[1])

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



    @property
    def screenpixels(self):
        size = (None, None)
        args = ["xrandr", "-q", "-d", ":0"]
        proc = subprocess.Popen(args,stdout=subprocess.PIPE)

        for line in proc.stdout:
            if isinstance(line, bytes):
                line = line.decode("utf-8")
                if "Screen" in line:
                    size = (int(line.split()[7]),  int(line.split()[9][:-1]))
        return size

    