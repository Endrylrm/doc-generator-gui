from ..services.readers import LayoutService


class LayoutStore:
    def __init__(self):
        self.__layoutService = LayoutService("data/layouts.json")
        self.__layouts = None

    def getAllLayouts(self):
        if self.__layouts is None:
            self.__layouts = self.__layoutService.load()

        return self.__layouts
