from PySide6 import QtWidgets, QtGui


class ColorButton(QtWidgets.QPushButton):

    def __init__(self, color: QtGui.QColor = None, *args, **kwargs):
        super(ColorButton, self).__init__(*args, **kwargs)

        self._color = color
        self.setFixedSize(32, 32)
        self.pressed.connect(self._on_pick_color_clicked)

    def value(self) -> QtGui.QColor:
        return self._color

    def setColor(self, color: QtGui.QColor):
        self._color = color
        if self._color:
            self.setStyleSheet(f'background-color: {self._color.name()};')
        else:
            self.setStyleSheet('')

    def _on_pick_color_clicked(self):
        dlg = QtWidgets.QColorDialog(self._color)
        if dlg.exec_():
            self.setColor(dlg.currentColor())
