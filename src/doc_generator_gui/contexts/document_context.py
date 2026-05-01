class DocumentContext:
    """
    This class is responsible for providing context on
    data between our printing services.
    """

    def __init__(self):
        """
        Initialization of the DocumentContext Class page.
        """

        self.output_path: str = ""
        self.strings_to_replace: dict[str, str] = {}
