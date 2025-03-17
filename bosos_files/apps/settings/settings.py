
from __future__ import annotations

import bauiv1 as bui
import bosos_files as bos

# export app Settings
class SettingsScreen(bos.AppWindow):

    def __init__(
        self,
        app_data,
        origin_widget: bui.Widget | None = None,
    ):

        super().__init__(
            app_data=app_data,
            origin_widget=origin_widget,
        )

        self._rebuild()

    def _rebuild(self) -> None:
        pass
