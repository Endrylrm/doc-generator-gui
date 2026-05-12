from typing import Any

from ..states.document_state import DocumentState
from ..states.input_state import InputState

from ..stores.company_data_store import CompanyDataStore


class DocumentController:
    """
    This class is responsible for controlling our states
    that we use when printing.
    """

    def __init__(self, companyDataStore: CompanyDataStore):
        self.__documentState = DocumentState()
        self.__inputState = InputState()

        self.__companyDataStore = companyDataStore

        self.setDefaultState()

    def getInputData(self) -> dict[str, str]:
        return self.__inputState.inputData

    def getInputHistory(self) -> dict[str, str]:
        return self.__inputState.inputHistory

    def getOutputPath(self) -> str:
        return self.__documentState.outputPath

    def getCompanyData(self) -> dict[str, str]:
        return self.__companyDataStore.getCompanyData()

    def updateInputData(self, key: str, value: str):
        self.__inputState.inputData[key] = value

    def updateInputHistory(self, key: str, value: str):
        self.__inputState.inputHistory[key] = value

    def mergeToInputData(self, dictToMerge: dict[str, str]):
        self.__inputState.inputData.update(dictToMerge)

    def mergeToInputHistory(self, dictToMerge: dict[str, str]):
        self.__inputState.inputHistory.update(dictToMerge)

    def setOutputPath(self, employeeName: str, path: str):
        """
        Sets the output path for our PDF files, by getting the
        name of the employee in our table and the current type.
        """

        self.__documentState.outputPath = f"{path} - {employeeName}.pdf"

    def setDefaultState(self):
        """
        Sets input_data with only the company data resetting
        the state to it's default value.
        """

        self.__inputState.inputData = {}

        companyData = {
            data["replace"]: data["value"] for data in self.getCompanyData().values()
        }

        self.__inputState.inputData.update(companyData)

    def clearInputState(self):
        self.__inputState.inputData = {}
        self.__inputState.inputHistory = {}

    def clearDocumentState(self):
        self.__documentState.outputPath = ""

    def clearAllStates(self):
        self.clearDocumentState()
        self.clearInputState()
