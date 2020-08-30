import gettext

from os import kill
from os.path import join, exists, abspath, dirname
from tempfile import gettempdir

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication, QMessageBox

from saccrec.core import Settings
from saccrec.settings import GUI_LANG
from saccrec.gui.main import MainWindow

settings = QSettings()

# Setting up i18n
LOCALE_PATH = join(abspath(dirname(dirname(__file__))), 'locales')
CURRENT_LANG = settings.value(GUI_LANG, 'en')

tr = gettext.translation('saccrec', LOCALE_PATH, languages=[CURRENT_LANG])
tr.install('saccrec')

# Checking Hardware Connections
DONGLE_CONNECTED = True
BOARD_CONNECTED = True

pid_path = join(gettempdir(), 'saccrec.pid')
if exists(pid_path):
    with open(pid_path, 'rt') as f:
        pid = int(f.read().strip())
        try:
            kill(pid, 0)
        except OSError:
            from serial.serialutil import SerialException

            from saccrec.engine.recording import initialize_board, close_board
            from saccrec.engine.errors import BoardNotConnectedError
            settings = Settings()
            try:
                board = initialize_board(settings)
                close_board(board)
            except BoardNotConnectedError:
                BOARD_CONNECTED = False
            except SerialException:
                DONGLE_CONNECTED = False
        else:
            print('Killed hanged process')


app = QApplication([])
app.setOrganizationName('SaccRec')
app.setApplicationName('SaccRec')

mainWindow = MainWindow()
mainWindow.showMaximized()

if not DONGLE_CONNECTED:
    QMessageBox.critical(
        mainWindow,
        _('Error'),
        _('El recibidor Bluetooth no está conectado al ordenador'),
        QMessageBox.Close
    )
    QApplication.exit(0)
elif not BOARD_CONNECTED:
    QMessageBox.critical(
        mainWindow,
        _('Error'),
        _('La tarjeta no está conectada'),
        QMessageBox.Close
    )
    QApplication.exit(0)
else:
    app.exec_()
