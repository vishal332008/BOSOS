# ba_meta require api 9

from __future__ import annotations
from dataclasses import dataclass

import os
import functools

import babase
import bauiv1 as bui
import bosos_files as bos

@dataclass
class App:

    name: str
    texture: str
    filename: str
    classname: str
    path: str

class HomeScreen:

    def __init__(
        self,
        transition: str = 'in_scale',
    ):
        # pylint: disable=too-many-statements
        app = bui.app
        assert app.classic is not None

        uiscale = bui.app.ui_v1.uiscale
        self._width = 1030.0 if uiscale is bui.UIScale.SMALL else 750.0
        x_inset = 150 if uiscale is bui.UIScale.SMALL else 0
        self._height = (
            390.0
            if uiscale is bui.UIScale.SMALL
            else 450.0 if uiscale is bui.UIScale.MEDIUM else 570.0
        )

        self._scroll_width = self._width - (100 + 2 * x_inset)
        self._scroll_height = self._height - (
            125.0 if uiscale is bui.UIScale.SMALL else 115.0
        )
        self._sub_width = self._scroll_width * 0.95
        self._sub_height = 0.0

        self._r = 'HomeScreen'

        self._root_widget = bui.containerwidget(
            parent=bui.app.mode.parent,
            size=(0, 0),
            toolbar_visibility='no_menu_minimal',
            transition=transition,
        )

        bui.containerwidget(
            edit=bui.app.mode.parent,
            selected_child=self._root_widget
        )

        self._scrollwidget = bui.scrollwidget(
            parent=self._root_widget,
            position=(50 + x_inset - self._width/2, 50 - self._height/2),
            simple_culling_v=20.0,
            highlight=False,
            size=(self._scroll_width, self._scroll_height),
            selection_loops_to_parent=True,
            color=(1,1,1),
        )
        bui.widget(edit=self._scrollwidget, right_widget=self._scrollwidget)
        self._subcontainer = bui.containerwidget(
            parent=self._scrollwidget,
            size=(self._sub_width, self._sub_height),
            background=False,
            selection_loops_to_parent=True,
        )

        self.apps: list[App] = []
        self._load_apps()
        self._build_ui()

    def _load_apps(self) -> None:

        folderlist = os.listdir(bos.APPS_PATH)
        for app in folderlist:
            names = get_app_and_class_name(
                path=(bos.APPS_PATH + os.sep + app), filename=app
            )
            if names is not None:
                appname = names[0].strip()
                classname = names[1].strip()
                if classname and appname:
                    self.apps.append(
                        App(
                            name=appname,
                            texture="texture",
                            filename=app,
                            classname=classname,
                            path=(bos.APPS_PATH + os.sep + app)
                        )
                    )

    def _build_ui(self) -> None:

        app = bui.app
        assert app.classic is not None
        uiscale = app.ui_v1.uiscale

        _apps_per_row = 7 # number of apps in a single row.
        # transforming the list in tabular form(so we don't to care about row/comn and list index)
        _sliced_apps_list = [
            self.apps[i:i+_apps_per_row] for i in range(0, len(self.apps), _apps_per_row)
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
                    texture=bui.gettexture(f'apps{os.sep}{appy.filename}{os.sep}logo'),
                )
                bui.buttonwidget(
                    edit=btn,
                    on_activate_call=(
                        functools.partial(
                            self._open_app,
                            window=babase.getclass(app_name, bos.AppWindow),
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

    def _open_app(self, window: bos.AppWindow, app_data: App, button: bui.Widget) -> None:
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.app.mode.home_screen = None
        window(app_data, origin_widget=button)
