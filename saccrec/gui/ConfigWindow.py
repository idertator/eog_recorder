from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtProperty
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from .Configuracion.DatosConfiguracionUI import Ui_Configuracion

class ConfigWindow(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(ConfigWindow, self).__init__(parent)

        self.padre = parent

        self.paginas = [_Page1(self)]

        for pagina in self.paginas:
            self.addPage(pagina)

        
        self.setWindowTitle("Nuevo Test - Registro de Datos")
        self.resize(640,480)

        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.finish_wizard)

    def finish_wizard(self):

        ancho = self.paginas[0].txt_horizontalsize.value()
        alto = self.paginas[0].txt_verticalsize.value()
        distancia = self.paginas[0].txt_maxdistance.value()

        if distancia > ancho * 0.9:

            mensaje = QMessageBox.question(self, 'Aviso','La distancia entre los puntos excede los límites de la pantalla', QMessageBox.Ok)
            self.show()

        else:

            self.padre.settings.screensize = (ancho, alto)
            self.padre.settings.distanceBetweenPoints = distancia
            self.padre.settings.capturePort = self.paginas[0].txt_captureport.value()



class _Page1(Ui_Configuracion, QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(_Page1, self).__init__(parent)

        self.setupUi(self)

        self.txt_captureport.setValue(int(parent.padre.settings.capturePort))
        self.txt_horizontalsize.setValue(parent.padre.settings.screensize[0])
        self.txt_verticalsize.setValue(parent.padre.settings.screensize[1])
        self.txt_maxdistance.setValue(float(parent.padre.settings.distanceBetweenPoints))

        