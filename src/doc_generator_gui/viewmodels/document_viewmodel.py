from ..contexts.document_context import DocumentContext


class DocumentViewModel:
    """
    This class is a ViewModel for controlling our document
    state that we use when printing.
    """

    def __init__(self):
        self.__documentContext = DocumentContext()

    def readHTMLFiles(self, fileToRead: str):
        """
        this function reads our terms html files, returning a dictionary
        containing all the html data.
        """

        tmplPath = "./data/Templates"

        with (
            open(f"{tmplPath}/header.html", "r", encoding="utf-8") as headerFile,
            open(f"{tmplPath}/{fileToRead}", "r", encoding="utf-8") as termoFile,
            open(f"{tmplPath}/footer.html", "r", encoding="utf-8") as footerFile,
        ):

            self.documentContext.currentHTML = {
                "header": headerFile.read(),
                "termo": termoFile.read(),
                "footer": footerFile.read(),
            }

    def getContext(self) -> DocumentContext:
        return self.__documentContext

    def getPrintType(self) -> str:
        return self.__documentContext.printType

    def setPrintType(self, printType: str) -> str:
        self.__documentContext.printType = printType

    def getOutputPath(self) -> str:
        return self.__documentContext.outputPath

    def setOutputPath(self, employeeName: str, path: str):
        """
        Sets the output path for our PDF files, by getting the
        name of the employee in our table and the current type.
        """

        self.__documentContext.outputPath = f"{path} - {employeeName}.pdf"

    def clearDocumentState(self):
        self.__documentContext.outputPath = ""
        self.__documentContext.currentHTML = {}
