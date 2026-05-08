from dataclasses import dataclass, field


@dataclass
class DocumentState:
    """
    This class is responsible for maintaining the state
    data between our printing services.
    """

    output_path: str = ""
    strings_to_replace: dict[str, str] = field(default_factory=dict)
    input_history: dict[str, str] = field(default_factory=dict)
