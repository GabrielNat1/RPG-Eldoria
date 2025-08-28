import os
import sys

def get_base_path():
    if getattr(sys, 'frozen', False):
        if hasattr(sys, '_MEIPASS'):
            return sys._MEIPASS
       
        return os.path.dirname(sys.executable)

    return os.path.dirname(os.path.abspath(__file__))

def get_asset_path(*paths):
    full_path = os.path.join(get_base_path(), *paths)
    if not os.path.exists(full_path):
        print(f"⚠️ Warning: Asset not found at {full_path}")
    return full_path

GRAPHICS_PATH = get_asset_path('graphics')
AUDIO_PATH    = get_asset_path('audio')
MAP_PATH      = get_asset_path('map')
FONT_PATH     = get_asset_path('graphics', 'font')
