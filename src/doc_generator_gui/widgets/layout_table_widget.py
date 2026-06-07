import re

from PySide6 import QtCore, QtGui, QtWidgets

from .cpf_input_widget import CpfInputWidget

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

        self._documentVM = documentVM
        self._inputVM = inputVM
        self._layoutVM = layoutVM

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
        self.setMinimumHeight(215)

        self._htmlRE = re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
        self._filenameRE = re.compile(r"['!*<>:?\"|/\\]")

        self._layoutVM.onLayoutChanged.connect(self.setDocumentLayout)

    @QtCore.Slot(str)
    def setDocumentLayout(self, layout_name: str = ""):
        """
        matches our selected document layout, changes the widgets
        and layout of the table widget accordingly.
        """

        if layout_name == None:
            return

        self.setRowCount(0)

        for key in self._layoutVM.getCurrentLayoutUI():
            self._addRowToTable(key)

    def validateRequiredInputs(self) -> InputValidationResult:
        """
        this just checks if our inputs are not empty
        and returns the check and the error message,
        if a input is required.
        """

        for row in range(self.rowCount()):
            isEmptyCell = self.cellWidget(row, 1).text() == ""
            isRequired = self._layoutVM.getUIValueByIndex(row, "required", False)
            errorMsg = self._layoutVM.getUIValueByIndex(row, "error_message", {})

            if isEmptyCell and isRequired:
                return InputValidationResult(False, errorMsg)

        return InputValidationResult(True)

    def _createRowDescription(
        self, component: UIComponent
    ) -> QtWidgets.QTableWidgetItem:
        descriptionFont = QtGui.QFont()
        descriptionFont.setBold(True)
        rowDescription = QtWidgets.QTableWidgetItem(component.get("description", ""))
        rowDescription.setFont(descriptionFont)
        rowDescription.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
        return rowDescription

    def _createRowInput(
        self, key: str, component: UIComponent
    ) -> QtWidgets.QLineEdit | CpfInputWidget:
        match component["type"]:
            case "cpf":
                rowInput = CpfInputWidget()
            case _:
                rowInput = QtWidgets.QLineEdit()
                rowInput.setMaxLength(component.get("max_text_length", 30000))
        rowInput.setPlaceholderText(component.get("placeholder", ""))
        rowInput.textEdited.connect(
            lambda: self._inputVM.setInputHistory(key, rowInput.text())
        )
        rowInput.setText(self._inputVM.getInputHistory().get(key, ""))
        return rowInput

    def _addRowToTable(self, key: str):
        """
        Adds a new row to our tablewidget based on our layout.
        """

        index = self.rowCount()
        layoutComponent = self._layoutVM.getCurrentLayoutUI()[key]
        self.setRowCount(index + 1)
        rowDescription = self._createRowDescription(layoutComponent)
        self.setItem(index, 0, rowDescription)
        rowInput = self._createRowInput(key, layoutComponent)
        self.setCellWidget(index, 1, rowInput)

    def getDataFromInputs(self):
        """
        Gets the data from every input and in our table widget
        adds to our string replace dictionary.
        """

        for row in range(self.rowCount()):
            if (currentText := self.cellWidget(row, 1).text()) == "":
                continue

            template = self._layoutVM.getUIValueByIndex(row, "template", "")

            currentText = re.sub(self._htmlRE, "", currentText)

            self._inputVM.setInputData(template, currentText)

    def getEmployeeName(self) -> str:
        for row in range(self.rowCount()):
            if self._layoutVM.getUIValueByIndex(row, "type", "") == "name":
                name = self.cellWidget(row, 1).text()
                name = re.sub(self._htmlRE, "", name)
                name = re.sub(self._filenameRE, "", name)
                return name

        return ""
