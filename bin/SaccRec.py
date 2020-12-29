#!/usr/bin/env python3.9
import gettext
import sys

from faulthandler import enable as enable_faulthandler
from os import kill, system, getpid, remove
from os.path import join, exists, abspath, dirname
from tempfile import gettempdir

from PySide2 import QtWidgets

import saccrec
from saccrec.settings import gui, hardware, initialize_screen
from saccrec.gui.main import MainWindow


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
    LOCALE_PATH = join(dirname(saccrec.__file__), 'locales')

    tr = gettext.translation('saccrec', LOCALE_PATH, languages=[gui.lang])
    tr.install('saccrec')


if __name__ == '__main__':
    kill_hanged_processes()

    declare_gui_running_pid()
    enable_faulthandler()

    setup_i18n()

    app = QtWidgets.QApplication()
    app.setOrganizationName('SaccRec')
    app.setApplicationName('SaccRec')

    main_window = MainWindow()
    main_window.showMaximized()

    initialize_screen(main_window)

    retcode = app.exec_()

    clear_gui_running_pid()

    sys.exit(retcode)
