import re

from ..controllers.document_controller import DocumentController


class HTMLTemplateService:
    """
    This class is responsible for working with the html template
    and cleaning our html for creation of PDFs.
    """

    def __init__(self, doc_controller: DocumentController):
        self.doc_controller = doc_controller

    def ReadHTMLFiles(self, file_to_read: str) -> dict[str, str]:
        """
        this function reads our terms html files, returning a dictionary
        containing all the html data.
        """

        tmpl_path = "./data/Templates"

        with (
            open(f"{tmpl_path}/header.html", "r", encoding="utf-8") as header_file,
            open(f"{tmpl_path}/{file_to_read}", "r", encoding="utf-8") as termo_file,
            open(f"{tmpl_path}/footer.html", "r", encoding="utf-8") as footer_file,
        ):

            html = {
                "header": header_file.read(),
                "termo": termo_file.read(),
                "footer": footer_file.read(),
            }

        return html

    def CleanHTML(self, html: dict[str, str]):
        for key in html:
            for old_str, new_str in self.doc_controller.GetInputData().items():
                html[key] = html[key].replace(old_str, new_str)

    def RemoveUnusedTemplate(self, html: dict[str, str]):
        for key in html:
            html[key] = re.sub(r"\$([a-zA-Z0-9_]+)\$", "", html[key])

    def Generate(self, file: str) -> dict[str, str]:
        """
        this function changes all the variables in our html with the correct data,
        returning a dictionary containing all cleaned html data.
        """

        html = self.ReadHTMLFiles(file)

        self.CleanHTML(html)

        # clean any variable that didn't get used
        # mostly those we put as not required
        self.RemoveUnusedTemplate(html)

        return html
