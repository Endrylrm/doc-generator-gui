from PySide6 import QtGui, QtCore, QtPrintSupport


class PrinterFactory:
    """
    This class is responsible for creating our QPrinters to
    use later on the creation of PDFs or printing physically
    """

    @classmethod
    def createPrinterToPDF(cls) -> QtPrintSupport.QPrinter:
        printer = cls._createPrinter()

        PDF_PRINTER_RESOLUTION: int = 600

        printer.setOutputFormat(QtPrintSupport.QPrinter.OutputFormat.PdfFormat)
        printer.setResolution(PDF_PRINTER_RESOLUTION)
        return printer

    @classmethod
    def createPrinterToNative(cls) -> QtPrintSupport.QPrinter:
        printer = cls._createPrinter()

        PRINTER_RESOLUTION: int = 600

        printer.setOutputFormat(QtPrintSupport.QPrinter.OutputFormat.NativeFormat)
        printer.setResolution(PRINTER_RESOLUTION)

        return printer

    @classmethod
    def _createPrinter(cls) -> QtPrintSupport.QPrinter:
        printer = QtPrintSupport.QPrinter(
            QtPrintSupport.QPrinter.PrinterMode.HighResolution
        )
        printer.setPageSize(QtGui.QPageSize.PageSizeId.A4)
        printer.setFullPage(True)
        printer.setPageMargins(QtCore.QMarginsF(0.5, 0.5, 0.5, 0.5))
        return printer
