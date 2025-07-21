import re
import os
def create_directory_name(game_title: str, folder_name) -> str:
    directory = game_title.replace(' ', '_')
    if len(directory) > 75:
        directory = directory[:75]
    return  os.path.join(folder_name,re.sub(r'[<>:"/\\|?*]', '_', directory).strip())
