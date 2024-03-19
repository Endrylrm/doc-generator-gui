__author__ = "Endryl Richard Monteiro"
__author_email__ = "Endrylrm@hotmail.com"

from PySide6 import QtWidgets, QtGui

from .gen_document import Gen_Document


# Main Window Widget
class App(QtWidgets.QMainWindow):
    """
    Main Window Widget "Application":

    This is our Main Window, it is responsible to Load, switch
    and show the frame that we want.
    """

    def __init__(
        self,
        AppTitle: str = None,
        AppWidth: int = None,
        AppHeight: int = None,
        AppIcon: str = None,
        *args,
        **kwargs
    ):
        """
        Main Window Widget "Application":
        Class App(AppTitle, AppWidth, AppHeight, AppIcon):
        AppTitle: Used to change the Application Window Title.
        AppWidth: Used to change the Application Window Width.
        AppHeight: Used to change the Application Window Height.
        AppIcon: Used to change the Application Icon.

        Initialization of Application (Main Window) Class.
        """

        super().__init__(*args, **kwargs)
        # Window Title
        if AppTitle is not None:
            self.setWindowTitle(AppTitle)
        # window size
        if AppWidth and AppHeight is not None:
            self.CenterWindow(AppWidth, AppHeight)
        # the Window icon
        if AppIcon is not None:
            self.setWindowIcon(QtGui.QIcon(AppIcon))
        # a container for our pages widgets
        self.container = QtWidgets.QWidget(self)
        # it's geometry is the size of our window
        self.container.setGeometry(0, 0, AppWidth, AppHeight)
        # our container grid layout
        self.containerGrid = QtWidgets.QGridLayout(self.container)
        # set our container layout a grid layout
        self.container.setLayout(self.containerGrid)
        # our pages / frames / widgets Dictionary
        self.pages = {}
        # current Page
        self.currentPage: str = None
        # init our pages
        self.InitPages(self.container)
        # show the main page when we open our app
        self.ShowPage("Gen_Document")
        # set our container as our central widget
        # so our pages / frames resize with our window
        self.setCentralWidget(self.container)

    # Initialization of pages/frames
    def InitPages(self, container):
        """
        Function InitPages(container)
        container: Our container module, to control our widget size.

        Initialization for our Frames/Pages, requires a container and
        we add each of our pages to our dictionary.
        """

        # Application Home Page
        self.pages["Gen_Document"] = Gen_Document(container, self)
        self.pages["Gen_Document"].hide()

        # for each of our pages
        for page in self.pages:
            # Add our pages to Main Window container grid
            self.containerGrid.addWidget(self.pages[page], 0, 0)

    # Page/Frame to show function
    def ShowPage(self, page: str):
        """
        Function ShowPage(page)
        page: The string reference for the page in our pages Dictionary.

        The Switch logic uses a Dictionary, where the selected key show
        the specific page/frame.
        """

        # hide our current page
        if self.currentPage is not None:
            self.pages[self.currentPage].hide()
        # show our new page
        self.pages[page].show()
        # set our current page as our new page
        self.currentPage = page

    # Center window function
    def CenterWindow(self, AppWidth: int = 300, AppHeight: int = 300):
        """
        Function CenterWindow(AppWidth, AppHeight)
        AppWidth: The width of our root/window widget.
        AppHeight: the height of our root/window widget.

        Center our windows on screen and controls it's size.
        """

        # set the size
        self.setGeometry(0, 0, AppWidth, AppHeight)
        # get the frame geometry (size and position)
        appGeometry = self.frameGeometry()
        # get the center of the screen
        screen = self.screen().availableGeometry().center()
        # Move the frame to the center of the screen
        appGeometry.moveCenter(screen)
        # Also move our widget to the center of the screen
        # based on the top left point
        self.move(appGeometry.topLeft())
