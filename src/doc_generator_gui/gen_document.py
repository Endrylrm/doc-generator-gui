__author__ = "Endryl Richard Monteiro"
__author_email__ = "Endrylrm@hotmail.com"

import os
import locale
import datetime

# utilities to help with creation of message boxes
from .msgboxutils import CreateInfoMessageBox, CreateWarningMessageBox

# PySide 6 stuff
from PySide6 import QtWidgets, QtGui, QtCore, QtPdf, QtPrintSupport

from .cpf_input import Cpf_Input

from xml.etree import ElementTree as et


# Key Extractor Page/Frame Widget
class Gen_Document(QtWidgets.QWidget):
    """
    Frame/Page Widget "Gerador de Termos de Responsabilidade":

    This Frame Module is responsible for generating our
    statement of responsibility for our employees.
    """

    def __init__(self, parent, controller):
        """
        Frame/Page Widget "Gerador de Termos de Responsabilidade":
        Class Gen_Document(parent, controller):
        parent: This widget parent, usually the container widget.
        controller: QT Main window, to control changing pages.

        Initialization of the Printer_Document Class page.
        """

        super().__init__(parent=parent)

        locale.setlocale(locale.LC_ALL, "")

        self.isDataManual: bool = False
        self.isDevolucao: bool = False
        self.isDesativarImpressao: bool = False
        self.isDesativarPreviewImpressao: bool = False
        self.fileTermo: str = ""
        self.fileTermoDevol: str = ""
        self.wordsToReplace: list[str] = []
        self.replaceWith: list[str] = []

        empresa_xml = et.parse("empresa.xml")
        root = empresa_xml.getroot()

        self.empresa_Dados: dict[str, str] = {
            root.find("nome").attrib["replace"]: root.find("nome").attrib["value"],
            root.find("cnpj").attrib["replace"]: root.find("cnpj").attrib["value"],
            root.find("rua").attrib["replace"]: root.find("rua").attrib["value"],
            root.find("bairro").attrib["replace"]: root.find("bairro").attrib["value"],
            root.find("cidade").attrib["replace"]: root.find("cidade").attrib["value"],
            root.find("estado").attrib["replace"]: root.find("estado").attrib["value"],
            root.find("pais").attrib["replace"]: root.find("pais").attrib["value"],
            root.find("cep").attrib["replace"]: root.find("cep").attrib["value"],
            root.find("fone").attrib["replace"]: root.find("fone").attrib["value"],
        }

        self.tiposImpressao: list[str] = [
            "Cartucho",
            "Celular",
            "iButton",
            "Impressora",
            "Inversor",
            "Notebook",
        ]

        # used to remove a variable from our words to replace variable
        # by adding the types we will hide the serial input
        self.tiposParaRemoverInput: list[str] = ["iButton", "Inversor"]

        # first create our widgets
        self.CreateWidgets(controller)
        # then set our grid layout and config
        self.GridConfigs()

        self.MatchPrintType()

    # Creation of widgets on screen
    def CreateWidgets(self, controller):
        """
        Function CreateWidgets(controller)
        controller: Our main window / controller widget.

        Used to create new widgets (labels, buttons, etc.),
        controller is used in buttons to show another page/frame widget.
        """

        # Label - Title
        self.LabelTitle = QtWidgets.QLabel(
            self, text="<b>Gerador de Termos de Responsabilidade</b>"
        )
        # separator - Title
        self.separatorTitle = QtWidgets.QFrame(self)
        self.separatorTitle.setLineWidth(1)
        self.separatorTitle.setFrameShape(QtWidgets.QFrame.HLine)
        self.separatorTitle.setFrameShadow(QtWidgets.QFrame.Sunken)
        # Label - Print Type
        self.LabelPrintTypeComboBox = QtWidgets.QLabel(
            self, text="<b>Layout de Impressão</b>"
        )
        # ComboBox - Print Type
        self.PrintTypeComboBox = QtWidgets.QComboBox(self)
        for print_type in self.tiposImpressao:
            self.PrintTypeComboBox.addItem(print_type)
        self.PrintTypeComboBox.currentTextChanged.connect(self.MatchPrintType)
        # separator - ComboBox
        self.separatorComboBox = QtWidgets.QFrame(self)
        self.separatorComboBox.setLineWidth(1)
        self.separatorComboBox.setFrameShape(QtWidgets.QFrame.HLine)
        self.separatorComboBox.setFrameShadow(QtWidgets.QFrame.Sunken)
        # Label - Employee Name
        self.LabelEmployee = QtWidgets.QLabel(
            self, text="<b>Nome do Funcionário (Obrigatório):</b>"
        )
        # LineEdit - Nome do funcionário
        self.EmployeeNameInput = QtWidgets.QLineEdit(self)
        self.EmployeeNameInput.setPlaceholderText("Digite o nome do funcionário...")
        # Label - CPF do funcionário
        self.LabelEmployeeCPF = QtWidgets.QLabel(
            self, text="<b>CPF / CNPJ do Funcionário (Obrigatório):</b>"
        )
        # LineEdit - CPF do funcionário
        self.EmployeeCPFInput = Cpf_Input(self)
        # Label - Marca / Modelo do dispositivo
        self.LabelDevice = QtWidgets.QLabel(self)
        # LineEdit - Marca / Modelo do dispositivo
        self.DeviceInput = QtWidgets.QLineEdit(self)
        # Label - Serial / IMEI do dispositivo
        self.LabelDeviceSerial = QtWidgets.QLabel(self)
        # LineEdit - Serial / IMEI do dispositivo
        self.DeviceSerialInput = QtWidgets.QLineEdit(self)
        # Label - Observação
        self.LabelDeviceNote = QtWidgets.QLabel(
            self, text="<b>Observação (Opcional):</b>"
        )
        # LineEdit - Observação
        self.DeviceNoteInput = QtWidgets.QLineEdit(self)
        # CheckBox - Ativar Data Manual
        self.DataManual = QtWidgets.QCheckBox(self, text="Ativar Data Manual.")
        self.DataManual.setToolTip(
            "<b>Ativar Data Manual:</b>\nDesativa a data automâtica e permite a seleção de datas."
        )
        self.DataManual.stateChanged.connect(self.CheckDataManual)
        # CheckBox - Devolução
        self.Devolucao = QtWidgets.QCheckBox(self, text="Devolução de Dispositivo.")
        self.Devolucao.stateChanged.connect(self.CheckDevolucao)
        self.Devolucao.setToolTip(
            "<b>Devolução de Dispositivo.:</b>\nAtive para gerar os termos de devolução."
        )
        # CheckBox - Desativar Visualização de Impressão
        self.DesativarPreviewImpressao = QtWidgets.QCheckBox(
            self, text="Desativar visualização de impressão."
        )
        self.DesativarPreviewImpressao.stateChanged.connect(self.CheckPreviewImpressao)
        self.DesativarPreviewImpressao.setToolTip(
            "<b>Desativar visualização de impressão.:</b>\nDesativa a visualização de impressão."
        )
        # CheckBox - Desativar Impressão
        self.DesativarImpressao = QtWidgets.QCheckBox(
            self, text="Desativar impressão automática."
        )
        self.DesativarImpressao.stateChanged.connect(self.CheckImpressao)
        self.DesativarImpressao.setToolTip(
            "<b>Desativar impressão automática.:</b>\nDesativa a impressão automática, gerando apenas o PDF."
        )
        # DateTimeEdit - Data Manual
        self.DatePicker = QtWidgets.QDateTimeEdit(self)
        self.DatePicker.setCalendarPopup(True)
        self.DatePicker.setDateTime(QtCore.QDateTime.currentDateTime())
        self.DatePicker.setDisplayFormat("dddd, dd 'de' MMMM 'de' yyyy")
        self.DatePicker.setEnabled(False)
        # separator - Buttons
        self.separatorButton = QtWidgets.QFrame(self)
        self.separatorButton.setLineWidth(1)
        self.separatorButton.setFrameShape(QtWidgets.QFrame.HLine)
        self.separatorButton.setFrameShadow(QtWidgets.QFrame.Sunken)
        # PushButton - Gerar Documento
        self.buttonGenDoc = QtWidgets.QPushButton(
            self, text="\N{Document} " + "Gerar Documento"
        )
        self.buttonGenDoc.clicked.connect(self.GenerateDocument)

    # Grid Configuration
    def GridConfigs(self):
        """
        Function GridConfigs()

        Used to configure this frame grid (columns and rows) for our widgets.
        """

        # Grid Creation
        widgetGridLayout = QtWidgets.QGridLayout(self)
        # Label - Título
        widgetGridLayout.addWidget(
            self.LabelTitle, 0, 0, 1, 2, QtGui.Qt.AlignmentFlag.AlignCenter
        )
        # separator - Título
        widgetGridLayout.addWidget(self.separatorTitle, 1, 0, 1, 2)
        # Label - Tipo de impressão
        widgetGridLayout.addWidget(
            self.LabelPrintTypeComboBox, 2, 0, 1, 2, QtGui.Qt.AlignmentFlag.AlignCenter
        )
        # ComboBox - Tipo de impressão
        widgetGridLayout.addWidget(self.PrintTypeComboBox, 3, 0, 1, 2)
        # separator - Tipo de impressão ComboBox
        widgetGridLayout.addWidget(self.separatorComboBox, 4, 0, 1, 2)
        # Label - Nome do Funcionário
        widgetGridLayout.addWidget(
            self.LabelEmployee, 5, 0, 1, 1, QtGui.Qt.AlignmentFlag.AlignLeft
        )
        # LineEdit - Nome do Funcionário Input
        widgetGridLayout.addWidget(self.EmployeeNameInput, 6, 0, 1, 1)
        # Label - CPF do funcionário
        widgetGridLayout.addWidget(
            self.LabelEmployeeCPF, 5, 1, 1, 1, QtGui.Qt.AlignmentFlag.AlignLeft
        )
        # LineEdit - CPF do funcionário Input
        widgetGridLayout.addWidget(self.EmployeeCPFInput, 6, 1, 1, 1)
        # Label - Marca / Modelo do dispositivo
        widgetGridLayout.addWidget(
            self.LabelDevice, 7, 0, 1, 1, QtGui.Qt.AlignmentFlag.AlignLeft
        )
        # LineEdit - Marca / Modelo do dispositivo
        widgetGridLayout.addWidget(self.DeviceInput, 8, 0, 1, 1)
        # Label - Serial / IMEI do dispositivo
        widgetGridLayout.addWidget(
            self.LabelDeviceSerial, 7, 1, 1, 1, QtGui.Qt.AlignmentFlag.AlignLeft
        )
        # LineEdit - Serial / IMEI do dispositivo
        widgetGridLayout.addWidget(self.DeviceSerialInput, 8, 1, 1, 1)
        # Label - Observação
        widgetGridLayout.addWidget(
            self.LabelDeviceNote, 9, 0, 1, 2, QtGui.Qt.AlignmentFlag.AlignLeft
        )
        # LineEdit - Observação
        widgetGridLayout.addWidget(self.DeviceNoteInput, 10, 0, 1, 2)
        # CheckBox - Ativar Data Manual
        widgetGridLayout.addWidget(self.DataManual, 11, 0, 1, 1)
        # DateTimeEdit - Data Manual
        widgetGridLayout.addWidget(self.DatePicker, 11, 1, 1, 1)
        # CheckBox - Ativar Devolução
        widgetGridLayout.addWidget(self.Devolucao, 12, 0, 1, 1)
        # CheckBox - Desativar Visualização de Impressão
        widgetGridLayout.addWidget(self.DesativarPreviewImpressao, 12, 1, 1, 1)
        # CheckBox - Desativar Impressão
        widgetGridLayout.addWidget(self.DesativarImpressao, 13, 0, 1, 1)
        # separator - Buttons
        widgetGridLayout.addWidget(self.separatorButton, 15, 0, 1, 2)
        # PushButton - Gerar Documento
        widgetGridLayout.addWidget(self.buttonGenDoc, 16, 0, 1, 2)
        # space between widgets
        widgetGridLayout.setSpacing(10)
        # stretch last row
        widgetGridLayout.setRowStretch(14, 1)
        # set this widget layout to the grid layout
        self.setLayout(widgetGridLayout)

    def MatchPrintType(self):
        """
        Function MatchPrintType()

        matches our selected Print layout, changes the text and layout
        accordingly.
        """

        match self.PrintTypeComboBox.currentText():
            case "Cartucho":
                self.LabelDeviceSerial.setEnabled(True)
                self.DeviceSerialInput.setEnabled(True)
                self.LabelDeviceSerial.setHidden(False)
                self.DeviceSerialInput.setHidden(False)
                self.wordsToReplace = [
                    "$cartucho$",
                    "$impressora$",
                    "$name$",
                    "$cpf$",
                    "$obs$",
                ]
                self.fileTermo = "termo_cartucho.html"
                self.fileTermoDevol = "termo_cartucho_devol.html"
                self.LabelDevice.setText(
                    "<b>Cartucho de Impressora do Funcionário (Obrigatório):</b>"
                )
                self.LabelDeviceSerial.setText(
                    "<b>Modelo de impressora do Funcionário (Obrigatório):</b>"
                )
                self.DeviceInput.clear()
                self.DeviceInput.setPlaceholderText(
                    "Digite o cartucho de impressora a ser entregue ao funcionário..."
                )
                self.DeviceInput.setMaxLength(100)
                self.DeviceSerialInput.clear()
                self.DeviceSerialInput.setPlaceholderText(
                    "Digite o modelo de impressora que será usado esse cartucho..."
                )
                self.DeviceSerialInput.setMaxLength(100)
                self.DeviceNoteInput.setPlaceholderText(
                    "Digite uma observação referente a esse cartucho de impressora..."
                )
            case "Celular":
                self.LabelDeviceSerial.setEnabled(True)
                self.DeviceSerialInput.setEnabled(True)
                self.LabelDeviceSerial.setHidden(False)
                self.DeviceSerialInput.setHidden(False)
                self.wordsToReplace = [
                    "$celular$",
                    "$imei$",
                    "$name$",
                    "$cpf$",
                    "$obs$",
                ]
                self.fileTermo = "termo_celular.html"
                self.fileTermoDevol = "termo_celular_devol.html"
                self.LabelDevice.setText("<b>Celular do Funcionário (Obrigatório):</b>")
                self.LabelDeviceSerial.setText(
                    "<b>IMEI do Celular do Funcionário (Obrigatório):</b>"
                )
                self.DeviceInput.clear()
                self.DeviceInput.setPlaceholderText(
                    "Digite o Celular a ser entregue ao funcionário..."
                )
                self.DeviceInput.setMaxLength(100)
                self.DeviceSerialInput.clear()
                self.DeviceSerialInput.setPlaceholderText(
                    "Digite o IMEI do Celular a ser entregue ao funcionário..."
                )
                self.DeviceSerialInput.setMaxLength(33)
                self.DeviceNoteInput.setPlaceholderText(
                    "Digite uma observação referente a esse celular..."
                )
            case "iButton":
                self.DeviceSerialInput.clear()
                self.LabelDeviceSerial.setEnabled(False)
                self.DeviceSerialInput.setEnabled(False)
                self.LabelDeviceSerial.setHidden(True)
                self.DeviceSerialInput.setHidden(True)
                self.wordsToReplace = ["$button$", "$name$", "$cpf$", "$obs$"]
                self.fileTermo = "termo_ibutton.html"
                self.fileTermoDevol = "termo_ibutton_devol.html"
                self.LabelDevice.setText("<b>Código do iButton (Obrigatório):</b>")
                self.DeviceInput.clear()
                self.DeviceInput.setPlaceholderText(
                    "Digite o código do iButton a ser entregue ao funcionário..."
                )
                self.DeviceInput.setMaxLength(12)
                self.DeviceNoteInput.setPlaceholderText(
                    "Digite uma observação referente a esse iButton..."
                )
            case "Impressora":
                self.LabelDeviceSerial.setEnabled(True)
                self.DeviceSerialInput.setEnabled(True)
                self.LabelDeviceSerial.setHidden(False)
                self.DeviceSerialInput.setHidden(False)
                self.wordsToReplace = [
                    "$impressora$",
                    "$serial$",
                    "$name$",
                    "$cpf$",
                    "$obs$",
                ]
                self.fileTermo = "termo_impressora.html"
                self.fileTermoDevol = "termo_impressora_devol.html"
                self.LabelDevice.setText(
                    "<b>Impressora do Funcionário (Obrigatório):</b>"
                )
                self.LabelDeviceSerial.setText(
                    "<b>Serial da impressora do Funcionário (Obrigatório):</b>"
                )
                self.DeviceInput.clear()
                self.DeviceInput.setPlaceholderText(
                    "Digite a impressora a ser entregue ao funcionário..."
                )
                self.DeviceInput.setMaxLength(100)
                self.DeviceSerialInput.clear()
                self.DeviceSerialInput.setPlaceholderText(
                    "Digite o Serial da impressora a ser entregue ao funcionário..."
                )
                self.DeviceSerialInput.setMaxLength(10)
                self.DeviceNoteInput.setPlaceholderText(
                    "Digite uma observação referente a essa impressora..."
                )
            case "Inversor":
                self.DeviceSerialInput.clear()
                self.LabelDeviceSerial.setEnabled(False)
                self.DeviceSerialInput.setEnabled(False)
                self.LabelDeviceSerial.setHidden(True)
                self.DeviceSerialInput.setHidden(True)
                self.wordsToReplace = ["$inversor$", "$name$", "$cpf$", "$obs$"]
                self.fileTermo = "termo_inversor.html"
                self.fileTermoDevol = "termo_inversor_devol.html"
                self.LabelDevice.setText(
                    "<b>Marca/Modelo do inversor (Obrigatório):</b>"
                )
                self.DeviceInput.clear()
                self.DeviceInput.setPlaceholderText(
                    "Digite o inversor a ser entregue ao funcionário..."
                )
                self.DeviceInput.setMaxLength(100)
                self.DeviceNoteInput.setPlaceholderText(
                    "Digite uma observação referente a esse inversor..."
                )
            case "Notebook":
                self.LabelDeviceSerial.setEnabled(True)
                self.DeviceSerialInput.setEnabled(True)
                self.LabelDeviceSerial.setHidden(False)
                self.DeviceSerialInput.setHidden(False)
                self.wordsToReplace = [
                    "$notebook$",
                    "$serial$",
                    "$name$",
                    "$cpf$",
                    "$obs$",
                ]
                self.fileTermo = "termo_notebook.html"
                self.fileTermoDevol = "termo_notebook_devol.html"
                self.LabelDevice.setText(
                    "<b>Notebook do Funcionário (Obrigatório):</b>"
                )
                self.LabelDeviceSerial.setText(
                    "<b>Serial do Notebook do Funcionário (Obrigatório):</b>"
                )
                self.DeviceInput.clear()
                self.DeviceInput.setPlaceholderText(
                    "Digite o Notebook a ser entregue ao funcionário..."
                )
                self.DeviceInput.setMaxLength(100)
                self.DeviceSerialInput.clear()
                self.DeviceSerialInput.setPlaceholderText(
                    "Digite o Serial do Notebook a ser entregue ao funcionário..."
                )
                self.DeviceSerialInput.setMaxLength(10)
                self.DeviceNoteInput.setPlaceholderText(
                    "Digite uma observação referente a esse Notebook..."
                )
            case _:
                print("opção não encontrada!!!")

    def CheckInputs(self) -> bool:
        deviceString: str = ""
        msgBoxIcon = QtGui.QIcon("gen_document.ico")
        if self.EmployeeNameInput.text() == "":
            CreateInfoMessageBox(
                "Aviso - Campo Nome está vazio!",
                "Sem nome do funcionário!",
                "Por gentileza, coloque o nome do funcionário.",
                msgWinIcon=msgBoxIcon,
            )
            return False
        if self.EmployeeCPFInput.text() == "":
            CreateInfoMessageBox(
                "Aviso - Campo CPF está vazio!",
                "Sem CPF do funcionário!",
                "Por gentileza, coloque o CPF do funcionário.",
                msgWinIcon=msgBoxIcon,
            )
            return False
        if self.DeviceInput.text() == "":
            match self.PrintTypeComboBox.currentText():
                case "Cartucho":
                    deviceString = "Cartucho de impressora"
                case "Celular":
                    deviceString = "Marca/Modelo de Celular"
                case "iButton":
                    deviceString = "Código do iButton"
                case "Impressora":
                    deviceString = "Marca/Modelo de Impressora"
                case "Inversor":
                    deviceString = "Marca/Modelo de inversor"
                case "Notebook":
                    deviceString = "Marca/Modelo de Notebook"
            CreateInfoMessageBox(
                f"Aviso - Campo {deviceString} está vazio!",
                f"Sem {deviceString} do funcionário!",
                f"Por gentileza, coloque o {deviceString} do funcionário.",
                msgWinIcon=msgBoxIcon,
            )
            return False
        if (
            self.DeviceSerialInput.text() == ""
            and self.PrintTypeComboBox.currentText() not in self.tiposParaRemoverInput
        ):
            match self.PrintTypeComboBox.currentText():
                case "Cartucho":
                    deviceString = "Marca/Modelo de impressora"
                case "Celular":
                    deviceString = "IMEI do Celular"
                case "iButton":
                    deviceString = "Código do iButton"
                case "Impressora":
                    deviceString = "Serial da Impressora"
                case "Inversor":
                    deviceString = "Marca/Modelo de inversor"
                case "Notebook":
                    deviceString = "Serial do Notebook"
            CreateInfoMessageBox(
                f"Aviso - Campo {deviceString} está vazio!",
                f"Sem {deviceString} do funcionário!",
                f"Por gentileza, coloque o {deviceString} do funcionário.",
                msgWinIcon=msgBoxIcon,
            )
            return False
        else:
            return True

    def CheckDataManual(self):
        if self.DataManual.isChecked():
            self.isDataManual = True
            self.DatePicker.setEnabled(True)
        else:
            self.isDataManual = False
            self.DatePicker.setEnabled(False)

    def CheckDevolucao(self):
        if self.Devolucao.isChecked():
            self.isDevolucao = True
        else:
            self.isDevolucao = False

    def CheckImpressao(self):
        if self.DesativarImpressao.isChecked():
            self.isDesativarImpressao = True
        else:
            self.isDesativarImpressao = False

    def CheckPreviewImpressao(self):
        if self.DesativarPreviewImpressao.isChecked():
            self.isDesativarPreviewImpressao = True
        else:
            self.isDesativarPreviewImpressao = False
            print(self.isDesativarImpressao)

    def OutputPath(self) -> str:
        if not self.isDevolucao:
            output: str = (
                f"./Termos/Termo de Entrega de {self.PrintTypeComboBox.currentText()} - "
                + self.EmployeeNameInput.text()
                + ".pdf"
            )
        else:
            output: str = (
                f"./Termos/Termo de Devolução de {self.PrintTypeComboBox.currentText()} - "
                + self.EmployeeNameInput.text()
                + ".pdf"
            )

        return output

    def ReadHtmlFiles(self) -> dict[str, str]:
        fileToRead = self.fileTermo if not self.isDevolucao else self.fileTermoDevol

        with (
            open("./Templates/header.html", "r", encoding="utf-8") as header_file,
            open(f"./Templates/{fileToRead}", "r", encoding="utf-8") as termo_file,
            open("./Templates/footer.html", "r", encoding="utf-8") as footer_file,
        ):
            headerfiledata: str = header_file.read()
            termodata: str = termo_file.read()
            footerfiledata: str = footer_file.read()

        obsTermo: str = self.DeviceNoteInput.text()

        if obsTermo != "":
            obsTermo = "<b>Observação:</b> " + obsTermo

        self.replaceWith.append(self.DeviceInput.text())
        if not self.PrintTypeComboBox.currentText() in self.tiposParaRemoverInput:
            self.replaceWith.append(self.DeviceSerialInput.text())
        self.replaceWith.append(self.EmployeeNameInput.text())
        self.replaceWith.append(self.EmployeeCPFInput.text())
        self.replaceWith.append(obsTermo)

        for old_word, new_word in zip(self.wordsToReplace, self.replaceWith):
            termodata = termodata.replace(old_word, new_word)

        for variavel, dados in self.empresa_Dados.items():
            termodata = termodata.replace(variavel, dados)
            headerfiledata = headerfiledata.replace(variavel, dados)
            footerfiledata = footerfiledata.replace(variavel, dados)

        if not self.isDataManual:
            dataAtual: str = str(datetime.datetime.now().strftime("%A, %d de %B de %Y"))

            footerfiledata = footerfiledata.replace("$data$", str(dataAtual))
        else:
            footerfiledata = footerfiledata.replace("$data$", self.DatePicker.text())

        return {
            "header_html": headerfiledata,
            "termo_html": termodata,
            "footer_html": footerfiledata,
        }

    def GeneratePDF(self, output: str):
        htmlData: dict[str, str] = self.ReadHtmlFiles()

        # print(filedata)
        pdf_printer = QtPrintSupport.QPrinter(
            QtPrintSupport.QPrinter.PrinterMode.HighResolution
        )
        pdf_printer.setOutputFormat(pdf_printer.OutputFormat.PdfFormat)
        pdf_printer.setResolution(600)
        pdf_printer.setFullPage(True)
        pdf_printer.setOutputFileName(output)
        pdf_printer.setPageSize(QtGui.QPageSize.PageSizeId.A4)
        pdf_printer.setPageMargins(QtCore.QMarginsF(0.5, 0.5, 0.5, 0.5))
        pdf_painter = QtGui.QPainter()
        pdf_Doc = QtGui.QTextDocument()
        pdf_Doc_PaintCtx = pdf_Doc.documentLayout().PaintContext()
        pdf_Doc.setTextWidth(530)
        pdf_painter.begin(pdf_printer)
        pdf_painter.scale(8.5, 8.5)
        pdf_painter.translate(0, 5)
        pdf_Doc.setHtml(htmlData["header_html"])
        pdf_Doc.documentLayout().draw(pdf_painter, pdf_Doc_PaintCtx)
        pdf_painter.translate(30, 72)
        pdf_Doc.setHtml(htmlData["termo_html"])
        pdf_Doc.documentLayout().draw(pdf_painter, pdf_Doc_PaintCtx)
        pdf_painter.translate(-30, 665)
        pdf_Doc.setHtml(htmlData["footer_html"])
        pdf_Doc.documentLayout().draw(pdf_painter, pdf_Doc_PaintCtx)
        pdf_painter.end()

    def PrintDocument(self, input_pdf: str):
        printer = QtPrintSupport.QPrinter(
            QtPrintSupport.QPrinter.PrinterMode.HighResolution
        )
        printer.setPageSize(QtGui.QPageSize.PageSizeId.A4)
        printer.setResolution(607)
        printer.setFullPage(True)
        printer.setPageMargins(QtCore.QMarginsF(0.5, 0.5, 0.5, 0.5))

        def PaintingDocument():
            pdf_file = QtPdf.QPdfDocument()
            pdf_file.load(input_pdf)
            size = QtGui.QPageSize.sizePixels(QtGui.QPageSize.PageSizeId.A4, 600)
            imagefromPDF = pdf_file.render(0, size)
            painter = QtGui.QPainter()
            painter.begin(printer)
            painter.translate(2, 0)
            painter.drawImage(0, 0, imagefromPDF)
            painter.end()

        if not self.isDesativarPreviewImpressao:
            printPreviewDialog = QtPrintSupport.QPrintPreviewDialog(printer)
            printPreviewDialog.setWindowTitle(
                f"Imprimir Termo de {self.PrintTypeComboBox.currentText()}"
            )
            printPreviewDialogIcon = QtGui.QIcon("gen_document.ico")
            printPreviewDialog.setWindowIcon(printPreviewDialogIcon)
            printPreviewDialog.paintRequested.connect(PaintingDocument)
        else:
            printDialog = QtPrintSupport.QPrintDialog(printer)

            if printDialog.exec() == printDialog.DialogCode.Accepted:
                PaintingDocument()

    def GenerateDocument(self):
        if not self.CheckInputs():
            return

        Output: str = self.OutputPath()
        self.GeneratePDF(Output)

        if not self.isDesativarImpressao:
            self.PrintDocument(Output)

        self.replaceWith.clear()
