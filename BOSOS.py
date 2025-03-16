# ba_meta require api 9

# pylint: disable=all
from __future__ import annotations

import babase
import _babase
import _baclassic
import bauiv1 as bui

import bosos_files as bos

from bacommon.app import AppExperience
from babase._appintent import AppIntentExec, AppIntentDefault

import datetime
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from babase import AppIntent


# ba_meta export babase.AppMode
class Activate(babase.AppMode):

    def __init__(self) -> None:
        
        self.home_screen: bos.HomeScreen | None = None
        self.parent: bui.Widget | None = None
        self.desktop: bui.Widget | None = None
        self.open_apps = {}

    @override
    @classmethod
    def get_app_experience(cls) -> AppExperience:
        return AppExperience.EMPTY

    @override
    @classmethod
    def _supports_intent(cls, intent: AppIntent) -> bool:
        # We support default and exec intents currently.
        return isinstance(intent, AppIntentExec | AppIntentDefault)

    @override
    @classmethod
    def _can_handle_intent(cls, intent: babase.AppIntent) -> bool:
        # We support default and exec intents currently.
        return isinstance(
            intent, babase.AppIntentExec | babase.AppIntentDefault
        )

    @override
    def handle_intent(self, intent: AppIntent) -> None:
        if isinstance(intent, AppIntentExec):
            _babase.empty_app_mode_handle_app_intent_exec(intent.code)
            return
        assert isinstance(intent, AppIntentDefault)
        _babase.empty_app_mode_handle_app_intent_default()

    @override
    def on_activate(self) -> None:
        babase.app._subsystem_registration_ended = False
        bosos_appmode = babase.AppSubsystem()
        bosos_appmode.on_screen_size_change = self.update_desktop
        babase.app._subsystem_registration_ended = True

        _baclassic.classic_app_mode_activate()
        bos.setup_textures()

        self.parent = bui.containerwidget(
            size=(0, 0),
            toolbar_visibility='no_menu_minimal'
        )
        size = bui.get_virtual_screen_size()
        time = datetime.datetime.now()

        self.wallpaper = bui.imagewidget(
            parent=self.parent,
            size=(size[0], size[1] - 40),
            position=(-size[0]/2, -size[1]/2 + 40),
            texture=bui.gettexture('alwaysLandBGColor') 
        )
        # 'flagColor', 'eggTex3', 'alwaysLandBGColor', 'menuBG'

        self.taskbar = bui.imagewidget(
            parent=self.parent,
            size=(size[0], 40),
            position=(-size[0]/2, -size[1]/2),
            texture=bui.gettexture('flagColor'),
            color=(0.4, 0.4, 0.4),
        )

        self.time = bui.buttonwidget(
            parent=self.parent,
            size=(100, 37.5),
            label=time.strftime("%H:%M\n%d/%m - %A"),
            position=(size[0]/2 - 100, -size[1]/2),
            button_type='square',
            text_scale=2,
            textcolor=(2.5, 2.5, 2.5),
            texture=bui.gettexture('flagColor'),
            color=(0.4, 0.4, 0.4),
            on_activate_call=lambda: print("date works"),
        )

        def update_time():
            bui.buttonwidget(
                edit=self.time,
                label=datetime.datetime.now().strftime("%H:%M\n%d/%m - %A"),
            )

        def set_timer():
            update_time()
            self.update_time_timer = babase.AppTimer(60, update_time, repeat=True)

        babase.apptimer(60 - time.second, set_timer)

        self.home_button = bui.buttonwidget(
            parent=self.parent,
            size=(40, 37.5),
            label='',
            position=(-size[0]/2, -size[1]/2),
            button_type='square',
            texture=bui.gettexture('flagColor'),
            color=(0.4, 0.4, 0.4),
            on_activate_call=self.home_pressed,
        )

        self.home_btn_img = bui.imagewidget(
            parent=self.parent,
            position=(-size[0]/2 + 5, -size[1]/2 + 5),
            size=(30, 30),
            texture=bui.gettexture('logo'),
            draw_controller=self.home_button,
        )
        
        self.desktop = bui.containerwidget(
            parent=self.parent,
            size=(0, 0), # (size[0], size[1] - 40),
            position=(-size[0]/2, -size[1]/2 + 40),
            
        )

    def home_pressed(self):
        if self.home_screen is None:
            self.home_screen = bos.HomeScreen()
        else:
            bui.containerwidget(edit=self.home_screen._root_widget, transition='out_scale')
            self.home_screen = None

    def add_app(self, app_data, tex: bui.Texture):
        size = bui.get_virtual_screen_size()
        self.open_apps.update({
            app_data.name: bui.buttonwidget(
                parent=self.parent,
                size=(30, 30),
                position=(-size[0]/2 + 100 + (len(self.open_apps) * 50), -size[1]/2 + 5),
                texture=tex,
                label='',
                color=(1, 1, 1),
                on_activate_call=lambda: print("apps")
            )
        })

    def refresh_open_apps(self):
        size = bui.get_virtual_screen_size()
        for num, button in enumerate(self.open_apps.values()):
            bui.buttonwidget(
                edit=button,
                position=(-size[0]/2 + 100 + ((num) * 50), -size[1]/2 + 5),
            )

    def close_app(self, app_data):
        self.open_apps[app_data.name].delete()
        del self.open_apps[app_data.name]
        self.refresh_open_apps()

    def update_desktop(self):
        try:
            size=bui.get_virtual_screen_size()
            bui.imagewidget(
                edit=self.wallpaper,
                size=(size[0], size[1] - 40),
                position=(-size[0]/2, -size[1]/2 + 40),
            )
            bui.imagewidget(
                edit=self.taskbar,
                size=(size[0], 40),
                position=(-size[0]/2, -size[1]/2),
            )
            bui.buttonwidget(
                edit=self.time,
                position=(size[0]/2 - 100, -size[1]/2),
            )
            bui.buttonwidget(
                edit=self.home_button,
                position=(-size[0]/2, -size[1]/2),
            )
            bui.imagewidget(
                edit=self.home_btn_img,
                position=(-size[0]/2 + 5, -size[1]/2 + 5),
            )
        except: pass

    @override
    def on_deactivate(self) -> None:
        self.update_time_timer = None
        print("hmm bye")
