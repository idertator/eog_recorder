from PyQt5.QtWidgets import QMainWindow

from saccrec.core.Stimulator import Stimulator

class StimulatorWindow(QMainWindow):
    
    def __init__(self):
        super(StimulatorWindow, self).__init__()

        self.initUI()

        self._stimulator = Stimulator(self)
        self.setCentralWidget(self._stimulator)
        


    def initUI(self):
        self.show()