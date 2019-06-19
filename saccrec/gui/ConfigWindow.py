from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtProperty
from PyQt5 import QtWidgets

from .Configuracion.DatosConfiguracionUI import Ui_Configuracion

class ConfigWindow(QtWidgets.QWizard):
    def __init__(self, settings, parent=None):
        super(ConfigWindow, self).__init__(parent)

        self.settings = settings

        self.paginas = [_Page1(self)]

        for pagina in self.paginas:
            self.addPage(pagina)

        
        self.setWindowTitle("Nuevo Test - Registro de Datos")
        self.resize(640,480)

        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.finish_wizard)

    def finish_wizard(self):
        # Guardar configuracion
        pass 

class _Page1(Ui_Configuracion, QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(_Page1, self).__init__(parent)

        self.setupUi(self)

        