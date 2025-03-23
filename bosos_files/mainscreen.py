# ba_meta require api 9

from __future__ import annotations

import bauiv1 as bui
import bosos_files as bos

from datetime import datetime
from bosos_files.appdrawer import AppDrawer


class MainScreen(bui.Window):
    """ The first screen when app mode activates. """

    def __init__(self) -> None:

        scrn_size = bui.get_virtual_screen_size()
        self.width = scrn_size[0]
        self.height = scrn_size[1]

        # The Main Widget of all widgets.
        super().__init__(
            root_widget=bui.containerwidget(
                parent=bui.get_special_widget("overlay_stack"),
                size=(self.width, self.height - 50),
                background=False
            )
        )

        self.wallpaper = bui.imagewidget(
            parent=self._root_widget,
            size=(self.width, self.height),
            texture=bui.gettexture("alwaysLandBGColor"),
        )

        self.taskbar = TaskBar(self)

    def __del__(self) -> None:
        self.taskbar._init_timer = None
        self._root_widget.delete()


class TaskBar:

    def __init__(self, mainscreen: MainScreen):

        self.width = mainscreen.width
        self.height = 50.0
        self._root_widget = bui.containerwidget(
            parent=mainscreen._root_widget,
            size=(self.width, self.height),
            background=False
        )

        self._bg_tex: bui.Widget | None = None
        self._menu_btn: bui.Widgte | None = None
        self._time_widget: bui.Widget | None = None
        self._app_drawer: AppDrawer | None = None

        self._time_update_timer: bui.AppTimer | None = None
        self._init_timer: bui.AppTimer | None = None

        self.build_ui()

    def build_ui(self) -> None:

        self._bg_tex = bui.imagewidget(
            parent=self._root_widget,
            size=(self.width, self.height-2),
            color=(0.4, 0.4, 0.4),
            texture=bui.gettexture("flagColor"),
        )

        time = datetime.now()
        self._time_widget = bui.buttonwidget(
            parent=self._root_widget,
            position=(self.width - 130, 0),
            size=(130, self.height - 5),
            label=time.strftime("%H:%M\n%d/%m - %A"),
            text_scale=0.8,
            textcolor=(2.5, 2.5, 2.5),
            button_type='square',
            texture=bui.gettexture('flagColor'),
            color=(0.4, 0.4, 0.4),
        )

        self._init_timer = bui.AppTimer(60 - time.second, self._set_time_timer)

        self._menu_btn = bui.buttonwidget(
            parent=self._root_widget,
            size=(self.height, self.height-4),
            label="",
            texture=bui.gettexture("flagColor"),
            color=(0.4, 0.4, 0.4),
            icon=bui.gettexture("logo"),
            on_activate_call=self._open_menu,
        )

    def _update_time(self) -> None:

        time = datetime.now()
        bui.buttonwidget(
            edit=self._time_widget,
            label=time.strftime("%H:%M\n%d/%m - %A")
        )

    def _set_time_timer(self) -> None:

        bui.buttonwidget(
            edit=self._time_widget,
            label=datetime.now().strftime("%H:%M\n%d/%m - %A")
        )
        self._time_update_timer = bui.AppTimer(
            60, self._update_time, repeat=True
        )

    def _open_menu(self) -> None:
        if self._app_drawer is None:
            self._app_drawer = AppDrawer(self._menu_btn)
        else:
            self._app_drawer.close()

    def __del__(self) -> None:
       self._time_update_timer = None