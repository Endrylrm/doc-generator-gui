from ..services.readers import ReaderService


class LayoutStore:
    def __init__(self, reader: ReaderService):
        self.__layoutService = reader
        self.__layouts = None

    def getAllLayouts(self):
        if self.__layouts is None:
            self.__layouts = self.__layoutService.load()

        return self.__layouts
