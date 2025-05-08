import os
import sys

def get_base_path():
    """Returns the base path for assets considering both development and compiled environments"""
    if getattr(sys, 'frozen', False):  # Quando for um .exe
        return sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Quando rodar com Python

def get_asset_path(*paths):
    """Joins the base path with additional paths to locate assets"""
    return os.path.join(get_base_path(), *paths)

# Common paths
GRAPHICS_PATH = get_asset_path('graphics')
AUDIO_PATH = get_asset_path('audio')
MAP_PATH = get_asset_path('map')
FONT_PATH = get_asset_path('graphics', 'font')
