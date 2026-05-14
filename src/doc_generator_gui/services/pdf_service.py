from PySide6 import QtGui

from ..contexts.document_context import DocumentContext
from ..contexts.print_context import PrintContext

from ..factories.printer_factory import PrinterFactory


class PDFService:
    """
    This class is responsible for generating our PDFs to later
    be printed physically.
    """

    def __init__(self, documentContext: DocumentContext):
        self.documentContext = documentContext
        self.printer = PrinterFactory.createPrinterToPDF()

    def paintFromHTML(
        self, doc: QtGui.QTextDocument, painter: QtGui.QPainter, point: list, html: str
    ):
        """
        begin painting by changing the html in our QTextDocument,
        also translating the QPainter when necessary and call the draw
        function of our DocumentLayout to start painting.
        """

        documentPaintCtx = doc.documentLayout().PaintContext()

        painter.translate(point[0], point[1])

        doc.setHtml(html)
        doc.documentLayout().draw(painter, documentPaintCtx)

    def generate(self):
        """
        we use a QPrinter, QPainter and QTextdocument to generate a
        PDF file of our HTML, we scale our painter and use the function
        PaintHTML to paint the html to a new PDF file.
        """

        PDF_PAINTER_SCALE: float = 8.5
        PDF_TEXT_WIDTH: int = 530

        HEADER_LOCATION: list[int] = [0, 5]
        MAIN_LOCATION: list[int] = [30, 72]
        FOOTER_LOCATION: list[int] = [-30, 665]

        self.printer.setOutputFileName(self.documentContext.outputPath)

        pdfDocument = QtGui.QTextDocument()
        pdfDocument.setTextWidth(PDF_TEXT_WIDTH)

        htmlData = self.documentContext.currentHTML

        with PrintContext(self.printer) as ctx:
            ctx.painter.scale(PDF_PAINTER_SCALE, PDF_PAINTER_SCALE)
            self.paintFromHTML(
                pdfDocument, ctx.painter, HEADER_LOCATION, htmlData["header"]
            )
            self.paintFromHTML(
                pdfDocument, ctx.painter, MAIN_LOCATION, htmlData["termo"]
            )
            self.paintFromHTML(
                pdfDocument, ctx.painter, FOOTER_LOCATION, htmlData["footer"]
            )
