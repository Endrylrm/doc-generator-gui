import json

from typing import Protocol


class ReaderService(Protocol):
    def load(self): ...


class LayoutJsonService(ReaderService):
    """
    This class is responsible for providing information on
    the layouts of our UI.
    """

    def __init__(self, path: str):
        self.path = path

    def load(self):
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)


class CompanyJsonService(ReaderService):
    """
    This class is responsible for providing information on
    the company data.
    """

    def __init__(self, path: str):
        self.path = path

    def load(self):
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)
