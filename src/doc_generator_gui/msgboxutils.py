__author__ = "Endryl Richard Monteiro"
__author_email__ = "Endrylrm@hotmail.com"

from PySide6.QtGui import *
from PySide6.QtWidgets import *

"""
Message Box Utilities:
Creation and editing of message box made faster.
"""


# Edit properties in a Message Box
def EditMessageBoxProps(
    msg: QMessageBox,
    msg_win_title=None,
    msg_text=None,
    msg_info_text=None,
    msg_detail_text=None,
    msg_icon=None,
    msg_buttons=None,
    msg_default_button=None,
    msg_escape_button=None,
    msg_win_icon=None,
):
    """
    Function EditMessageBoxProps(msg, msg_win_title, msg_text, msg_info_text, msg_icon, msg_buttons, msg_default_button, msg_escape_button)
    msg: The message box created previously.
    msg_win_title: the window title of our message box.
    msg_text: the text in our message box.
    msg_info_text: the information text in our message box.
    msg_detail_text: the detailed text of our message box.
    msg_icon: the icon on our message box.
    msg_buttons: the button on our message box.
    msg_default_button: the confirmation button/key, defaults to enter.
    msg_escape_button: the escape button/key, defaults to esc.
    msg_win_icon: used to add a icon to the window of our message box. \n
    Used to edit properties in our message Box.
    """
    if msg is None:
        print("no MessageBox to Edit!")
        return

    # set message box window title, if it's not none.
    if msg_win_title is not None:
        msg.setWindowTitle(msg_win_title)
    # set message box text, if it's not none.
    if msg_text is not None:
        msg.setText(msg_text)
    # set our informative text, if it's not none.
    if msg_info_text is not None:
        msg.setInformativeText(msg_info_text)
    # set our detailed text, if it's not none.
    if msg_detail_text is not None:
        msg.setDetailedText(msg_detail_text)
    # set message box icon, if it's not none.
    if msg_icon is not None:
        msg.setIcon(msg_icon)
    # set message box button, if it's not none.
    if msg_buttons is not None:
        msg.setStandardButtons(msg_buttons)
    # set message box default confirmation button/key (enter key), if it's not none.
    if msg_default_button is not None:
        msg.setDefaultButton(msg_default_button)
    # set message box escape confirmation button/key (esc key), if it's not none.
    if msg_escape_button is not None:
        msg.setEscapeButton(msg_escape_button)

    if msg_win_icon is not None:
        msg.setWindowIcon(msg_win_icon)


# Display a Message Box
def DisplayMessageBox(msg: QMessageBox):
    """
    Function DisplayMessageBox(msg)
    msg: The message box you want to execute/display. \n
    Used to display a message box.
    """

    # execute the message box
    msg.exec()


# Create a new Message Box
def CreateMessageBox(
    msg_win_title=None,
    msg_text=None,
    msg_info_text=None,
    msg_detail_text=None,
    msg_icon=QMessageBox.Information,
    msg_buttons=QMessageBox.Ok,
    msg_default_button=None,
    msg_escape_button=None,
    msg_win_icon=None,
) -> QMessageBox:
    """
    Function CreateMessageBox(msg_win_title, msg_text, msg_info_text, msg_detail_text, msg_icon, msg_buttons, msg_default_button, msg_escape_button, msg_win_icon)
    msg_win_title: Message box window title.
    msg_text: The text in our message box.
    msg_info_text: the information text in our message box.
    msg_detail_text: the detailed text of our message box, defaults to None.
    msg_icon: the icon on our message box (defaults to QMessageBox.Information).
    msg_buttons: the button on our message box (defaults to QMessageBox.Ok).
    msg_default_button: the confirmation button/key, defaults to enter.
    msg_escape_button: the escape button/key, defaults to esc.
    msg_win_icon: used to add a icon to the window of our message box.\n
    Used to create a new message box, that's editable to your needs,
    returns a QMessageBox object.
    """

    # create a new message box
    msg = QMessageBox()
    # set message box window title, if it's not none.
    if msg_win_title is not None:
        msg.setWindowTitle(msg_win_title)
    # set message box text, if it's not none.
    if msg_text is not None:
        msg.setText(msg_text)
    # set our informative text, if it's not none.
    if msg_info_text is not None:
        msg.setInformativeText(msg_info_text)
    # set our detailed text, if it's not none.
    if msg_detail_text is not None:
        msg.setDetailedText(msg_detail_text)
    # set message box icon, if it's not none.
    if msg_icon is not None:
        msg.setIcon(msg_icon)
    # set message box button, if it's not none.
    if msg_buttons is not None:
        msg.setStandardButtons(msg_buttons)
    # set message box default confirmation button/key (enter key), if it's not none.
    if msg_default_button is not None:
        msg.setDefaultButton(msg_default_button)
    # set message box escape confirmation button/key (esc key), if it's not none.
    if msg_escape_button is not None:
        msg.setEscapeButton(msg_escape_button)
    if msg_win_title is not None:
        msg.setWindowTitle(msg_win_title)
    if msg_win_icon is not None:
        msg.setWindowIcon(msg_win_icon)
    # return our new message box
    return msg


# Create a new Information Message Box
def CreateInfoMessageBox(
    msg_win_title,
    msg_text,
    msg_info_text,
    msg_detail_text=None,
    msg_buttons=QMessageBox.Ok,
    msg_default_button=None,
    msg_escape_button=None,
    msg_win_icon=None,
):
    """
    Function CreateInfoMessageBox(winTitle, msg_text, msg_info_text, msg_detail_text, msg_buttons, msg_default_button, msg_escape_button)
    msg_win_title: Message box window title.
    msg_text: The text in our message box.
    msg_info_text: the information text in our message box.
    msg_detail_text: the detailed text of our message box, defaults to None.
    msg_buttons: the button on our message box (defaults to QMessageBox.Ok).
    msg_default_button: the confirmation button/key, defaults to enter.
    msg_escape_button: the escape button/key, defaults to esc.
    msg_win_icon: used to add a icon to the window of our message box. \n
    Used to create a new information message box and display it.
    """

    # create a new message box
    msg = CreateMessageBox(
        # set message box window title
        msg_win_title=msg_win_title,
        # set message box text
        msg_text=msg_text,
        # set our information text.
        msg_info_text=msg_info_text,
        # set our detailed text.
        msg_detail_text=msg_detail_text,
        # this is a information message box
        msg_icon=QMessageBox.Information,
        # set message box button
        msg_buttons=msg_buttons,
        # set message box default confirmation button/key (enter key)
        msg_default_button=msg_default_button,
        # set message box escape confirmation button/key (esc key)
        msg_escape_button=msg_escape_button,
        msg_win_icon=msg_win_icon,
    )
    # execute the message box
    DisplayMessageBox(msg)


# Create a new Warning Message Box
def CreateWarningMessageBox(
    msg_win_title,
    msg_text,
    msg_info_text,
    msg_detail_text=None,
    msg_buttons=QMessageBox.Ok,
    msg_default_button=None,
    msg_escape_button=None,
    msg_win_icon=None,
):
    """
    Function CreateWarningMessageBox(winTitle, msg_text, msg_info_text, msg_detail_text, msg_buttons, msg_default_button, msg_escape_button)
    msg_win_title: Message box window title.
    msg_text: The text in our message box.
    msg_info_text: the information text in our message box.
    msg_detail_text: the detailed text of our message box, defaults to None.
    msg_buttons: the button on our message box (defaults to QMessageBox.Ok).
    msg_default_button: the confirmation button/key, defaults to enter.
    msg_escape_button: the escape button/key, defaults to esc.
    msg_win_icon: used to add a icon to the window of our message box. \n
    Used to create a new Warning message box and display it.
    """

    # create a new message box
    msg = CreateMessageBox(
        # set message box window title
        msg_win_title=msg_win_title,
        # set message box text
        msg_text=msg_text,
        # set our information text.
        msg_info_text=msg_info_text,
        # set our detailed text.
        msg_detail_text=msg_detail_text,
        # this is a Warning message box
        msg_icon=QMessageBox.Warning,
        # set message box button
        msg_buttons=msg_buttons,
        # set message box default confirmation button/key (enter key)
        msg_default_button=msg_default_button,
        # set message box escape confirmation button/key (esc key)
        msg_escape_button=msg_escape_button,
        msg_win_icon=msg_win_icon,
    )
    # execute the message box
    DisplayMessageBox(msg)


# Create a new Critical/Error Message Box
def CreateErrorMessageBox(
    msg_win_title,
    msg_text,
    msg_info_text,
    msg_detail_text=None,
    msg_buttons=QMessageBox.Ok,
    msg_default_button=None,
    msg_escape_button=None,
    msg_win_icon=None,
):
    """
    Function CreateErrorMessageBox(winTitle, msg_text, msg_info_text, msg_detail_text, msg_buttons, msg_default_button, msg_escape_button)
    msg_win_title: Message box window title.
    msg_text: The text in our message box.
    msg_info_text: the information text in our message box.
    msg_detail_text: the detailed text of our message box, defaults to None.
    msg_buttons: the button on our message box (defaults to QMessageBox.Ok).
    msg_default_button: the confirmation button/key, defaults to enter.
    msg_escape_button: the escape button/key, defaults to esc.
    msg_win_icon: used to add a icon to the window of our message box. \n
    Used to create a new critical/error message box and display it.
    """

    # create a new message box
    msg = CreateMessageBox(
        # set message box window title
        msg_win_title=msg_win_title,
        # set message box text
        msg_text=msg_text,
        # set our information text.
        msg_info_text=msg_info_text,
        # set our detailed text.
        msg_detail_text=msg_detail_text,
        # this is a Critical/Error message box
        msg_icon=QMessageBox.Critical,
        # set message box button
        msg_buttons=msg_buttons,
        # set message box default confirmation button/key (enter key)
        msg_default_button=msg_default_button,
        # set message box escape confirmation button/key (esc key)
        msg_escape_button=msg_escape_button,
        msg_win_icon=msg_win_icon,
    )
    # execute the message box
    DisplayMessageBox(msg)


# Create a new Question Message Box
def CreateQuestionMessageBox(
    msg_win_title,
    msg_text,
    msg_info_text,
    msg_detail_text=None,
    msg_buttons=QMessageBox.Ok,
    msg_default_button=None,
    msg_escape_button=None,
    msg_win_icon=None,
) -> QMessageBox:
    """
    Function CreateQuestionMessageBox(winTitle, msg_text, msg_info_text, msg_detail_text, msg_buttons, msg_default_button, msg_escape_button)
    msg_win_title: Message box window title.
    msg_text: The text in our message box.
    msg_info_text: the information text in our message box.
    msg_detail_text: the detailed text of our message box, defaults to None.
    msg_buttons: the button on our message box (defaults to QMessageBox.Ok).
    msg_default_button: the confirmation button/key, defaults to enter.
    msg_escape_button: the escape button/key, defaults to esc.
    msg_win_icon: used to add a icon to the window of our message box. \n
    Used to create a new Question message box, returns a QMessageBox object.
    """

    # create a new message box
    msg = CreateMessageBox(
        # set message box window title
        msg_win_title=msg_win_title,
        # set message box text
        msg_text=msg_text,
        # set our information text.
        msg_info_text=msg_info_text,
        # set our detailed text.
        msg_detail_text=msg_detail_text,
        # this is a Critical/Error message box
        msg_icon=QMessageBox.Question,
        # set message box button
        msg_buttons=msg_buttons,
        # set message box default confirmation button/key (enter key)
        msg_default_button=msg_default_button,
        # set message box escape confirmation button/key (esc key)
        msg_escape_button=msg_escape_button,
        msg_win_icon=msg_win_icon,
    )
    # return our new Question message box
    return msg
