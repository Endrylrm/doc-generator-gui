__author__ = "Endryl Richard Monteiro"
__author_email__ = "Endrylrm@hotmail.com"

import sys

from PySide6 import QtWidgets, QtCore
from doc_generator_gui.app import App


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

    window = App("Gerador de Termos", 800, 600, "gen_document.ico")
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
