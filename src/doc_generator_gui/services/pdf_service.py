from PySide6 import QtGui, QtCore, QtPdf, QtPrintSupport

from ..contexts.print_context import PrintContext

from ..states.document_state import DocumentState

from ..factories.printer_factory import PrinterFactory


class PDFService:
    """
    This class is responsible for generating our PDFs to later
    be printed physically.
    """

    def __init__(self, doc_state: DocumentState):
        self.doc_state = doc_state
        self.printer = PrinterFactory.create_pdf_printer()

    def PaintFromHTML(
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

        PDF_PAINTER_SCALE: float = 8.5
        PDF_TEXT_WIDTH: int = 530

        HEADER_LOCATION: list[int] = [0, 5]
        MAIN_LOCATION: list[int] = [30, 72]
        FOOTER_LOCATION: list[int] = [-30, 665]

        self.printer.setOutputFileName(self.doc_state.output_path)

        pdf_Doc = QtGui.QTextDocument()
        pdf_Doc.setTextWidth(PDF_TEXT_WIDTH)

        with PrintContext(self.printer) as ctx:
            ctx.painter.scale(PDF_PAINTER_SCALE, PDF_PAINTER_SCALE)
            self.PaintFromHTML(
                pdf_Doc, ctx.painter, HEADER_LOCATION, html_data["header"]
            )
            self.PaintFromHTML(pdf_Doc, ctx.painter, MAIN_LOCATION, html_data["termo"])
            self.PaintFromHTML(
                pdf_Doc, ctx.painter, FOOTER_LOCATION, html_data["footer"]
            )
