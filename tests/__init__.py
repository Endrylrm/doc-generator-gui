import unittest


def OutputPath(
    devolucao: bool,
    print_type_combobox: str,
    input_employee_name: str,
) -> str:
    if not devolucao:
        output: str = (
            f"./Termos/Termo de Entrega de {print_type_combobox} - "
            + input_employee_name
            + ".pdf"
        )
    else:
        output: str = (
            f"./Termos/Termo de Devolução de {print_type_combobox} - "
            + input_employee_name
            + ".pdf"
        )

    return output


def format_as_cpf_or_cnpj(cpf_or_cnpj: str):
    # Get the current text from the QLineEdit
    text = cpf_or_cnpj

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

    return text


class TestMethods(unittest.TestCase):
    def test_output_path(self):
        self.assertEqual(
            OutputPath(True, "Cartucho", "TESTE"),
            "./Termos/Termo de Devolução de Cartucho - TESTE.pdf",
        )

    def test_cpf(self):
        self.assertEqual(
            format_as_cpf_or_cnpj("00000000000"),
            "000.000.000-00",
        )

    def test_cnpj(self):
        self.assertEqual(
            format_as_cpf_or_cnpj("00000000000000"),
            "00.000.000/0000-00",
        )


if __name__ == "__main__":
    unittest.main()
