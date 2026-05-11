from PySide6 import QtCore, QtGui, QtWidgets

from .cpf_input import CpfInput

from ..states.document_state import DocumentState

from ..stores.layout_store import LayoutStore


class LayoutTableWidget(QtWidgets.QTableWidget):
    """
    This widget is responsible for the table widget
    which changes depending on the selected layout.
    """

    def __init__(
        self,
        parent=None,
        doc_state: DocumentState | None = None,
        layout_store: LayoutStore | None = None,
        layout_combobox: QtWidgets.QComboBox | None = None,
    ):
        super().__init__(parent=parent)

        self.doc_state = doc_state
        self.layout_store = layout_store

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

        self.layout_store.SetCurrentLayout(layout_name)

        keys = [
            key
            for key in self.layout_store.GetCurrentLayout().keys()
            if key != "config"
        ]

        table_rows = list(map(self.AddRowToTable, keys))

    def HasEmptyInputs(self) -> tuple[bool, str]:
        """
        this just checks if our inputs are not empty
        and returns the check and the error message,
        if a input is required.
        """

        error_msg = ""

        for row in range(self.rowCount()):
            is_empty_cell = self.cellWidget(row, 1).text() == ""
            is_required = self.layout_store.GetValueFromLayout(row, "required")
            error_msg = self.layout_store.GetValueFromLayout(row, "error_message")

            if is_empty_cell and is_required:
                return True, error_msg

        return False, error_msg

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
        if key in self.doc_state.input_history:
            row_input.setText(self.doc_state.input_history[key])
        return row_input

    def SetInputHistoryData(self, key: str, text: str):
        self.doc_state.input_history[key] = text

    def AddRowToTable(self, key: str):
        """
        Adds a new row to our tablewidget based on our json layout.
        """

        index = self.rowCount()
        row_layout = self.layout_store.GetCurrentLayout()[key]
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
            str_to_replace = self.layout_store.GetValueFromLayout(row, "replace")

            current_text = self.cellWidget(row, 1).text()

            if current_text == "":
                continue

            prefix = self.layout_store.GetValueFromLayout(row, "prefix")
            suffix = self.layout_store.GetValueFromLayout(row, "suffix")
            current_text = prefix + current_text + suffix

            self.doc_state.input_data[str_to_replace] = current_text

    def GetEmployeeName(self) -> str:
        for row in range(self.rowCount()):
            if self.layout_store.GetValueFromLayout(row, "type") == "name":
                name = self.cellWidget(row, 1).text()
                return name

        return ""

    def SetOutputPath(self, is_device_return: bool = False) -> str:
        """
        Sets the output path for our PDF files, by getting the
        name of the employee in our table and the current type.
        """

        default_path = (
            self.layout_store.GetCurrentLayout()["config"]["output_devol"]
            if is_device_return
            else self.layout_store.GetCurrentLayout()["config"]["output"]
        )

        name = self.GetEmployeeName()

        output_path = f"{default_path} - {name}.pdf"

        return output_path
