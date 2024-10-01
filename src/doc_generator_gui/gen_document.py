__author__ = "Endryl Richard Monteiro"
__author_email__ = "Endrylrm@hotmail.com"

import os
import locale
import datetime
import json

# utilities to help with creation of message boxes
from .msgboxutils import CreateInfoMessageBox, CreateWarningMessageBox

# PySide 6 stuff
from PySide6 import QtWidgets, QtGui, QtCore, QtPdf, QtPrintSupport

from .cpf_input import Cpf_Input

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
        self.output_path: str = ""

        self.last_name = ""
        self.last_cpf = ""

        self.strings_to_replace: dict = {}

        self.layout_dict: dict = {}
        self.current_layout: dict = {}

        self.ReadConfigFiles()
        
        # first create our widgets
        self.CreateWidgets(controller)
        # then set our grid layout and config
        self.GridConfigs()

        self.MatchPrintType()

    def ReadConfigFiles(self):
        with (
            open("company.json", "r", encoding="utf-8") as company_file,
            open("layouts.json", "r", encoding="utf-8") as layout_file,
        ):
            company_file_data = json.loads(company_file.read())
            layouts = json.loads(layout_file.read())

        self.layout_dict = layouts

        for key in company_file_data.keys():
            replace = company_file_data[key]["replace"]
            value = company_file_data[key]["value"]
            self.strings_to_replace[replace] = value

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
        for print_type in self.layout_dict.keys():
            self.print_type_combobox.addItem(print_type)
        self.print_type_combobox.currentTextChanged.connect(self.MatchPrintType)
        # separator - ComboBox
        self.separator_combobox = QtWidgets.QFrame(self)
        self.separator_combobox.setLineWidth(1)
        self.separator_combobox.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator_combobox.setFrameShadow(QtWidgets.QFrame.Sunken)
        # separator - CheckBox
        self.separator_checkbox = QtWidgets.QFrame(self)
        self.separator_checkbox.setLineWidth(1)
        self.separator_checkbox.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator_checkbox.setFrameShadow(QtWidgets.QFrame.Sunken)
        # Table - Layouts Data
        table_headers = [
            "Descrição",
            "Preencher",
        ]
        self.tableDocument = QtWidgets.QTableWidget()
        self.tableDocument.setRowCount(0)
        self.tableDocument.setColumnCount(2)
        self.tableDocument.setHorizontalHeaderLabels(table_headers)
        self.tableDocument.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        self.tableDocument.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        self.tableDocument.setSelectionBehavior(
            self.tableDocument.selectionBehavior().SelectItems
        )
        self.tableDocument.setSelectionMode(
            self.tableDocument.selectionMode().SingleSelection
        )

        self.tableDocument.verticalHeader().setVisible(False)
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
        # Table - Data Layouts
        widget_grid_layout.addWidget(self.tableDocument, 5, 0, 6, 2)
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
        self.date_picker.setEnabled(False)
        
        if self.data_manual.isChecked():
            self.date_picker.setEnabled(True)
            

    def CheckEmptyInputs(self) -> bool:
        """
        Function CheckEmptyInputs()

        this just checks if out inputs are not empty and
        open a message box to tell the user if a required
        input is empty.
        """

        msg_box_icon = QtGui.QIcon("gen_document.ico")
        for row in range(self.tableDocument.rowCount()):
            if (
                self.tableDocument.cellWidget(row, 1).text() == ""
                and self.GetValueFromLayout(row, "error_message") != ""
            ):
                CreateInfoMessageBox(
                    f"Aviso - Campo {self.GetValueFromLayout(row, "error_message")} está vazio!",
                    f"Sem {self.GetValueFromLayout(row, "error_message")}!",
                    f"Por gentileza, coloque o {self.GetValueFromLayout(row, "error_message")}.",
                    msg_win_icon=msg_box_icon,
                )
                return False
        return True

    def AddRowToTable(
        self,
        description: str,
        placeholder: str,
        text_length: int,
        row_type: str,
    ):
        """
        Function AddRowToTable(description, description, placeholder, text_length, row_type)
        description: description of the row.
        placeholder: placeholder text for the line edit.
        text_length: the max text length for our line edit.
        row_type: type of row.

        Adds a new row to our tablewidget based on our json layout.
        """

        index = self.tableDocument.rowCount()
        description_font = QtGui.QFont()
        description_font.setBold(True)
        self.tableDocument.setRowCount(index + 1)
        item_description = QtWidgets.QTableWidgetItem(description)
        item_description.setFont(description_font)
        item_description.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
        self.tableDocument.setItem(index, 0, item_description)
        if row_type == "name":
            item_input = QtWidgets.QLineEdit()
            item_input.setPlaceholderText(placeholder)
            item_input.setMaxLength(text_length)
            item_input.textChanged.connect(self.SetLastName)
            if self.last_name != "":
                item_input.setText(self.last_name)
            self.tableDocument.setCellWidget(index, 1, item_input)
        if row_type == "cpf":
            item_input = Cpf_Input()
            item_input.setPlaceholderText(placeholder)
            item_input.textChanged.connect(self.SetLastCPF)
            if self.last_cpf != "":
                item_input.setText(self.last_cpf)
            self.tableDocument.setCellWidget(index, 1, item_input)
        if row_type not in ["name", "cpf"]: 
            item_input = QtWidgets.QLineEdit()
            item_input.setPlaceholderText(placeholder)
            item_input.setMaxLength(text_length)
            self.tableDocument.setCellWidget(index, 1, item_input)

    def SetLastName(self, text):
        self.last_name = text
    
    def SetLastCPF(self, text):
        self.last_cpf = text
        
    def GetValueFromLayout(self, index: int, key: str):
        """
        Function GetValueFromLayout(index, key)
        index: the index of the parent key.
        key: the key we want the value.

        we convert our dictionary items in a list, then we returns the
        data from the dictionary based on the index of a parent key, 
        by selecting the corresponding key.
        """

        layout_data = list(self.current_layout.items())[index][1]
        return layout_data[key] if key in layout_data else ""

    def MatchPrintType(self):
        """
        Function MatchPrintType()

        matches our selected Print layout, changes the text and layout
        of the table widget accordingly.
        """

        self.tableDocument.setRowCount(0)

        if self.print_type_combobox.currentText() != None:
            self.current_layout = self.layout_dict[
                self.print_type_combobox.currentText()
            ]
            for key in self.current_layout.keys():
                if key == "Config":
                    self.file_termo = self.current_layout["Config"]["termo"]
                    self.file_termo_devol = self.current_layout["Config"]["termo_devol"]
                else:
                    self.AddRowToTable(
                        self.current_layout[key]["description"],
                        self.current_layout[key]["placeholder"],
                        (
                            self.current_layout[key]["maxTextLength"]
                            if "maxTextLength" in self.current_layout[key]
                            else 500
                        ),
                        self.current_layout[key]["type"],
                    )

    def SetOutputPath(self) -> str:
        """
        Function SetOutputPath()

        Sets the output path for our PDF files, by getting the
        name of the employee in our table and the current type.
        """

        print_type = self.print_type_combobox.currentText()

        for row in range(self.tableDocument.rowCount()):
            if self.GetValueFromLayout(row, "type") == "name":
                name = self.tableDocument.cellWidget(row, 1).text()

        self.output_path = (
            f"./Termos/Termo de Devolução de {print_type} - {name}.pdf"
        )

        if not self.devolucao.isChecked():
            self.output_path = (
                f"./Termos/Termo de Entrega de {print_type} - {name}.pdf"
            )

    def ReadHtmlFiles(self) -> dict[str, str]:
        """
        Function ReadHtmlFiles()

        this function read our terms html files, returning a dictionary
        containing all the html data.
        """

        file_to_read = (
            self.file_termo if not self.devolucao.isChecked() else self.file_termo_devol
        )

        with (
            open("./Templates/header.html", "r", encoding="utf-8") as header_file,
            open(f"./Templates/{file_to_read}", "r", encoding="utf-8") as termo_file,
            open("./Templates/footer.html", "r", encoding="utf-8") as footer_file,
        ):

            html_file = {
                "header_html": header_file.read(),
                "termo_html": termo_file.read(),
                "footer_html": footer_file.read(),
            }

        return html_file

    def GetDataFromInputs(self):
        """
        Function GetDataFromInputs()

        Gets the data from every input and adds to our string
        replace dictionary.
        """

        for row in range(self.tableDocument.rowCount()):
            str_to_replace = self.GetValueFromLayout(row, "replace")

            current_text = self.tableDocument.cellWidget(row, 1).text()

            if current_text != "":
                if self.GetValueFromLayout(row, "prefix") != "":
                    prefix = self.GetValueFromLayout(row, "prefix")
                    current_text = prefix + current_text

                if self.GetValueFromLayout(row, "suffix") != "":
                    suffix = self.GetValueFromLayout(row, "suffix")
                    current_text = current_text + suffix

            self.strings_to_replace[str_to_replace] = current_text

    def ReturnCleanHTML(self):
        """
        Function ReturnCleanHTML()

        this function changes all the variables in our html with the correct data,
        returning a dictionary containing all cleaned html data.
        """

        self.GetDataFromInputs()

        html_file = self.ReadHtmlFiles()        

        for old_string, new_string in self.strings_to_replace.items():
            html_file["header_html"] = html_file["header_html"].replace(old_string, new_string)
            html_file["termo_html"] = html_file["termo_html"].replace(old_string, new_string)
            html_file["footer_html"] = html_file["footer_html"].replace(old_string, new_string)

        if not self.data_manual.isChecked():
            data_atual: str = str(
                datetime.datetime.now().strftime("%A, %d de %B de %Y")
            )

            html_file["footer_html"] = html_file["footer_html"].replace("$data$", str(data_atual))
        else:
            html_file["footer_html"] = html_file["footer_html"].replace(
                "$data$", self.date_picker.text()
            )

        cleaned_html_file: dict = {
            "header_html": html_file["header_html"],
            "termo_html": html_file["termo_html"],
            "footer_html": html_file["footer_html"],
        }

        return cleaned_html_file

    def GeneratePDF(
        self,
        printer: QtPrintSupport.QPrinter,
        painter: QtGui.QPainter,
    ):
        """
        Function GeneratePDF(printer, painter)
        printer: the printer responsible to generate the PDF file.
        painter: the painter responsible to paint out HTML to the PDF file.

        we use a QPrinter, QPainter and QTextdocument to generate a
        PDF file of our HTML, we scale our painter and begin painting
        by changing the html in our text document, also translating the
        painter when necessary and call the draw function of our PaintContext
        to start painting.
        """

        html_data: dict = self.ReturnCleanHTML()

        printer.setOutputFormat(printer.OutputFormat.PdfFormat)
        printer.setResolution(600)
        printer.setOutputFileName(self.output_path)
        pdf_Doc = QtGui.QTextDocument()
        pdf_Doc_PaintCtx = pdf_Doc.documentLayout().PaintContext()
        pdf_Doc.setTextWidth(530)
        painter.begin(printer)
        painter.scale(8.5, 8.5)
        painter.translate(0, 5)
        pdf_Doc.setHtml(html_data["header_html"])
        pdf_Doc.documentLayout().draw(painter, pdf_Doc_PaintCtx)
        painter.translate(30, 72)
        pdf_Doc.setHtml(html_data["termo_html"])
        pdf_Doc.documentLayout().draw(painter, pdf_Doc_PaintCtx)
        painter.translate(-30, 665)
        pdf_Doc.setHtml(html_data["footer_html"])
        pdf_Doc.documentLayout().draw(painter, pdf_Doc_PaintCtx)
        painter.end()

    def PrintDocument(self, printer: QtPrintSupport.QPrinter, painter: QtGui.QPainter):
        """
        Function PrintDocument(printer, painter)
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
            pdf_file.load(self.output_path)
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
        """
        Function GenerateDocument()

        Responsible to start the PDF creation and sending to a
        printer (optional).
        """

        if not self.CheckEmptyInputs():
            return

        printer = QtPrintSupport.QPrinter(
            QtPrintSupport.QPrinter.PrinterMode.HighResolution
        )
        printer.setPageSize(QtGui.QPageSize.PageSizeId.A4)
        printer.setFullPage(True)
        printer.setPageMargins(QtCore.QMarginsF(0.5, 0.5, 0.5, 0.5))

        painter = QtGui.QPainter()

        self.SetOutputPath()

        self.GeneratePDF(printer, painter)

        if not self.desativar_impressao.isChecked():
            self.PrintDocument(printer, painter)
