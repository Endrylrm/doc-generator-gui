import sys

from PySide6 import QtWidgets, QtCore
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

    window = MainView("Gerador de Termos", 800, 600, "gen_document.ico")
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
