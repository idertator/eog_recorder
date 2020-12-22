import gettext
import sys

from faulthandler import enable as enable_faulthandler
from os import kill, system
from os.path import join, exists, abspath, dirname
from tempfile import gettempdir

from PySide6.QtWidgets import QApplication

from saccrec.gui.main import MainWindow
from saccrec.settings import gui, hardware, initialize_screen


def kill_hanged_process():
    pid_path = join(gettempdir(), 'saccrec.pid')
    if exists(pid_path):
        with open(pid_path, 'rt') as f:
            pid = int(f.read().strip())
            try:
                kill(pid, 0)
            except OSError:
                pass
            else:
                print('Killed hanged process')


def check_serial_latency():
    device = (hardware.port or '/dev/ttyUSB0').split('/')[-1]
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


def setup_i18n():
    LOCALE_PATH = join(abspath(dirname(dirname(__file__))), 'locales')

    tr = gettext.translation('saccrec', LOCALE_PATH, languages=[gui.lang])
    tr.install('saccrec')


if __name__ == '__main__':
    enable_faulthandler()

    kill_hanged_process()
    setup_i18n()
    check_serial_latency()

    app = QApplication([])
    app.setOrganizationName('SaccRec')
    app.setApplicationName('SaccRec')

    main_window = MainWindow()
    main_window.showMaximized()

    initialize_screen(main_window)

    sys.exit(app.exec_())
