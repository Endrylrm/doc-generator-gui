# Gerador de Documentos para empresas

Esse software tem a função de gerar documentos em PDF para empresas usando HTML e CSS, através do PySide6 (QT) e Playwright.

para iniciá-lo, use `uv run main` no seu terminal ou empacote e use o executável.

<b style="color: red;">Atenção:</b> Esse projeto que criei é com o intuito de estudar programação através da linguagem Python e me auxiliar com essa parte de termos onde estava trabalhando, não deve ser usado em produção, devido a possíveis falhas de seguranças ou bugs.

## Usando o Gerador de Documentos

Esse pequeno sistema foi pensado na simplicidade, através da sua interface gráfica e na facilidade de adicionar novos layouts de documentos.

![Interface Gráfica](/assets/img/gui.png "Interface Gráfica")

No momento atual a usabilidade é manual, só precisa preencher os campos com os dados e marcar as opções que deseja usar:

![Usabilidade](/assets/img/gui-using.png "Usabilidade")

Após preencher e marcar as opções desejadas, é só clicar em "Gerar Documento" e irá aparecer um visualizador de seu documento para impressão (caso não tenha marcado a opção "Desativar visualização de impressão"):

![Visualizador de impressão](/assets/img/print-preview.png "Visualizador de impressão")

## Estrutura do Projeto

```text
assets/
└─── icons/									# Ícones da aplicação
data/
├─── layouts/								# Layouts de impressão em json
├─── templates/								# Templates dos Documentos em HTML
└─── company.json							# Dados da empresa
documents/									# Documentos gerados pelo sistema
src/
├─── doc_generator_gui/
│    ├─── contexts/
│    │ 	  ├─── document_context.py			# Contexto do documento atual
│    │ 	  └─── print_context.py				# Contexto usado para Impressão
│    ├─── core/
│    │ 	  ├─── di_container.py				# Container de injeção de dependência
│    │ 	  └─── providers.py					# Providers de injeção de dependência
│    ├─── factories/
│    │ 	  ├─── dialog_factory.py			# Factory para criação de Dialogs
│    │ 	  └─── printer_factory.py			# Factory para criação QPrinter/QPainter
│    ├─── schemas/
│    │ 	  ├─── components.py				# Schema dos componentes GUI do Layout
│    │ 	  └─── layouts.py					# Schema do Layout de Documentos
│    ├─── services/
│    │ 	  ├─── pdf_service.py				# Serviço de criação de PDF
│    │ 	  ├─── printer_service.py			# Serviço de impressão
│    │ 	  ├─── readers.py					# Leitores de Arquivos
│    │ 	  └─── template_engine_service.py	# Serviço de HTML Template
│    ├─── validations/
│    │ 	  └─── results.py					# Resultados das validações
│    ├─── viewmodels/
│    │ 	  ├─── document_viewmodel.py		# Viewmodel dos documentos a serem criados
│    │ 	  ├─── input_viewmodel.py			# Viewmodel dos inputs
│    │ 	  └─── layout_viewmodel.py			# Viewmodel dos layouts json
│    ├─── views/
│    │ 	  ├─── document_generator_view.py	# View do gerador de documentos
│    │ 	  └─── main_view.py					# View principal - Container
│    ├─── widgets/
│    │ 	  ├─── cpf_input_widget.py			# Widget númerico - Input de CPF/CNPJ
│    │ 	  └─── layout_table_widget.py		# Widget Tabela - Layouts
│    ├─── bootstrap.py						# Bootstrap para iniciar a aplicação quando empacotado
│    └─── main.py							# Entrypoint da aplicação
tests/
├─── test_cpf_cnpj.py						# Teste - Validação de CPF/CNPJ
└─── test_output_path.py					# Teste - Caminho dos Documentos
upx/										# UPX - Reduzir tamanhos dos executáveis (Windows e Linux)
build_nuitka.py								# Build com Nuitka
build_pyinstaller.py						# Build com Pyinstaller
```

## Extendendo/Adicionando novos tipo de documentos

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
				"error_message": {
    				"window_title": "Aviso - Campo Nome do funcionário está vazio!",
    				"title_text": "Sem Nome do funcionário!",
    				"info_text": "Por gentileza, coloque o Nome do funcionário."
				},
				"template": "name"
			},
			"cpf": {
				"type": "cpf",
				"required": true,
				"description": "CPF / CNPJ do Funcionário (Obrigatório):",
				"placeholder": "Observação: Digite apenas os números do CPF ou CNPJ, formatação automática.",
				"error_message": {
    				"window_title": "Aviso - Campo CPF / CNPJ do funcionário está vazio!",
    				"title_text": "Sem CPF / CNPJ do funcionário!",
    				"info_text": "Por gentileza, coloque o CPF / CNPJ do funcionário."
				},
				"template": "cpf"
			},
			"celular": {
				"type": "celular",
				"required": true,
				"description": "Celular do Funcionário (Obrigatório):",
				"placeholder": "Digite o Celular a ser entregue ao funcionário...",
				"error_message": {
    				"window_title": "Aviso - Campo Marca/Modelo do Celular do Funcionário está vazio!",
    				"title_text": "Sem Marca/Modelo do Celular do Funcionário!",
    				"info_text": "Por gentileza, coloque o Marca/Modelo do Celular do Funcionário."
				},
				"template": "celular"
			},
			"imei1": {
				"type": "imei1",
				"required": true,
				"description": "IMEI 1 do Celular do Funcionário (Obrigatório):",
				"placeholder": "Digite o IMEI 1 do Celular a ser entregue ao funcionário...",
				"error_message": {
    				"window_title": "Aviso - Campo IMEI 1 do Celular do Funcionário está vazio!",
    				"title_text": "Sem IMEI 1 do Celular do Funcionário!",
    				"info_text": "Por gentileza, coloque o IMEI 1 do Celular do Funcionário."
				},
				"max_text_length": 15,
				"template": "imei1"
			},
			"imei2": {
				"type": "imei2",
				"required": true,
				"description": "IMEI 2 do Celular do Funcionário (Obrigatório):",
				"placeholder": "Digite o IMEI 2 do Celular a ser entregue ao funcionário...",
				"error_message": {
    				"window_title": "Aviso - Campo IMEI 2 do Celular do Funcionário está vazio!",
    				"title_text": "Sem IMEI 2 do Celular do Funcionário!",
    				"info_text": "Por gentileza, coloque o IMEI 2 do Celular do Funcionário."
				},
				"max_text_length": 15,
				"template": "imei2"
			},
			"remark": {
				"type": "remark",
				"required": false,
				"description": "Observação (Opcional):",
				"placeholder": "Digite uma observação referente a esse celular...",
				"error_message": {
    				"window_title": "Aviso - Campo Observação do Celular do Funcionário está vazio!",
    				"title_text": "Sem Observação do Celular do Funcionário!",
    				"info_text": "Por gentileza, coloque a Observação do Celular do Funcionário."
				},
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

Outros:
- [`imageio`](https://imageio.readthedocs.io/en/stable/index.html) - usado pelo Nuitka para converter ícones

## Build

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

## Deploy

Exemplo para realizar o deploy da aplicação no Linux:

```bash
# Faça a build da aplicação
uv run build_nuitka.py

# mover a aplicação para a pasta desejada
mv main.dist $HOME/Applications/doc_generator_gui

# iniciar a aplicação
cd $HOME/Applications/doc_generator_gui
./main.bin
```