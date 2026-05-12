from typing import Any

from ..states.layout_state import LayoutState

from ..stores.layout_store import LayoutStore


class LayoutController:
    """
    This class is responsible for controlling the layout
    our table widget uses.
    """

    def __init__(self, layout_store: LayoutStore):
        self.__layout_state = LayoutState()

        self.__layout_store = layout_store

    def GetValueFromLayout(self, index: int, key: str) -> Any | str:
        """
        we convert our dictionary items in a list, then we returns the
        data from the dictionary based on the index of a parent key,
        by selecting the corresponding key.
        """

        layout_data = list(self.__layout_state.cur_layout.items())[index][1]
        return layout_data[key] if key in layout_data else ""

    def GetCurrentLayout(self) -> dict:
        return self.__layout_state.cur_layout

    def SetCurrentLayout(self, key: str) -> dict:
        self.__layout_state.cur_layout = self.GetAllLayouts()[key]

    def GetAllLayouts(self) -> dict[str, str]:
        return self.__layout_store.GetAllLayouts()

    def ClearLayoutState(self):
        self.__layout_state.cur_layout = {}
