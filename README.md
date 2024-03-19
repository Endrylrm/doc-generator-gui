# Gerador de termos para empresas

Esse software tem a função de gerar termos em PDF para empresas usando HTML e CSS, através do PySide6 (QT).

<b style="color: red;">Atenção:</b> Esse projeto que criei é com o intuito de estudar programação através da linguagem Python e não deve ser usado em produção, devido a possíveis falhas de seguranças ou bugs.

## Usando o Gerador de Termos

Esse pequeno sistema foi pensado na simplicidade, através da sua interface gráfica e na facilidade de adicionar novos layouts de termos.

![Interface Gráfica](/assets/img/gui.png "Interface Gráfica")

No momento atual a usabilidade é manual, só precisa preencher os campos com os dados e marcar as opções que quiser usar:

![Usabilidade](/assets/img/gui-using.png "Usabilidade")

Após preencher e marcar as opções desejadas, é só clicar em "Gerar Documento" e irá aparecer um visualizador de seu documento para impressão (caso não tenha marcado a opção "Desativar visualização de impressão"):

![Visualizador de impressão](/assets/img/print-preview.png "Visualizador de impressão")

## Extendendo

<b style="color: purple;">TODO:</b> em desenvolvimento.

## Build / Deploy

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