from PySide6 import QtWidgets

from ..viewmodels.document_viewmodel import DocumentViewModel
from ..viewmodels.layout_viewmodel import LayoutViewModel


class LayoutTabWidget(QtWidgets.QTabBar):
    """
    This widget is responsible for changing our
    documents layouts.
    """

    def __init__(
        self,
        parent=None,
        documentVM: DocumentViewModel | None = None,
        layoutVM: LayoutViewModel | None = None,
    ):
        super().__init__(parent=parent)

        self._documentVM = documentVM
        self._layoutVM = layoutVM

        for layout in self._layoutVM.getAllLayouts().keys():
            self.addTab(layout)

        self.tabBarClicked.connect(self.switchLayoutTab)

    def switchLayoutTab(self, index: int):
        layout = self.tabText(index)
        self._layoutVM.setCurrentLayout(layout)
        self._documentVM.setPrintType(layout)
