from dataclasses import dataclass, field


@dataclass
class InputState:
    """
    This class is responsible for maintaining the state
    of our inputs, so our controller can yuse them between
    our printing services.
    """

    input_data: dict[str, str] = field(default_factory=dict)
    input_history: dict[str, str] = field(default_factory=dict)
