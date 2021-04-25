#!/usr/bin/env python3.9
import gettext
import sys
from faulthandler import enable as enable_faulthandler
from os import getpid, kill, remove, system
from os.path import abspath, dirname, exists, join
from tempfile import gettempdir

from PySide6 import QtWidgets

from saccrec.gui.main import MainWindow

from .settings import gui, hardware, initialize_screen

_GUI_PID_FILE = '/tmp/saccrec_gui.pid'


def declare_gui_running_pid():
    with open('/tmp/saccrec_gui.pid', 'wt') as f:
        f.write(f'{getpid()}\n')


def clear_gui_running_pid():
    if exists(_GUI_PID_FILE):
        remove(_GUI_PID_FILE)


def kill_hanged_processes():
    if exists(_GUI_PID_FILE):
        with open(_GUI_PID_FILE, 'rt') as f:
            pid = int(f.read().strip())
            try:
                kill(pid, 0)
            except OSError:
                pass
            else:
                print('Killed hanged process')


def setup_i18n():
    LOCALE_PATH = join(dirname(__file__), 'locales')

    tr = gettext.translation('saccrec', LOCALE_PATH, languages=[gui.lang])
    tr.install('saccrec')


def improve_ftdi_latency():
    for i in range(4):
        path = f'/dev/ttyUSB{i}'
        if exists(path):
            system(f'setserial {path} low_latency')


def main():
    kill_hanged_processes()

    improve_ftdi_latency()

    declare_gui_running_pid()
    enable_faulthandler()

    app = QtWidgets.QApplication()
    app.setOrganizationName('idertator')
    app.setApplicationName('SaccRec')

    setup_i18n()

    main_window = MainWindow()
    main_window.showMaximized()

    initialize_screen(main_window)

    retcode = app.exec_()

    clear_gui_running_pid()

    sys.exit(retcode)


if __name__ == '__main__':
    main()
