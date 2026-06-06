import os

from PySide6 import QtCore

from ..contexts.document_context import DocumentContext

from ..services.template_engine_service import TemplateEngineService
from ..services.pdf_service import PDFService
from ..services.printer_service import PrinterService


class DocumentViewModel(QtCore.QObject):
    """
    This class is a ViewModel for controlling our document
    state that we use when printing.
    """

    onPrintTypeChanged = QtCore.Signal(str)
    onOutputChanged = QtCore.Signal(str)

    def __init__(
        self,
        documentContext: DocumentContext,
        tmplEngineService: TemplateEngineService,
        pdfService: PDFService,
        printerService: PrinterService,
    ):
        super().__init__()
        self._documentContext = documentContext

        self._tmplEngineService = tmplEngineService
        self._pdfService = pdfService
        self._printerService = printerService

    def parseHTML(self, fileToRead: str, input_data: dict[str, str]):
        self._tmplEngineService.render(fileToRead, input_data)

    def generatePDF(self):
        self._pdfService.generate()

    def sendToPrinter(self, disablePrintPreview: bool = False):
        self._printerService.print(disablePrintPreview)

    def getContext(self) -> DocumentContext:
        return self._documentContext

    def getPrintType(self) -> str:
        return self._documentContext.printType

    def setPrintType(self, printType: str) -> str:
        self._documentContext.printType = printType
        self.onPrintTypeChanged.emit(printType)

    def getOutputPath(self) -> str:
        return self._documentContext.outputPath

    def setOutputPath(self, employeeName: str, path: str):
        """
        Sets the output path for our PDF files, by getting the
        name of the employee in our table and the current type.
        """

        self._documentContext.outputPath = f"{path} - {employeeName}.pdf"
        self.onOutputChanged.emit(self._documentContext.outputPath)

    def setDefaultState(self):
        self._documentContext.outputPath = ""
        self._documentContext.currentHTML = ""

    def clearDocumentState(self):
        self._documentContext.printType = ""
        self._documentContext.outputPath = ""
        self._documentContext.currentHTML = ""
