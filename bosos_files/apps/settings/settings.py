# pylint: disable=all

from __future__ import annotations

from typing import override

import math
import babase
import bauiv1 as bui
import bascenev1 as bs

# export app Settings
class SettingsScreen(bui.MainWindow):
    def __init__(
        self,
        transition: str | None = 'in_right',
        origin_widget: bui.Widget | None = None,
    ):
        # pylint: disable=too-many-statements

        app = bui.app
        assert app.classic is not None

        uiscale = bui.app.ui_v1.uiscale
        self._width = 1030.0 if uiscale is bui.UIScale.SMALL else 670.0
        x_inset = 150 if uiscale is bui.UIScale.SMALL else 0
        self._height = (
            390.0
            if uiscale is bui.UIScale.SMALL
            else 450.0 if uiscale is bui.UIScale.MEDIUM else 520.0
        )
        top_extra = 10 if uiscale is bui.UIScale.SMALL else 0

        super().__init__(
            root_widget=bui.containerwidget(
                size=(self._width, self._height + top_extra),
                toolbar_visibility='menu_minimal',
                scale=(
                    2.04
                    if uiscale is bui.UIScale.SMALL
                    else 1.4 if uiscale is bui.UIScale.MEDIUM else 1.0
                ),
                stack_offset=(
                    (0, 10) if uiscale is bui.UIScale.SMALL else (0, 0)
                ),
            ),
            transition=transition,
            origin_widget=origin_widget,
        )

        self._scroll_width = self._width - (100 + 2 * x_inset)
        self._scroll_height = self._height - (
            125.0 if uiscale is bui.UIScale.SMALL else 115.0
        )
        self._sub_width = self._scroll_width * 0.95
        self._sub_height = 870.0
        self._spacing = 32

        if uiscale is bui.UIScale.SMALL:
            bui.containerwidget(
                edit=self._root_widget, on_cancel_call=self.main_window_back
            )
            self._back_button = None
        else:
            self._back_button = bui.buttonwidget(
                parent=self._root_widget,
                position=(53 + x_inset, self._height - 60),
                size=(140, 60),
                scale=0.8,
                autoselect=True,
                label=bui.Lstr(resource='backText'),
                button_type='back',
                on_activate_call=self.main_window_back,
            )
            bui.containerwidget(
                edit=self._root_widget, cancel_button=self._back_button
            )

        if self._back_button is not None:
            bui.buttonwidget(
                edit=self._back_button,
                button_type='backSmall',
                size=(60, 60),
                label=bui.charstr(bui.SpecialChar.BACK),
            )

        self._scrollwidget = bui.scrollwidget(
            parent=self._root_widget,
            position=(50 + x_inset, 50),
            simple_culling_v=20.0,
            highlight=False,
            size=(self._scroll_width, self._scroll_height),
            selection_loops_to_parent=True,
        )
        bui.widget(edit=self._scrollwidget, right_widget=self._scrollwidget)
        self._subcontainer = bui.containerwidget(
            parent=self._scrollwidget,
            size=(self._sub_width, self._sub_height),
            background=False,
            selection_loops_to_parent=True,
        )

        # img = bui.imagewidget(
        #     #parent=self._root_widget,
        #     size=bui.get_virtual_screen_size(),
        #     texture=bui.gettexture('flagColor')
        # )
        
        # def abc():
        #     bui.imagewidget(
        #         edit=img,
        #         size=bui.get_virtual_screen_size())

        # self.blah = bui.AppTimer(1, abc, repeat=True)

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

