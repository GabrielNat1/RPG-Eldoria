import os
import sys

def get_base_path():
    """
    Returns the base path for assets.
    - If packaged (Nuitka/PyInstaller), use the executable directory.
    - Otherwise, use the project root (one level above the 'code' folder).
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    
    # For development: move one folder up from 'code'
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_asset_path(*paths):
    """
    Constructs the full path to an asset.
    Prints a warning if the asset does not exist.
    """
    full_path = os.path.join(get_base_path(), *paths)
    if not os.path.exists(full_path):
        print(f"⚠️ Warning: Asset not found at {full_path}")
    return full_path

# Asset folders
GRAPHICS_PATH = get_asset_path('graphics')
AUDIO_PATH    = get_asset_path('audio')
MAP_PATH      = get_asset_path('map')
FONT_PATH     = get_asset_path('graphics', 'font')
