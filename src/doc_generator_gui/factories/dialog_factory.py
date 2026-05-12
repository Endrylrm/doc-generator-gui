from PySide6 import QtWidgets


class DialogFactory:
    """
    This class is responsible for creating our Message boxes
    or dialogs in the application
    """

    @classmethod
    def __createMessageBox(
        cls,
        msgWinTitle=None,
        msgText=None,
        msgInfoText=None,
        msgDetailText=None,
        msgIcon=QtWidgets.QMessageBox.Information,
        msgButtons=QtWidgets.QMessageBox.Ok,
        msgDefaultButton=None,
        msgEscapeButton=None,
        msgWinIcon=None,
    ) -> QtWidgets.QMessageBox:
        """
        msgWinTitle: Message box window title.
        msgText: The text in our message box.
        msgInfoText: the information text in our message box.
        msgDetailText: the detailed text of our message box, defaults to None.
        msgIcon: the icon on our message box (defaults to QMessageBox.Information).
        msgButtons: the button on our message box (defaults to QMessageBox.Ok).
        msgDefaultButton: the confirmation button/key, defaults to enter.
        msgEscapeButton: the escape button/key, defaults to esc.
        msgWinIcon: used to add a icon to the window of our message box.

        Used to create a new message box, that's editable to your needs,
        returns a QMessageBox object.
        """

        msg = QtWidgets.QMessageBox()

        if msgWinTitle is not None:
            msg.setWindowTitle(msgWinTitle)
        if msgText is not None:
            msg.setText(msgText)
        if msgInfoText is not None:
            msg.setInformativeText(msgInfoText)
        if msgDetailText is not None:
            msg.setDetailedText(msgDetailText)
        if msgIcon is not None:
            msg.setIcon(msgIcon)
        if msgButtons is not None:
            msg.setStandardButtons(msgButtons)
        if msgDefaultButton is not None:
            msg.setDefaultButton(msgDefaultButton)
        if msgEscapeButton is not None:
            msg.setEscapeButton(msgEscapeButton)
        if msgWinTitle is not None:
            msg.setWindowTitle(msgWinTitle)
        if msgWinIcon is not None:
            msg.setWindowIcon(msgWinIcon)

        return msg

    @classmethod
    def createInfoMessageBox(
        cls,
        msgWinTitle,
        msgText,
        msgInfoText,
        msgDetailText=None,
        msgButtons=QtWidgets.QMessageBox.Ok,
        msgDefaultButton=None,
        msgEscapeButton=None,
        msgWinIcon=None,
    ):
        """
        msgWinTitle: Message box window title.
        msgText: The text in our message box.
        msgInfoText: the information text in our message box.
        msgDetailText: the detailed text of our message box, defaults to None.
        msgButtons: the button on our message box (defaults to QMessageBox.Ok).
        msgDefaultButton: the confirmation button/key, defaults to enter.
        msgEscapeButton: the escape button/key, defaults to esc.
        msgWinIcon: used to add a icon to the window of our message box.

        Used to create a new information message box and display it.
        """

        msg = cls.__createMessageBox(
            msgWinTitle=msgWinTitle,
            msgText=msgText,
            msgInfoText=msgInfoText,
            msgDetailText=msgDetailText,
            msg_icon=QtWidgets.QMessageBox.Information,
            msgButtons=msgButtons,
            msgDefaultButton=msgDefaultButton,
            msgEscapeButton=msgEscapeButton,
            msgWinIcon=msgWinIcon,
        )

        msg.exec()

    @classmethod
    def createWarningMessageBox(
        cls,
        msgWinTitle,
        msgText,
        msgInfoText,
        msgDetailText=None,
        msgButtons=QtWidgets.QMessageBox.Ok,
        msgDefaultButton=None,
        msgEscapeButton=None,
        msgWinIcon=None,
    ):
        """
        msgWinTitle: Message box window title.
        msgText: The text in our message box.
        msgInfoText: the information text in our message box.
        msgDetailText: the detailed text of our message box, defaults to None.
        msgButtons: the button on our message box (defaults to QMessageBox.Ok).
        msgDefaultButton: the confirmation button/key, defaults to enter.
        msgEscapeButton: the escape button/key, defaults to esc.
        msgWinIcon: used to add a icon to the window of our message box.

        Used to create a new Warning message box and display it.
        """

        msg = cls.__createMessageBox(
            msgWinTitle=msgWinTitle,
            msgText=msgText,
            msgInfoText=msgInfoText,
            msgDetailText=msgDetailText,
            msg_icon=QtWidgets.QMessageBox.Warning,
            msgButtons=msgButtons,
            msgDefaultButton=msgDefaultButton,
            msgEscapeButton=msgEscapeButton,
            msgWinIcon=msgWinIcon,
        )

        msg.exec()

    @classmethod
    def createErrorMessageBox(
        cls,
        msgWinTitle,
        msgText,
        msgInfoText,
        msgDetailText=None,
        msgButtons=QtWidgets.QMessageBox.Ok,
        msgDefaultButton=None,
        msgEscapeButton=None,
        msgWinIcon=None,
    ):
        """
        msgWinTitle: Message box window title.
        msgText: The text in our message box.
        msgInfoText: the information text in our message box.
        msgDetailText: the detailed text of our message box, defaults to None.
        msgButtons: the button on our message box (defaults to QMessageBox.Ok).
        msgDefaultButton: the confirmation button/key, defaults to enter.
        msgEscapeButton: the escape button/key, defaults to esc.
        msgWinIcon: used to add a icon to the window of our message box.

        Used to create a new critical/error message box and display it.
        """

        msg = cls.__createMessageBox(
            msgWinTitle=msgWinTitle,
            msgText=msgText,
            msgInfoText=msgInfoText,
            msgDetailText=msgDetailText,
            msg_icon=QtWidgets.QMessageBox.Critical,
            msgButtons=msgButtons,
            msgDefaultButton=msgDefaultButton,
            msgEscapeButton=msgEscapeButton,
            msgWinIcon=msgWinIcon,
        )

        msg.exec()

    @classmethod
    def createQuestionMessageBox(
        cls,
        msgWinTitle,
        msgText,
        msgInfoText,
        msgDetailText=None,
        msgButtons=QtWidgets.QMessageBox.Ok,
        msgDefaultButton=None,
        msgEscapeButton=None,
        msgWinIcon=None,
    ):
        """
        msgWinTitle: Message box window title.
        msgText: The text in our message box.
        msgInfoText: the information text in our message box.
        msgDetailText: the detailed text of our message box, defaults to None.
        msgButtons: the button on our message box (defaults to QMessageBox.Ok).
        msgDefaultButton: the confirmation button/key, defaults to enter.
        msgEscapeButton: the escape button/key, defaults to esc.
        msgWinIcon: used to add a icon to the window of our message box.

        Used to create a new Question message box, returns a QMessageBox object.
        """

        msg = cls.__createMessageBox(
            msgWinTitle=msgWinTitle,
            msgText=msgText,
            msgInfoText=msgInfoText,
            msgDetailText=msgDetailText,
            msg_icon=QtWidgets.QMessageBox.Question,
            msgButtons=msgButtons,
            msgDefaultButton=msgDefaultButton,
            msgEscapeButton=msgEscapeButton,
            msgWinIcon=msgWinIcon,
        )

        return msg
