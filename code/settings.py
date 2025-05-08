"""
    -------------------------------------------
    @ *settings.py* 
    
    @ *note: This file contains all game configuration variables including:* @
    - Display settings (resolution, FPS)
    - Game constants (tile size, chunk size)
    - UI configuration and colors
    - Weapon and magic system data
    - Enemy statistics and behavior
    - Performance settings
    - Audio paths and volume controls
    -------------------------------------------

"""

import os
import sys
from paths import *

# Add base path resolution at the top
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

WIDTH = 1280
HEIGTH = 720
FPS = 60

# chunks config
TILESIZE = 64 
CHUNKSIZE = 24  
VISIBLE_CHUNKS = 3 
CHUNKS_FOLDER = './cache'

#hitbox config
HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'grass': -10,
    'invisible': 0
}

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = get_asset_path('graphics', 'font', 'joystix.ttf')
UI_FONT_SIZE = 18

# General colors
BLACK_COLOR = '#000000'
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# UI Colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
STAMINA_COLOR = 'green'  
UI_BORDER_COLOR_ACTIVE = 'gold'

# Upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# Weapons
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': get_asset_path('graphics', 'weapons', 'sword', 'full.png')},
    'lance': {'cooldown': 400, 'damage': 30, 'graphic': get_asset_path('graphics', 'weapons', 'lance', 'full.png')},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic': get_asset_path('graphics', 'weapons', 'axe', 'full.png')},
    'rapier': {'cooldown': 50, 'damage': 8, 'graphic': get_asset_path('graphics', 'weapons', 'rapier', 'full.png')},
    'sai': {'cooldown': 80, 'damage': 10, 'graphic': get_asset_path('graphics', 'weapons', 'sai', 'full.png')}
}

# Magic
magic_data = {
    'flame': {'strength': 5, 'cost': 20, 'graphic': get_asset_path('graphics', 'particles', 'flame', 'fire.png')},
    'heal': {'strength': 20, 'cost': 10, 'graphic': get_asset_path('graphics', 'particles', 'heal', 'heal.png')}
}

# Enemy
monster_data = {
    'squid': {'health': 100, 'exp': 100, 'damage': 20, 'attack_type': 'slash', 
              'attack_sound': get_asset_path('audio', 'attack', 'slash.wav'), 
              'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    'raccoon': {'health': 300, 'exp': 250, 'damage': 40, 'attack_type': 'claw',
                'attack_sound': get_asset_path('audio', 'attack', 'claw.wav'),
                'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
    'spirit': {'health': 100, 'exp': 110, 'damage': 8, 'attack_type': 'thunder',
               'attack_sound': get_asset_path('audio', 'attack', 'slash.wav'), # Alterado para usar slash.wav
               'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
    'bamboo': {'health': 70, 'exp': 120, 'damage': 6, 'attack_type': 'leaf_attack',
               'attack_sound': get_asset_path('audio', 'attack', 'slash.wav'), # Alterado para usar slash.wav
               'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}
}

# Settings
settings = [
    {"name": "Fullscreen", "type": "toggle", "value": True},
    {"name": "Borderless", "type": "toggle", "value": False},
    {"name": "Resolution", "type": "choice", "choices": [(1280, 720), (1920, 1080), (800, 600), (1024, 768), (1280, 720), (1366, 768)], "value": 1},
    {"name": "Game", "type": "choice", "choices": ["optimized", "normal", "extreme performance"], "value": 1},
    {"name": "Gamma", "type": "slider", "value": 50, "min": 0, "max": 100},  # Default to 50
    {"name": "Back", "type": "action"}
]

"""
    -------------------------------------------
    Performance Mode Settings
    - enemy spawn distance: 1500
    - enemy despawn distance: 2000
    - optimized: 1 chunk visible
    - normal: 2 chunks visible
    - extreme performance: 3 chunks visible
    -------------------------------------------
"""

ENEMY_SPAWN_DISTANCE = 1500  
ENEMY_DESPAWN_DISTANCE = 2000 

PERFORMANCE_MODE = 'normal'  # Default performance mode

if PERFORMANCE_MODE == 'optimized':
    VISIBLE_CHUNKS = 1  
elif PERFORMANCE_MODE == 'normal':
    VISIBLE_CHUNKS = 2
else:
    VISIBLE_CHUNKS = 3



"""
    -------------------------------------------
    
            @ *constants audio* @
    
    -------------------------------------------
    
"""

# Audio paths and settings
AUDIO_PATHS = {
    'intro': get_asset_path('audio', 'main_intro.ogg'),
    'menu_select': get_asset_path('audio', 'menu', 'Menu1.wav'),
    'menu_back': get_asset_path('audio', 'menu', 'Menu6.wav'),
    'menu_change': get_asset_path('audio', 'menu', 'Menu9.wav'),
    'main_menu': get_asset_path('audio', 'main_menu.ogg'),
    'pause_menu': get_asset_path('audio', 'pause_menu.ogg'),
    'main_game': get_asset_path('audio', 'main.ogg'),
    'heal': get_asset_path('audio', 'heal.wav'),
    'flame': get_asset_path('audio', 'Fire.wav'),
    'death': get_asset_path('audio', 'death.wav'),
    'hit': get_asset_path('audio', 'hit.wav'),
    'fight': get_asset_path('audio', 'fight.ogg'),
    'npc_talk': get_asset_path('audio', 'npc', 'talking_sfx', 'Talking.mp3')
}

VOLUME_SETTINGS = {
    'music': 0.5,
    'menu_effects': 2.5,
    'enemy_effects': 0.6
}

# Audio settings
MASTER_VOLUME = 0.5