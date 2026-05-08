import json

from ..readers.json_reader import JsonReader


class LayoutStore:
    """
    This class is responsible for providing information on
    the layouts of our UI.
    """

    def __init__(self, path: str):
        self.__layouts = JsonReader.Load(path)
        self.__cur_layout = {}

    def GetLayout(self, key: str):
        return self.__layouts[key]

    def GetAllLayouts(self):
        return self.__layouts

    def GetValueFromLayout(self, index: int, key: str):
        """
        we convert our dictionary items in a list, then we returns the
        data from the dictionary based on the index of a parent key,
        by selecting the corresponding key.
        """

        layout_data = list(self.__cur_layout.items())[index][1]
        return layout_data[key] if key in layout_data else ""

    def GetCurrentLayout(self) -> dict:
        return self.__cur_layout

    def SetCurrentLayout(self, key: str) -> dict:
        self.__cur_layout = self.GetLayout(key)
