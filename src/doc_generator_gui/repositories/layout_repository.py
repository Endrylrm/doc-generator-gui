import json


class LayoutRepository:
    """
    This class is responsible for providing information on
    the layouts of our UI.
    """

    def __init__(self, path: str):
        self.__layouts = self.__LoadLayouts(path)

    def GetLayout(self, key: str):
        return self.__layouts[key]

    def GetAllLayouts(self):
        return self.__layouts

    def GetValueFromLayout(self, cur_layout: dict, index: int, key: str):
        """
        we convert our dictionary items in a list, then we returns the
        data from the dictionary based on the index of a parent key,
        by selecting the corresponding key.
        """

        layout_data = list(cur_layout.items())[index][1]
        return layout_data[key] if key in layout_data else ""

    def __LoadLayouts(self, path: str) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
