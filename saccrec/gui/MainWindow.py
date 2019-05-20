import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):

    def __init__(self):
    	super().__init__()
    	self.initUI()

    def newMenu(self, nombre):
        menubar = self.menuBar()
        menu = menubar.addMenu(nombre)
        return menu

    def initUI(self):
        exitAct = QAction(QIcon('saccrec/gui/images/exit.svg'), '&Exit', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        aboutUs = QAction(QIcon('saccrec/gui/images/interrogacion.png'), '&About Us',self)

        self.statusBar()

        fileMenu = self.newMenu('&File')
        fileMenu.addAction(exitAct)

        helpMenu = self.newMenu('&Help')
        helpMenu.addAction(aboutUs)
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('EyeTracker OpenBCI')
        self.show()