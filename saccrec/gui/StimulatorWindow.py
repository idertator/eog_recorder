import subprocess
import math
from datetime import datetime

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer

from saccrec.core.Stimulator import Stimulator
from saccrec.core.Stimulator import BallPosition

class StimulatorWindow(QMainWindow):
    
    def __init__(self, tipo = None, parent=None):
        super(StimulatorWindow, self).__init__(parent)

        self.padre = parent

        self.tipo = tipo

        self.initUI()

        self._stimulator = Stimulator(self)
        self._ballposition = BallPosition(60000, 3000, 500)
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
    def distanceFromCenter(self):
        if(self.tipo == '1' or self.tipo == '3'):
            angulo_vision = 30
        else:
            angulo_vision = self.padre.test.stimulation_angle 

        distance_from_mid = self.distancePoints / 2
        pantalla_horizontal = self.screensize[0]

        densidad_pixeles = self.screenpixels[0] / self.screensize[0]

        return math.floor(distance_from_mid * densidad_pixeles)

    @property
    def distanceFromPatient(self):
        pantalla_diagonal = 22 # 22 pulgadas
        angulo_vision = 10 # grados
        distancia_paciente = 50 # centimetros

        pantalla_horizontal = (pantalla_diagonal / 16) * 9 # Se toma la proporcion en ancho, se da por hecho q se usa una pantalla de relacion de aspecto 16:9
        pantalla_horizontal_cm = pantalla_horizontal * 2.54 # Pulgadas a centimetros

        densidad_pixeles = self.screenpixels[0] / pantalla_horizontal_cm

        distancia_del_centro = distancia_paciente * (math.sin(math.radians(angulo_vision)) / math.sin(math.radians(90 - angulo_vision)))

        return math.floor(distancia_del_centro * densidad_pixeles)

    @property
    def deltatime(self):
        difference = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f") - datetime.strptime(str(self.initialTimeStamp), "%Y-%m-%d %H:%M:%S.%f")
        delta = difference.seconds * 1000 + int(difference.microseconds/1000)
        return delta

    
    def onTimerTimeout(self, *args):
        left = self.rect().center().x() - self.distanceFromCenter
        right = self.rect().center().x() + self.distanceFromCenter

        print(self.distanceFromCenter)

        if self._ballposition.isRight(self.deltatime):
            self._stimulator.position = right, self.rect().center().y()
        else:
            self._stimulator.position = left, self.rect().center().y()


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

    