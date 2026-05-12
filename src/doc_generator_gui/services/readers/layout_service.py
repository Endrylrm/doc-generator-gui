import json

from .reader_service import ReaderService


class LayoutService(ReaderService):
    """
    This class is responsible for providing information on
    the layouts of our UI.
    """

    def __init__(self, path: str):
        self.path = path

    def Load(self):
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)
