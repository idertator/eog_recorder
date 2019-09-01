from os import kill
from os.path import join, exists
from tempfile import gettempdir

from PyQt5.QtWidgets import QApplication

from saccrec.core import Settings
from saccrec.gui import MainWindow


pid_path = join(gettempdir(), 'saccrec.pid')
if exists(pid_path):
    with open(pid_path, 'rt') as f:
        pid = int(f.read().strip())
        try:
            kill(pid, 0)
        except OSError:
            from saccrec.engine.recording import initialize_board, close_board
            settings = Settings()
            board = initialize_board(settings)
            close_board(board)
        else:
            print('Killed hanged process')


app = QApplication([])

mainWindow = MainWindow()
mainWindow.showMaximized()

app.exec_()