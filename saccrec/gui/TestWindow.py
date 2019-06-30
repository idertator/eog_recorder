import math

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtProperty, QDate
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog

from saccrec.gui.NewTest.DatosPacienteUI import Ui_DatosPaciente
from saccrec.gui.NewTest.DatosPruebaUI import Ui_DatosPrueba
from saccrec.gui.NewTest.DatosArchivoUI import Ui_DatosArchivo
from saccrec.core.Patient import Patient


class MagicWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(MagicWizard, self).__init__(parent)

        self.padre = parent

        self.paginas = [Page1(self),Page2(self),Page3(self)]

        for pagina in self.paginas:
            self.addPage(pagina)

        
        self.setWindowTitle("Nuevo Test - Registro de Datos")
        self.resize(640,480)

        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.finish_wizard)


    def finish_wizard(self):

        self.padre.test.patient = Patient(self.paginas[0].txtName.text,self.paginas[0].borndateDate.date, self.paginas[0].comboGenre.currentText, self.paginas[0].comboGenre.currentText)
        
        self.padre.test.stimulation_angle = self.paginas[1].txt_angulo.value()
        self.padre.test.mean_duration = self.paginas[1].txt_mean_duration.value()
        self.padre.test.variation = self.paginas[1].txt_variaton.value()
        self.padre.test.test_duration = self.paginas[1].txt_testduration.value()

        self.padre.test.output_file_path = self.paginas[2].txtPath.text()

        QMessageBox.question(self,'Aviso','La prueba consta de 3 partes: calibración inicial, prueba y calibración final. Presione OK para continuar.', QMessageBox.Ok)
        QMessageBox.question(self,'Aviso','Se debe ubicar el paciente a '+str(self.distanceFromPatient)+' cm de la pantalla. Presione Ok para continuar.', QMessageBox.Ok)

        self.padre._calibrationWindow1.runStimulator()


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
        


class Page1(Ui_DatosPaciente, QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        
        self.setupUi(self)

        self.txtName.setText(parent.padre.settings.initialName)
        self.borndateDate.setDate(QDate(1990,1,1))
        

class Page2(Ui_DatosPrueba, QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        
        self.setupUi(self)

        self.txt_angulo.setValue(30)
        self.txt_mean_duration.setValue(3.0)
        self.txt_variaton.setValue(1.0)
        self.txt_testduration.setValue(60.0)


class Page3(Ui_DatosArchivo, QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page3, self).__init__(parent)

        self.setupUi(self)
        
        self.searchButton.clicked.connect(self.file_open)

    def file_open(self):
        name = QFileDialog.getSaveFileName(self, 'Open File')
        self.txtPath.setText(name[0])


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wizard = MagicWizard()
    wizard.show()
    sys.exit(app.exec_())