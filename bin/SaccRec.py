import gettext
import sys

from faulthandler import enable as enable_faulthandler
from os import kill, system, getpid, remove
from os.path import join, exists, abspath, dirname
from tempfile import gettempdir

from PySide6.QtWidgets import QApplication

from saccrec.settings import gui, hardware, initialize_screen
from saccrec.gui.main import MainWindow


_GUI_PID_FILE = '/tmp/saccrec_gui.pid'
_REC_PID_FILE = '/tmp/saccrec_rec.pid'


def declare_gui_running_pid():
    with open('/tmp/saccrec_gui.pid', 'wt') as f:
        f.write(f'{getpid()}\n')


def clear_gui_running_pid():
    if exists(_GUI_PID_FILE):
        remove(_GUI_PID_FILE)


def kill_hanged_processes():
    pid_path = join(gettempdir(), 'saccrec.pid')
    for pid_path in [_GUI_PID_FILE, _REC_PID_FILE]:
        if exists(pid_path):
            with open(pid_path, 'rt') as f:
                pid = int(f.read().strip())
                try:
                    kill(pid, 0)
                except OSError:
                    pass
                else:
                    print('Killed hanged process')


def setup_i18n():
    LOCALE_PATH = join(abspath(dirname(dirname(__file__))), 'locales')

    tr = gettext.translation('saccrec', LOCALE_PATH, languages=[gui.lang])
    tr.install('saccrec')


if __name__ == '__main__':
    kill_hanged_processes()

    declare_gui_running_pid()
    enable_faulthandler()

    setup_i18n()

    app = QApplication([])
    app.setOrganizationName('SaccRec')
    app.setApplicationName('SaccRec')

    main_window = MainWindow()
    main_window.showMaximized()

    initialize_screen(main_window)

    retcode = app.exec_()

    clear_gui_running_pid()

    sys.exit(retcode)
