from dataclasses import dataclass

from typing import Callable, Type


@dataclass
class Provider:
    implementation: Type | None = None
    factory: Callable | None = None
    singleton: bool = False
