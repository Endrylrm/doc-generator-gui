from PySide6 import QtGui, QtCore, QtPdf, QtPrintSupport

from ..contexts.document_context import DocumentContext


class PrinterService:
    """
    This class is responsible for printing our documents
    physically for our employees.
    """

    def __init__(self, document_ctx: DocumentContext):
        """
        Initialization of the Printer_Service Class page.
        """

        self.document_ctx = document_ctx

        self.printer = QtPrintSupport.QPrinter(
            QtPrintSupport.QPrinter.PrinterMode.HighResolution
        )
        self.printer.setPageSize(QtGui.QPageSize.PageSizeId.A4)
        self.printer.setFullPage(True)
        self.printer.setPageMargins(QtCore.QMarginsF(0.5, 0.5, 0.5, 0.5))

    def PaintDocument(self):
        """
        this function is responsible to convert our pdf file in a
        image and then use a QPainter to paint to a native printer.
        """

        PDF_PRINTER_RESOLUTION: int = 600
        PAINTER_SCALE: float = 1
        START_LOCATION: list[int] = [2, 0]

        pdf_file = QtPdf.QPdfDocument()
        pdf_file.load(self.document_ctx.output_path)

        size = QtGui.QPageSize.sizePixels(
            QtGui.QPageSize.PageSizeId.A4, PDF_PRINTER_RESOLUTION
        )

        image_from_pdf = pdf_file.render(0, size)

        painter = QtGui.QPainter()
        painter.begin(self.printer)
        painter.scale(PAINTER_SCALE, PAINTER_SCALE)
        painter.translate(START_LOCATION[0], START_LOCATION[1])
        painter.drawImage(0, 0, image_from_pdf)
        painter.end()

    def PrintDialog(self, print_type: str):
        """
        this function is responsible for creating a print dialog.
        """

        print_dialog = QtPrintSupport.QPrintDialog(self.printer)
        print_dialog.setWindowTitle(f"Imprimir Termo de {print_type}")
        print_dialog_icon = QtGui.QIcon("gen_document.ico")
        print_dialog.setWindowIcon(print_dialog_icon)
        if print_dialog.exec() == print_dialog.DialogCode.Accepted:
            self.PaintDocument()

    def PrintPreviewDialog(self, print_type: str):
        """
        this function is responsible for creating a print dialog
        with preview.
        """

        print_preview_dialog = QtPrintSupport.QPrintPreviewDialog(self.printer)
        print_preview_dialog.setWindowTitle(f"Imprimir Termo de {print_type}")
        print_preview_dialog_icon = QtGui.QIcon("gen_document.ico")
        print_preview_dialog.setWindowIcon(print_preview_dialog_icon)
        print_preview_dialog.paintRequested.connect(self.PaintDocument)
        print_preview_dialog.exec()

    def PrintDocument(self, disable_print_preview: bool = False, print_type: str = ""):
        """
        this function is responsible to send our PDF file to a native
        printer, it uses a QPrinter to send to a native printer,
        QPrintPreviewDialog to preview or QPrintDialog for fast printing.
        """

        PRINTER_RESOLUTION: int = 607

        self.printer.setOutputFormat(QtPrintSupport.QPrinter.OutputFormat.NativeFormat)
        self.printer.setResolution(PRINTER_RESOLUTION)

        if disable_print_preview:
            self.PrintDialog(print_type)

        if not disable_print_preview:
            self.PrintPreviewDialog(print_type)
