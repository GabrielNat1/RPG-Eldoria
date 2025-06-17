import os
import sys

def get_base_path():
    """Returns the base path for assets considering both development and compiled environments"""
    if getattr(sys, 'frozen', False):  # Quando for um .exe
        base = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
    else:
        # When running with Python, go up one level from 'code' directory to reach project root
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return base

def get_asset_path(*paths):
    """Joins the base path with additional paths to locate assets"""
    full_path = os.path.join(get_base_path(), *paths)
    if not os.path.exists(full_path):
        print(f"Warning: Asset not found at {full_path}")
    return full_path

# Common paths
GRAPHICS_PATH = get_asset_path('graphics')
AUDIO_PATH = get_asset_path('audio')
MAP_PATH = get_asset_path('map')
FONT_PATH = get_asset_path('graphics', 'font')
