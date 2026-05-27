from typing import NamedTuple

from ..schemas.components import InputErrorMessage


class InputValidationResult(NamedTuple):
    isValid: bool
    errorMessage: InputErrorMessage | None = None
