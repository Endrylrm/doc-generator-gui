from typing import Any

from ..services.readers import ICompanyReader


class InputViewModel:
    """
    This class is a ViewModel for managing our inputs
    state that we use before printing.
    """

    def __init__(self, reader: ICompanyReader):
        self._companyDataReader = reader

        self._inputData = {}
        self._inputHistory = {}

        self.setDefaultState()

    def getInputData(self) -> dict[str, str]:
        return self._inputData

    def getInputHistory(self) -> dict[str, str]:
        return self._inputHistory

    def getCompanyData(self) -> dict[str, str]:
        companyData = self._companyDataReader.load()

        return companyData

    def updateInputData(self, key: str, value: str):
        self._inputData[key] = value

    def updateInputHistory(self, key: str, value: str):
        self._inputHistory[key] = value

    def setDefaultState(self):
        """
        Sets input_data with only the company data resetting
        the state to it's default value.
        """

        if not self._inputData:
            # we load the company data on the first time.
            companyData = {
                data["replace"]: data["value"]
                for data in self.getCompanyData().values()
            }

            self._inputData.update(companyData)
            return

        # slice everything, except the company data
        self._inputData = dict(list(self._inputData.items())[:9])

    def clearInputState(self):
        self._inputData = {}
        self._inputHistory = {}
