from typing import Any, Generator

from ..services.readers import ILayoutReader

from ..schemas.components import UIComponent
from ..schemas.layouts import LayoutContainer, Layout, LayoutConfig


class LayoutViewModel:
    """
    This class is a ViewModel for controlling the layout
    our table widget uses.
    """

    def __init__(self, reader: ILayoutReader):
        self._layoutReader = reader

        self._layouts = None
        self._curLayout = ""

    def getLayoutValueByIndex(self, index: int, key: str) -> Any | str:
        """
        we convert our dictionary items in a list, then we returns the
        data from the dictionary based on the index of a parent key,
        by selecting the corresponding key.
        """

        layoutData = list(self.getCurrentLayoutUI().values())[index]
        return layoutData.get(key, "")

    def _getCurrentLayout(self) -> Layout:
        return self.getAllLayouts().get(self._curLayout, {})

    def getCurrentLayoutUI(self) -> dict[str, UIComponent]:
        return self._getCurrentLayout().get("user_interface", {})

    def getCurrentLayoutConfig(self) -> LayoutConfig:
        return self._getCurrentLayout().get("config", {})

    def setCurrentLayout(self, key: str):
        self._curLayout = key

    def getAllLayouts(self) -> LayoutContainer:
        if self._layouts is None:
            self._layouts = self._layoutReader.load()

        return self._layouts

    def clearLayoutState(self):
        self._curLayout = ""
        self._layouts = {}
