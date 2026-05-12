from dataclasses import dataclass, field


@dataclass
class DocumentState:
    """
    This class is responsible for maintaining the state data
    for our controller to use between our printing services.
    """

    output_path: str = ""
