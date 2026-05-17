import sys

from PySide6 import QtWidgets, QtCore

from .core.di_container import DIContainer

from .contexts.document_context import DocumentContext

from .services.readers import ICompanyReaderService, ILayoutReaderService
from .services.readers import CompanyJsonService, LayoutJsonService

from .services.template_engine_service import TemplateEngineService
from .services.pdf_service import PDFService
from .services.printer_service import PrinterService

from .viewmodels.document_viewmodel import DocumentViewModel
from .viewmodels.input_viewmodel import InputViewModel
from .viewmodels.layout_viewmodel import LayoutViewModel

from .views.main_view import MainView


def main():
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
        ICompanyReaderService, lambda: CompanyJsonService("data/company.json")
    )
    container.registerFactory(
        ILayoutReaderService, lambda: LayoutJsonService("data/layouts.json")
    )

    # Register Services
    container.register(TemplateEngineService)
    container.register(PDFService)
    container.register(PrinterService)

    # Register ViewModels
    container.register(DocumentViewModel)
    container.register(InputViewModel)
    container.register(LayoutViewModel)

    window = MainView(
        title="Gerador de Termos",
        width=800,
        height=600,
        icon="gen_document.ico",
        documentVM=container.resolve(DocumentViewModel),
        inputVM=container.resolve(InputViewModel),
        layoutVM=container.resolve(LayoutViewModel),
    )
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
