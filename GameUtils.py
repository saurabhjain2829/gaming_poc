
def create_directory_name(game_title: str) -> str:
    directory = game_title.replace(' ', '_')
    if len(directory) > 75:
        directory = directory[:75]
    return directory