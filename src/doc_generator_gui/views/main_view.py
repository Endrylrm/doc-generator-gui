from PySide6 import QtWidgets, QtGui

from ..viewmodels.document_viewmodel import DocumentViewModel
from ..viewmodels.input_viewmodel import InputViewModel
from ..viewmodels.layout_viewmodel import LayoutViewModel

from .document_generator_view import DocumentGeneratorView


class MainView(QtWidgets.QMainWindow):
    """
    This is our Main Window, it is responsible to show
    the view that we want.
    """

    def __init__(
        self,
        title: str = None,
        width: int = None,
        height: int = None,
        icon: str = None,
        documentVM: DocumentViewModel | None = None,
        inputVM: InputViewModel | None = None,
        layoutVM: LayoutViewModel | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        if title is not None:
            self.setWindowTitle(title)
        if width and height is not None:
            self._centerWindow(width, height)
        if icon is not None:
            self.setWindowIcon(QtGui.QIcon(icon))

        self.documentGenerator = DocumentGeneratorView(
            self, documentVM, inputVM, layoutVM
        )

        self.container = QtWidgets.QWidget(self)
        self.container.setGeometry(0, 0, width, height)
        self.containerGrid = QtWidgets.QGridLayout(self.container)
        self.containerGrid.addWidget(self.documentGenerator)
        self.container.setLayout(self.containerGrid)
        self.setCentralWidget(self.container)

    def _centerWindow(self, width: int = 300, height: int = 300):
        """
        Center our windows on screen and controls it's size.
        """

        self.setGeometry(0, 0, width, height)
        appGeometry = self.frameGeometry()
        screen = self.screen().availableGeometry().center()
        appGeometry.moveCenter(screen)
        self.move(appGeometry.topLeft())
