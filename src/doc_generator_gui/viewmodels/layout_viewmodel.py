from typing import Any, Generator

from ..services.readers import ReaderService


class LayoutViewModel:
    """
    This class is a ViewModel for controlling the layout
    our table widget uses.
    """

    def __init__(self, reader: ReaderService):
        self.__layoutService = reader

        self.__layouts = None
        self.__curLayout = {}

    def getValueFromLayout(self, index: int, key: str) -> Any | str:
        """
        we convert our dictionary items in a list, then we returns the
        data from the dictionary based on the index of a parent key,
        by selecting the corresponding key.
        """

        layoutData = list(self.__curLayout.items())[index][1]
        return layoutData[key] if key in layoutData else ""

    def getCurrentLayout(self) -> dict:
        return self.__curLayout

    def setCurrentLayout(self, key: str) -> dict:
        self.__curLayout = self.getAllLayouts()[key]

    def getAllLayouts(self) -> dict[str, str]:
        if self.__layouts is None:
            self.__layouts = self.__layoutService.load()

        return self.__layouts

    def filterCurrentLayout(self) -> Generator[str]:
        filteredKeys = (key for key in self.__curLayout if key != "config")
        return filteredKeys

    def clearLayoutState(self):
        self.__curLayout = {}
        self.__layouts = {}
