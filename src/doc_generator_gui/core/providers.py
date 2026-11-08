from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Provider:
    implementation: type | None = None
    factory: Callable | None = None
    singleton: bool = False
