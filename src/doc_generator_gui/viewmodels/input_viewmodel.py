from typing import Any

from PySide6 import QtCore

from ..services.readers import ICompanyReader


class InputViewModel(QtCore.QObject):
    """
    This class is a ViewModel for managing our inputs
    state that we use before printing.
    """

    onInputDataChanged = QtCore.Signal(str, str)
    onInputHistoryChanged = QtCore.Signal(str, str)

    def __init__(self, reader: ICompanyReader):
        super().__init__()
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

    def setInputData(self, key: str, value: str):
        self._inputData[key] = value

    def setInputHistory(self, key: str, value: str):
        self._inputHistory[key] = value

    def setDefaultState(self):
        """
        Sets input_data with only the company data resetting
        the state to it's default value.
        """

        if not self._inputData:
            # we load the company data on the first time.
            self._inputData.update(self.getCompanyData())
            return

        # slice everything, except the company data
        self._inputData = dict(list(self._inputData.items())[:9])

    def clearInputState(self):
        self._inputData.clear()
        self._inputHistory.clear()
