from typing import Any, Generator

from PySide6 import QtCore

from ..services.readers import ILayoutReader

from ..schemas.components import UIComponent
from ..schemas.layouts import LayoutContainer, Layout, LayoutConfig


class LayoutViewModel(QtCore.QObject):
    """
    This class is a ViewModel for controlling the layout
    our table widget uses.
    """

    onLayoutChanged = QtCore.Signal(str)

    def __init__(self, reader: ILayoutReader):
        super().__init__()
        self._layoutReader = reader

        self._layouts = None
        self._curLayout = ""

    def getUIValueByIndex(self, index: int, key: str, default: Any = None) -> Any:
        """
        The current layout user_interface is converted into a list
        of values, allowing indexed access to the user_interface.
        Then the requested value of a key in UIComponent is retrieved
        by the index.
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
        self.onLayoutChanged.emit(key)

    def getAllLayouts(self) -> LayoutContainer:
        if self._layouts is None:
            self._layouts = self._layoutReader.load()

        return self._layouts

    def clearLayoutState(self):
        self._curLayout = ""
        self._layouts.clear()
