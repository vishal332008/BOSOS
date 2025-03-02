from __future__ import annotations

import bauiv1 as bui

class AppWindow:
    """ Common class for all apps """

    def __init__(
        self,
        *,
        name: str,
        icon: bui.Texture | None = None,
        width: float = 800.0,
        height: float = 600.0,
        transition: str | None,
        origin_widget: bui.Widget | None,
        refresh_on_screen_size_changes: bool = False,
     ) -> None:

        self._width = width
        self._height = height

        self._root_widget=bui.containerwidget(
            parent=bui.app.mode.parent,
            size=(0, 0),
            transition=transition,
        )

        window = bui.imagewidget(
            parent=self._root_widget,
            size=(self._width, self._height),
            position=(-self._width/2, -self._height/2),
            texture=bui.gettexture('white'),
        )

        window_top = bui.imagewidget(
            parent=self._root_widget,
            size=(self._width, 40),
            position=(-self._width/2, self._height/2 - 40),
            texture=bui.gettexture('white'),
            color=(0.35, 0.35, 0.35),
        )

        self._name = name
        self._icon = icon if icon else bui.gettexture("white")

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
            parent=self._root_widget,
            position=(self._width/2 - 40, self._height/2 - 37.5),
            size=(40, 35),
            label='X',
            textcolor=(0.4, 0.4, 0.4),
            button_type="square",
            texture=bui.gettexture("white"),
            color=(1, 0, 0),
            on_activate_call=self.close,
        )

        self.name_widget = bui.textwidget(
            parent=self._root_widget,
            position=(-self._width/2 + 40, self._height/2 - 10),
            size=(0, 0),
            scale=0.8,
            color=(1, 1, 1),
            text=bui.Lstr(value=self._name),
        )

        self.icon_widget = bui.imagewidget(
            parent=self._root_widget,
            position=(-self._width/2 + 5, self._height/2 - 35),
            size=(30, 30),
            texture=self._icon,
        )

        bui.containerwidget(
            edit=self._root_widget,
            cancel_button=self.close_btn,
            selected_child=self.close_btn,
        )

    def close(self) -> None:

        # no-op if our underlying widget is dead or on its way out.
        if not self._root_widget or self._root_widget.transitioning_out:
            return

        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        self.home_screen = bui.app.mode.home_screen_type(transition='in_scale')
