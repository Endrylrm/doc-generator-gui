from typing import Any

from ..states.document_state import DocumentState
from ..states.input_state import InputState

from ..stores.company_data_store import CompanyDataStore


class DocumentController:
    """
    This class is responsible for controlling our states
    that we use when printing.
    """

    def __init__(self, company_data_store: CompanyDataStore):
        self.__doc_state = DocumentState()
        self.__input_state = InputState()

        self.__company_data_store = company_data_store

        self.SetDefaultState()

    def GetInputData(self) -> dict[str, str]:
        return self.__input_state.input_data

    def GetInputHistory(self) -> dict[str, str]:
        return self.__input_state.input_history

    def GetOutputPath(self) -> str:
        return self.__doc_state.output_path

    def GetCompanyData(self) -> dict[str, str]:
        return self.__company_data_store.GetCompanyData()

    def UpdateInputData(self, key: str, value: str):
        self.__input_state.input_data[key] = value

    def UpdateInputHistory(self, key: str, value: str):
        self.__input_state.input_history[key] = value

    def MergeToInputData(self, dict_to_merge: dict[str, str]):
        self.__input_state.input_history.update(dict_to_merge)

    def SetOutputPath(self, employee_name: str, path: str):
        """
        Sets the output path for our PDF files, by getting the
        name of the employee in our table and the current type.
        """

        self.__doc_state.output_path = f"{path} - {employee_name}.pdf"

    def SetDefaultState(self):
        """
        Sets input_data with only the company data resetting
        the state to it's default value.
        """

        self.__input_state.input_data = {}

        company_data = {
            data["replace"]: data["value"] for data in self.GetCompanyData().values()
        }

        self.__input_state.input_data.update(company_data)

    def ClearInputState(self):
        self.__input_state.input_data = {}
        self.__input_state.input_history = {}

    def ClearDocumentState(self):
        self.__doc_state.output_path = ""

    def ClearAllStates(self):
        self.ClearDocumentState()
        self.ClearInputState()
