# ba_meta require api 9

from __future__ import annotations
from typing import TYPE_CHECKING, override

import babase
import _babase
import _baclassic

import bauiv1 as bui
import bosos_files as bos

from bacommon.app import AppExperience
from babase._appintent import AppIntentExec, AppIntentDefault


if TYPE_CHECKING:
    from babase import AppIntent


# ba_meta export babase.AppMode
class Activate(babase.AppMode):

    def __init__(self) -> None:
        
        self.main_screen: bos.MainScreen | None = None

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
        bosos_appmode.on_screen_size_change = self.update_screen
        babase.app._subsystem_registration_ended = True

        _baclassic.classic_app_mode_activate()
        # bos.setup_textures()
        
        self.main_screen = bos.MainScreen()

    @override
    def update_screen(self) -> None:
        # recreate on screen update.
        self.main_screen = bos.MainScreen()

    @override
    def on_deactivate(self) -> None:

        self.main_screen = None
        print("hmm bye")
