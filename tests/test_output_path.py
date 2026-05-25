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


def test_output_path():
    assert (
        OutputPath(True, "Cartucho", "TESTE")
        == "./Termos/Termo de Devolução de Cartucho - TESTE.pdf"
    )
