from typing import Any

from ..services.readers import ReaderService


class InputViewModel:
    """
    This class is a ViewModel for managing our inputs
    state that we use before printing.
    """

    def __init__(self, reader: ReaderService):
        self.__companyDataService = reader

        self.__inputData = {}
        self.__inputHistory = {}

        self.setDefaultState()

    def getInputData(self) -> dict[str, str]:
        return self.__inputData

    def getInputHistory(self) -> dict[str, str]:
        return self.__inputHistory

    def getCompanyData(self) -> dict[str, str]:
        companyData = self.__companyDataService.load()

        return companyData

    def updateInputData(self, key: str, value: str):
        self.__inputData[key] = value

    def updateInputHistory(self, key: str, value: str):
        self.__inputHistory[key] = value

    def mergeToInputData(self, dictToMerge: dict[str, str]):
        self.__inputData.update(dictToMerge)

    def mergeToInputHistory(self, dictToMerge: dict[str, str]):
        self.__inputHistory.update(dictToMerge)

    def setDefaultState(self):
        """
        Sets input_data with only the company data resetting
        the state to it's default value.
        """

        if self.__inputData:
            # slice everything, except the company data
            self.__inputData = dict(list(self.__inputData.items())[:9])
            return

        # we load the company data on the first time.
        companyData = {
            data["replace"]: data["value"] for data in self.getCompanyData().values()
        }

        self.__inputData.update(companyData)

    def clearInputState(self):
        self.__inputData = {}
        self.__inputHistory = {}
