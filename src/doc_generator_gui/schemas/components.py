from typing import TypedDict, Literal


class BaseUI(TypedDict):
    type: str


class BaseInputUI(BaseUI):
    required: bool
    description: str
    placeholder: str
    error_message: str
    replace: str


class InputUI(BaseInputUI):
    type: Literal["normal", "name", "remark"]
    max_text_length: int


class CPFInputUI(BaseInputUI):
    type: Literal["cpf"]


type UIComponent = InputUI | CPFInputUI
