import locale

from datetime import datetime

from PySide6 import QtWidgets, QtGui, QtCore

from .widgets.layout_table_widget import LayoutTableWidget

from .controllers.document_controller import DocumentController

from .services.html_template_service import HTMLTemplateService
from .services.pdf_service import PDFService
from .services.printer_service import PrinterService
from .services.readers.layout_service import LayoutService
from .services.readers.company_data_service import CompanyDataService

from .stores.layout_store import LayoutStore
from .stores.company_data_store import CompanyDataStore

from .factories.dialog_factory import DialogFactory


class GenDocument(QtWidgets.QWidget):
    """
    This Frame Module is responsible for generating our
    statement of responsibility for our employees.
    """

    def __init__(self, parent, controller):
        super().__init__(parent=parent)

        locale.setlocale(locale.LC_ALL, "")

        self.doc_controller = DocumentController(LayoutStore(), CompanyDataStore())

        self.html_tmpl_service = HTMLTemplateService(self.doc_controller)
        self.pdf_service = PDFService(self.doc_controller)
        self.printer_service = PrinterService(self.doc_controller)

        self.CreateWidgets(controller)
        self.GridConfiguration()

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
        self.label_layout_combobox = QtWidgets.QLabel(
            self, text="<b>Layout de Impressão</b>"
        )
        # ComboBox - Print Type
        self.layout_combobox = QtWidgets.QComboBox(self)
        print_types = list(
            map(
                self.layout_combobox.addItem,
                self.doc_controller.GetAllLayouts().keys(),
            )
        )
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
        self.table_document = LayoutTableWidget(
            self, self.doc_controller, self.layout_combobox
        )
        # CheckBox - Ativar Data Manual
        self.enable_date_picker = QtWidgets.QCheckBox(self, text="Ativar Data Manual.")
        self.enable_date_picker.setToolTip(
            "<b>Ativar Data Manual:</b>\nDesativa a data automâtica e permite a seleção de datas."
        )
        self.enable_date_picker.stateChanged.connect(self.EnableDatePicker)
        # CheckBox - Devolução
        self.is_device_return = QtWidgets.QCheckBox(
            self, text="Devolução de Dispositivo."
        )
        self.is_device_return.setToolTip(
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

    def GridConfiguration(self):
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
            self.label_layout_combobox,
            2,
            0,
            1,
            2,
            QtGui.Qt.AlignmentFlag.AlignCenter,
        )
        # ComboBox - Tipo de impressão
        widget_grid_layout.addWidget(self.layout_combobox, 3, 0, 1, 2)
        # separator - Tipo de impressão ComboBox
        widget_grid_layout.addWidget(self.separator_combobox, 4, 0, 1, 2)
        # Table - Data Layouts
        widget_grid_layout.addWidget(self.table_document, 5, 0, 6, 2)
        # separator - CheckBox
        widget_grid_layout.addWidget(self.separator_checkbox, 11, 0, 1, 2)
        # CheckBox - Ativar Data Manual
        widget_grid_layout.addWidget(self.enable_date_picker, 12, 0, 1, 1)
        # DateTimeEdit - Data Manual
        widget_grid_layout.addWidget(self.date_picker, 12, 1, 1, 1)
        # CheckBox - Ativar Devolução
        widget_grid_layout.addWidget(self.is_device_return, 13, 0, 1, 1)
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

    def EnableDatePicker(self):
        is_date_selectable: bool = (
            True if self.enable_date_picker.isChecked() else False
        )
        self.date_picker.setEnabled(is_date_selectable)

    def GenerateDocument(self):
        """
        Responsible to start the PDF creation and sending to a
        printer (optional).
        """

        result = self.table_document.ValidateRequiredInputs()

        if not result.is_valid:
            msg_box_icon = QtGui.QIcon("gen_document.ico")

            DialogFactory.CreateInfoMessageBox(
                f"Aviso - Campo {result.error_message} está vazio!",
                f"Sem {result.error_message}!",
                f"Por gentileza, coloque o {result.error_message}.",
                msg_win_icon=msg_box_icon,
            )
            return

        self.table_document.GetDataFromInputs()

        employee_name = self.table_document.GetEmployeeName()
        is_device_return = self.is_device_return.isChecked()
        self.doc_controller.SetOutputPath(employee_name, is_device_return)

        file_to_read = (
            self.doc_controller.GetCurrentLayout()["config"]["termo"]
            if not self.is_device_return.isChecked()
            else self.doc_controller.GetCurrentLayout()["config"]["termo_devol"]
        )

        date_text = (
            self.date_picker.text()
            if self.enable_date_picker.isChecked()
            else str(datetime.now().strftime("%A, %d de %B de %Y"))
        )

        self.doc_controller.GetInputData()["$data$"] = date_text

        clean_html = self.html_tmpl_service.Parse(file_to_read)
        self.pdf_service.Generate(clean_html)

        if not self.disable_printer.isChecked():
            self.printer_service.PrintDocument(
                self.disable_printer_preview.isChecked(),
                self.layout_combobox.currentText(),
            )

        # set the state to it's default value after using it
        self.doc_controller.SetDefaultState()
