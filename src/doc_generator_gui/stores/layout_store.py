from ..services.readers import LayoutService


class LayoutStore:
    def __init__(self):
        self._layout_service = LayoutService("data/layouts.json")
        self._layouts = None

    def GetAllLayouts(self):
        if self._layouts is None:
            self._layouts = self._layout_service.Load()

        return self._layouts
