from typing import Any

from ..states.document_state import DocumentState
from ..states.input_state import InputState
from ..states.layout_state import LayoutState

from ..stores.layout_store import LayoutStore
from ..stores.company_data_store import CompanyDataStore


class DocumentController:
    """
    This class is responsible for controlling our states
    that we use when printing.
    """

    def __init__(self, layout_store: LayoutStore, company_data_store: CompanyDataStore):
        self.__doc_state = DocumentState()
        self.__input_state = InputState()
        self.__layout_state = LayoutState()

        self.__layout_store = layout_store
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

    def SetOutputPath(self, employee_name: str, is_device_return: bool):
        """
        Sets the output path for our PDF files, by getting the
        name of the employee in our table and the current type.
        """
        default_path = (
            self.GetCurrentLayout()["config"]["output_devol"]
            if is_device_return
            else self.GetCurrentLayout()["config"]["output"]
        )

        self.__doc_state.output_path = f"{default_path} - {employee_name}.pdf"

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

    def GetValueFromLayout(self, index: int, key: str) -> Any | str:
        """
        we convert our dictionary items in a list, then we returns the
        data from the dictionary based on the index of a parent key,
        by selecting the corresponding key.
        """

        layout_data = list(self.__layout_state.cur_layout.items())[index][1]
        return layout_data[key] if key in layout_data else ""

    def GetCurrentLayout(self) -> dict:
        return self.__layout_state.cur_layout

    def SetCurrentLayout(self, key: str) -> dict:
        self.__layout_state.cur_layout = self.GetAllLayouts()[key]

    def GetAllLayouts(self) -> dict[str, str]:
        return self.__layout_store.GetAllLayouts()

    def ClearInputState(self):
        self.__input_state.input_data = {}
        self.__input_state.input_history = {}

    def ClearDocumentState(self):
        self.__doc_state.output_path = ""

    def ClearLayoutState(self):
        self.__layout_state.cur_layout = {}

    def ClearAllStates(self):
        self.ClearDocumentState()
        self.ClearInputState()
        self.ClearLayoutState()
