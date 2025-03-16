from __future__ import annotations

import bauiv1 as bui

import bosos_files as bos

import os

class AppWindow:
    """ Common class for all apps """

    def __init__(
        self,
        *,
        app_data,
        width: float = 800.0,
        height: float = 600.0,
        transition: str | None,
        origin_widget: bui.Widget | None,
        refresh_on_screen_size_changes: bool = False,
     ) -> None:

        self._app_data = app_data
        self._width = width
        self._height = height

        self.window_widget = bui.containerwidget(
            parent=bui.app.mode.parent,
            size=(0, 0),
            transition=transition,
        )

        bui.containerwidget(
            edit=bui.app.mode.parent,
            selected_child=self.window_widget
        )

        window = bui.imagewidget(
            parent=self.window_widget,
            size=(self._width, self._height),
            position=(-self._width/2, -self._height/2),
            texture=bui.gettexture('white'),
        )

        window_top = bui.imagewidget(
            parent=self.window_widget,
            size=(self._width, 30),
            position=(-self._width/2, self._height/2 - 30),
            texture=bui.gettexture('white'),
            color=(0.35, 0.35, 0.35),
        )

        self._name = self._app_data.name
        texture_name = (
            f'apps{os.sep}{self._app_data.filename}{os.sep}logo'
            if self._app_data.filename else "white"
        )
        self._icon = bui.gettexture(texture_name)

        # Windows that size tailor themselves to exact screen dimensions
        # can pass True for this. Generally this only applies to small
        # ui scale and at larger scales windows simply fit in the
        # virtual safe area.
        self.refreshes_on_screen_size_changes = refresh_on_screen_size_changes

        # Windows can be flagged as auxiliary when not related to the
        # main UI task at hand. UI code may choose to handle auxiliary
        # windows in special ways, such as by implicitly replacing
        # existing auxiliary windows with new ones instead of keeping
        # old ones as back targets.
        self.main_window_is_auxiliary: bool = True

        self.window_origin_widget = origin_widget

        self.close_btn = bui.buttonwidget(
            parent=self.window_widget,
            position=(self._width/2 - 30, self._height/2 - 27.5),
            size=(30, 25),
            label='X',
            textcolor=(0.4, 0.4, 0.4),
            button_type="square",
            texture=bui.gettexture("white"),
            color=(1, 0, 0),
            on_activate_call=self.close,
        )

        self.name_widget = bui.textwidget(
            parent=self.window_widget,
            position=(-self._width/2 + 30, self._height/2 - 5),
            size=(0, 0),
            scale=0.7,
            color=(1, 1, 1),
            text=bui.Lstr(value=self._name),
        )

        self.icon_widget = bui.imagewidget(
            parent=self.window_widget,
            position=(-self._width/2 + 5, self._height/2 - 25),
            size=(20, 20),
            texture=self._icon,
        )

        bui.containerwidget(
            edit=self.window_widget,
            cancel_button=self.close_btn,
            selected_child=self.close_btn,
        )
        
        self._root_widget = bui.scrollwidget(
            parent=self.window_widget,
            size=(self._width, self._height - 30),
            position=(-self._width/2, -self._height/2),
            background=False,
            border_opacity=0.0,
        )
        
        bui.app.mode.add_app(app_data, self._icon)

    def close(self) -> None:

        # no-op if our underlying widget is dead or on its way out.
        if not self.window_widget or self.window_widget.transitioning_out:
            return

        bui.app.mode.close_app(self._app_data)

        bui.containerwidget(edit=self.window_widget, transition='out_scale')
        # bui.app.mode.home_screen = bos.HomeScreen(transition='in_scale')
