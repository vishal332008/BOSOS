from __future__ import annotations

import os

import bauiv1 as bui
import bosos_files as bos


class AppWindow:
    """ Common/Base class for all apps """

    def __init__(
        self,
        *,
        app_data,
        origin_widget: bui.Widget | None,
     ) -> None:

        self._app_data = app_data

        scrn_width = bui.app.mode.main_screen.width
        scrn_height = bui.app.mode.main_screen.height

        self.width = scrn_width * 0.7
        self.height = scrn_height * 0.6

        xpos = (scrn_width-self.width)/2
        ypos = (scrn_height-self.height)/2

        texture_name = (
            f'apps{os.sep}{self._app_data.filename}{os.sep}logo'
            if self._app_data.filename else "white"
        )

        self._root_widget = bui.containerwidget(
            parent=bui.app.mode.main_screen._root_widget,
            position=(xpos, ypos),
            size=(self.width, self.height),
            transition="in_scale",
            scale_origin_stack_offset=origin_widget.get_screen_space_center(),
            background=False
        )

        self._bg_tex = bui.imagewidget(
            parent=self._root_widget,
            size=(self.width, self.height),
            texture=bui.gettexture("white"),
            color=(0, 0, 0),
        )

        self._top_bar = bui.imagewidget(
            parent=self._root_widget,
            position=(0, self.height),
            size=(self.width, 40),
            texture=bui.gettexture("white")
        )

        self._icon_img = bui.imagewidget(
            parent=self._root_widget,
            position=(5, self.height+5),
            size=(30, 30),
            texture=bui.gettexture(texture_name),
        )

        self._name = bui.textwidget(
            parent=self._root_widget,
            position=(40, self.height+35),
            text=app_data.name,
            max_height=30,
            size=(0, 0),
        )

        self._close_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(self.width-40, self.height),
            size=(40, 40),
            label="X",
            texture=bui.gettexture("white"),
            color=(1, 0.2, 0.2),
            on_activate_call=self.close
        )

        bui.containerwidget(edit=self._root_widget, cancel_button=self._close_btn)

    def close(self) -> None:

        bui.containerwidget(edit=self._root_widget, transition="out_scale")
        # bui.app.mode.main_screen.taskbar._app_drawer = bos.AppDrawer(
        #     bui.app.mode.main_screen.taskbar._menu_btn  
        # )
