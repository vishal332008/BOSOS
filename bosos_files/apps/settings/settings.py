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
        app_data,
        width: float = 800.0,
        height: float = 600.0,
        transition: str | None = 'in_right',
        origin_widget: bui.Widget | None = None,
    ):

        super().__init__(
            name=app_data.name,
            filename=app_data.filename,
            width=width,
            height=height,
            transition=transition,
            origin_widget=origin_widget,
        )

        self._rebuild()

    def _rebuild(self) -> None:
        pass
