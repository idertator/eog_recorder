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

    @testDuration.setter
    def testDuration(self, duration:int):
        self._settings.setValue('testDuration', duration)

    @initialName.setter
    def initialName(self, name: str):
        self._settings.setValue('InitialName', name)
