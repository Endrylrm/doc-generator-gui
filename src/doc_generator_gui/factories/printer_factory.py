from PySide6 import QtGui, QtCore, QtPrintSupport


class PrinterFactory:
    """
    This class is responsible for creating our QPrinters to
    use later on the creation of PDFs or printing physically
    """

    @classmethod
    def create_pdf_printer(cls) -> QtPrintSupport.QPrinter:
        printer = cls.__create_printer()

        PDF_PRINTER_RESOLUTION: int = 600

        printer.setOutputFormat(QtPrintSupport.QPrinter.OutputFormat.PdfFormat)
        printer.setResolution(PDF_PRINTER_RESOLUTION)
        return printer

    @classmethod
    def create_native_printer(cls) -> QtPrintSupport.QPrinter:
        printer = cls.__create_printer()

        PRINTER_RESOLUTION: int = 600

        printer.setOutputFormat(QtPrintSupport.QPrinter.OutputFormat.NativeFormat)
        printer.setResolution(PRINTER_RESOLUTION)

        return printer

    @classmethod
    def __create_printer(cls) -> QtPrintSupport.QPrinter:
        printer = QtPrintSupport.QPrinter(
            QtPrintSupport.QPrinter.PrinterMode.HighResolution
        )
        printer.setPageSize(QtGui.QPageSize.PageSizeId.A4)
        printer.setFullPage(True)
        printer.setPageMargins(QtCore.QMarginsF(0.5, 0.5, 0.5, 0.5))
        return printer
