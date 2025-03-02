# ba_meta require api 9

from __future__ import annotations

import bauiv1 as bui

class AppWindow(bui.Window):
    """
        Common class for all apps
    """
    def __init__(
        self,
        *,
        name: str = "AppName",
        icon: bui.Texture | None = None,
        width: float = 800.0,
        height: float = 600.0,
        transition: str | None,
        origin_widget: bauiv1.Widget | None,
        cleanupcheck: bool = True,
        refresh_on_screen_size_changes: bool = False,
     ) -> None:
        
        self._width = width
        self._height = height
        
        super().__init__(
            root_widget=bui.containerwidget(
                size=(self._width, self._height),
                transition=transition,
            ), 
           cleanupcheck=cleanupcheck
        )
        
        self._name = name
        self._icon = icon if icon else bui.gettexture("white")
        
        # Windows that size tailor themselves to exact screen dimensions
        # can pass True for this. Generally this only applies to small
        # ui scale and at larger scales windows simply fit in the
        # virtual safe area.
        self.refreshes_on_screen_size_changes = refresh_on_screen_size_changes
        
        # Windows can be flagged as auxiliary when not related to the
        # main UI task at hand. UI code may choose to handle auxiliary
        # windows in special ways, such as by implicitly replacing
        # existing auxiliary windows with new ones instead of keeping
        # old ones as back targets.
        self.main_window_is_auxiliary: bool = True
        
        self.window_origin_widget = origin_widget
        
        self.close_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(self._width - 100, self._height - 50),
            size=(40, 40),
            label='',
            button_type="square",
            texture=bui.gettexture("crossOut"),
            on_activate_call=self.close,
        )
        
        self.name_widget = bui.textwidget(
            parent=self._root_widget,
            position=(120, self._height - 20),
            size=(0, 0),
            text=bui.Lstr(value=self._name),
        )
        
        self.icon_widget = bui.imagewidget(
            parent=self._root_widget,
            position=(70, self._height - 50),
            size=(40, 40),
            texture=self._icon,
        )
        
        bui.containerwidget(
            edit=self._root_widget,
            cancel_button=self.close_btn
        )
    
    def close(self) -> None:
       
        # no-op if our underlying widget is dead or on its way out.
        if not self._root_widget or self._root_widget.transitioning_out:
            return
       
        bui.containerwidget(edit=self._root_widget, transition='out_left')
        
        bui.app.ui_v1.set_main_window(
            bui.app.mode.home_screen_type(transition=None),
            suppress_warning=True,
            is_top_level=True
        )
        