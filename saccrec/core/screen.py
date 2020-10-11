from PyQt5.QtCore import QObject, QRect
from PyQt5.QtWidgets import qApp


class Screen(QObject):

    def __init__(self, parent=None):
        super(Screen, self).__init__(parent=parent)

        self._screen_count = None
        self._primary_screen_rect = None
        self._secondary_screen_rect = None

        qApp.screenAdded.connect(self._reset_screen_count)
        qApp.screenRemoved.connect(self._reset_screen_count)

        self._reset_screen_count()

    def _reset_screen_count(self, *args) -> int:
        self._screen_count = qApp.desktop().screenCount()
        self._primary_screen_rect = qApp.desktop().screenGeometry(0)
        if self._screen_count > 1:
            self._secondary_screen_rect = qApp.desktop().screenGeometry(1)
        else:
            self._secondary_screen_rect = qApp.desktop().screenGeometry(0)

    @property
    def screen_count(self) -> int:
        return self._screen_count

    @property
    def primary_screen_rect(self) -> QRect:
        return self._primary_screen_rect

    @property
    def secondary_screen_rect(self) -> QRect:
        return self._secondary_screen_rect
