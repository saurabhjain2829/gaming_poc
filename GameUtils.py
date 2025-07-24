import re
import os


def create_directory_name(game_title: str, folder_name) -> str:
    game_title=remove_special_symbols(game_title)
    if len(game_title) > 75:
        game_title = game_title[:75]
        
    folder_name=remove_special_symbols(folder_name)
    
    return  os.path.join(folder_name,game_title)


def remove_special_symbols(input: str) -> str:
    sanitized = re.sub(r"[<>:\"/\\|?*,\'`&;~%=.\s!@#$^(){}\[\]+]", "_", input)
    sanitized = re.sub(r"_+", "_", sanitized)  # Collapse multiple underscores
    sanitized = sanitized.strip("_")           # Remove leading/trailing underscores
    return sanitized