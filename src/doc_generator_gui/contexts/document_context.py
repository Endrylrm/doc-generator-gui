import json


class DocumentContext:
    """
    This class is responsible for providing context on
    data between our printing services.
    """

    def __init__(self):
        self.output_path: str = ""
        self.strings_to_replace: dict[str, str] = {}
