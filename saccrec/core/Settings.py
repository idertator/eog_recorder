from PyQt5.QtCore import QSettings


class Settings(object):

    def __init__(self, parent=None):
        self._settings = QSettings('umautm', 'saccrec', parent)

    @property
    def initialName(self) -> str:
        return self._settings.value('InitialName', 'John')

    @property
    def testDuration(self) -> int:
        return self._settings.value('testDuration', 30)

    @property
    def screensize(self) -> tuple:
        return self._settings.value('ScreenSize',(32,18))

    @property
    def distanceBetweenPoints(self) -> float:
        return self._settings.value('DistanceBetweenPoints',5.0)

    @property
    def capturePort(self) -> int:
        return self._settings.value('capturePort',0)

    @testDuration.setter
    def testDuration(self, duration:int):
        self._settings.setValue('testDuration', duration)

    @initialName.setter
    def initialName(self, name: str):
        self._settings.setValue('InitialName', name)

    @screensize.setter
    def screensize(self, size: tuple):
        self._settings.setValue('ScreenSize', size)

    @distanceBetweenPoints.setter
    def distanceBetweenPoints(self, distance: float):
        self._settings.setValue('DistanceBetweenPoints', distance)

    @capturePort.setter
    def capturePort(self, port: int):
        self._settings.setValue('capturePort', port)

