__author__ = "Endryl Richard Monteiro"
__author_email__ = "Endrylrm@hotmail.com"

from PySide6.QtGui import *
from PySide6.QtWidgets import *


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
    msg: The message box created previously.
    msg_win_title: the window title of our message box.
    msg_text: the text in our message box.
    msg_info_text: the information text in our message box.
    msg_detail_text: the detailed text of our message box.
    msg_icon: the icon on our message box.
    msg_buttons: the button on our message box.
    msg_default_button: the confirmation button/key, defaults to enter.
    msg_escape_button: the escape button/key, defaults to esc.
    msg_win_icon: used to add a icon to the window of our message box.

    Used to edit properties in our message Box.
    """

    if msg is None:
        print("no MessageBox to Edit!")
        return

    if msg_win_title is not None:
        msg.setWindowTitle(msg_win_title)
    if msg_text is not None:
        msg.setText(msg_text)
    if msg_info_text is not None:
        msg.setInformativeText(msg_info_text)
    if msg_detail_text is not None:
        msg.setDetailedText(msg_detail_text)
    if msg_icon is not None:
        msg.setIcon(msg_icon)
    if msg_buttons is not None:
        msg.setStandardButtons(msg_buttons)
    if msg_default_button is not None:
        msg.setDefaultButton(msg_default_button)
    if msg_escape_button is not None:
        msg.setEscapeButton(msg_escape_button)

    if msg_win_icon is not None:
        msg.setWindowIcon(msg_win_icon)


def DisplayMessageBox(msg: QMessageBox):
    """
    msg: The message box you want to execute/display.

    Used to display a message box.
    """

    msg.exec()


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
    msg_win_title: Message box window title.
    msg_text: The text in our message box.
    msg_info_text: the information text in our message box.
    msg_detail_text: the detailed text of our message box, defaults to None.
    msg_icon: the icon on our message box (defaults to QMessageBox.Information).
    msg_buttons: the button on our message box (defaults to QMessageBox.Ok).
    msg_default_button: the confirmation button/key, defaults to enter.
    msg_escape_button: the escape button/key, defaults to esc.
    msg_win_icon: used to add a icon to the window of our message box.

    Used to create a new message box, that's editable to your needs,
    returns a QMessageBox object.
    """

    msg = QMessageBox()

    if msg_win_title is not None:
        msg.setWindowTitle(msg_win_title)
    if msg_text is not None:
        msg.setText(msg_text)
    if msg_info_text is not None:
        msg.setInformativeText(msg_info_text)
    if msg_detail_text is not None:
        msg.setDetailedText(msg_detail_text)
    if msg_icon is not None:
        msg.setIcon(msg_icon)
    if msg_buttons is not None:
        msg.setStandardButtons(msg_buttons)
    if msg_default_button is not None:
        msg.setDefaultButton(msg_default_button)
    if msg_escape_button is not None:
        msg.setEscapeButton(msg_escape_button)
    if msg_win_title is not None:
        msg.setWindowTitle(msg_win_title)
    if msg_win_icon is not None:
        msg.setWindowIcon(msg_win_icon)

    return msg


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
    msg_win_title: Message box window title.
    msg_text: The text in our message box.
    msg_info_text: the information text in our message box.
    msg_detail_text: the detailed text of our message box, defaults to None.
    msg_buttons: the button on our message box (defaults to QMessageBox.Ok).
    msg_default_button: the confirmation button/key, defaults to enter.
    msg_escape_button: the escape button/key, defaults to esc.
    msg_win_icon: used to add a icon to the window of our message box.

    Used to create a new information message box and display it.
    """

    msg = CreateMessageBox(
        msg_win_title=msg_win_title,
        msg_text=msg_text,
        msg_info_text=msg_info_text,
        msg_detail_text=msg_detail_text,
        msg_icon=QMessageBox.Information,
        msg_buttons=msg_buttons,
        msg_default_button=msg_default_button,
        msg_escape_button=msg_escape_button,
        msg_win_icon=msg_win_icon,
    )

    DisplayMessageBox(msg)


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
    msg_win_title: Message box window title.
    msg_text: The text in our message box.
    msg_info_text: the information text in our message box.
    msg_detail_text: the detailed text of our message box, defaults to None.
    msg_buttons: the button on our message box (defaults to QMessageBox.Ok).
    msg_default_button: the confirmation button/key, defaults to enter.
    msg_escape_button: the escape button/key, defaults to esc.
    msg_win_icon: used to add a icon to the window of our message box.

    Used to create a new Warning message box and display it.
    """

    msg = CreateMessageBox(
        msg_win_title=msg_win_title,
        msg_text=msg_text,
        msg_info_text=msg_info_text,
        msg_detail_text=msg_detail_text,
        msg_icon=QMessageBox.Warning,
        msg_buttons=msg_buttons,
        msg_default_button=msg_default_button,
        msg_escape_button=msg_escape_button,
        msg_win_icon=msg_win_icon,
    )

    DisplayMessageBox(msg)


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
    msg_win_title: Message box window title.
    msg_text: The text in our message box.
    msg_info_text: the information text in our message box.
    msg_detail_text: the detailed text of our message box, defaults to None.
    msg_buttons: the button on our message box (defaults to QMessageBox.Ok).
    msg_default_button: the confirmation button/key, defaults to enter.
    msg_escape_button: the escape button/key, defaults to esc.
    msg_win_icon: used to add a icon to the window of our message box.

    Used to create a new critical/error message box and display it.
    """

    msg = CreateMessageBox(
        msg_win_title=msg_win_title,
        msg_text=msg_text,
        msg_info_text=msg_info_text,
        msg_detail_text=msg_detail_text,
        msg_icon=QMessageBox.Critical,
        msg_buttons=msg_buttons,
        msg_default_button=msg_default_button,
        msg_escape_button=msg_escape_button,
        msg_win_icon=msg_win_icon,
    )

    DisplayMessageBox(msg)


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
    msg_win_title: Message box window title.
    msg_text: The text in our message box.
    msg_info_text: the information text in our message box.
    msg_detail_text: the detailed text of our message box, defaults to None.
    msg_buttons: the button on our message box (defaults to QMessageBox.Ok).
    msg_default_button: the confirmation button/key, defaults to enter.
    msg_escape_button: the escape button/key, defaults to esc.
    msg_win_icon: used to add a icon to the window of our message box.

    Used to create a new Question message box, returns a QMessageBox object.
    """

    msg = CreateMessageBox(
        msg_win_title=msg_win_title,
        msg_text=msg_text,
        msg_info_text=msg_info_text,
        msg_detail_text=msg_detail_text,
        msg_icon=QMessageBox.Question,
        msg_buttons=msg_buttons,
        msg_default_button=msg_default_button,
        msg_escape_button=msg_escape_button,
        msg_win_icon=msg_win_icon,
    )

    return msg
