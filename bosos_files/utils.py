
from __future__ import annotations
from dataclasses import dataclass

import os
import re
import shutil

import bauiv1 as bui

CURRENT_DIR = os.path.dirname(__file__) # THE directory of this file e.g. ../mods/bosos_files or ../workspace_name/bosos_files 
APPS_PATH = CURRENT_DIR + os.sep + "apps" # ../bosos_files/apps
TEXTURE_DIR = os.getcwd() + os.sep + "ba_data" + os.sep + "textures" # bombsquad texture dir path
APP_DIR_NAME = "apps_textures" 
APP_TEXTURE_DIR = TEXTURE_DIR + os.sep + APP_DIR_NAME # ../ba_data/textures/APP_DIR_NAME where all apps textures stored.

@dataclass
class App:

    name: str
    texture: str
    filename: str
    classname: str
    path: str


def setup_textures() -> None:
    
    if not os.path.exists(APP_TEXTURE_DIR):
        try: 
            os.mkdir(APP_TEXTURE_DIR)
        except PermissionError:
            print("Texture setup failed: ", end="")
            print("path", f"\"{TEXTURE_DIR}\"" , "has no permission to create directory.")
            return None

    apps = os.listdir(APPS_PATH)
    for app in apps:
        dest_tex_path = APP_TEXTURE_DIR + os.sep + app
        if not os.path.exists(dest_tex_path):
            os.mkdir(dest_tex_path)
            src_tex_path = _get_app_src_tex_path(app)
            if src_tex_path:
                shutil.copy(src_tex_path, dest_tex_path)
            else:
                print("No texture found for app: ", app)


def _get_app_src_tex_path(app: str) -> str:

    assert bui.app.classic is not None

    path = APPS_PATH + os.sep + app + os.sep
    if bui.app.classic.platform == "android":
        path += "logo.ktx"   
    else:
        path += "logo.dds"

    return path if os.path.exists(path) else ""
    

def get_app_and_class_name(path, filename) -> list[str] | None:

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
                    print("ERROR: NO CLASS FOUND AFTER "
                            f"\'# export app {app_and_class[0]}\' in {filename}.py"
                    )
                    return None

            if pattern2.match(line):
                class_line = True
                app_and_class[0] = pattern2.match(line).group(1).replace('_', ' ')

        return None


def load_apps() -> list[App]:
    
    apps: list[App] = []
    
    folderlist = os.listdir(APPS_PATH)
    for app in folderlist:
        names = get_app_and_class_name(
            path=(APPS_PATH + os.sep + app), filename=app
        )

        if names is None:
            continue
        
        appname = names[0].strip()
        classname = names[1].strip()
        if classname and appname:
            texture = "white"
            if os.path.exists(APP_TEXTURE_DIR):
                tex_path = APP_TEXTURE_DIR + os.sep + app
                tex_list = os.listdir(tex_path)
                if os.path.exists(tex_path) and tex_list:
                    texture = (
                        APP_DIR_NAME + os.sep + app
                        + os.sep + "logo"
                    )
            
            apps.append(
                App(
                    name=appname,
                    texture=texture,
                    filename=app,
                    classname=classname,
                    path=(APPS_PATH + os.sep + app)
                )
            )

    return apps
