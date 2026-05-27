from typing import TypedDict, Literal


class InputErrorMessage(TypedDict):
    window_title: str
    title_text: str
    info_text: str


class BaseUI(TypedDict):
    type: str


class BaseInputUI(BaseUI):
    required: bool
    description: str
    placeholder: str
    error_message: InputErrorMessage
    template: str


class InputUI(BaseInputUI):
    max_text_length: int


class CPFInputUI(BaseInputUI):
    type: Literal["cpf"]


type UIComponent = InputUI | CPFInputUI
