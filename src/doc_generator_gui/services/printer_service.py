from PySide6 import QtGui, QtPdf, QtPrintSupport

from ..contexts.document_context import DocumentContext
from ..contexts.print_context import PrintContext

from ..factories.printer_factory import PrinterFactory


class PrinterService:
    """
    This class is responsible for printing our documents
    physically for our employees.
    """

    def __init__(self, documentContext: DocumentContext):
        self._documentContext = documentContext
        self.printer = PrinterFactory.createPrinterToNative()

    def paintDocument(self):
        """
        this function is responsible to convert our pdf file in a
        image and then use a QPainter to paint to a native printer.
        """

        PDF_PRINTER_RESOLUTION: int = 600
        PAINTER_SCALE: float = 1
        START_LOCATION: list[int] = [2, 0]

        pdfFile = QtPdf.QPdfDocument()
        pdfFile.load(self._documentContext.outputPath)

        size = QtGui.QPageSize.sizePixels(
            QtGui.QPageSize.PageSizeId.A4, PDF_PRINTER_RESOLUTION
        )

        with PrintContext(self.printer) as ctx:
            for curPage in range(pdfFile.pageCount()):
                if curPage > 0:
                    self.printer.newPage()

                pageImageFromPDF = pdfFile.render(curPage, size)

                ctx.painter.scale(PAINTER_SCALE, PAINTER_SCALE)
                ctx.painter.translate(START_LOCATION[0], START_LOCATION[1])
                ctx.painter.drawImage(0, 0, pageImageFromPDF)

    def printDialog(self):
        """
        this function is responsible for creating a print dialog.
        """

        printDialog = QtPrintSupport.QPrintDialog(self.printer)
        printDialog.setWindowTitle(
            f"Imprimir termo de {self._documentContext.printType}"
        )
        printDialogIcon = QtGui.QIcon("gen_document.ico")
        printDialog.setWindowIcon(printDialogIcon)
        if printDialog.exec() == printDialog.DialogCode.Accepted:
            self.paintDocument()

    def printPreviewDialog(self):
        """
        this function is responsible for creating a print dialog
        with preview.
        """

        printPreviewDialog = QtPrintSupport.QPrintPreviewDialog(self.printer)
        printPreviewDialog.setWindowTitle(
            f"Imprimir termo de {self._documentContext.printType}"
        )
        printPreviewDialogIcon = QtGui.QIcon("gen_document.ico")
        printPreviewDialog.setWindowIcon(printPreviewDialogIcon)
        printPreviewDialog.paintRequested.connect(self.paintDocument)
        printPreviewDialog.exec()

    def print(self, disablePrintPreview: bool = False):
        """
        this function is responsible to send our PDF file to a native
        printer, it uses a QPrinter to send to a native printer,
        QPrintPreviewDialog to preview or QPrintDialog for fast printing.
        """

        if disablePrintPreview:
            self.printDialog()
            return

        self.printPreviewDialog()
