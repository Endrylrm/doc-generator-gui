__author__ = "Endryl Richard Monteiro"
__author_email__ = "Endrylrm@hotmail.com"

from PySide6 import QtWidgets, QtGui

from .gen_document import Gen_Document


class App(QtWidgets.QMainWindow):
    """
    Main Window Widget "Application":

    This is our Main Window, it is responsible to Load, switch
    and show the frame that we want.
    """

    def __init__(
        self,
        app_title: str = None,
        app_width: int = None,
        app_height: int = None,
        app_icon: str = None,
        *args,
        **kwargs
    ):
        """
        Main Window Widget "Application":

        Initialization of Application (Main Window) Class.
        """

        super().__init__(*args, **kwargs)
        if app_title is not None:
            self.setWindowTitle(app_title)
        if app_width and app_height is not None:
            self.CenterWindow(app_width, app_height)
        if app_icon is not None:
            self.setWindowIcon(QtGui.QIcon(app_icon))
        self.container = QtWidgets.QWidget(self)
        self.container.setGeometry(0, 0, app_width, app_height)
        self.container_grid = QtWidgets.QGridLayout(self.container)
        self.container.setLayout(self.container_grid)
        self.pages = {}
        self.current_page: str = None
        self.InitPages(self.container)
        self.ShowPage("Gen_Document")
        self.setCentralWidget(self.container)

    def InitPages(self, container):
        """
        Initialization for our Frames/Pages, requires a container and
        we add each of our pages to our dictionary.
        """

        # Application Home Page
        self.pages["Gen_Document"] = Gen_Document(container, self)
        self.pages["Gen_Document"].hide()

        for page in self.pages:
            self.container_grid.addWidget(self.pages[page], 0, 0)

    def ShowPage(self, page: str):
        """
        The Switch logic uses a Dictionary, where the selected key show
        the specific page/frame.
        """

        if self.current_page is not None:
            self.pages[self.current_page].hide()
        self.pages[page].show()
        self.current_page = page

    def CenterWindow(self, app_width: int = 300, app_height: int = 300):
        """
        Center our windows on screen and controls it's size.
        """

        # set the size of our window
        self.setGeometry(0, 0, app_width, app_height)
        # get the frame geometry (size and position)
        app_geometry = self.frameGeometry()
        # get the center of the screen
        screen = self.screen().availableGeometry().center()
        # Move the frame to the center of the screen
        app_geometry.moveCenter(screen)
        # Also move our widget to the center of the screen
        # based on the top left point
        self.move(app_geometry.topLeft())
