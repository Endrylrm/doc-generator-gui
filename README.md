# Gerador de termos para empresas

Esse software tem a função de gerar termos em PDF para empresas usando HTML e CSS, através do PySide6 (QT).

para iniciá-lo, use `uv run main` no seu terminal ou empacote e use o executável.

<b style="color: red;">Atenção:</b> Esse projeto que criei é com o intuito de estudar programação através da linguagem Python e me auxiliar com essa parte de termos onde estava trabalhando, não deve ser usado em produção, devido a possíveis falhas de seguranças ou bugs.

## Usando o Gerador de Termos

Esse pequeno sistema foi pensado na simplicidade, através da sua interface gráfica e na facilidade de adicionar novos layouts de termos.

![Interface Gráfica](/assets/img/gui.png "Interface Gráfica")

No momento atual a usabilidade é manual, só precisa preencher os campos com os dados e marcar as opções que deseja usar:

![Usabilidade](/assets/img/gui-using.png "Usabilidade")

Após preencher e marcar as opções desejadas, é só clicar em "Gerar Documento" e irá aparecer um visualizador de seu documento para impressão (caso não tenha marcado a opção "Desativar visualização de impressão"):

![Visualizador de impressão](/assets/img/print-preview.png "Visualizador de impressão")

## Extendendo

Layouts de impressão são criados através dos arquivos `.json` na pasta `data/layouts/` e os dados da empresa ficam no arquivo `data/company.json`.

Exemplo - `layouts.json`:

```json
{
    "Celular": {
		"user_interface": {
			"name": {
				"type": "name",
				"required": true,
				"description": "Nome do Funcionário (Obrigatório):",
				"placeholder": "Digite o nome do funcionário...",
				"error_message": "Nome do funcionário",
				"template": "name"
			},
			"cpf": {
				"type": "cpf",
				"required": true,
				"description": "CPF / CNPJ do Funcionário (Obrigatório):",
				"placeholder": "Observação: Digite apenas os números do CPF ou CNPJ, formatação automática.",
				"error_message": "CPF / CNPJ do funcionário",
				"template": "cpf"
			},
			"celular": {
				"type": "celular",
				"required": true,
				"description": "Celular do Funcionário (Obrigatório):",
				"placeholder": "Digite o Celular a ser entregue ao funcionário...",
				"error_message": "Celular do Funcionário",
				"template": "celular"
			},
			"imei1": {
				"type": "imei1",
				"required": true,
				"description": "IMEI 1 do Celular do Funcionário (Obrigatório):",
				"placeholder": "Digite o IMEI 1 do Celular a ser entregue ao funcionário...",
				"error_message": "IMEI 1 do Celular do Funcionário",
				"max_text_length": 15,
				"template": "imei1"
			},
			"imei2": {
				"type": "imei2",
				"required": true,
				"description": "IMEI 2 do Celular do Funcionário (Obrigatório):",
				"placeholder": "Digite o IMEI 2 do Celular a ser entregue ao funcionário...",
				"error_message": "IMEI 2 do Celular do Funcionário",
				"max_text_length": 15,
				"template": "imei2"
			},
			"remark": {
				"type": "remark",
				"required": false,
				"description": "Observação (Opcional):",
				"placeholder": "Digite uma observação referente a esse celular...",
				"error_message": "Observação do Celular do Funcionário",
				"template": "obs"
			}
		},
		"config": {
            "document_template": "termo_celular.html",
			"output": "./documents/Termo de Entrega de Celular"
		}
    }
}
```

## Dependências

usamos os seguintes pacotes para o sistema funcionar:
- [`PySide6`](https://doc.qt.io/qtforpython-6/index.html)
- [`Jinja2`](https://jinja.palletsprojects.com/en/stable/)
- [`playwright`](https://playwright.dev/python/)

podemos usar os seguintes pacotes para empacotarmos o sistema:
- [`Nuitka`](https://nuitka.net/)
- [`PyInstaller`](https://pyinstaller.org/en/stable/)

usamos os seguintes pacotes para criação e execução de testes:
- [`pytest`](https://docs.pytest.org/en/stable/)
- [`pytest-qt`](https://pytest-qt.readthedocs.io/en/latest/intro.html)

## Build / Deploy

se precisa criar um executável para seus usuários, usamos o [`PyInstaller`](https://pyinstaller.org/en/stable/) ou o [`Nuitka (Recomendado)`](https://nuitka.net/).

Para isso possuímos scripts, onde você irá escolher o metodo de compilação que você deseja:

<details>
<summary>Nuitka</summary>

> `uv run build_nuitka.py`

</details>

<details>
<summary>Pyinstaller</summary>

> `uv run build_pyinstaller.py`

</details>