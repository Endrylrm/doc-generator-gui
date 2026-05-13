from typing import Any, Generator

from ..states.layout_state import LayoutState

from ..stores.layout_store import LayoutStore


class LayoutController:
    """
    This class is responsible for controlling the layout
    our table widget uses.
    """

    def __init__(self, layoutStore: LayoutStore):
        self.__layoutState = LayoutState()

        self.__layoutStore = layoutStore

    def getValueFromLayout(self, index: int, key: str) -> Any | str:
        """
        we convert our dictionary items in a list, then we returns the
        data from the dictionary based on the index of a parent key,
        by selecting the corresponding key.
        """

        layoutData = list(self.__layoutState.curLayout.items())[index][1]
        return layoutData[key] if key in layoutData else ""

    def getCurrentLayout(self) -> dict:
        return self.__layoutState.curLayout

    def setCurrentLayout(self, key: str) -> dict:
        self.__layoutState.curLayout = self.getAllLayouts()[key]

    def getAllLayouts(self) -> dict[str, str]:
        return self.__layoutStore.getAllLayouts()

    def filterCurrentLayout(self) -> Generator[str]:
        filteredKeys = (key for key in self.__layoutState.curLayout if key != "config")
        return filteredKeys

    def clearLayoutState(self):
        self.__layoutState.curLayout = {}
