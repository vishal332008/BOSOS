import babase
import bauiv1 as bui

import os
import re
import shutil

PYTHON_PATH = babase.app.env.python_directory_user
APPS_PATH = PYTHON_PATH + os.sep + 'bosos_files' + os.sep + 'apps'

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
            print(f"Warning: No Textures found for {app} (app logo might be missing)")
            continue

        path = f'{os.getcwd()}{os.sep}ba_data{os.sep}textures{os.sep}apps{os.sep}'
        for tex in textures:
            if not os.path.exists(path + app):
                os.makedirs(path + app, exist_ok=True)
            shutil.copy(
                APPS_PATH + os.sep + app + os.sep + tex,
                path + app + os.sep + tex
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
