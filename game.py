# ba_meta require api 9

# pylint: disable=all
from __future__ import annotations

import babase
import babase._app
import bauiv1 as bui
import bascenev1 as bs

import bauiv1lib.mainmenu as mmw
import bascenev1lib.mainmenu as mma
from babase._general import getclass
from bauiv1lib.mainmenu import MainMenuWindow
from bascenev1lib.mainmenu import MainMenuActivity

import os
import re
import shutil
import functools
from typing import override

PYTHON_PATH = babase.app.env.python_directory_user
APPS_PATH = PYTHON_PATH + os.sep + 'apps'
pos = [0,0]

def setup_textures():
    buiapp = bui.app
    assert buiapp.classic is not None
    
    apps = os.listdir(APPS_PATH)
    for app in apps:
        files = os.listdir(APPS_PATH + os.sep + app)
        if buiapp.classic.platform == 'android':
            textures = [tex for tex in files if tex.endswith('.ktx')]
        else:
            textures = [tex for tex in files if tex.endswith('.dds')]

        if textures == []:
            print(f"{app} out")
            continue

        path = f'{os.getcwd()}{os.sep}ba_data{os.sep}textures{os.sep}apps{os.sep}'
        for tex in textures:
            if not os.path.exists(path + app):
                os.makedirs(path + app, exist_ok=True)
            shutil.copy(
                APPS_PATH + os.sep + app + os.sep + tex,
                path + app + os.sep + tex
            )

class NewMainMenuActivity(MainMenuActivity):
    def _make_logo(
        self,
        x: float,
        y: float,
        scale: float,
        delay: float,
        *,
        custom_texture: str | None = None,
        jitter_scale: float = 1.0,
        rotate: float = 0.0,
        vr_depth_offset: float = 0.0,
    ) -> None:
        super()._make_logo(
            x=x,
            y=y,
            scale=scale,
            delay=delay,
            custom_texture=custom_texture,
            jitter_scale=jitter_scale,
            rotate=rotate,
            vr_depth_offset=vr_depth_offset
        )
        if custom_texture is None:
            pos[0] = x
            pos[1] = y

class NewMainMenuWindow(MainMenuWindow):
    def _refresh(self) -> None:
        super()._refresh()
        helpers = [142, 32] if bs.app.lang.language == "Chinese" else [130, 18]
        bui.buttonwidget(
            parent=self._root_widget,
            position=(pos[0] + helpers[0], pos[1] + helpers[1]),
            size=(135, 135),
            label='',
            scale = 0.85 if bs.app.lang.language == "Chinese" else 0.989,
            selectable=False,
            on_activate_call=self._bomb_pressed,
            texture=bui.gettexture('empty'),
        )

    def _bomb_pressed(self):
        self.main_window_replace(
            HomeScreen(transition=None)
        )

class App():
    def __init__(self, name, texture, filename, classname, path):
        self.name = name
        self.texture = texture
        self.filename = filename
        self.classname = classname
        self.path = path

class HomeScreen(bui.MainWindow):
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
            transition='in_scale',
            origin_widget=origin_widget,
        )

        self._scroll_width = self._width - (100 + 2 * x_inset)
        self._scroll_height = self._height - (
            125.0 if uiscale is bui.UIScale.SMALL else 115.0
        )
        self._sub_width = self._scroll_width * 0.95
        self._sub_height = 870.0
        self._spacing = 32

        self._r = 'HomeScreen'

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

    def get_app_and_class_name(self, path, filename) -> list[str] | None:
        pattern1 = re.compile(r'^class (\w+)\s*\(')
        pattern2 = re.compile(r'^# export app (\w+)$') # r'^#\s+export\s+app\s+(\w+)$'
        app_and_class = [0, 1]
        with open(path + os.sep + filename + '.py', 'r', encoding='utf-8') as file:
            class_line = False
            for line in file:
                if class_line:
                    match = pattern1.match(line)
                    if match:
                        app_and_class[1] = match.group(1)
                        return app_and_class
                    else:
                        print("ERROR: NO CLASS FOUND AFTER" 
                              f"\'# export app {app_and_class[0]}\' in {filename}.py"
                        )
                        return None
                if pattern2.match(line):
                    class_line = True
                    app_and_class[0] = pattern2.match(line).group(1)
            return None

    def _load_apps(self) -> None:
        folderlist = os.listdir(APPS_PATH)
        for app in folderlist:
            names = self.get_app_and_class_name(
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

        num = 6 if uiscale is bui.UIScale.SMALL else 5
        rows = int(len(self.apps)/num) + (0 if len(self.apps)%num==0 else 1)
        columns = (len(self.apps)
                   if len(self.apps) < num
                   else len(self.apps)%num
                   if len(self.apps)%num!=0
                   else num
        )
        x_pos = 40 if uiscale is bui.UIScale.SMALL else 60
        y_pos = rows * 100
        count = 0

        bui.containerwidget(edit=self._subcontainer, size=(self._sub_width,(rows+1) * 100))
        for row in range(rows):
            for column in range((columns if row==(rows-1) else num)):
                appy = self.apps[count]
                app_name = f"apps.{appy.filename}.{appy.filename}.{appy.classname}"
                btn = bui.buttonwidget(
                    parent=self._subcontainer,
                    position=(x_pos, y_pos),
                    size=(60, 60),
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
                            window=getclass(app_name, bui.MainWindow),
                            button=btn
                        )
                    )
                )
                bui.textwidget(
                    parent=self._subcontainer,
                    position=(x_pos + 30, y_pos - 15),
                    size=(0, 0),
                    scale=0.75,
                    draw_controller=btn,
                    maxwidth=50,
                    text=bui.Lstr(value=appy.name),
                    h_align='center',
                    v_align='center',
                )
                count += 1
                x_pos += 90
            y_pos -= 100
            x_pos = 40 if uiscale is bui.UIScale.SMALL else 60

    def _open_app(self, window: bui.MainWindow, button: bui.buttonwidget) -> None:
        if not self.main_window_has_control():
            return
        self.main_window_replace(
            window(origin_widget=button),
        )

# ba_meta export plugin
class ActivateByVishuuu(babase.Plugin):
    def __init__(self) -> None:
        mma.MainMenuActivity = NewMainMenuActivity
        mmw.MainMenuWindow = NewMainMenuWindow
        setup_textures()
