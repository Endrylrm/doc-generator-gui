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

        self.file_termo: str = ""
        self.file_termo_devol: str = ""
        self.strings_to_replace: list[str] = []

        empresa_xml = et.parse("empresa.xml")
        root = empresa_xml.getroot()

        self.empresa_dados: dict[str, str] = {
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

        self.tipos_impressao: list[str] = [
            "Cartucho",
            "Celular",
            "iButton",
            "Impressora",
            "Inversor",
            "Notebook",
        ]

        # used to remove a variable from our words to replace variable
        # by adding the types we will hide the serial input
        self.types_to_remove_input: list[str] = ["iButton", "Inversor"]

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
        self.label_title = QtWidgets.QLabel(
            self, text="<b>Gerador de Termos de Responsabilidade</b>"
        )
        # separator - Title
        self.separator_title = QtWidgets.QFrame(self)
        self.separator_title.setLineWidth(1)
        self.separator_title.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator_title.setFrameShadow(QtWidgets.QFrame.Sunken)
        # Label - Print Type
        self.label_print_type_combobox = QtWidgets.QLabel(
            self, text="<b>Layout de Impressão</b>"
        )
        # ComboBox - Print Type
        self.print_type_combobox = QtWidgets.QComboBox(self)
        for print_type in self.tipos_impressao:
            self.print_type_combobox.addItem(print_type)
        self.print_type_combobox.currentTextChanged.connect(self.MatchPrintType)
        # separator - ComboBox
        self.separator_combobox = QtWidgets.QFrame(self)
        self.separator_combobox.setLineWidth(1)
        self.separator_combobox.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator_combobox.setFrameShadow(QtWidgets.QFrame.Sunken)
        # Label - Employee Name
        self.label_employee = QtWidgets.QLabel(
            self, text="<b>Nome do Funcionário (Obrigatório):</b>"
        )
        # LineEdit - Nome do funcionário
        self.input_employee_name = QtWidgets.QLineEdit(self)
        self.input_employee_name.setPlaceholderText("Digite o nome do funcionário...")
        # Label - CPF do funcionário
        self.label_employee_cpf = QtWidgets.QLabel(
            self, text="<b>CPF / CNPJ do Funcionário (Obrigatório):</b>"
        )
        # LineEdit - CPF do funcionário
        self.input_employee_cpf = Cpf_Input(self)
        # Label - Marca / Modelo do dispositivo
        self.label_device = QtWidgets.QLabel(self)
        # LineEdit - Marca / Modelo do dispositivo
        self.input_device = QtWidgets.QLineEdit(self)
        # Label - Serial / IMEI do dispositivo
        self.label_device_serial = QtWidgets.QLabel(self)
        # LineEdit - Serial / IMEI do dispositivo
        self.input_device_serial = QtWidgets.QLineEdit(self)
        # Label - Observação
        self.label_device_note = QtWidgets.QLabel(
            self, text="<b>Observação (Opcional):</b>"
        )
        # LineEdit - Observação
        self.input_device_note = QtWidgets.QLineEdit(self)
        # separator - CheckBox
        self.separator_checkbox = QtWidgets.QFrame(self)
        self.separator_checkbox.setLineWidth(1)
        self.separator_checkbox.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator_checkbox.setFrameShadow(QtWidgets.QFrame.Sunken)
        # CheckBox - Ativar Data Manual
        self.data_manual = QtWidgets.QCheckBox(self, text="Ativar Data Manual.")
        self.data_manual.setToolTip(
            "<b>Ativar Data Manual:</b>\nDesativa a data automâtica e permite a seleção de datas."
        )
        self.data_manual.stateChanged.connect(self.CheckDataManual)
        # CheckBox - Devolução
        self.devolucao = QtWidgets.QCheckBox(self, text="Devolução de Dispositivo.")
        self.devolucao.setToolTip(
            "<b>Devolução de Dispositivo.:</b>\nAtive para gerar os termos de devolução."
        )
        # CheckBox - Desativar Visualização de Impressão
        self.desativar_preview_impressao = QtWidgets.QCheckBox(
            self, text="Desativar visualização de impressão."
        )
        self.desativar_preview_impressao.setToolTip(
            "<b>Desativar visualização de impressão.:</b>\nDesativa a visualização de impressão."
        )
        # CheckBox - Desativar Impressão
        self.desativar_impressao = QtWidgets.QCheckBox(
            self, text="Desativar impressão automática."
        )
        self.desativar_impressao.setToolTip(
            "<b>Desativar impressão automática.:</b>\nDesativa a impressão automática, gerando apenas o PDF."
        )
        # DateTimeEdit - Data Manual
        self.date_picker = QtWidgets.QDateTimeEdit(self)
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setDateTime(QtCore.QDateTime.currentDateTime())
        self.date_picker.setDisplayFormat("dddd, dd 'de' MMMM 'de' yyyy")
        self.date_picker.setEnabled(False)
        # separator - Buttons
        self.separator_buttons = QtWidgets.QFrame(self)
        self.separator_buttons.setLineWidth(1)
        self.separator_buttons.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator_buttons.setFrameShadow(QtWidgets.QFrame.Sunken)
        # PushButton - Gerar Documento
        self.button_gen_doc = QtWidgets.QPushButton(
            self, text="\N{Document} " + "Gerar Documento"
        )
        self.button_gen_doc.clicked.connect(self.GenerateDocument)

    # Grid Configuration
    def GridConfigs(self):
        """
        Function GridConfigs()

        Used to configure this frame grid (columns and rows) for our widgets.
        """

        # Grid Creation
        widget_grid_layout = QtWidgets.QGridLayout(self)
        # Label - Título
        widget_grid_layout.addWidget(
            self.label_title, 0, 0, 1, 2, QtGui.Qt.AlignmentFlag.AlignCenter
        )
        # separator - Título
        widget_grid_layout.addWidget(self.separator_title, 1, 0, 1, 2)
        # Label - Tipo de impressão
        widget_grid_layout.addWidget(
            self.label_print_type_combobox,
            2,
            0,
            1,
            2,
            QtGui.Qt.AlignmentFlag.AlignCenter,
        )
        # ComboBox - Tipo de impressão
        widget_grid_layout.addWidget(self.print_type_combobox, 3, 0, 1, 2)
        # separator - Tipo de impressão ComboBox
        widget_grid_layout.addWidget(self.separator_combobox, 4, 0, 1, 2)
        # Label - Nome do Funcionário
        widget_grid_layout.addWidget(
            self.label_employee, 5, 0, 1, 1, QtGui.Qt.AlignmentFlag.AlignLeft
        )
        # LineEdit - Nome do Funcionário Input
        widget_grid_layout.addWidget(self.input_employee_name, 6, 0, 1, 1)
        # Label - CPF do funcionário
        widget_grid_layout.addWidget(
            self.label_employee_cpf, 5, 1, 1, 1, QtGui.Qt.AlignmentFlag.AlignLeft
        )
        # LineEdit - CPF do funcionário Input
        widget_grid_layout.addWidget(self.input_employee_cpf, 6, 1, 1, 1)
        # Label - Marca / Modelo do dispositivo
        widget_grid_layout.addWidget(
            self.label_device, 7, 0, 1, 1, QtGui.Qt.AlignmentFlag.AlignLeft
        )
        # LineEdit - Marca / Modelo do dispositivo
        widget_grid_layout.addWidget(self.input_device, 8, 0, 1, 1)
        # Label - Serial / IMEI do dispositivo
        widget_grid_layout.addWidget(
            self.label_device_serial, 7, 1, 1, 1, QtGui.Qt.AlignmentFlag.AlignLeft
        )
        # LineEdit - Serial / IMEI do dispositivo
        widget_grid_layout.addWidget(self.input_device_serial, 8, 1, 1, 1)
        # Label - Observação
        widget_grid_layout.addWidget(
            self.label_device_note, 9, 0, 1, 2, QtGui.Qt.AlignmentFlag.AlignLeft
        )
        # LineEdit - Observação
        widget_grid_layout.addWidget(self.input_device_note, 10, 0, 1, 2)
        # separator - CheckBox
        widget_grid_layout.addWidget(self.separator_checkbox, 11, 0, 1, 2)
        # CheckBox - Ativar Data Manual
        widget_grid_layout.addWidget(self.data_manual, 12, 0, 1, 1)
        # DateTimeEdit - Data Manual
        widget_grid_layout.addWidget(self.date_picker, 12, 1, 1, 1)
        # CheckBox - Ativar Devolução
        widget_grid_layout.addWidget(self.devolucao, 13, 0, 1, 1)
        # CheckBox - Desativar Visualização de Impressão
        widget_grid_layout.addWidget(self.desativar_preview_impressao, 13, 1, 1, 1)
        # CheckBox - Desativar Impressão
        widget_grid_layout.addWidget(self.desativar_impressao, 14, 0, 1, 1)
        # separator - Buttons
        widget_grid_layout.addWidget(self.separator_buttons, 16, 0, 1, 2)
        # PushButton - Gerar Documento
        widget_grid_layout.addWidget(self.button_gen_doc, 17, 0, 1, 2)
        # space between widgets
        widget_grid_layout.setSpacing(10)
        # stretch last row
        widget_grid_layout.setRowStretch(15, 1)
        # set this widget layout to the grid layout
        self.setLayout(widget_grid_layout)

    def CheckDataManual(self):
        if self.data_manual.isChecked():
            self.date_picker.setEnabled(True)
        else:
            self.date_picker.setEnabled(False)

    def CheckInputs(self) -> bool:
        """
        Function CheckInputs()

        this just checks if out inputs are not empty and
        open a message box to tell the user if a required
        input is empty.
        """

        device_str: str = ""
        msg_box_icon = QtGui.QIcon("gen_document.ico")
        if self.input_employee_name.text() == "":
            CreateInfoMessageBox(
                "Aviso - Campo Nome está vazio!",
                "Sem nome do funcionário!",
                "Por gentileza, coloque o nome do funcionário.",
                msg_win_icon=msg_box_icon,
            )
            return False
        if self.input_employee_cpf.text() == "":
            CreateInfoMessageBox(
                "Aviso - Campo CPF está vazio!",
                "Sem CPF do funcionário!",
                "Por gentileza, coloque o CPF do funcionário.",
                msg_win_icon=msg_box_icon,
            )
            return False
        if self.input_device.text() == "":
            match self.print_type_combobox.currentText():
                case "Cartucho":
                    device_str = "Cartucho de impressora"
                case "Celular":
                    device_str = "Marca/Modelo de Celular"
                case "iButton":
                    device_str = "Código do iButton"
                case "Impressora":
                    device_str = "Marca/Modelo de Impressora"
                case "Inversor":
                    device_str = "Marca/Modelo de inversor"
                case "Notebook":
                    device_str = "Marca/Modelo de Notebook"
                case _:
                    device_str = "Opção não implementada"
            CreateInfoMessageBox(
                f"Aviso - Campo {device_str} está vazio!",
                f"Sem {device_str} do funcionário!",
                f"Por gentileza, coloque o {device_str} do funcionário.",
                msg_win_icon=msg_box_icon,
            )
            return False
        if (
            self.input_device_serial.text() == ""
            and self.print_type_combobox.currentText() not in self.types_to_remove_input
        ):
            match self.print_type_combobox.currentText():
                case "Cartucho":
                    device_str = "Marca/Modelo de impressora"
                case "Celular":
                    device_str = "IMEI do Celular"
                case "Impressora":
                    device_str = "Serial da Impressora"
                case "Notebook":
                    device_str = "Serial do Notebook"
                case _:
                    device_str = "Opção não implementada"
            CreateInfoMessageBox(
                f"Aviso - Campo {device_str} está vazio!",
                f"Sem {device_str} do funcionário!",
                f"Por gentileza, coloque o {device_str} do funcionário.",
                msg_win_icon=msg_box_icon,
            )
            return False
        else:
            return True

    def ConfigPrintType(
        self,
        strings_to_replace: list[str],
        termo_filename: str = "",
        termo_devol_filename: str = "",
        device_text: str = "",
        device_serial_text: str = "",
        device_placeholder: str = "",
        device_serial_placeholder: str = "",
        remark_placeholder: str = "",
        device_text_length: int = 200,
        device_serial_text_length: int = 200,
        device_serial_input_enabled: bool = True,
    ):
        """
        Function ConfigPrintType(strings_to_replace, termo_filename, termo_devol_filename, device_text,)

        strings_to_replace: the strings we are going to replace on our terms.
        termo_filename: Our term html file name.
        termo_devol_filename: out devolution term html file name.
        device_text: the text to show on the device label.
        device_serial_text: the text to show on the device serial label.
        device_placeholder: the placeholder text to show on the device input.
        device_serial_placeholder: the placeholder text to show on the device serial input.
        remark_placeholder: the placeholder text to show on the remark input.
        device_text_length: the max length of the text on the device input.
        device_serial_text_length: the max length of the text on the device serial input.
        device_serial_input_enabled: set if the serial input is enabled and visible.

        Configures our Print layout, changes the text and gui layout
        accordingly.
        """

        enable_device_input = True if device_serial_input_enabled == True else False
        hide_device_input = False if device_serial_input_enabled == True else True
        self.label_device_serial.setEnabled(enable_device_input)
        self.input_device_serial.setEnabled(enable_device_input)
        self.label_device_serial.setHidden(hide_device_input)
        self.input_device_serial.setHidden(hide_device_input)
        self.strings_to_replace = strings_to_replace
        self.file_termo = termo_filename
        self.file_termo_devol = termo_devol_filename
        self.label_device.setText(device_text)
        self.label_device_serial.setText(device_serial_text)
        self.input_device.clear()
        self.input_device.setPlaceholderText(device_placeholder)
        self.input_device.setMaxLength(device_text_length)
        self.input_device_serial.clear()
        self.input_device_serial.setPlaceholderText(device_serial_placeholder)
        self.input_device_serial.setMaxLength(device_serial_text_length)
        self.input_device_note.setPlaceholderText(remark_placeholder)

    def MatchPrintType(self):
        """
        Function MatchPrintType()

        matches our selected Print layout, changes the text and layout
        accordingly.
        """

        match self.print_type_combobox.currentText():
            case "Cartucho":
                self.ConfigPrintType(
                    ["$cartucho$", "$impressora$", "$name$", "$cpf$", "$obs$"],
                    "termo_cartucho.html",
                    "termo_cartucho_devol.html",
                    "<b>Cartucho de Impressora do Funcionário (Obrigatório):</b>",
                    "<b>Modelo de impressora do Funcionário (Obrigatório):</b>",
                    "Digite o cartucho de impressora a ser entregue ao funcionário...",
                    "Digite o modelo de impressora que será usado esse cartucho...",
                    "Digite uma observação referente a esse cartucho de impressora...",
                )
            case "Celular":
                self.ConfigPrintType(
                    ["$celular$", "$imei$", "$name$", "$cpf$", "$obs$"],
                    "termo_celular.html",
                    "termo_celular_devol.html",
                    "<b>Celular do Funcionário (Obrigatório):</b>",
                    "<b>IMEI do Celular do Funcionário (Obrigatório):</b>",
                    "Digite o Celular a ser entregue ao funcionário...",
                    "Digite o IMEI do Celular a ser entregue ao funcionário...",
                    "Digite uma observação referente a esse celular...",
                    device_serial_text_length=33,
                )
            case "iButton":
                self.ConfigPrintType(
                    ["$button$", "$name$", "$cpf$", "$obs$"],
                    "termo_ibutton.html",
                    "termo_ibutton_devol.html",
                    "<b>Código do iButton (Obrigatório):</b>",
                    device_placeholder="Digite o código do iButton a ser entregue ao funcionário...",
                    remark_placeholder="Digite uma observação referente a esse iButton...",
                    device_text_length=12,
                    device_serial_input_enabled=False,
                )
            case "Impressora":
                self.ConfigPrintType(
                    ["$impressora$", "$serial$", "$name$", "$cpf$", "$obs$"],
                    "termo_impressora.html",
                    "termo_impressora_devol.html",
                    "<b>Impressora do Funcionário (Obrigatório):</b>",
                    "<b>Serial da impressora do Funcionário (Obrigatório):</b>",
                    "Digite a impressora a ser entregue ao funcionário...",
                    "Digite o Serial da impressora a ser entregue ao funcionário...",
                    "Digite uma observação referente a essa impressora...",
                    device_serial_text_length=10,
                )
            case "Inversor":
                self.ConfigPrintType(
                    ["$inversor$", "$name$", "$cpf$", "$obs$"],
                    "termo_inversor.html",
                    "termo_inversor_devol.html",
                    "<b>Marca/Modelo do inversor (Obrigatório):</b>",
                    device_placeholder="Digite o inversor a ser entregue ao funcionário...",
                    remark_placeholder="Digite uma observação referente a esse inversor...",
                    device_serial_input_enabled=False,
                )
            case "Notebook":
                self.ConfigPrintType(
                    ["$notebook$", "$serial$", "$name$", "$cpf$", "$obs$"],
                    "termo_notebook.html",
                    "termo_notebook_devol.html",
                    "<b>Notebook do Funcionário (Obrigatório):</b>",
                    "<b>Serial do Notebook do Funcionário (Obrigatório):</b>",
                    "Digite o Notebook a ser entregue ao funcionário...",
                    "Digite o Serial do Notebook a ser entregue ao funcionário...",
                    "Digite uma observação referente a esse Notebook...",
                )
            case _:
                print("opção não implementada.")

    def OutputPath(self) -> str:
        if not self.devolucao.isChecked():
            output: str = (
                f"./Termos/Termo de Entrega de {self.print_type_combobox.currentText()} - "
                + self.input_employee_name.text()
                + ".pdf"
            )
        else:
            output: str = (
                f"./Termos/Termo de Devolução de {self.print_type_combobox.currentText()} - "
                + self.input_employee_name.text()
                + ".pdf"
            )

        return output

    def ReadHtmlFiles(self) -> dict[str, str]:
        """
        Function ReadHtmlFiles()

        this read our terms html files and replaces the placeholder
        strings with the strings in our self.strings_to_replace list,
        returning a dictionary containing all the html data.
        """

        file_to_read = (
            self.file_termo if not self.devolucao.isChecked() else self.file_termo_devol
        )

        with (
            open("./Templates/header.html", "r", encoding="utf-8") as header_file,
            open(f"./Templates/{file_to_read}", "r", encoding="utf-8") as termo_file,
            open("./Templates/footer.html", "r", encoding="utf-8") as footer_file,
        ):
            header_file_data: str = header_file.read()
            termo_data: str = termo_file.read()
            footer_file_data: str = footer_file.read()

        obsTermo: str = self.input_device_note.text()

        if obsTermo != "":
            obsTermo = "<b>Observação:</b> " + obsTermo

        new_strings: list[str] = []

        new_strings.append(self.input_device.text())
        if not self.print_type_combobox.currentText() in self.types_to_remove_input:
            new_strings.append(self.input_device_serial.text())
        new_strings.append(self.input_employee_name.text())
        new_strings.append(self.input_employee_cpf.text())
        new_strings.append(obsTermo)

        for old_string, new_string in zip(self.strings_to_replace, new_strings):
            termo_data = termo_data.replace(old_string, new_string)

        for variable, data in self.empresa_dados.items():
            termo_data = termo_data.replace(variable, data)
            header_file_data = header_file_data.replace(variable, data)
            footer_file_data = footer_file_data.replace(variable, data)

        if not self.data_manual.isChecked():
            data_atual: str = str(
                datetime.datetime.now().strftime("%A, %d de %B de %Y")
            )

            footer_file_data = footer_file_data.replace("$data$", str(data_atual))
        else:
            footer_file_data = footer_file_data.replace(
                "$data$", self.date_picker.text()
            )

        changed_html_file: dict = {
            "header_html": header_file_data,
            "termo_html": termo_data,
            "footer_html": footer_file_data,
        }

        return changed_html_file

    def GeneratePDF(
        self,
        output: str,
        pdf_printer: QtPrintSupport.QPrinter,
        pdf_painter: QtGui.QPainter,
    ):
        """
        Function GeneratePDF(output, pdf_printer, painter)
        output: output path for the PDF file.
        pdf_printer: the printer responsible to generate the PDF file.
        pdf_painter: the painter responsible to paint out HTML to the PDF file.

        we use a QPrinter, QPainter and QTextdocument to generate a
        PDF file of our HTML, we scale our painter and begin painting
        by changing the html in our text document, also translating the
        painter when necessary and call the draw function of our PaintContext
        to start painting.
        """

        html_data: dict[str, str] = self.ReadHtmlFiles()

        pdf_printer.setOutputFormat(pdf_printer.OutputFormat.PdfFormat)
        pdf_printer.setResolution(600)
        pdf_printer.setOutputFileName(output)
        pdf_Doc = QtGui.QTextDocument()
        pdf_Doc_PaintCtx = pdf_Doc.documentLayout().PaintContext()
        pdf_Doc.setTextWidth(530)
        pdf_painter.begin(pdf_printer)
        pdf_painter.scale(8.5, 8.5)
        pdf_painter.translate(0, 5)
        pdf_Doc.setHtml(html_data["header_html"])
        pdf_Doc.documentLayout().draw(pdf_painter, pdf_Doc_PaintCtx)
        pdf_painter.translate(30, 72)
        pdf_Doc.setHtml(html_data["termo_html"])
        pdf_Doc.documentLayout().draw(pdf_painter, pdf_Doc_PaintCtx)
        pdf_painter.translate(-30, 665)
        pdf_Doc.setHtml(html_data["footer_html"])
        pdf_Doc.documentLayout().draw(pdf_painter, pdf_Doc_PaintCtx)
        pdf_painter.end()

    def PrintDocument(
        self, input_pdf: str, printer: QtPrintSupport.QPrinter, painter: QtGui.QPainter
    ):
        """
        Function PrintDocument(input_pdf, printer, painter)
        input_pdf: the path of our PDF file to send to a native printer.
        printer: the printer responsible to send to our native printer.
        painter: the painter responsible to paint out the PDF file to our native printer.

        this function is responsible to send our PDF file to a native
        printer, it uses a QPrinter to send to a native printer,
        QPrintPreviewDialog to preview or QPrintDialog to a fast printing.
        """

        printer.setOutputFormat(printer.OutputFormat.NativeFormat)
        printer.setResolution(607)

        def PaintingDocument():
            """
            Function PaintingDocument()

            this nested function is responsible to convert our pdf file
            in a image and then use a QPainter to paint to a native printer.
            """

            pdf_file = QtPdf.QPdfDocument()
            pdf_file.load(input_pdf)
            size = QtGui.QPageSize.sizePixels(QtGui.QPageSize.PageSizeId.A4, 600)
            image_from_pdf = pdf_file.render(0, size)
            painter.begin(printer)
            painter.scale(1, 1)
            painter.translate(2, 0)
            painter.drawImage(0, 0, image_from_pdf)
            painter.end()

        if not self.desativar_preview_impressao.isChecked():
            print_preview_dialog = QtPrintSupport.QPrintPreviewDialog(printer)
            print_preview_dialog.setWindowTitle(
                f"Imprimir Termo de {self.print_type_combobox.currentText()}"
            )
            print_preview_dialog_icon = QtGui.QIcon("gen_document.ico")
            print_preview_dialog.setWindowIcon(print_preview_dialog_icon)
            print_preview_dialog.paintRequested.connect(PaintingDocument)
            print_preview_dialog.exec()
        else:
            print_dialog = QtPrintSupport.QPrintDialog(printer)

            if print_dialog.exec() == print_dialog.DialogCode.Accepted:
                PaintingDocument()

    def GenerateDocument(self):
        if not self.CheckInputs():
            return

        printer = QtPrintSupport.QPrinter(
            QtPrintSupport.QPrinter.PrinterMode.HighResolution
        )
        printer.setPageSize(QtGui.QPageSize.PageSizeId.A4)
        printer.setFullPage(True)
        printer.setPageMargins(QtCore.QMarginsF(0.5, 0.5, 0.5, 0.5))

        painter = QtGui.QPainter()

        Output: str = self.OutputPath()

        self.GeneratePDF(Output, printer, painter)

        if not self.desativar_impressao.isChecked():
            self.PrintDocument(Output, printer, painter)
