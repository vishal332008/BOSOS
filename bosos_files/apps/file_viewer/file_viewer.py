# pylint: disable=all

from __future__ import annotations

from typing import override

import babase
import bauiv1 as bui
import bascenev1 as bs
from bauiv1lib.qrcode import QRCodeWindow

import os
import functools

# export app FileViewer
class FileViewerScreen(bui.MainWindow):
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
                # color=(1.0, 1.0, 1.0),
            ),
            transition=transition,
            origin_widget=origin_widget,
        )

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

        self._audio_button: bui.Widget | None = None
        self._texture_button: bui.Widget | None = None

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

    def _build_ui(self) -> None:
        self._audio_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(self._width/2 - 180, self._height/2),
            size=(360, 120),
            label='Audio',
            text_scale=1.3,
        )
        self._texture_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(self._width/2 - 180, self._height/2 - 130),
            size=(360, 120),
            label='Textures',
            text_scale=1.3,
            on_activate_call=self._open_textures_window
        )

    def _open_textures_window(self):
        if not self.main_window_has_control():
            return
        self.main_window_replace(
            TexturesWindow(origin_widget=self._texture_button),
        )

class TexturesWindow(bui.MainWindow):
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

        self._r = 'TextureViewScreen'

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
        extn = '.ktx' if app.classic.platform == 'android' else '.dds'

        files = os.listdir(f'{os.getcwd()}{os.sep}ba_data{os.sep}textures')
        textures = [tex.split('.')[0] for tex in files if tex.endswith(extn)]
        num = 6 if uiscale is bui.UIScale.SMALL else 5
        rows = int(len(textures)/num) + (0 if len(textures)%num==0 else 1)
        columns = (len(textures)
                   if len(textures) < num
                   else len(textures)%num
                   if len(textures)%num!=0
                   else num
        )
        x_pos = 40 if uiscale is bui.UIScale.SMALL else 60
        y_pos = rows * 100
        index = 0

        bui.containerwidget(edit=self._subcontainer, size=(self._sub_width,(rows+1) * 100))
        for row in range(rows):
            for column in range((columns if row==(rows-1) else num)):
                texture = bui.gettexture(textures[index])
                btn = bui.buttonwidget(
                    parent=self._subcontainer,
                    position=(x_pos, y_pos),
                    size=(60, 60),
                    color=(1.0, 1.0, 1.0),
                    button_type='square',
                    label='',
                    texture=texture,
                    mesh_opaque = bui.getmesh('level_select_button_opaque'),
                    mesh_transparent = bui.getmesh('level_select_button_transparent'),
                    mask_texture = bui.gettexture('frameInset'),

                    # mask_texture=bui.gettexture('frameInset') #('mapPreviewMask'),
                )
                bui.buttonwidget(
                    edit=btn,
                    on_activate_call=functools.partial(
                        QRCodeWindow, btn, texture
                    )
                )
                bui.textwidget(
                    parent=self._subcontainer,
                    position=(x_pos + 30, y_pos - 15),
                    size=(0, 0),
                    scale=0.75,
                    draw_controller=btn,
                    maxwidth=50,
                    text=bui.Lstr(value=textures[index]),
                    h_align='center',
                    v_align='center',
                )
                index += 1
                x_pos += 90
            y_pos -= 100
            x_pos = 40 if uiscale is bui.UIScale.SMALL else 60
