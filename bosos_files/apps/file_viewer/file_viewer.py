
from __future__ import annotations

import os
import functools
import bauiv1 as bui
import bosos_files as bos


# export app File_Viewer
class FileViewerScreen(bos.AppWindow):

    def __init__(
        self,
        app_data,
        origin_widget: bui.Widget | None = None,
    ):

        app = bui.app
        assert app.classic is not None

        super().__init__(
            app_data=app_data,
            origin_widget=origin_widget,
        )

        self._audio_button: bui.Widget | None = None
        self._texture_button: bui.Widget | None = None

        self._build_ui()

    def _build_ui(self) -> None:

        self._audio_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(self.width/2 - 180, self.height/2),
            size=(360, 120),
            label='Audio',
            text_scale=1.3,
        )
        self._texture_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(self.width/2 - 180, self.height/2 - 130),
            size=(360, 120),
            label='Textures',
            text_scale=1.3,
            on_activate_call=self._open_textures_window
        )

    def _open_textures_window(self):
        print("open texture button pressed")
