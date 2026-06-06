import locale

from datetime import datetime

from PySide6 import QtWidgets, QtGui, QtCore

from ..widgets.layout_table_widget import LayoutTableWidget
from ..widgets.layout_tab_widget import LayoutTabWidget

from ..viewmodels.document_viewmodel import DocumentViewModel
from ..viewmodels.input_viewmodel import InputViewModel
from ..viewmodels.layout_viewmodel import LayoutViewModel

from ..factories.dialog_factory import DialogFactory


class DocumentGeneratorView(QtWidgets.QWidget):
    """
    This Frame Module is responsible for generating our
    documents for our employees.
    """

    def __init__(
        self,
        parent,
        documentVM: DocumentViewModel,
        inputVM: InputViewModel,
        layoutVM: LayoutViewModel,
    ):
        super().__init__(parent=parent)

        locale.setlocale(locale.LC_ALL, "")

        self._documentVM = documentVM
        self._inputVM = inputVM
        self._layoutVM = layoutVM

        self._createWidgets(parent)
        self._setGridConfiguration()

        self.tabs.switchLayoutTab(0)

    def _createWidgets(self, controller):
        """
        Used to create new widgets (labels, buttons, etc.),
        controller (main window / controller widget) is used
        in buttons to show another page/frame widget.
        """

        # Tabs - layout
        self.tabs = LayoutTabWidget(self, self._documentVM, self._layoutVM)
        # Label - Title
        self.labelTitle = QtWidgets.QLabel(self, text="<b>Gerador de Documentos</b>")
        self._layoutVM.onLayoutChanged.connect(
            lambda layout: self.labelTitle.setText(
                f"<b>Gerador de Documentos - {layout}</b>"
            )
        )
        # separator - Title
        self.separatorTitle = QtWidgets.QFrame(self)
        self.separatorTitle.setLineWidth(1)
        self.separatorTitle.setFrameShape(QtWidgets.QFrame.HLine)
        self.separatorTitle.setFrameShadow(QtWidgets.QFrame.Sunken)
        # Table - Layouts Data
        self.tableDocument = LayoutTableWidget(
            self, self._documentVM, self._inputVM, self._layoutVM
        )
        # separator - CheckBox
        self.separatorCheckbox = QtWidgets.QFrame(self)
        self.separatorCheckbox.setLineWidth(1)
        self.separatorCheckbox.setFrameShape(QtWidgets.QFrame.HLine)
        self.separatorCheckbox.setFrameShadow(QtWidgets.QFrame.Sunken)
        # CheckBox - Ativar Data Manual
        self.isDateSelectable = QtWidgets.QCheckBox(self, text="Ativar Data Manual.")
        self.isDateSelectable.setToolTip(
            "<b>Ativar Data Manual:</b>\nDesativa a data automâtica e permite a seleção de datas."
        )
        self.isDateSelectable.stateChanged.connect(self._enableDatePicker)
        # CheckBox - Desativar Visualização de Impressão
        self.disablePrinterPreview = QtWidgets.QCheckBox(
            self, text="Desativar visualização de impressão."
        )
        self.disablePrinterPreview.setToolTip(
            "<b>Desativar visualização de impressão.:</b>\nDesativa a visualização de impressão."
        )
        # CheckBox - Desativar Impressão
        self.disablePrinter = QtWidgets.QCheckBox(
            self, text="Desativar impressão automática."
        )
        self.disablePrinter.setToolTip(
            "<b>Desativar impressão automática.:</b>\nDesativa a impressão automática, gerando apenas o PDF."
        )
        # DateTimeEdit - Data Manual
        self.datePicker = QtWidgets.QDateTimeEdit(self)
        self.datePicker.setCalendarPopup(True)
        self.datePicker.setDateTime(QtCore.QDateTime.currentDateTime())
        self.datePicker.setDisplayFormat("dddd, dd 'de' MMMM 'de' yyyy")
        self.datePicker.setEnabled(False)
        # separator - Buttons
        self.separatorButtons = QtWidgets.QFrame(self)
        self.separatorButtons.setLineWidth(1)
        self.separatorButtons.setFrameShape(QtWidgets.QFrame.HLine)
        self.separatorButtons.setFrameShadow(QtWidgets.QFrame.Sunken)
        # PushButton - Gerar Documento
        self.buttonGenDoc = QtWidgets.QPushButton(
            self, text="\N{DOCUMENT} " + "Gerar Documento"
        )
        self.buttonGenDoc.clicked.connect(self._generateDocument)

    def _setGridConfiguration(self):
        """
        Used to configure this frame grid (columns and rows) for our widgets.
        """

        # Grid Layout
        widgetGridLayout = QtWidgets.QGridLayout(self)
        # Tabs - layout
        widgetGridLayout.addWidget(self.tabs, 0, 0, 1, 2)
        # Label - Título
        widgetGridLayout.addWidget(
            self.labelTitle, 1, 0, 1, 2, QtGui.Qt.AlignmentFlag.AlignCenter
        )
        # separator - Título
        widgetGridLayout.addWidget(self.separatorTitle, 2, 0, 1, 2)
        # Table - Data Layouts
        widgetGridLayout.addWidget(self.tableDocument, 3, 0, 6, 2)
        # separator - CheckBox
        widgetGridLayout.addWidget(self.separatorCheckbox, 9, 0, 1, 2)
        # CheckBox - Ativar Data Manual
        widgetGridLayout.addWidget(self.isDateSelectable, 10, 0, 1, 1)
        # DateTimeEdit - Data Manual
        widgetGridLayout.addWidget(self.datePicker, 10, 1, 1, 1)
        # CheckBox - Desativar Visualização de Impressão
        widgetGridLayout.addWidget(self.disablePrinterPreview, 11, 0, 1, 1)
        # CheckBox - Desativar Impressão
        widgetGridLayout.addWidget(self.disablePrinter, 11, 1, 1, 1)
        # separator - Buttons
        widgetGridLayout.addWidget(self.separatorButtons, 13, 0, 1, 2)
        # PushButton - Gerar Documento
        widgetGridLayout.addWidget(self.buttonGenDoc, 14, 0, 1, 2)
        # space between widgets
        widgetGridLayout.setSpacing(10)
        # stretch a specific row
        widgetGridLayout.setRowStretch(12, 1)
        # set this widget layout to the grid layout
        self.setLayout(widgetGridLayout)

    def _enableDatePicker(self):
        isDateSelectable: bool = True if self.isDateSelectable.isChecked() else False
        self.datePicker.setEnabled(isDateSelectable)

    def _generateDocument(self):
        """
        Responsible to start the PDF creation and sending to a
        printer (optional).
        """

        result = self.tableDocument.validateRequiredInputs()

        if not result.isValid:
            msgBoxIcon = QtGui.QIcon("assets/icons/gen_document.png")

            DialogFactory.createInfoMessageBox(
                result.errorMessage["window_title"],
                result.errorMessage["title_text"],
                result.errorMessage["info_text"],
                msgWinIcon=msgBoxIcon,
            )
            return

        self.tableDocument.getDataFromInputs()

        employeeName = self.tableDocument.getEmployeeName()
        defaultPath = self._layoutVM.getCurrentLayoutConfig().get("output", "")
        self._documentVM.setOutputPath(employeeName, defaultPath)

        dateText = (
            self.datePicker.text()
            if self.isDateSelectable.isChecked()
            else str(datetime.now().strftime("%A, %d de %B de %Y"))
        )

        self._inputVM.setInputData("data", dateText)

        fileToRead = self._layoutVM.getCurrentLayoutConfig().get(
            "document_template", ""
        )

        self._documentVM.parseHTML(fileToRead, self._inputVM.getInputData())
        self._documentVM.generatePDF()

        if not self.disablePrinter.isChecked():
            self._documentVM.sendToPrinter(self.disablePrinterPreview.isChecked())

        # set the ViewModel state to it's default value after using it
        self._inputVM.setDefaultState()
        self._documentVM.setDefaultState()
