from logging import Handler, INFO, ERROR, WARN, DEBUG

from PySide6 import QtWidgets


class LoggerWidget(Handler, QtWidgets.QPlainTextEdit):
    def __init__(self, parent=None):
        QtWidgets.QPlainTextEdit.__init__(self, parent)
        Handler.__init__(self)

        self.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)

        fmt = "<span>{msg}</span><br>"
        if record.levelno == ERROR:
            fmt = '<span style="color: red">{msg}</span><br>'
        elif record.levelno == INFO:
            fmt = '<span style="color: blue">{msg}</span><br>'
        elif record.levelno == DEBUG:
            fmt = '<span style="color: green">{msg}</span><br>'
        elif record.levelno == WARN:
            fmt = '<span style="color: yellow">{msg}</span><br>'

        try:
            self.textCursor().insertHtml(fmt.format(msg=msg))
            self.repaint()
        except ValueError as error:
            print(f"ValueError: {msg}")
            print(error)
