from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtProperty
from PyQt5 import QtWidgets

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

class _Page1(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(_Page1, self).__init__(parent)

        self.etiqueta_datos = QtWidgets.QLabel(self)
        self.etiqueta_datos.setGeometry(QtCore.QRect(10, 10, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.etiqueta_datos.setFont(font)
        self.etiqueta_datos.setAutoFillBackground(False)
        self.etiqueta_datos.setObjectName("etiqueta_datos")
        self.screensize = QtWidgets.QLabel(self)
        self.screensize.setGeometry(QtCore.QRect(20, 80, 171, 16))
        self.screensize.setObjectName("puertocaptura")
        self.puertocaptura = QtWidgets.QLabel(self)
        self.puertocaptura.setGeometry(QtCore.QRect(20, 50, 131, 16))
        self.puertocaptura.setObjectName("puertocaptura")
        self.distancia_paciente = QtWidgets.QLabel(self)
        self.distancia_paciente.setGeometry(QtCore.QRect(20, 110, 191, 16))
        self.distancia_paciente.setObjectName("distancia_paciente")
        self.txt_puerto_captura = QtWidgets.QSpinBox(self)
        self.txt_puerto_captura.setGeometry(QtCore.QRect(250, 40, 62, 22))
        self.txt_puerto_captura.setObjectName("txt_puerto_captura")
        self.txt_screensize = QtWidgets.QSpinBox(self)
        self.txt_screensize.setGeometry(QtCore.QRect(250, 70, 62, 22))
        self.txt_screensize.setObjectName("txt_screensizeX")
        self.txt_distancia_paciente = QtWidgets.QSpinBox(self)
        self.txt_distancia_paciente.setGeometry(QtCore.QRect(250, 100, 62, 22))
        self.txt_distancia_paciente.setObjectName("txt_distancia_paciente")
        
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.etiqueta_datos.setText(_translate("Dialog", "Datos de configuración"))
        self.screensize.setText(_translate("Dialog", "Tamaño de pantalla(inch):"))
        self.puertocaptura.setText(_translate("Dialog", "Puerto de Captura:"))
        self.distancia_paciente.setText(_translate("Dialog", "Distancia del paciente:"))