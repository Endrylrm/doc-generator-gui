from PySide6 import QtWidgets, QtGui

from .gen_document import GenDocument


class Application(QtWidgets.QMainWindow):
    """
    This is our Main Window, it is responsible to Load, switch
    and show the frame that we want.
    """

    def __init__(
        self,
        title: str = None,
        width: int = None,
        height: int = None,
        icon: str = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        if title is not None:
            self.setWindowTitle(title)
        if width and height is not None:
            self.centerWindow(width, height)
        if icon is not None:
            self.setWindowIcon(QtGui.QIcon(icon))
        self.container = QtWidgets.QWidget(self)
        self.container.setGeometry(0, 0, width, height)
        self.containerGrid = QtWidgets.QGridLayout(self.container)
        self.container.setLayout(self.containerGrid)
        self.pages = {}
        self.currentPage: str = None
        self.initPages(self.container)
        self.showPage("GenDocument")
        self.setCentralWidget(self.container)

    def initPages(self, container):
        """
        Initialization for our Frames/Pages, requires a container and
        we add each of our pages to our dictionary.
        """

        # Application Home Page
        self.pages["GenDocument"] = GenDocument(container, self)
        self.pages["GenDocument"].hide()

        for page in self.pages:
            self.containerGrid.addWidget(self.pages[page], 0, 0)

    def showPage(self, page: str):
        """
        The Switch logic uses a Dictionary, where the selected key show
        the specific page/frame.
        """

        if self.currentPage is not None:
            self.pages[self.currentPage].hide()
        self.pages[page].show()
        self.currentPage = page

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
