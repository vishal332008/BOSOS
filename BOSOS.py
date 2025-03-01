# ba_meta require api 9

# pylint: disable=all
from __future__ import annotations

import babase
import _babase
import _baclassic
import bauiv1 as bui

from bosos_files.home import HomeScreen
from bosos_files.utils import setup_textures

from bacommon.app import AppExperience
from babase._appintent import AppIntentExec, AppIntentDefault

import datetime
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from babase import AppIntent


# ba_meta export babase.AppMode
class Activate(babase.AppMode):
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
    
        # Setting up all textures from apps
        setup_textures()

        # Wallpaper
        parent = bui.containerwidget(size=(0, 0), toolbar_visibility='no_menu_minimal')
        size=bui.get_virtual_screen_size()
        time = datetime.datetime.now()

        self.wallpaper = bui.imagewidget(
            parent=parent,
            size=(size[0], size[1] - 40),
            position=(-size[0]/2, -size[1]/2 + 40),
            texture=bui.gettexture('alwaysLandBGColor') 
        )
        # 'flagColor', 'eggTex3', 'alwaysLandBGColor', 'menuBG'

        self.taskbar = bui.imagewidget(
            parent=parent,
            size=(size[0], 40),
            position=(-size[0]/2, -size[1]/2),
            texture=bui.gettexture('flagColor'),
            color=(0.4, 0.4, 0.4),
        )

        self.time = bui.textwidget(
            parent=parent,
            size=(60, 40),
            text=time.strftime("%H:%M\n%d/%m - %A"),
            position=(size[0]/2 - 100, -size[1]/2),
            # maxwidth=150,
            scale=0.5,
            h_align="center",
            v_align="center",
            color=(2.5, 2.5, 2.5),
            on_activate_call=lambda: print("date works")
        )

        def update_time():
            bui.textwidget(
                edit=self.time,
                text=datetime.datetime.now().strftime("%H:%M\n%d/%m - %A")
            )

        def set_timer():
            update_time()
            self.update_time_timer = babase.AppTimer(60, update_time, repeat=True)

        babase.apptimer(60 - time.second, set_timer)

        # Main Window / Desktop
        babase.app.ui_v1.set_main_window(
            HomeScreen(transition=None),
            suppress_warning=True,
            is_top_level=True
        )

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
            bui.textwidget(
                edit=self.time,
                size=(60, 40),
                position=(size[0]/2 - 100, -size[1]/2),
            )
        except: pass

    @override
    def on_deactivate(self) -> None:
        self.update_time_timer = None
        print("hmm bye")
