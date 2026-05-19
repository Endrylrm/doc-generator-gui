from typing import TypedDict

from .components import UIComponent


class LayoutConfig(TypedDict):
    template: str
    output: str


class Layout(TypedDict):
    user_interface: dict[str, UIComponent]
    config: LayoutConfig


class LayoutContainer(TypedDict):
    layouts: dict[str, Layout]
