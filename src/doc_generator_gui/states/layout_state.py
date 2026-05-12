from dataclasses import dataclass, field


@dataclass
class LayoutState:
    """
    This class is responsible for maintaining the state
    of our UI Layout.
    """

    cur_layout: dict[str, str] = field(default_factory=dict)
