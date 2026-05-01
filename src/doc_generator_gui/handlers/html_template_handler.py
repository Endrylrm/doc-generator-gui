import json

from ..contexts.document_context import DocumentContext


class HTMLTemplateHandler:
    """
    This class is responsible for working with the html template
    and cleaning our html for creation of PDFs.
    """

    def __init__(self, doc_context: DocumentContext):
        """
        Initialization of the HTMLTemplateHandler Class page.
        """

        self.doc_context = doc_context

        self.ReadCompanyData()

    def ReadCompanyData(self):
        """
        this function reads our company.json, adding data to our strings
        to replace dictionary, then later we use this data to replace the
        html template data and create our PDFs.
        """

        with open("company.json", "r", encoding="utf-8") as company_file:
            company_file_data = json.loads(company_file.read())

        for key in company_file_data.keys():
            replace = company_file_data[key]["replace"]
            value = company_file_data[key]["value"]
            self.doc_context.strings_to_replace[replace] = value

    def ReadHTMLFiles(self, file_to_read: str) -> dict[str, str]:
        """
        this function reads our terms html files, returning a dictionary
        containing all the html data.
        """

        with (
            open("./Templates/header.html", "r", encoding="utf-8") as header_file,
            open(f"./Templates/{file_to_read}", "r", encoding="utf-8") as termo_file,
            open("./Templates/footer.html", "r", encoding="utf-8") as footer_file,
        ):

            html = {
                "header": header_file.read(),
                "termo": termo_file.read(),
                "footer": footer_file.read(),
            }

        return html

    def Handle_HTML(self, file: str, date_text: str = "") -> dict[str, str]:
        """
        this function changes all the variables in our html with the correct data,
        returning a dictionary containing all cleaned html data.
        """

        html = self.ReadHTMLFiles(file)

        for old_string, new_string in self.doc_context.strings_to_replace.items():
            html["header"] = html["header"].replace(old_string, new_string)
            html["termo"] = html["termo"].replace(old_string, new_string)
            html["footer"] = html["footer"].replace(old_string, new_string)

        html["footer"] = html["footer"].replace("$data$", date_text)

        return html
