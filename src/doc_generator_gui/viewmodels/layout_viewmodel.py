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

    def getLayoutValueByIndex(
        self, index: int, key: str, default: Any = None
    ) -> Any | None:
        """
        The current layout dictionary is converted into a list of
        values, allowing indexed access to a layout entry. Then the
        requested value is retrieved from that entry by the index.
        """

        layoutData = list(self.getCurrentLayoutUI().values())[index]
        return layoutData.get(key, default)

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
        self._layouts.clear()
