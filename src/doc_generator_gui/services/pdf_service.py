from PySide6 import QtGui, QtCore, QtPdf, QtPrintSupport

from ..contexts.document_context import DocumentContext

from ..constants import (
    PDF_PAINTER_SCALE,
    PDF_PRINTER_RESOLUTION,
    PDF_TEXT_WIDTH,
    HEADER_LOCATION,
    MAIN_LOCATION,
    FOOTER_LOCATION,
)


class PDFService:
    """
    This class is responsible for generating our PDFs to later
    be printed physically.
    """

    def __init__(self, doc_context: DocumentContext):
        """
        Initialization of the PDF_Service Class page.
        """

        self.doc_context = doc_context

        self.printer = QtPrintSupport.QPrinter(
            QtPrintSupport.QPrinter.PrinterMode.HighResolution
        )
        self.printer.setPageSize(QtGui.QPageSize.PageSizeId.A4)
        self.printer.setFullPage(True)
        self.printer.setPageMargins(QtCore.QMarginsF(0.5, 0.5, 0.5, 0.5))

    def PaintHTML(
        self, doc: QtGui.QTextDocument, painter: QtGui.QPainter, point: list, html: str
    ):
        """
        begin painting by changing the html in our QTextDocument,
        also translating the QPainter when necessary and call the draw
        function of our DocumentLayout to start painting.
        """

        doc_PaintCtx = doc.documentLayout().PaintContext()

        painter.translate(point[0], point[1])

        doc.setHtml(html)
        doc.documentLayout().draw(painter, doc_PaintCtx)

    def Generate(self, html_data: dict):
        """
        we use a QPrinter, QPainter and QTextdocument to generate a
        PDF file of our HTML, we scale our painter and use the function
        PaintHTML to paint the html to a new PDF file.
        """

        self.printer.setOutputFormat(QtPrintSupport.QPrinter.OutputFormat.PdfFormat)
        self.printer.setResolution(PDF_PRINTER_RESOLUTION)
        self.printer.setOutputFileName(self.doc_context.output_path)

        pdf_Doc = QtGui.QTextDocument()
        pdf_Doc.setTextWidth(PDF_TEXT_WIDTH)

        painter = QtGui.QPainter()
        painter.begin(self.printer)
        painter.scale(PDF_PAINTER_SCALE, PDF_PAINTER_SCALE)
        self.PaintHTML(pdf_Doc, painter, HEADER_LOCATION, html_data["header"])
        self.PaintHTML(pdf_Doc, painter, MAIN_LOCATION, html_data["termo"])
        self.PaintHTML(pdf_Doc, painter, FOOTER_LOCATION, html_data["footer"])
        painter.end()
