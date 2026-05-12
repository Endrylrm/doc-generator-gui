from dataclasses import dataclass


@dataclass(frozen=True)
class InputValidationResult:
    isValid: bool
    errorMessage: str | None = None
