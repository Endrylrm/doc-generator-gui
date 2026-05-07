__author__ = "Endryl Richard Monteiro"
__author_email__ = "Endrylrm@hotmail.com"

import locale
import json

from datetime import datetime

from PySide6 import QtWidgets, QtGui, QtCore, QtPdf, QtPrintSupport

from .helpers.dialog_helpers import CreateInfoMessageBox, CreateWarningMessageBox

from .widgets.cpf_input import Cpf_Input

from .contexts.document_context import DocumentContext

from .handlers.html_template_handler import HTMLTemplateHandler

from .services.pdf_service import PDFService
from .services.printer_service import PrinterService

from .loaders.company_data_loader import CompanyDataLoader


class GenDocument(QtWidgets.QWidget):
    """
    This Frame Module is responsible for generating our
    statement of responsibility for our employees.
    """

    def __init__(self, parent, controller):
        """
        Initialization of the Gen_Document Class page.
        """

        super().__init__(parent=parent)

        locale.setlocale(locale.LC_ALL, "")

        self.document_ctx = DocumentContext()

        self.html_tmpl_handler = HTMLTemplateHandler(self.document_ctx)
        self.pdf_service = PDFService(self.document_ctx)
        self.printer_service = PrinterService(self.document_ctx)

        self.company_loader = CompanyDataLoader("company.json", self.document_ctx)
        self.company_loader.load()

        # a dictionary to remember data from our inputs
        self.input_history: dict = {}

        self.layouts: dict = {}
        self.cur_layout: dict = {}

        self.ReadLayouts()

        self.CreateWidgets(controller)
        self.GridConfigs()

        self.MatchPrintType()

    def ReadLayouts(self):
        with open("layouts.json", "r", encoding="utf-8") as layout_file:
            layouts = json.loads(layout_file.read())

        self.layouts = layouts

    def CreateWidgets(self, controller):
        """
        Used to create new widgets (labels, buttons, etc.),
        controller (main window / controller widget) is used in buttons
        to show another page/frame widget.
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
        print_types = list(map(self.print_type_combobox.addItem, self.layouts.keys()))
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
        table_headers = ["Descrição", "Preencher"]
        self.table_document = QtWidgets.QTableWidget()
        self.table_document.setRowCount(0)
        self.table_document.setColumnCount(2)
        self.table_document.setHorizontalHeaderLabels(table_headers)
        self.table_document.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        self.table_document.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        self.table_document.setSelectionBehavior(
            self.table_document.selectionBehavior().SelectItems
        )
        self.table_document.setSelectionMode(
            self.table_document.selectionMode().SingleSelection
        )
        self.table_document.verticalHeader().setVisible(False)
        # CheckBox - Ativar Data Manual
        self.manual_date = QtWidgets.QCheckBox(self, text="Ativar Data Manual.")
        self.manual_date.setToolTip(
            "<b>Ativar Data Manual:</b>\nDesativa a data automâtica e permite a seleção de datas."
        )
        self.manual_date.stateChanged.connect(self.CheckManualDate)
        # CheckBox - Devolução
        self.devolution = QtWidgets.QCheckBox(self, text="Devolução de Dispositivo.")
        self.devolution.setToolTip(
            "<b>Devolução de Dispositivo.:</b>\nAtive para gerar os termos de devolução."
        )
        # CheckBox - Desativar Visualização de Impressão
        self.disable_printer_preview = QtWidgets.QCheckBox(
            self, text="Desativar visualização de impressão."
        )
        self.disable_printer_preview.setToolTip(
            "<b>Desativar visualização de impressão.:</b>\nDesativa a visualização de impressão."
        )
        # CheckBox - Desativar Impressão
        self.disable_printer = QtWidgets.QCheckBox(
            self, text="Desativar impressão automática."
        )
        self.disable_printer.setToolTip(
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
            self, text="\N{DOCUMENT} " + "Gerar Documento"
        )
        self.button_gen_doc.clicked.connect(self.GenerateDocument)

    def GridConfigs(self):
        """
        Used to configure this frame grid (columns and rows) for our widgets.
        """

        # Grid Layout
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
        widget_grid_layout.addWidget(self.table_document, 5, 0, 6, 2)
        # separator - CheckBox
        widget_grid_layout.addWidget(self.separator_checkbox, 11, 0, 1, 2)
        # CheckBox - Ativar Data Manual
        widget_grid_layout.addWidget(self.manual_date, 12, 0, 1, 1)
        # DateTimeEdit - Data Manual
        widget_grid_layout.addWidget(self.date_picker, 12, 1, 1, 1)
        # CheckBox - Ativar Devolução
        widget_grid_layout.addWidget(self.devolution, 13, 0, 1, 1)
        # CheckBox - Desativar Visualização de Impressão
        widget_grid_layout.addWidget(self.disable_printer_preview, 13, 1, 1, 1)
        # CheckBox - Desativar Impressão
        widget_grid_layout.addWidget(self.disable_printer, 14, 0, 1, 1)
        # separator - Buttons
        widget_grid_layout.addWidget(self.separator_buttons, 16, 0, 1, 2)
        # PushButton - Gerar Documento
        widget_grid_layout.addWidget(self.button_gen_doc, 17, 0, 1, 2)
        # space between widgets
        widget_grid_layout.setSpacing(10)
        # stretch a specific row
        widget_grid_layout.setRowStretch(15, 1)
        # set this widget layout to the grid layout
        self.setLayout(widget_grid_layout)

    def CheckManualDate(self):
        is_manual_date: bool = True if self.manual_date.isChecked() else False
        self.date_picker.setEnabled(is_manual_date)

    def CheckEmptyInputs(self) -> bool:
        """
        this just checks if our inputs are not empty and
        open a message box to tell the user if a required
        input is empty.
        """

        msg_box_icon = QtGui.QIcon("gen_document.ico")
        for row in range(self.table_document.rowCount()):
            if (
                self.table_document.cellWidget(row, 1).text() == ""
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

    def CreateRowDescription(self, layout: dict) -> QtWidgets.QTableWidgetItem:
        description_font = QtGui.QFont()
        description_font.setBold(True)
        row_description = QtWidgets.QTableWidgetItem(layout["description"])
        row_description.setFont(description_font)
        row_description.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
        return row_description

    def CreateRowInput(self, key: str, layout: dict) -> QtWidgets.QLineEdit | Cpf_Input:
        max_text_length = layout["maxTextLength"] if "maxTextLength" in layout else 900
        row_input = QtWidgets.QLineEdit() if layout["type"] != "cpf" else Cpf_Input()
        row_input.setPlaceholderText(layout["placeholder"])
        row_input.textEdited.connect(
            lambda: self.SetInputHistoryData(key, row_input.text())
        )
        if key in self.input_history and self.input_history[key] != "":
            row_input.setText(self.input_history[key])
        if layout["type"] != "cpf":
            row_input.setMaxLength(max_text_length)
        return row_input

    def SetInputHistoryData(self, key: str, text: str):
        self.input_history[key] = text

    def AddRowToTable(self, key: str):
        """
        Adds a new row to our tablewidget based on our json layout.
        """

        index = self.table_document.rowCount()
        row_layout = self.cur_layout[key]
        self.table_document.setRowCount(index + 1)
        row_description = self.CreateRowDescription(row_layout)
        self.table_document.setItem(index, 0, row_description)
        row_input = self.CreateRowInput(key, row_layout)
        self.table_document.setCellWidget(index, 1, row_input)

    def GetValueFromLayout(self, index: int, key: str):
        """
        we convert our dictionary items in a list, then we returns the
        data from the dictionary based on the index of a parent key,
        by selecting the corresponding key.
        """

        layout_data = list(self.cur_layout.items())[index][1]
        return layout_data[key] if key in layout_data else ""

    def MatchPrintType(self):
        """
        matches our selected Print layout, changes the text and layout
        of the table widget accordingly.
        """

        if self.print_type_combobox.currentText() == None:
            return

        self.table_document.setRowCount(0)

        self.cur_layout = self.layouts[self.print_type_combobox.currentText()]
        keys = [key for key in self.cur_layout.keys() if key != "config"]
        table_rows = list(map(self.AddRowToTable, keys))

    def SetOutputPath(self):
        """
        Sets the output path for our PDF files, by getting the
        name of the employee in our table and the current type.
        """

        print_type = self.print_type_combobox.currentText()

        for row in range(self.table_document.rowCount()):
            if self.GetValueFromLayout(row, "type") == "name":
                name = self.table_document.cellWidget(row, 1).text()

        self.document_ctx.output_path = (
            f"./Termos/Termo de Devolução de {print_type} - {name}.pdf"
            if self.devolution.isChecked()
            else f"./Termos/Termo de Entrega de {print_type} - {name}.pdf"
        )

    def GetDataFromInputs(self):
        """
        Gets the data from every input and in our table widget
        adds to our string replace dictionary.
        """

        for row in range(self.table_document.rowCount()):
            str_to_replace = self.GetValueFromLayout(row, "replace")

            current_text = self.table_document.cellWidget(row, 1).text()

            if current_text != "":
                prefix = self.GetValueFromLayout(row, "prefix")
                suffix = self.GetValueFromLayout(row, "suffix")
                current_text = prefix + current_text + suffix

            self.document_ctx.strings_to_replace[str_to_replace] = current_text

    def GenerateDocument(self):
        """
        Responsible to start the PDF creation and sending to a
        printer (optional).
        """

        if not self.CheckEmptyInputs():
            return

        self.GetDataFromInputs()
        self.SetOutputPath()

        file_to_read = (
            self.cur_layout["config"]["termo"]
            if not self.devolution.isChecked()
            else self.cur_layout["config"]["termo_devol"]
        )

        cur_date = (
            self.date_picker.text()
            if self.manual_date.isChecked()
            else str(datetime.now().strftime("%A, %d de %B de %Y"))
        )

        self.pdf_service.Generate(
            self.html_tmpl_handler.HandleHTML(file_to_read, cur_date)
        )

        if not self.disable_printer.isChecked():
            self.printer_service.PrintDocument(
                self.disable_printer_preview.isChecked(),
                self.print_type_combobox.currentText(),
            )
