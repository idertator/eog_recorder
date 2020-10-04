import gettext

from faulthandler import enable as enable_faulthandler
from os import kill, system
from os.path import join, exists, abspath, dirname
from tempfile import gettempdir

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication, QMessageBox

from saccrec.core import Settings
from saccrec.settings import GUI_LANG, OPENBCI_PORT
from saccrec.gui.main import MainWindow

enable_faulthandler()

settings = QSettings()


def check_serial_latency():
    device = settings.value(OPENBCI_PORT, '/dev/ttyUSB0').split('/')[-1]
    config_file = f'/sys/bus/usb-serial/devices/{device}/latency_timer'

    try:
        latency = None
        with open(config_file, 'rt') as f:
            latency = int(f.readline().strip())
        if latency > 1:
            system(f'setserial /dev/{device} low_latency')
            print(f'FTDI latency to {device} was set to 1ms')
    except FileNotFoundError:
        print('Device not connected')


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
            try:
                from saccrec.settings import OPENBCI_SAMPLING_RATE
                openbci_port = settings.value(OPENBCI_PORT)
                openbci_sampling_rate = settings.value(OPENBCI_SAMPLING_RATE, 250)

                board = initialize_board(
                    settings=Settings(),
                    openbci_port=openbci_port,
                    sampling_rate=openbci_sampling_rate
                )
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

check_serial_latency()

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
