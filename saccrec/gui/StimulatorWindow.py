import subprocess
from datetime import datetime

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer

from saccrec.core.Stimulator import Stimulator
from saccrec.core.Stimulator import BallPosition

class StimulatorWindow(QMainWindow):
    
    def __init__(self):
        super(StimulatorWindow, self).__init__()

        self.initUI()

        self._stimulator = Stimulator(self)
        self._ballposition = BallPosition(60000, 1000, 1000)
        self._stimulatorTimer = QTimer()
        self._stimulatorTimer.setInterval(60)
        self._stimulatorTimer.timeout.connect(self.onTimerTimeout)

        self.setCentralWidget(self._stimulator)
    

    def initUI(self):
        self.resize(self.screensize[0],self.screensize[1])

    def runStimulator(self):
        self.show()
        self.initialTimeStamp = datetime.now()
        print('Initial timestamp: '+str(self.initialTimeStamp))
        self._stimulatorTimer.start()

    
    @property
    def stimulator(self):
        return self._stimulator        


    @property
    def distanceFromCenter(self):
        return 50

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
        else:
            self._stimulator.position = left, self.rect().center().y()


    @property
    def screensize(self):
        size = (None, None)
        args = ["xrandr", "-q", "-d", ":0"]
        proc = subprocess.Popen(args,stdout=subprocess.PIPE)

        for line in proc.stdout:
            if isinstance(line, bytes):
                line = line.decode("utf-8")
                if "Screen" in line:
                    size = (int(line.split()[7]),  int(line.split()[9][:-1]))
        return size

    