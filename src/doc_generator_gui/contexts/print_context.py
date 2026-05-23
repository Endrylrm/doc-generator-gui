from PySide6 import QtGui, QtPrintSupport


class PrintContext:
    """
    This class is responsible is a context manager for the
    QPrinters and QPainters used on our printing services.
    """

    def __init__(self, printer: QtPrintSupport.QPrinter):
        self.printer = printer
        self.painter = QtGui.QPainter()

    def __enter__(self):
        self.painter.begin(self.printer)
        return self

    def __exit__(self, exc_type, exc, tb):
        self.painter.end()
