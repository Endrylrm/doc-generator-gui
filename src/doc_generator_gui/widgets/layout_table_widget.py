import re

from PySide6 import QtCore, QtGui, QtWidgets

from .cpf_input import CpfInput

from ..schemas.components import UIComponent

from ..viewmodels.document_viewmodel import DocumentViewModel
from ..viewmodels.input_viewmodel import InputViewModel
from ..viewmodels.layout_viewmodel import LayoutViewModel

from ..validations.results import InputValidationResult


class LayoutTableWidget(QtWidgets.QTableWidget):
    """
    This widget is responsible for the table widget
    which changes depending on the selected layout.
    """

    def __init__(
        self,
        parent=None,
        documentVM: DocumentViewModel | None = None,
        inputVM: InputViewModel | None = None,
        layoutVM: LayoutViewModel | None = None,
    ):
        super().__init__(parent=parent)

        self.documentVM = documentVM
        self.inputVM = inputVM
        self.layoutVM = layoutVM

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

        self._htmlRE = re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
        self._filenameRE = re.compile(r"['!*<>:?\"|/\\]")

    def setTableLayout(self, layout_name: str = ""):
        """
        matches our selected Print layout, changes the text
        and layout of the table widget accordingly.
        """

        if layout_name == None:
            return

        self.setRowCount(0)

        self.layoutVM.setCurrentLayout(layout_name)
        self.documentVM.setPrintType(layout_name)

        for key in self.layoutVM.getCurrentLayoutUI():
            self.addRowToTable(key)

    def validateRequiredInputs(self) -> InputValidationResult:
        """
        this just checks if our inputs are not empty
        and returns the check and the error message,
        if a input is required.
        """

        for row in range(self.rowCount()):
            isEmptyCell = self.cellWidget(row, 1).text() == ""
            isRequired = self.layoutVM.getLayoutValueByIndex(row, "required", "")
            errorMsg = self.layoutVM.getLayoutValueByIndex(row, "error_message", "")

            if isEmptyCell and isRequired:
                return InputValidationResult(False, errorMsg)

        return InputValidationResult(True)

    def createRowDescription(
        self, component: UIComponent
    ) -> QtWidgets.QTableWidgetItem:
        descriptionFont = QtGui.QFont()
        descriptionFont.setBold(True)
        rowDescription = QtWidgets.QTableWidgetItem(component.get("description", ""))
        rowDescription.setFont(descriptionFont)
        rowDescription.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
        return rowDescription

    def createRowInput(
        self, key: str, component: UIComponent
    ) -> QtWidgets.QLineEdit | CpfInput:
        match component["type"]:
            case "cpf":
                rowInput = CpfInput()
            case _:
                rowInput = QtWidgets.QLineEdit()
                rowInput.setMaxLength(component.get("max_text_length", 30000))
        rowInput.setPlaceholderText(component.get("placeholder", ""))
        rowInput.textEdited.connect(
            lambda: self.setInputHistoryData(key, rowInput.text())
        )
        rowInput.setText(self.inputVM.getInputHistory().get(key, ""))
        return rowInput

    def setInputHistoryData(self, key: str, text: str):
        self.inputVM.updateInputHistory(key, text)

    def addRowToTable(self, key: str):
        """
        Adds a new row to our tablewidget based on our layout.
        """

        index = self.rowCount()
        layoutComponent = self.layoutVM.getCurrentLayoutUI()[key]
        self.setRowCount(index + 1)
        rowDescription = self.createRowDescription(layoutComponent)
        self.setItem(index, 0, rowDescription)
        rowInput = self.createRowInput(key, layoutComponent)
        self.setCellWidget(index, 1, rowInput)

    def getDataFromInputs(self):
        """
        Gets the data from every input and in our table widget
        adds to our string replace dictionary.
        """

        for row in range(self.rowCount()):
            if (currentText := self.cellWidget(row, 1).text()) == "":
                continue

            template = self.layoutVM.getLayoutValueByIndex(row, "template", "")

            if (prefix := self.layoutVM.getLayoutValueByIndex(row, "prefix", "")) != "":
                prefix = re.sub(self._htmlRE, "", prefix)
                prefix = "<b>" + prefix + "</b> "

            if (suffix := self.layoutVM.getLayoutValueByIndex(row, "suffix", "")) != "":
                suffix = re.sub(self._htmlRE, "", suffix)
                suffix = " <b>" + suffix + "</b>"

            currentText = re.sub(self._htmlRE, "", currentText)
            currentText = prefix + currentText + suffix

            self.inputVM.updateInputData(template, currentText)

    def getEmployeeName(self) -> str:
        for row in range(self.rowCount()):
            if self.layoutVM.getLayoutValueByIndex(row, "type", "") == "name":
                name = self.cellWidget(row, 1).text()
                name = re.sub(self._htmlRE, "", name)
                name = re.sub(self._filenameRE, "", name)
                return name

        return ""
