# PySide 6 stuff
from PySide6 import QtWidgets


class Cpf_Input(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        QtWidgets.QLineEdit.__init__(self, parent=parent)
        self.setPlaceholderText("Observação: Digitar só números, formata automaticamente.")
        self.textChanged.connect(self.format_text)
        self.setMaxLength(18)

    def format_text(self):
        # Get the current text from the QLineEdit
        text = self.text()

        # Remove any non-digit characters
        text = "".join(filter(str.isdigit, text))

        # Format as a common format for both CPF and CNPJ (e.g., 123.456.789-01 or 12.345.678/9012-34)
        if len(text) <= 11:
            # Format as CPF
            if len(text) >= 4:
                text = f"{text[:3]}.{text[3:]}"
            if len(text) >= 8:
                text = f"{text[:7]}.{text[7:]}"
            if len(text) >= 12:
                text = f"{text[:11]}-{text[11:]}"
        else:
            # Format as CNPJ
            if len(text) >= 3:
                text = f"{text[:2]}.{text[2:]}"
            if len(text) >= 7:
                text = f"{text[:6]}.{text[6:]}"
            if len(text) >= 11:
                text = f"{text[:10]}/{text[10:]}"
            if len(text) >= 16:
                text = f"{text[:15]}-{text[15:]}"

        # Set the formatted text back to the QLineEdit
        self.setText(text)
