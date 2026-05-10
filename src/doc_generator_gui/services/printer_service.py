from PySide6 import QtGui, QtPdf, QtPrintSupport

from ..contexts.print_context import PrintContext

from ..states.document_state import DocumentState

from ..factories.printer_factory import PrinterFactory


class PrinterService:
    """
    This class is responsible for printing our documents
    physically for our employees.
    """

    def __init__(self, doc_state: DocumentState):
        self.doc_state = doc_state
        self.printer = PrinterFactory.create_native_printer()

    def PaintDocument(self):
        """
        this function is responsible to convert our pdf file in a
        image and then use a QPainter to paint to a native printer.
        """

        PDF_PRINTER_RESOLUTION: int = 600
        PAINTER_SCALE: float = 1
        START_LOCATION: list[int] = [2, 0]

        pdf_file = QtPdf.QPdfDocument()
        pdf_file.load(self.doc_state.output_path)

        size = QtGui.QPageSize.sizePixels(
            QtGui.QPageSize.PageSizeId.A4, PDF_PRINTER_RESOLUTION
        )

        with PrintContext(self.printer) as ctx:
            for cur_page in range(pdf_file.pageCount()):
                if cur_page > 0:
                    self.printer.newPage()

                page_image_from_pdf = pdf_file.render(cur_page, size)

                ctx.painter.scale(PAINTER_SCALE, PAINTER_SCALE)
                ctx.painter.translate(START_LOCATION[0], START_LOCATION[1])
                ctx.painter.drawImage(0, 0, page_image_from_pdf)

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

        if disable_print_preview:
            self.PrintDialog(print_type)
            return

        self.PrintPreviewDialog(print_type)
