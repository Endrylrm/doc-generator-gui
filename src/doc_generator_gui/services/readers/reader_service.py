import json

from typing import Protocol


class ReaderService(Protocol):
    path: str

    def Load(self): ...
