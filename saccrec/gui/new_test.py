from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtProperty
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from .NewTest.DatosPacienteUI import Ui_DatosPaciente
from .NewTest.DatosPruebaUI import Ui_DatosPrueba
from .NewTest.DatosArchivoUI import Ui_DatosArchivo


class MagicWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(MagicWizard, self).__init__(parent)

        self.paginas = [Page1(self),Page2(self),Page3(self)]

        for pagina in self.paginas:
            self.addPage(pagina)

        
        self.setWindowTitle("Nuevo Test - Registro de Datos")
        self.resize(640,480)

        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.finish_wizard)


    def finish_wizard(self):
        # Guardar configuracion y empezar a obtener las muestras
        pass 


class Page1(Ui_DatosPaciente, QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        
        self.setupUi(self)


class Page2(Ui_DatosPrueba, QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        
        self.setupUi(self)


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