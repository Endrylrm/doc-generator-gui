import re

from ..controllers.document_controller import DocumentController


class HTMLTemplateService:
    """
    This class is responsible for working with the html template
    and cleaning our html for creation of PDFs.
    """

    def __init__(self, documentController: DocumentController):
        self.documentController = documentController

    def readHTMLFiles(self, fileToRead: str) -> dict[str, str]:
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

            html = {
                "header": headerFile.read(),
                "termo": termoFile.read(),
                "footer": footerFile.read(),
            }

        return html

    def buildCleanHTML(self, html: dict[str, str]):
        for key in html:
            for oldString, newString in self.documentController.getInputData().items():
                html[key] = html[key].replace(oldString, newString)

    def removeUnusedTemplate(self, html: dict[str, str]):
        for key in html:
            html[key] = re.sub(r"\$([a-zA-Z0-9_]+)\$", "", html[key])

    def parse(self, file: str) -> dict[str, str]:
        """
        this function changes all the variables in our html with the correct data,
        returning a dictionary containing all cleaned html data.
        """

        html = self.readHTMLFiles(file)

        self.buildCleanHTML(html)

        # clean any variable that didn't get used
        # mostly those we put as not required
        self.removeUnusedTemplate(html)

        return html
