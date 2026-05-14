import locale

from datetime import datetime

from PySide6 import QtWidgets, QtGui, QtCore

from ..widgets.layout_table_widget import LayoutTableWidget

from ..viewmodels.document_viewmodel import DocumentViewModel
from ..viewmodels.input_viewmodel import InputViewModel
from ..viewmodels.layout_viewmodel import LayoutViewModel

from ..services.html_template_service import HTMLTemplateService
from ..services.pdf_service import PDFService
from ..services.printer_service import PrinterService
from ..services.readers import CompanyJsonService, LayoutJsonService

from ..factories.dialog_factory import DialogFactory


class DocumentGeneratorView(QtWidgets.QWidget):
    """
    This Frame Module is responsible for generating our
    statement of responsibility for our employees.
    """

    def __init__(self, parent):
        super().__init__(parent=parent)

        locale.setlocale(locale.LC_ALL, "")

        self.documentVM = DocumentViewModel()
        self.inputVM = InputViewModel(CompanyJsonService("data/company.json"))
        self.layoutVM = LayoutViewModel(LayoutJsonService("data/layouts.json"))

        self.htmlTemplateService = HTMLTemplateService(self.documentVM.documentContext)
        self.pdfService = PDFService(self.documentVM.documentContext)
        self.printerService = PrinterService(self.documentVM.documentContext)

        self.createWidgets(parent)
        self.setGridConfiguration()

        # start with a tab opened
        self.switchLayoutTab(0)

    def createWidgets(self, controller):
        """
        Used to create new widgets (labels, buttons, etc.),
        controller (main window / controller widget) is used in buttons
        to show another page/frame widget.
        """

        # Tabs - layout
        self.tabs = QtWidgets.QTabBar(self)
        for layout in self.layoutVM.getAllLayouts().keys():
            self.tabs.addTab(layout)
        self.tabs.tabBarClicked.connect(self.switchLayoutTab)
        # Label - Title
        self.labelTitle = QtWidgets.QLabel(
            self, text="<b>Gerador de Termos de Responsabilidade</b>"
        )
        # separator - Title
        self.separatorTitle = QtWidgets.QFrame(self)
        self.separatorTitle.setLineWidth(1)
        self.separatorTitle.setFrameShape(QtWidgets.QFrame.HLine)
        self.separatorTitle.setFrameShadow(QtWidgets.QFrame.Sunken)
        # Table - Layouts Data
        self.tableDocument = LayoutTableWidget(
            self, self.documentVM, self.inputVM, self.layoutVM
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
        self.isDateSelectable.stateChanged.connect(self.enableDatePicker)
        # CheckBox - Devolução
        self.isDeviceReturn = QtWidgets.QCheckBox(
            self, text="Devolução de Dispositivo."
        )
        self.isDeviceReturn.setToolTip(
            "<b>Devolução de Dispositivo.:</b>\nAtive para gerar os termos de devolução."
        )
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
        self.buttonGenDoc.clicked.connect(self.generateDocument)

    def setGridConfiguration(self):
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
        # CheckBox - Ativar Devolução
        widgetGridLayout.addWidget(self.isDeviceReturn, 11, 0, 1, 1)
        # CheckBox - Desativar Visualização de Impressão
        widgetGridLayout.addWidget(self.disablePrinterPreview, 11, 1, 1, 1)
        # CheckBox - Desativar Impressão
        widgetGridLayout.addWidget(self.disablePrinter, 12, 0, 1, 1)
        # separator - Buttons
        widgetGridLayout.addWidget(self.separatorButtons, 15, 0, 1, 2)
        # PushButton - Gerar Documento
        widgetGridLayout.addWidget(self.buttonGenDoc, 16, 0, 1, 2)
        # space between widgets
        widgetGridLayout.setSpacing(10)
        # stretch a specific row
        widgetGridLayout.setRowStretch(13, 1)
        # set this widget layout to the grid layout
        self.setLayout(widgetGridLayout)

    def switchLayoutTab(self, index):
        layout = self.tabs.tabText(index)
        self.tableDocument.setTableLayout(layout)
        self.labelTitle.setText(
            f"<b>Gerador de Termos de Responsabilidade - {layout}</b>"
        )

    def enableDatePicker(self):
        isDateSelectable: bool = True if self.isDateSelectable.isChecked() else False
        self.datePicker.setEnabled(isDateSelectable)

    def generateDocument(self):
        """
        Responsible to start the PDF creation and sending to a
        printer (optional).
        """

        result = self.tableDocument.validateRequiredInputs()

        if not result.isValid:
            msgBoxIcon = QtGui.QIcon("gen_document.ico")

            DialogFactory.createInfoMessageBox(
                f"Aviso - Campo {result.errorMessage} está vazio!",
                f"Sem {result.errorMessage}!",
                f"Por gentileza, coloque o {result.errorMessage}.",
                msgWinIcon=msgBoxIcon,
            )
            return

        self.tableDocument.getDataFromInputs()

        employeeName = self.tableDocument.getEmployeeName()
        defaultPath = (
            self.layoutVM.getCurrentLayout()["config"]["output_devol"]
            if self.isDeviceReturn.isChecked()
            else self.layoutVM.getCurrentLayout()["config"]["output"]
        )
        self.documentVM.setOutputPath(employeeName, defaultPath)

        fileToRead = (
            self.layoutVM.getCurrentLayout()["config"]["termo"]
            if not self.isDeviceReturn.isChecked()
            else self.layoutVM.getCurrentLayout()["config"]["termo_devol"]
        )

        self.documentVM.readHTMLFiles(fileToRead)

        dateText = (
            self.datePicker.text()
            if self.isDateSelectable.isChecked()
            else str(datetime.now().strftime("%A, %d de %B de %Y"))
        )

        self.inputVM.getInputData()["$data$"] = dateText

        self.htmlTemplateService.parse(self.inputVM.getInputData())
        self.pdfService.generate()

        if not self.disablePrinter.isChecked():
            self.printerService.print(self.disablePrinterPreview.isChecked())

        # set the ViewModel state to it's default value after using it
        self.inputVM.setDefaultState()
        self.documentVM.clearDocumentState()
