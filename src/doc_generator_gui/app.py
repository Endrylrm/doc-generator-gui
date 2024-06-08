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
        app_title: str = None,
        app_width: int = None,
        app_height: int = None,
        app_icon: str = None,
        *args,
        **kwargs
    ):
        """
        Main Window Widget "Application":
        Class App(app_title, app_width, app_height, app_icon):
        app_title: Used to change the Application Window Title.
        app_width: Used to change the Application Window Width.
        app_height: Used to change the Application Window Height.
        app_icon: Used to change the Application Icon.

        Initialization of Application (Main Window) Class.
        """

        super().__init__(*args, **kwargs)
        # Window Title
        if app_title is not None:
            self.setWindowTitle(app_title)
        # window size
        if app_width and app_height is not None:
            self.CenterWindow(app_width, app_height)
        # the Window icon
        if app_icon is not None:
            self.setWindowIcon(QtGui.QIcon(app_icon))
        # a container for our pages widgets
        self.container = QtWidgets.QWidget(self)
        # it's geometry is the size of our window
        self.container.setGeometry(0, 0, app_width, app_height)
        # our container grid layout
        self.container_grid = QtWidgets.QGridLayout(self.container)
        # set our container layout a grid layout
        self.container.setLayout(self.container_grid)
        # our pages / frames / widgets Dictionary
        self.pages = {}
        # current Page
        self.current_page: str = None
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
            self.container_grid.addWidget(self.pages[page], 0, 0)

    # Page/Frame to show function
    def ShowPage(self, page: str):
        """
        Function ShowPage(page)
        page: The string reference for the page in our pages Dictionary.

        The Switch logic uses a Dictionary, where the selected key show
        the specific page/frame.
        """

        # hide our current page
        if self.current_page is not None:
            self.pages[self.current_page].hide()
        # show our new page
        self.pages[page].show()
        # set our current page as our new page
        self.current_page = page

    # Center window function
    def CenterWindow(self, app_width: int = 300, app_height: int = 300):
        """
        Function CenterWindow(app_width, app_height)
        app_width: The width of our root/window widget.
        app_height: the height of our root/window widget.

        Center our windows on screen and controls it's size.
        """

        # set the size
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
