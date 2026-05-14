from PySide6 import QtWidgets


class CpfInput(QtWidgets.QLineEdit):
    """
    This widget is responsible for the CPF/CNPJ input
    formatting while typing.
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.textEdited.connect(self.formatText)
        self.setMaxLength(18)

    def formatText(self):
        cursor = self.cursorPosition()

        # Remove any non-digit characters and limit to 14 characters
        text = "".join(filter(str.isdecimal, self.text()))[:14]

        # correct cursor position, slice before filtering
        digitsBeforeCursor = len("".join(filter(str.isdecimal, self.text()[:cursor])))

        # Format as a common format for both CPF and CNPJ (e.g., 123.456.789-01 or 12.345.678/9012-34)
        formatted = (
            self.formatAsCPF(text) if len(text) <= 11 else self.formatAsCNPJ(text)
        )

        self.setText(formatted)

        newCursor = self.cursorFromDigits(formatted, digitsBeforeCursor)
        self.setCursorPosition(newCursor)

    def formatAsCPF(self, text: str) -> str:
        if len(text) >= 4:
            text = f"{text[:3]}.{text[3:]}"
        if len(text) >= 8:
            text = f"{text[:7]}.{text[7:]}"
        if len(text) >= 12:
            text = f"{text[:11]}-{text[11:]}"
        return text

    def formatAsCNPJ(self, text: str) -> str:
        if len(text) >= 3:
            text = f"{text[:2]}.{text[2:]}"
        if len(text) >= 7:
            text = f"{text[:6]}.{text[6:]}"
        if len(text) >= 11:
            text = f"{text[:10]}/{text[10:]}"
        if len(text) >= 16:
            text = f"{text[:15]}-{text[15:]}"
        return text

    def cursorFromDigits(self, formatted: str, digitsCount: int) -> int:
        if digitsCount <= 0:
            return 0

        count = 0

        for index, char in enumerate(formatted):
            if char.isdecimal():
                count += 1
            if count >= digitsCount:
                return index + 1

        return len(formatted)
