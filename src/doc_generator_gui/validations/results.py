from typing import NamedTuple


class InputValidationResult(NamedTuple):
    isValid: bool
    errorMessage: str | None = None
