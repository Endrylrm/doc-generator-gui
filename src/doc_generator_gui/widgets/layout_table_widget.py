from PySide6 import QtCore, QtGui, QtWidgets

from .cpf_input import CpfInput

from ..controllers.document_controller import DocumentController

from ..validations.results import InputValidationResult


class LayoutTableWidget(QtWidgets.QTableWidget):
    """
    This widget is responsible for the table widget
    which changes depending on the selected layout.
    """

    def __init__(
        self,
        parent=None,
        doc_controller: DocumentController | None = None,
        layout_combobox: QtWidgets.QComboBox | None = None,
    ):
        super().__init__(parent=parent)

        self.doc_controller = doc_controller

        table_headers = ["Descrição", "Preencher"]

        self.setRowCount(0)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(table_headers)
        self.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        self.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        self.setSelectionBehavior(self.selectionBehavior().SelectItems)
        self.setSelectionMode(self.selectionMode().SingleSelection)
        self.verticalHeader().setVisible(False)

        layout_combobox.currentTextChanged.connect(self.SetTableLayout)
        self.SetTableLayout(layout_combobox.currentText())

    def SetTableLayout(self, layout_name: str = ""):
        """
        matches our selected Print layout, changes the text and layout
        of the table widget accordingly.
        """

        if layout_name == None:
            return

        self.setRowCount(0)

        self.doc_controller.SetCurrentLayout(layout_name)

        keys = [
            key
            for key in self.doc_controller.GetCurrentLayout().keys()
            if key != "config"
        ]

        table_rows = list(map(self.AddRowToTable, keys))

    def ValidateRequiredInputs(self) -> InputValidationResult:
        """
        this just checks if our inputs are not empty
        and returns the check and the error message,
        if a input is required.
        """

        for row in range(self.rowCount()):
            is_empty_cell = self.cellWidget(row, 1).text() == ""
            is_required = self.doc_controller.GetValueFromLayout(row, "required")
            error_msg = self.doc_controller.GetValueFromLayout(row, "error_message")

            if is_empty_cell and is_required:
                return InputValidationResult(False, error_msg)

        return InputValidationResult(True)

    def CreateRowDescription(self, layout: dict) -> QtWidgets.QTableWidgetItem:
        description_font = QtGui.QFont()
        description_font.setBold(True)
        row_description = QtWidgets.QTableWidgetItem(layout["description"])
        row_description.setFont(description_font)
        row_description.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
        return row_description

    def CreateRowInput(self, key: str, layout: dict) -> QtWidgets.QLineEdit | CpfInput:
        max_text_length = layout["maxTextLength"] if "maxTextLength" in layout else 900
        row_input = QtWidgets.QLineEdit() if layout["type"] != "cpf" else CpfInput()
        row_input.setPlaceholderText(layout["placeholder"])
        row_input.textEdited.connect(
            lambda: self.SetInputHistoryData(key, row_input.text())
        )
        if layout["type"] != "cpf":
            row_input.setMaxLength(max_text_length)
        if key in self.doc_controller.GetInputHistory():
            row_input.setText(self.doc_controller.GetInputHistory()[key])
        return row_input

    def SetInputHistoryData(self, key: str, text: str):
        self.doc_controller.UpdateInputHistory(key, text)

    def AddRowToTable(self, key: str):
        """
        Adds a new row to our tablewidget based on our json layout.
        """

        index = self.rowCount()
        row_layout = self.doc_controller.GetCurrentLayout()[key]
        self.setRowCount(index + 1)
        row_description = self.CreateRowDescription(row_layout)
        self.setItem(index, 0, row_description)
        row_input = self.CreateRowInput(key, row_layout)
        self.setCellWidget(index, 1, row_input)

    def GetDataFromInputs(self):
        """
        Gets the data from every input and in our table widget
        adds to our string replace dictionary.
        """

        for row in range(self.rowCount()):
            template = self.doc_controller.GetValueFromLayout(row, "replace")

            current_text = self.cellWidget(row, 1).text()

            if current_text == "":
                continue

            prefix = self.doc_controller.GetValueFromLayout(row, "prefix")
            suffix = self.doc_controller.GetValueFromLayout(row, "suffix")
            current_text = prefix + current_text + suffix

            self.doc_controller.UpdateInputData(template, current_text)

    def GetEmployeeName(self) -> str:
        for row in range(self.rowCount()):
            if self.doc_controller.GetValueFromLayout(row, "type") == "name":
                name = self.cellWidget(row, 1).text()
                return name

        return ""
