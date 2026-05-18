from typing import Any, Generator

from ..services.readers import ILayoutReader


class LayoutViewModel:
    """
    This class is a ViewModel for controlling the layout
    our table widget uses.
    """

    def __init__(self, reader: ILayoutReader):
        self._layoutReader = reader

        self._layouts = None
        self._curLayout = ""

    def getValueFromLayout(self, index: int, key: str) -> Any | str:
        """
        we convert our dictionary items in a list, then we returns the
        data from the dictionary based on the index of a parent key,
        by selecting the corresponding key.
        """

        layoutData = list(self.getCurrentLayout().items())[index][1]
        return layoutData.get(key, "")

    def getCurrentLayout(self) -> dict[str, Any]:
        return self.getAllLayouts().get(self._curLayout)

    def setCurrentLayout(self, key: str):
        self._curLayout = key

    def getAllLayouts(self) -> dict[str, Any]:
        if self._layouts is None:
            self._layouts = self._layoutReader.load()

        return self._layouts

    def filterCurrentLayout(self) -> Generator[str]:
        filteredKeys = (key for key in self.getCurrentLayout() if key != "config")
        return filteredKeys

    def clearLayoutState(self):
        self._curLayout = ""
        self._layouts = {}
