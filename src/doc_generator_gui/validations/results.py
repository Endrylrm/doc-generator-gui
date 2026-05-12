from dataclasses import dataclass


@dataclass(frozen=True)
class InputValidationResult:
    is_valid: bool
    error_message: str | None = None
