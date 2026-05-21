import json

from pathlib import Path
from typing import Protocol

from ..schemas.layouts import LayoutContainer


class ILayoutReader(Protocol):
    def load(self) -> LayoutContainer: ...


class ICompanyReader(Protocol):
    def load(self) -> dict[str, str]: ...


class LayoutJsonReader(ILayoutReader):
    """
    This class is responsible for providing information on
    the layouts of our UI.
    """

    def __init__(self, path: str):
        self.path = path

    def load(self) -> LayoutContainer:
        data = {}

        for file in Path(self.path).glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                fileJson = json.load(f)
                data.update(fileJson)

        return data


class CompanyJsonReader(ICompanyReader):
    """
    This class is responsible for providing information on
    the company data.
    """

    def __init__(self, path: str):
        self.path = path

    def load(self) -> dict[str, str]:
        with open(self.path, "r", encoding="utf-8") as file:
            return self._normalizeData(json.load(file))

    def _normalizeData(self, data: dict) -> dict[str, str]:
        normalized = {data[key]["template"]: data[key]["value"] for key in data}

        return normalized
