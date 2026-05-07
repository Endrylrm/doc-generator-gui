import json

from ..contexts.document_context import DocumentContext


class CompanyDataLoader:
    """
    This class is responsible for loading the company
    data to our context.
    """

    def __init__(self, path: str, document_ctx: DocumentContext):
        self.path = path
        self.document_ctx = document_ctx

    def load(self):
        with open(self.path, "r", encoding="utf-8") as file:
            company_data = json.loads(file.read())

        for key in company_data.keys():
            replace = company_data[key]["replace"]
            value = company_data[key]["value"]
            self.document_ctx.strings_to_replace[replace] = value
