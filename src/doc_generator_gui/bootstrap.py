import sys

from PySide6 import QtWidgets, QtCore

from .core.di_container import DIContainer

from .contexts.document_context import DocumentContext

from .services.readers import ICompanyReader, ILayoutReader
from .services.readers import CompanyJsonReader, LayoutJsonReader

from .services.template_engine_service import TemplateEngineService
from .services.pdf_service import PDFService
from .services.printer_service import PrinterService

from .viewmodels.document_viewmodel import DocumentViewModel
from .viewmodels.input_viewmodel import InputViewModel
from .viewmodels.layout_viewmodel import LayoutViewModel

from .views.main_view import MainView


def bootstrap():
    app = QtWidgets.QApplication(sys.argv)

    translator = QtCore.QTranslator()

    if translator.load(
        QtCore.QLocale().system(),
        f"qtbase_{QtCore.QLocale().system().name()}",
        "",
        QtCore.QLibraryInfo.path(QtCore.QLibraryInfo.LibraryPath.TranslationsPath),
        ".qm",
    ):
        app.installTranslator(translator)

    # Dependency Injection - Container
    container = DIContainer()

    # Register Contexts
    container.register(DocumentContext, singleton=True)

    # Register Loaders / Readers
    container.registerFactory(
        ICompanyReader, lambda: CompanyJsonReader("data/company.json")
    )
    container.registerFactory(ILayoutReader, lambda: LayoutJsonReader("data/layouts/"))

    # Register Services
    container.register(TemplateEngineService)
    container.register(PDFService)
    container.register(PrinterService)

    # Register ViewModels
    container.register(DocumentViewModel)
    container.register(InputViewModel)
    container.register(LayoutViewModel)

    window = MainView(
        title="Gerador de Documentos",
        width=800,
        height=600,
        icon="gen_document.png",
        documentVM=container.resolve(DocumentViewModel),
        inputVM=container.resolve(InputViewModel),
        layoutVM=container.resolve(LayoutViewModel),
    )
    window.show()

    sys.exit(app.exec())
