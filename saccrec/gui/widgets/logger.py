from logging import Handler, INFO, ERROR, WARN, DEBUG

from PySide6 import QtCore, QtWidgets


class LoggerSignal(QtCore.QObject):
    signal = QtCore.Signal()

    def __init__(self):
        super(LoggerSignal, self).__init__()


class LoggerWidget(Handler, QtWidgets.QPlainTextEdit):

    def __init__(self, parent=None):
        QtWidgets.QPlainTextEdit.__init__(self, parent)
        Handler.__init__(self)

        self.setReadOnly(True)

        self.logger_signal = LoggerSignal()

    def emit(self, record):
        msg = self.format(record)

        fmt = '<span>{msg}</span><br>'
        if record.levelno == ERROR:
            fmt = '<span style="color: red">{msg}</span>'
        elif record.levelno == INFO:
            fmt = '<span style="color: blue">{msg}</span>'
        elif record.levelno == DEBUG:
            fmt = '<span style="color: green">{msg}</span>'
        elif record.levelno == WARN:
            fmt = '<span style="color: yellow">{msg}</span>'

        try:
            self.appendHtml(fmt.format(msg=msg))
            self.repaint()
            self.logger_signal.signal.emit()
        except ValueError as error:
            print(f'ValueError: {msg}')
            print(error)
