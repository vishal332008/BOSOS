
from __future__ import annotations

import os
import functools
import bauiv1 as bui
import bosos_files as bos


class AppDrawer:

    def __init__(self, origin_widget: bui.Widget):

        scrn_width = bui.app.mode.main_screen.width
        scrn_height = bui.app.mode.main_screen.height

        self.width = scrn_width * 0.7
        self.height = scrn_height * 0.6

        xpos = (scrn_width-self.width)/2
        ypos = (scrn_height-self.height)/2

        self._root_widget = bui.containerwidget(
            parent=bui.app.mode.main_screen._root_widget,
            position=(xpos, ypos),
            size=(self.width, self.height),
            transition="in_scale",
            scale_origin_stack_offset=origin_widget.get_screen_space_center(),
            claim_outside_clicks=True,
            on_outside_click_call=self.close,
            background=False
        )

        # self._bg_tex = bui.imagewidget(
        #     parent=self._root_widget,
        #     size=(self.width, self.height),
        #     # texture=bui.gettexture("white"),
        #     # color=(0.3, 0.5, 0.7)
        # )

        self._scrollwidget = bui.scrollwidget(
            parent=self._root_widget,
            size=(self.width, self.height),
            simple_culling_v=20.0,
            highlight=False,
            selection_loops_to_parent=True,
            color=(1, 1, 1),
        )
        bui.widget(edit=self._scrollwidget, right_widget=self._scrollwidget)

        self._sub_width = self.width * 0.95
        self._sub_height = 0.0
        self._subcontainer = bui.containerwidget(
            parent=self._scrollwidget,
            size=(self._sub_width, self._sub_height),
            background=False,
            selection_loops_to_parent=True,
        )

        self._build_ui()

    def _build_ui(self) -> None:

        apps = bos.load_apps()
        _apps_per_row = 7 # number of apps in a single row.
        # transforming the list into tabular form(so we don't to care about row/comn and list index)
        _sliced_apps_list = [
            apps[i:i+_apps_per_row] for i in range(0, len(apps), _apps_per_row)
        ]
        _btn_xpad = 20 # x padding before btn.
        _btn_ypad = 35 # y padding before btn.
        # The app btn width and height(according to subcontainer width and x padding)
        _btns_remain_width_total = self._sub_width - _btn_xpad * (_apps_per_row+1)
        _btn_size = _btns_remain_width_total/_apps_per_row

        rows = len(_sliced_apps_list) 
        self._sub_height = rows * _btn_size + rows * _btn_ypad + 80
        bui.containerwidget(edit=self._subcontainer, size=(self._sub_width, self._sub_height))

        x_pos = _btn_xpad
        y_pos = self._sub_height - _btn_ypad - _btn_size

        for app_row in _sliced_apps_list:
            for appy in app_row:
                app_name = f"bosos_files.apps.{appy.filename}.{appy.filename}.{appy.classname}"
                btn = bui.buttonwidget(
                    parent=self._subcontainer,
                    position=(x_pos, y_pos),
                    size=(_btn_size, _btn_size),
                    color=(1.0, 1.0, 1.0),
                    button_type='square',
                    label='',
                    texture=bui.gettexture(appy.texture),
                )
                bui.buttonwidget(
                    edit=btn,
                    on_activate_call=(
                        functools.partial(
                            self._open_app,
                            window=bui.getclass(app_name, bos.AppWindow),
                            app_data=appy,
                            button=btn,
                        )
                    )
                )
                bui.textwidget(
                    parent=self._subcontainer,
                    position=(x_pos+_btn_size/2, y_pos-5),
                    size=(0, 0),
                    scale=1.0,
                    draw_controller=btn,
                    maxwidth=_btn_size*0.8,
                    max_height=15,
                    text=bui.Lstr(value=appy.name),
                    h_align="center",
                )
                x_pos += _btn_size + _btn_xpad

            x_pos = _btn_xpad # reset when enter new row.
            y_pos -= _btn_size + _btn_ypad

    def _open_app(self, window: bos.AppWindow, app_data, button: bui.Widget) -> None:
        self.close()
        window(app_data=app_data, origin_widget=button)

    def close(self) -> None:

        bui.containerwidget(edit=self._root_widget, transition="out_scale")
        bui.app.mode.main_screen.taskbar._app_drawer = None

    def _clear_widgets(self) -> None:

        for child in self._root_widget.get_children():
            child.delete()

        self._root_widget.delete()
