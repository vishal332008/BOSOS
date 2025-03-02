# pylint: disable=all

from __future__ import annotations

from typing import override

import math
import babase
import bauiv1 as bui
import bascenev1 as bs

from bosos_files.app_window import AppWindow

# export app Settings
class SettingsScreen(AppWindow):

    def __init__(
        self,
        width: float = 800.0,
        height: float = 600.0,
        transition: str | None = 'in_right',
        origin_widget: bui.Widget | None = None,
    ):
        
        super().__init__(
            name="Settings",
            width=width,
            height=height,
            transition=transition,
            origin_widget=origin_widget,
        )

        self._rebuild()

    @override
    def get_main_window_state(self) -> bui.MainWindowState:
        # Support recreating our window for back/refresh purposes.
        cls = type(self)
        return bui.BasicMainWindowState(
            create_call=lambda transition, origin_widget: cls(
                transition=transition, origin_widget=origin_widget
            )
        )

    @override
    def on_main_window_close(self) -> None:
        pass

    def _rebuild(self) -> None:
        pass