# ba_meta require api 9

from __future__ import annotations
from typing import override 
from dataclasses import dataclass 

import os
import functools

import babase
import bauiv1 as bui

from .utils import get_app_and_class_name

PYTHON_PATH = babase.app.env.python_directory_user
APPS_PATH = PYTHON_PATH + os.sep + 'bosos_files' + os.sep + 'apps'

@dataclass
class App:
    
    name: str
    texture: str
    filename: str
    classname: str
    path: str

class HomeScreen(bui.MainWindow):

    def __init__(
        self,
        transition: str | None = None,
        origin_widget: bui.Widget | None = None,
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
        top_extra = 10 if uiscale is bui.UIScale.SMALL else 0

        super().__init__(
            root_widget=bui.containerwidget(
                size=(0,0),
                toolbar_visibility='no_menu_minimal',
                scale=(
                    2.04
                    if uiscale is bui.UIScale.SMALL
                    else 1.4 if uiscale is bui.UIScale.MEDIUM else 1.0
                ),
                stack_offset=(
                    (0, 10) if uiscale is bui.UIScale.SMALL else (0, 0)
                ),
            ),
            transition='in_scale',
            origin_widget=origin_widget,
        )

        bui.imagewidget(
            parent=self._root_widget,
            size=(self._width, self._height + top_extra),
            position=(-self._width/2, -(self._height + top_extra)/2),
            opacity=0.4,
            texture=bui.gettexture('null'),
            mask_texture=bui.gettexture('characterIconMask')
        )

        self._scroll_width = self._width - (100 + 2 * x_inset)
        self._scroll_height = self._height - (
            125.0 if uiscale is bui.UIScale.SMALL else 115.0
        )
        self._sub_width = self._scroll_width * 0.95
        self._sub_height = 0.0
        

        self._r = 'HomeScreen'

        # if uiscale is bui.UIScale.SMALL:
        #     bui.containerwidget(
        #         edit=self._root_widget, on_cancel_call=self.main_window_back
        #     )
        #     self._back_button = None
        # else:
        #     self._back_button = bui.buttonwidget(
        #         parent=self._root_widget,
        #         position=(53 + x_inset, self._height - 60),
        #         size=(140, 60),
        #         scale=0.8,
        #         autoselect=True,
        #         label=bui.Lstr(resource='backText'),
        #         button_type='back',
        #         on_activate_call=self.main_window_back,
        #     )
        #     bui.containerwidget(
        #         edit=self._root_widget, cancel_button=self._back_button
        #     )

        # if self._back_button is not None:
        #     bui.buttonwidget(
        #         edit=self._back_button,
        #         button_type='backSmall',
        #         size=(60, 60),
        #         label=bui.charstr(bui.SpecialChar.BACK),
        #     )

        self._scrollwidget = bui.scrollwidget(
            parent=self._root_widget,
            position=(50 + x_inset - self._width/2, 50 - self._height/2),
            simple_culling_v=20.0,
            highlight=False,
            size=(self._scroll_width, self._scroll_height),
            selection_loops_to_parent=True,
            border_opacity=0.1,
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

    def _load_apps(self) -> None:
    
        folderlist = os.listdir(APPS_PATH)
        for app in folderlist:
            names = get_app_and_class_name(
                path=(APPS_PATH + os.sep + app), filename=app
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
                            path=(APPS_PATH + os.sep + app)
                        )
                    )

    def _build_ui(self) -> None:
    
        app = bui.app
        assert app.classic is not None
        uiscale = app.ui_v1.uiscale
        
        _apps_per_row = 5 # number of apps in a single row.
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
                    texture=bui.gettexture("white"),
                )
                bui.buttonwidget(
                    edit=btn,
                    on_activate_call=(
                        functools.partial(
                            self._open_app,
                            window=babase.getclass(app_name, bui.MainWindow),
                            button=btn
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

    def _open_app(self, window: bui.MainWindow, button: bui.buttonwidget) -> None:
        if not self.main_window_has_control():
            print("This Window does not have Main Window Control.")
            return
        self.main_window_replace(
            window(origin_widget=button),
        )
