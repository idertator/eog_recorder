from PySide6 import QtCore, QtWidgets


class Screen(QtCore.QObject):
    def __init__(self, parent=None):
        super(Screen, self).__init__(parent=parent)

        qApp = QtWidgets.QApplication.instance()

        self._screens = qApp.screens()
        self._connect_handler()
        self._reset()

        qApp.screenAdded.connect(self._screen_count_changed)
        qApp.screenRemoved.connect(self._screen_count_changed)

    def _screen_count_changed(self):
        qApp = QtWidgets.QApplication.instance()

        self._disconnect_handler()
        self._screens = qApp.screens()
        self._connect_handler()
        self._reset()

    def _connect_handler(self):
        for screen in self._screens:
            screen.availableGeometryChanged.connect(self._reset)
            screen.geometryChanged.connect(self._reset)
            screen.logicalDotsPerInchChanged.connect(self._reset)
            screen.orientationChanged.connect(self._reset)
            screen.physicalDotsPerInchChanged.connect(self._reset)
            screen.physicalSizeChanged.connect(self._reset)
            screen.primaryOrientationChanged.connect(self._reset)
            screen.refreshRateChanged.connect(self._reset)
            screen.virtualGeometryChanged.connect(self._reset)

    def _disconnect_handler(self):
        for screen in self._screens:
            screen.availableGeometryChanged.disconnect(self._reset)
            screen.geometryChanged.disconnect(self._reset)
            screen.logicalDotsPerInchChanged.disconnect(self._reset)
            screen.orientationChanged.disconnect(self._reset)
            screen.physicalDotsPerInchChanged.disconnect(self._reset)
            screen.physicalSizeChanged.disconnect(self._reset)
            screen.primaryOrientationChanged.disconnect(self._reset)
            screen.refreshRateChanged.disconnect(self._reset)
            screen.virtualGeometryChanged.disconnect(self._reset)

    def _reset(self):
        primary_screen = self._screens[0]
        if len(self._screens) > 1:
            secondary_screen = self._screens[1]
        else:
            secondary_screen = self._screens[0]

        self._primary_screen_rect = primary_screen.availableGeometry()
        self._primary_screen_refresh_rate = primary_screen.refreshRate()
        self._secondary_screen_rect = secondary_screen.availableGeometry()
        self._secondary_screen_refresh_rate = secondary_screen.refreshRate()

    @property
    def primary_screen_rect(self) -> QtCore.QRect:
        return self._primary_screen_rect

    @property
    def primary_screen_refresh_rate(self) -> float:
        return self._primary_screen_refresh_rate

    @property
    def secondary_screen_rect(self) -> QtCore.QRect:
        return self._secondary_screen_rect

    @property
    def secondary_screen_refresh_rate(self) -> float:
        return self._secondary_screen_refresh_rate
