from os import kill
from os.path import join, exists
from tempfile import gettempdir

from PyQt5.QtWidgets import QApplication, QMessageBox

from saccrec.core import Settings
from saccrec.gui import MainWindow

BOARD_CONNECTED = True

pid_path = join(gettempdir(), 'saccrec.pid')
if exists(pid_path):
    with open(pid_path, 'rt') as f:
        pid = int(f.read().strip())
        try:
            kill(pid, 0)
        except OSError:
            from saccrec.engine.recording import initialize_board, close_board
            from saccrec.engine.errors import BoardNotConnectedError
            settings = Settings()
            try:
                board = initialize_board(settings)
                close_board(board)
            except BoardNotConnectedError:
                BOARD_CONNECTED = False
        else:
            print('Killed hanged process')


app = QApplication([])

mainWindow = MainWindow()
mainWindow.showMaximized()

if not BOARD_CONNECTED:
    QMessageBox.critical(
        mainWindow,
        'Error',
        'Board is not connected',
        QMessageBox.Close
    )
    QApplication.exit(0)
else:
    app.exec_()
