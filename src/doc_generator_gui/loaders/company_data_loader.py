import json

from ..states.document_state import DocumentState


class CompanyDataLoader:
    """
    This class is responsible for loading the company
    data to our State.
    """

    def __init__(self, path: str, doc_state: DocumentState):
        self.path = path
        self.doc_state = doc_state

    def Load(self):
        with open(self.path, "r", encoding="utf-8") as file:
            company_data = json.loads(file.read())

        for key in company_data.keys():
            replace = company_data[key]["replace"]
            value = company_data[key]["value"]
            self.doc_state.strings_to_replace[replace] = value
