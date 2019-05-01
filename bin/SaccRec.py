from PyQt5.QtWidgets import QApplication

from saccrec.gui.MainWindow import MainWindow

app = QApplication([])

mainWindow = MainWindow()
mainWindow.showMaximized()

app.exec_()