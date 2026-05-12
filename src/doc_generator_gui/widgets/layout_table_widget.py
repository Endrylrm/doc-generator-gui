from PySide6 import QtCore, QtGui, QtWidgets

from .cpf_input import CpfInput

from ..controllers.document_controller import DocumentController
from ..controllers.layout_controller import LayoutController

from ..validations.results import InputValidationResult


class LayoutTableWidget(QtWidgets.QTableWidget):
    """
    This widget is responsible for the table widget
    which changes depending on the selected layout.
    """

    def __init__(
        self,
        parent=None,
        documentController: DocumentController | None = None,
        layoutController: LayoutController | None = None,
    ):
        super().__init__(parent=parent)

        self.documentController = documentController
        self.layoutController = layoutController

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

    def setTableLayout(self, layout_name: str = ""):
        """
        matches our selected Print layout, changes the text and layout
        of the table widget accordingly.
        """

        if layout_name == None:
            return

        self.setRowCount(0)

        self.layoutController.setCurrentLayout(layout_name)

        keys = [
            key
            for key in self.layoutController.getCurrentLayout().keys()
            if key != "config"
        ]

        tableRows = list(map(self.addRowToTable, keys))

    def validateRequiredInputs(self) -> InputValidationResult:
        """
        this just checks if our inputs are not empty
        and returns the check and the error message,
        if a input is required.
        """

        for row in range(self.rowCount()):
            isEmptyCell = self.cellWidget(row, 1).text() == ""
            isRequired = self.layoutController.getValueFromLayout(row, "required")
            errorMsg = self.layoutController.getValueFromLayout(row, "error_message")

            if isEmptyCell and isRequired:
                return InputValidationResult(False, errorMsg)

        return InputValidationResult(True)

    def createRowDescription(self, layout: dict) -> QtWidgets.QTableWidgetItem:
        descriptionFont = QtGui.QFont()
        descriptionFont.setBold(True)
        rowDescription = QtWidgets.QTableWidgetItem(layout["description"])
        rowDescription.setFont(descriptionFont)
        rowDescription.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
        return rowDescription

    def createRowInput(self, key: str, layout: dict) -> QtWidgets.QLineEdit | CpfInput:
        maxTextLength = (
            layout["max_text_length"] if "max_text_length" in layout else 900
        )
        rowInput = QtWidgets.QLineEdit() if layout["type"] != "cpf" else CpfInput()
        rowInput.setPlaceholderText(layout["placeholder"])
        rowInput.textEdited.connect(
            lambda: self.setInputHistoryData(key, rowInput.text())
        )
        if layout["type"] != "cpf":
            rowInput.setMaxLength(maxTextLength)
        if key in self.documentController.getInputHistory():
            rowInput.setText(self.documentController.getInputHistory()[key])
        return rowInput

    def setInputHistoryData(self, key: str, text: str):
        self.documentController.updateInputHistory(key, text)

    def addRowToTable(self, key: str):
        """
        Adds a new row to our tablewidget based on our json layout.
        """

        index = self.rowCount()
        rowLayout = self.layoutController.getCurrentLayout()[key]
        self.setRowCount(index + 1)
        rowDescription = self.createRowDescription(rowLayout)
        self.setItem(index, 0, rowDescription)
        rowInput = self.createRowInput(key, rowLayout)
        self.setCellWidget(index, 1, rowInput)

    def getDataFromInputs(self):
        """
        Gets the data from every input and in our table widget
        adds to our string replace dictionary.
        """

        for row in range(self.rowCount()):
            template = self.layoutController.getValueFromLayout(row, "replace")

            currentText = self.cellWidget(row, 1).text()

            if currentText == "":
                continue

            prefix = self.layoutController.getValueFromLayout(row, "prefix")
            suffix = self.layoutController.getValueFromLayout(row, "suffix")
            currentText = prefix + currentText + suffix

            self.documentController.updateInputData(template, currentText)

    def getEmployeeName(self) -> str:
        for row in range(self.rowCount()):
            if self.layoutController.getValueFromLayout(row, "type") == "name":
                name = self.cellWidget(row, 1).text()
                return name

        return ""
