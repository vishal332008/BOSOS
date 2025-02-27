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
        print("hmm hi works")
        _baclassic.classic_app_mode_activate()
        
        # Setting up all textures from apps
        setup_textures()

        # Wallpaper
        self.wallpaper = bui.imagewidget(
            size=bui.get_virtual_screen_size(),
            texture=bui.gettexture('alwaysLandBGColor') 
        )
        # 'flagColor', 'eggTex3', 'alwaysLandBGColor', 'menuBG'

        self.blah = babase.AppTimer(0.2, self.update_wallpaper, repeat=True)

        # Main Window / Desktop
        babase.app.ui_v1.set_main_window(
            HomeScreen(transition=None),
            suppress_warning=True,
            is_top_level=True
        )

    def update_wallpaper(self):
        bui.imagewidget(
            edit=self.wallpaper,
            size=bui.get_virtual_screen_size()
        )

    @override
    def on_deactivate(self) -> None:
        self.blah = None
        print("hmm bye")
