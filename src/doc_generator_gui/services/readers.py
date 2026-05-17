import json

from typing import Protocol


class ILayoutReader(Protocol):
    def load(self) -> dict[str, str]: ...


class ICompanyReader(Protocol):
    def load(self) -> dict[str, str]: ...


class LayoutJsonReader(ILayoutReader):
    """
    This class is responsible for providing information on
    the layouts of our UI.
    """

    def __init__(self, path: str):
        self.path = path

    def load(self) -> dict[str, str]:
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)


class CompanyJsonReader(ICompanyReader):
    """
    This class is responsible for providing information on
    the company data.
    """

    def __init__(self, path: str):
        self.path = path

    def load(self) -> dict[str, str]:
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)
