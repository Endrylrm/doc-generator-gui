from dataclasses import dataclass, field


@dataclass
class LayoutState:
    """
    This class is responsible for maintaining the state
    of our table widget Layout, so our controller can easily
    change the table layout.
    """

    cur_layout: dict[str, str] = field(default_factory=dict)
