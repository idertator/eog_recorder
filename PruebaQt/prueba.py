from PyQt5.QtWidgets import QApplication

from ui.MainWindow import MainWindow


if __name__ == '__main__':
    app = QApplication([])

    mainWindow = MainWindow()
    mainWindow.showMaximized()

    app.exec_()