import re

from ..contexts.document_context import DocumentContext


class HTMLTemplateService:
    """
    This class is responsible for working with the html template
    and cleaning our html for creation of PDFs.
    """

    def __init__(self, documentContext: DocumentContext):
        self.documentContext = documentContext

    def buildCleanHTML(self, html: dict[str, str], input_data: dict[str, str]):
        for key in html:
            for oldString, newString in input_data.items():
                html[key] = html[key].replace(oldString, newString)

    def removeUnusedTemplate(self, html: dict[str, str]):
        for key in html:
            html[key] = re.sub(r"\$([a-zA-Z0-9_]+)\$", "", html[key])

    def parse(self, input_data: dict[str, str]):
        """
        this function changes all the variables in our html with the correct data,
        returning a dictionary containing all cleaned html data.
        """

        self.buildCleanHTML(self.documentContext.currentHTML, input_data)

        # clean any variable that didn't get used
        # mostly those we put as not required
        self.removeUnusedTemplate(self.documentContext.currentHTML)

        return self.documentContext.currentHTML
