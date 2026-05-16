from PySide6 import QtWidgets, QtGui

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
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        if title is not None:
            self.setWindowTitle(title)
        if width and height is not None:
            self.centerWindow(width, height)
        if icon is not None:
            self.setWindowIcon(QtGui.QIcon(icon))

        self.documentGenerator = DocumentGeneratorView(self)

        self.container = QtWidgets.QWidget(self)
        self.container.setGeometry(0, 0, width, height)
        self.containerGrid = QtWidgets.QGridLayout(self.container)
        self.containerGrid.addWidget(self.documentGenerator)
        self.container.setLayout(self.containerGrid)
        self.setCentralWidget(self.container)

    def centerWindow(self, width: int = 300, height: int = 300):
        """
        Center our windows on screen and controls it's size.
        """

        # set the size of our window
        self.setGeometry(0, 0, width, height)
        # get the frame geometry (size and position)
        appGeometry = self.frameGeometry()
        # get the center of the screen
        screen = self.screen().availableGeometry().center()
        # Move the frame to the center of the screen
        appGeometry.moveCenter(screen)
        # move our widget to the center of the screen
        # based on the top left point
        self.move(appGeometry.topLeft())
