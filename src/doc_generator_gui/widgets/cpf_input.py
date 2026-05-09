from PySide6 import QtWidgets


class CpfInput(QtWidgets.QLineEdit):
    """
    This widget is responsible for the CPF/CNPJ input
    formatting while typing.
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setPlaceholderText(
            "Observação: Digite apenas os números do CPF ou CNPJ, formatação automática."
        )
        self.textEdited.connect(self.format_text)
        self.setMaxLength(18)

    def format_text(self):
        cursor = self.cursorPosition()

        # Remove any non-digit characters
        text = "".join(filter(str.isdecimal, self.text()))

        # limit to 14 digits
        text = text[:14]

        # correct cursor position, slice before filtering
        digits_before_cursor = len("".join(filter(str.isdecimal, self.text()[:cursor])))

        # Format as a common format for both CPF and CNPJ (e.g., 123.456.789-01 or 12.345.678/9012-34)
        formatted = (
            self.format_as_cpf(text) if len(text) <= 11 else self.format_as_cnpj(text)
        )

        self.setText(formatted)

        new_cursor = self.cursor_from_digits(formatted, digits_before_cursor)
        self.setCursorPosition(new_cursor)

    def format_as_cpf(self, text: str) -> str:
        if len(text) >= 4:
            text = f"{text[:3]}.{text[3:]}"
        if len(text) >= 8:
            text = f"{text[:7]}.{text[7:]}"
        if len(text) >= 12:
            text = f"{text[:11]}-{text[11:]}"
        return text

    def format_as_cnpj(self, text: str) -> str:
        if len(text) >= 3:
            text = f"{text[:2]}.{text[2:]}"
        if len(text) >= 7:
            text = f"{text[:6]}.{text[6:]}"
        if len(text) >= 11:
            text = f"{text[:10]}/{text[10:]}"
        if len(text) >= 16:
            text = f"{text[:15]}-{text[15:]}"
        return text

    def cursor_from_digits(self, formatted: str, digits_count: int) -> int:
        if digits_count <= 0:
            return 0

        count = 0

        for index, char in enumerate(formatted):
            if char.isdecimal():
                count += 1
            if count >= digits_count:
                return index + 1

        return len(formatted)
