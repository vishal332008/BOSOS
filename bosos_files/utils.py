
from __future__ import annotations
from dataclasses import dataclass

import os
import re
import shutil

import babase
import bauiv1 as bui

CURRENT_DIR = os.path.dirname(__file__)
APPS_PATH = (
    babase.app.env.python_directory_user + os.sep + 'bosos_files' + os.sep + 'apps'
)

@dataclass
class App:

    name: str
    texture: str
    filename: str
    classname: str
    path: str


def setup_textures() -> None:

    buiapp = bui.app
    assert buiapp.classic is not None

    apps = os.listdir(APPS_PATH)
    texture_path = f"{os.getcwd()}{os.sep}ba_data{os.sep}textures{os.sep}apps{os.sep}"
    for app in apps:
        files = os.listdir(APPS_PATH + os.sep + app)
        if bui.app.classic.platform == 'android':
            textures = [tex for tex in files if tex.endswith('.ktx')]
        else:
            textures = [tex for tex in files if tex.endswith('.dds')]

        if textures == []:
            print(f"Warning: No Textures found for {app} (app logo might be missing)")
            continue

        for tex in textures:
            # try:
            #     if not os.path.exists(texture_path + os.sep + app):
            #         os.mkdir(texture_path + os.sep + app)

            #         shutil.copy(
            #             APPS_PATH + os.sep + app + os.sep + tex,
            #             texture_path + os.sep + app + os.sep + tex
            #         )

            # except Exception as e:
            #     print(e)
            if not os.path.exists(texture_path + app):
                os.makedirs(texture_path + app, exist_ok=True)
            shutil.copy(
                APPS_PATH + os.sep + app + os.sep + tex,
                texture_path + app + os.sep + tex
            )


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
        if names is not None:
            appname = names[0].strip()
            classname = names[1].strip()
            if classname and appname:
                apps.append(
                    App(
                        name=appname,
                        texture="texture",
                        filename=app,
                        classname=classname,
                        path=(APPS_PATH + os.sep + app)
                    )
                )

    return apps
