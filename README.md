# Gerador de termos para empresas

Esse software tem a função de gerar termos em PDF para empresas usando HTML e CSS, através do PySide6 (QT).

<b style="color: red;">Atenção:</b> Esse projeto que criei é com o intuito de estudar programação através da linguagem Python e me auxiliar com essa parte de termos onde estava trabalhando, não deve ser usado em produção, devido a possíveis falhas de seguranças ou bugs.

## 👨‍💻 Usando o Gerador de Termos

Esse pequeno sistema foi pensado na simplicidade, através da sua interface gráfica e na facilidade de adicionar novos layouts de termos.

![Interface Gráfica](/assets/img/gui.png "Interface Gráfica")

No momento atual a usabilidade é manual, só precisa preencher os campos com os dados e marcar as opções que quiser usar:

![Usabilidade](/assets/img/gui-using.png "Usabilidade")

Após preencher e marcar as opções desejadas, é só clicar em "Gerar Documento" e irá aparecer um visualizador de seu documento para impressão (caso não tenha marcado a opção "Desativar visualização de impressão"):

![Visualizador de impressão](/assets/img/print-preview.png "Visualizador de impressão")

## 💻 Extendendo

Layouts de impressão são criados através dos arquivos `.json` na pasta `data/layouts/` e os dados da empresa ficam no arquivo `data/company.json`.

Exemplo - `layouts.json`:

```json
{
    "Celular": {
		"user_interface": {
			"nome": {
				"type": "name",
				"required": true,
				"description": "Nome do Funcionário (Obrigatório):",
				"placeholder": "Digite o nome do funcionário...",
				"error_message": "Nome do funcionário",
				"template": "$name$"
			},
			"cpf": {
				"type": "cpf",
				"required": true,
				"description": "CPF / CNPJ do Funcionário (Obrigatório):",
				"placeholder": "Observação: Digite apenas os números do CPF, formatação automática.",
				"error_message": "CPF / CNPJ do funcionário",
				"template": "$cpf$"
			},
			"celular": {
				"type": "normal",
				"required": true,
				"description": "Celular do Funcionário (Obrigatório):",
				"placeholder": "Digite o Celular a ser entregue ao funcionário...",
				"error_message": "Celular do Funcionário",
				"template": "$celular$"
			},
			"imei": {
				"type": "normal",
				"required": true,
				"description": "IMEI do Celular do Funcionário (Obrigatório):",
				"placeholder": "Digite o IMEI do Celular a ser entregue ao funcionário...",
				"error_message": "IMEI do Celular do Funcionário",
				"maxTextLength": 33,
				"template": "$imei$"
			},
			"remark": {
				"type": "remark",
				"required": false,
				"description": "Observação (Opcional):",
				"placeholder": "Digite uma observação referente a esse celular...",
				"error_message": "Observação do Celular do Funcionário",
				"prefix": "Observação:",
				"template": "$obs$"
			}
		},
		"Config": {
            "document_template": "termo_celular.html",
			"output": "./documents/Termo de Entrega de Celular"
		}
    }
}
```

## 🛠️ Build / Deploy

se precisa criar um executável para seus usuários, usamos o [`PyInstaller`](https://pyinstaller.org/en/stable/) ou o [`Nuitka (Recomendado)`](https://nuitka.net/).

Para isso possuímos dois scripts no poetry:

<details>
<summary>Nuitka</summary>

> `poetry run build-nuitka`

</details>

<details>
<summary>Pyinstaller</summary>

> `poetry run build-pyinstaller`

</details>