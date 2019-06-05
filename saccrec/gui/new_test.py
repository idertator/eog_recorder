from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtProperty
from PyQt5 import QtWidgets


class MagicWizard(QtWidgets.QWizard):
    def __init__(self, settings, parent=None):
        super(MagicWizard, self).__init__(parent)

        self.settings = settings

        self.paginas = [Page1(self),Page2(self),Page3(self),Page4(self)]

        for pagina in self.paginas:
            self.addPage(pagina)

        
        self.setWindowTitle("Nuevo Test - Registro de Datos")
        self.resize(640,480)

        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.finish_wizard)


    def finish_wizard(self):
        # Guardar configuracion y empezar a obtener las muestras



class Page1(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        
        self.etiqueta_datos = QtWidgets.QLabel(self)
        self.etiqueta_datos.setGeometry(QtCore.QRect(10, 10, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.etiqueta_datos.setFont(font)
        self.etiqueta_datos.setAutoFillBackground(False)
        self.etiqueta_datos.setObjectName("etiqueta_datos")
        self.etiqueta_nombres = QtWidgets.QLabel(self)
        self.etiqueta_nombres.setGeometry(QtCore.QRect(20, 60, 71, 16))
        self.etiqueta_nombres.setObjectName("etiqueta_nombres")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(20, 120, 131, 16))
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 150, 55, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 55, 16))
        self.label_2.setObjectName("label_2")
        self.text_nombres = QtWidgets.QLineEdit(self)
        self.text_nombres.setGeometry(QtCore.QRect(180, 60, 201, 22))
        self.text_nombres.setObjectName("text_nombres")
        self.dateEdit = QtWidgets.QDateEdit(self)
        self.dateEdit.setGeometry(QtCore.QRect(180, 120, 201, 22))
        self.dateEdit.setObjectName("dateEdit")
        self.combo_genero = QtWidgets.QComboBox(self)
        self.combo_genero.setGeometry(QtCore.QRect(180, 90, 201, 22))
        self.combo_genero.setObjectName("combo_genero")
        self.combo_genero.addItem("")
        self.combo_genero.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(self)
        self.comboBox_2.setGeometry(QtCore.QRect(180, 150, 201, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.etiqueta_datos.setText(_translate("Dialog", "Datos del paciente"))
        self.etiqueta_nombres.setText(_translate("Dialog", "Nombres:"))
        self.label_3.setText(_translate("Dialog", "Fecha de nacimiento:"))
        self.label.setText(_translate("Dialog", "Estado:"))
        self.label_2.setText(_translate("Dialog", "Genero:"))
        self.combo_genero.setItemText(0, _translate("Dialog", "Masculino"))
        self.combo_genero.setItemText(1, _translate("Dialog", "Femenino"))
        self.comboBox_2.setItemText(0, _translate("Dialog", "Desconocido"))
        self.comboBox_2.setItemText(1, _translate("Dialog", "Control"))
        self.comboBox_2.setItemText(2, _translate("Dialog", "Presintomático SCA2"))
        self.comboBox_2.setItemText(3, _translate("Dialog", "SCA2"))


class Page2(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        
        self.etiqueta_datos = QtWidgets.QLabel(self)
        self.etiqueta_datos.setGeometry(QtCore.QRect(10, 10, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.etiqueta_datos.setFont(font)
        self.etiqueta_datos.setAutoFillBackground(False)
        self.etiqueta_datos.setObjectName("etiqueta_datos")
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(20, 80, 171, 16))
        self.label_5.setObjectName("label_5")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(20, 140, 131, 16))
        self.label_4.setObjectName("label_4")
        self.etiqueta_nombres_2 = QtWidgets.QLabel(self)
        self.etiqueta_nombres_2.setGeometry(QtCore.QRect(20, 50, 131, 16))
        self.etiqueta_nombres_2.setObjectName("etiqueta_nombres_2")
        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(20, 110, 191, 16))
        self.label_6.setObjectName("label_6")
        self.spinBox = QtWidgets.QSpinBox(self)
        self.spinBox.setGeometry(QtCore.QRect(250, 40, 61, 22))
        self.spinBox.setObjectName("spinBox")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox.setGeometry(QtCore.QRect(250, 70, 62, 22))
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_2.setGeometry(QtCore.QRect(250, 100, 62, 22))
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.doubleSpinBox_3 = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_3.setGeometry(QtCore.QRect(250, 130, 62, 22))
        self.doubleSpinBox_3.setObjectName("doubleSpinBox_3")
        
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.etiqueta_datos.setText(_translate("Dialog", "Datos de la prueba"))
        self.label_5.setText(_translate("Dialog", "Duración media del estímulo:"))
        self.label_4.setText(_translate("Dialog", "Duración de la prueba:"))
        self.etiqueta_nombres_2.setText(_translate("Dialog", "Ángulo de estímulo:"))
        self.label_6.setText(_translate("Dialog", "Rango de variación en segundos:"))


class Page3(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page3, self).__init__(parent)

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

class Page4(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page4, self).__init__(parent)

        self.etiqueta_datos = QtWidgets.QLabel(self)
        self.etiqueta_datos.setGeometry(QtCore.QRect(10, 10, 241, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.etiqueta_datos.setFont(font)
        self.etiqueta_datos.setAutoFillBackground(False)
        self.etiqueta_datos.setObjectName("etiqueta_datos")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(30, 50, 55, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(20, 70, 391, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.boton_buscar = QtWidgets.QPushButton(self)
        self.boton_buscar.setGeometry(QtCore.QRect(420, 68, 93, 25))
        self.boton_buscar.setObjectName("boton_buscar")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.etiqueta_datos.setText(_translate("Dialog", "Datos de almacenamiento"))
        self.label.setText(_translate("Dialog", "Directorio:"))
        self.boton_buscar.setText(_translate("Dialog", "Buscar..."))

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wizard = MagicWizard()
    wizard.show()
    sys.exit(app.exec_())