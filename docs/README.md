<h1 align="center">
   🎮 <strong>RPG Eldoria</strong> 🎮
</h1>

<img src='https://github.com/user-attachments/assets/29986fe7-23d2-4662-bc62-96244db0e1c7'>

## Introduction 🌍
**RPG Eldoria** is a 2D RPG developed in **Python** using the Pygame library. Inspired by games like **Stardew Valley** and **Dark Souls**, the game combines a **pixel art** visual style with challenging combat and exploration mechanics. Designed to ensure a smooth and accessible experience, the game implements various optimizations and unique features focused on performance and gameplay depth.

<br>

## Directory Structure 📂

The project directory is organized to separate the different parts of the game, such as audio, graphics, and code. Below is an overview of the directory structure:

```plaintext
RPG-ELDORIA/
├── audio/                     # Game audio files 🎶
├── code/                      # Game source code 💻
├── docs/                      # Project documentation 📄
├── graphics/                  # Visual assets for the game 🎨
│   ├── dialog/                # Dialogue boxes and fonts for NPCs 🗨️
│   ├── environment/           # Environment elements and map objects 🌿
│   ├── font/                  # Fonts used in the game 🅰️
│   ├── grass/                 # Grass sprites 🌾
│   ├── icon/                  # Game icons 🔑
│   ├── monsters/              # Monster and enemy sprites 👹
│   ├── npc/                   # NPC sprites and animations 🧑‍🤝‍🧑
│   ├── objects/               # Interactive objects in the map 🧳
│   ├── particles/             # Particle effects ✨
│   ├── player/                # Player character sprites 🧑‍🎮
│   ├── run_right/             # Running animation to the right ➡️
│   ├── test/                  # Test resources 🧪
│   ├── tilemap/               # Map and tilesets 🗺️
│   ├── ui/                    # User interface elements 🖥️
├── map/                       # Game map files 🌍
├── weapons/                   # Weapon sprites 🏹
├── warn.txt                   # Game warnings and logs ⚠️
├── .gitignore                 # Git ignored files 🚫
├── requirements.txt           # List of project dependencies 📑
```

<br>

---

## Key Features ⚙️

### 1. Optimized Chunk System 🌲
- **Map based on chunks**:
  - The world is divided into small areas called **chunks**.
  - Only chunks near the player are loaded, optimizing performance and reducing memory usage.
  - Explored chunks are temporarily stored in a folder called `chunk`.
    - After the player exits the game, the folder is automatically cleared.
    - In the future, the **save progress** feature will be added to preserve explored areas.
  - **Dynamic loading**: Chunks are loaded automatically as the player approaches new areas. <br>

- **Benefits**:
  - Reduces resource usage on lower-spec machines.
  - Decreases overall game loading times.
  - Ensures previously visited areas don't need to be reloaded during the same session.

---

### 2. NPC and Quest System 🧑‍🤝‍🧑
- **NPC Interactions**:
  - NPCs are key elements of the game, offering dynamic dialogues with a typing effect for immersion.
  - NPC responses vary depending on the player's progress and accumulated points. <br>

- **Quest System**:
  - NPCs assign **missions** (quests) to the player.
  - Each completed mission grants an **exclusive reward**, such as:
    - New weapons ⚔️.
    - Rare items 🎁. <br>

---

<br>

### 3. Full Menu System 🖥️
The main menu offers several customizable options: <br>
- **Performance modes**: 
  - **Optimized**: Balances graphics quality and performance.
  - **Normal**: Standard game configuration.
  - **Extreme Performance**: For low-performance devices, reducing visual effects for smoother gameplay.<br>
    
- **Screen settings**:
  - Full screen.
  - Borderless window.
  - Manual resolution adjustment.<br>
    
- **Sound effects**: 
  - Unique sounds for buttons and interactions in the menu, enhancing the player's experience.<br>
    
- **Cinematic Intro**: 
  - Before the game starts, an animated intro tells the backstory of Eldoria, introducing the player to the universe and its challenges.<br>

---

### 4. Particle System ✨
- **Visual Effects**:
  - Animated particles for attacks, explosions, spells, and weather effects (such as rain and dust).
  - Optimized effects for different performance modes.

---

### 5. Map Creation and Management 🗺️
- **Tiled Engine**:
  - The game map is designed using the **Tiled Map Editor**, allowing for:
    - Easy tile editing.
    - Addition of custom layers (such as objects, terrain, and collisions).<br>
  - The chunk system ensures that areas are dynamically loaded:
    - Chunks near the player are rendered.
    - Previously visited areas do not need to be reloaded.

---

### 6. Combat and Gameplay ⚔️
- **Dark Souls-inspired style**:
  - Challenging battles against enemies and bosses (boss fights).
  - Requires strategy and quick reflexes.<br>
- **Inventory System**:
  - Manage items collected throughout the game, such as weapons, potions, and other resources.
  - The inventory allows for equipping weapons and checking quest items. <br>

---

## Technologies Used 🛠️
- **Python 3.x** 🐍
- **Pygame**: For graphical rendering and gameplay control 🎮.
- **Tiled Map Editor**: For map creation and editing 🗺️.
- **SQLite** (future): For implementing the save system 💾. <br>

---

<br>

## File Overview 📂

### Code.py 📂
This file is the entry point to the game, containing the main function to initialize and run the game. It also applies the game settings and controls the flow of execution.
```bash
code.py/
├── debug.py    # Handles debugging features and logs for the game.
├── enemy.py    # Contains the logic for enemy behaviors and AI.
├── entity.py   # Base class for all entities in the game, including NPCs and players.
├── level.py    # Manages the game levels and interactions between entities.
├── magic.py    # Handles magical abilities, effects, and spells.
├── main.py     # The main script to initialize and run the game.
├── npc.py      # Manages NPCs, their dialogue, and quests.
├── particles.py# Handles the creation and behavior of particle effects.
├── player.py   # Defines the player character, their attributes, and actions.
├── settings.py # Configuration file for game settings (resolution, performance modes, etc.).
├── support.py  # Provides utility functions to support other modules.
├── tile.py     # Manages tiles and map rendering.
├── ui.py       # Handles the user interface, including buttons and menus.
└── upgrade.py  # Handles upgrading systems for player attributes.
```

### Explanation:

The `code.py/` folder contains all the essential files for the gameplay mechanics, game flow, and overall functionality. Each file is responsible for specific systems or features that are integral to how the game operates.

- **`debug.py` 🐞**: Manages debugging tools and logs, which help developers track errors and ensure smooth game development.
- **`enemy.py` 👾**: Contains the logic for enemy behaviors and AI. It determines how enemies react to the player and interact within the game world.
- **`entity.py` ⚙️**: A base class for all entities in the game, such as NPCs and players. This file holds the core properties and methods shared by all entities.
- **`level.py` 🏞️**: Manages game levels, including the loading and handling of different areas, and the interactions between entities within these levels.
- **`magic.py` ✨**: Defines magical abilities, spells, and effects that can be used by the player or enemies to alter the game world and combat dynamics.
- **`main.py` 🎮**: The entry point to the game. This script initializes and runs the game, managing the game loop and orchestrating the various game systems.
- **`npc.py` 🗣️**: Manages NPCs, including their behavior, dialogue, and any quests they may give the player, shaping the story and world-building.
- **`particles.py` 🌟**: Handles particle effects like explosions, sparks, and other visual effects that enhance the game's aesthetic and gameplay.
- **`player.py` 🏃**: Defines the player's character, including attributes, abilities, and actions, determining how the player interacts with the game world.
- **`settings.py` ⚙️**: Contains game configuration options such as resolution, performance modes, and other settings that control how the game runs on different systems.
- **`support.py` 🛠️**: Provides utility functions that assist other modules by performing repetitive or auxiliary tasks.
- **`tile.py` 🗺️**: Manages the game’s map tiles, including rendering and interactions with the world’s terrain and obstacles.
- **`ui.py` 💻**: Controls the user interface, including menus, buttons, and other interactive elements that the player uses to navigate the game.
- **`upgrade.py` ⬆️**: Handles the system for upgrading the player's attributes, such as health, damage, or abilities, allowing for character progression.

These files work together to provide all the necessary mechanics, UI, AI, and configurations that power the game. Each module plays a vital role in making the game function seamlessly.

---

### Graphics.py 📂
This directory contains all the visual assets for the game. These resources are dynamically loaded based on gameplay and performance requirements.
```bash
# graphics.py/
├── # monsters/ # Contains all the visual assets for monsters.
│   ├── # bamboo/ # Assets related to the bamboo monster.
│   ├── # raccoon/ # Assets related to the raccoon monster.
│   ├── # spirit/ # Assets related to the spirit monster.
│   └── # squid/ # Assets related to the squid monster.
├── # npc/ # Contains visual assets for Non-Playable Characters (NPCs).
│   ├── # forger/ # Assets related to the forger NPC.
│   └── # oldman/ # Assets related to the oldman NPC.
├── # particles/ # Contains visual assets for various particle effects.
│   ├── # aura/ # Assets for aura particle effects.
│   ├── # bamboo/ # Bamboo particle effects.
│   ├── # claw/ # Claw-related particle effects.
│   ├── # flame/ # Flame-related particle effects.
│   ├── # heal/ # Heal-related particle effects.
│   ├── # leaf_attack/ # Leaf attack particle effects.
│   ├── # leaf1/ # Various leaf-related particle effects.
│   ├── # leaf2/ # More leaf-related particle effects.
│   ├── # leaf3/ # More leaf-related particle effects.
│   ├── # leaf4/ # More leaf-related particle effects.
│   ├── # leaf5/ # More leaf-related particle effects.
│   ├── # leaf6/ # More leaf-related particle effects.
│   ├── # nova/ # Nova particle effects.
│   ├── # raccoon/ # Raccoon-related particle effects.
│   ├── # slash/ # Slash-related particle effects.
│   ├── # smoke/ # Smoke-related particle effects.
│   ├── # smoke_orange/ # Orange smoke particle effects.
│   ├── # smoke2/ # Another variation of smoke particle effects.
│   ├── # sparkle/ # Sparkle-related particle effects.
│   └── # thunder/ # Thunder-related particle effects.
├── # player/ # Contains visual assets for the player character's movements and actions.
│   ├── # down/ # Downward-facing animations for the player.
│   ├── # down_attack/ # Downward-facing attack animations.
│   ├── # down_idle/ # Downward-facing idle animations.
│   ├── # left/ # Left-facing animations for the player.
│   ├── # left_attack/ # Left-facing attack animations.
│   ├── # left_idle/ # Left-facing idle animations.
│   ├── # right/ # Right-facing animations for the player.
│   ├── # right_attack/ # Right-facing attack animations.
│   ├── # right_idle/ # Right-facing idle animations.
│   ├── # up/ # Upward-facing animations for the player.
│   ├── # up_attack/ # Upward-facing attack animations.
│   └── # up_idle/ # Upward-facing idle animations.
├── # ui/ # Contains visual assets related to the user interface (UI).
│   ├── # dialog/ # Dialog-related assets for the UI.
│   └── # emote/ # Emote-related assets for the UI.
└── # weapons/ # Contains visual assets for different weapons in the game.
    ├── # axe/ # Axe weapon-related assets.
    ├── # hammer/ # Hammer weapon-related assets.
    ├── # lance/ # Lance weapon-related assets.
    ├── # rapier/ # Rapier weapon-related assets.
    ├── # sai/ # Sai weapon-related assets.
    └── # sword/ # Sword weapon-related assets.

```
### Explanation:
The `graphics.py/` folder is where all the visual assets of the game are stored, categorized by different elements of the game. These include monsters, NPCs, particles, player animations, UI elements, and weapons. Each subfolder contains different sets of images, sprites, or animations that represent various in-game objects or effects.

- **`monsters/` 🧟**: This folder includes all the visual assets for the monsters you encounter in the game. Each subfolder (like `bamboo`, `raccoon`, etc.) contains the specific sprites and animations for each monster type.
- **`npc/` 👤**: This folder contains assets for NPCs, such as `forger` and `oldman`, which play important roles in the story or provide services to the player.
- **`particles/` ✨**: Here you'll find assets related to particle effects like healing, smoke, flame, and various attack effects used to enhance the visual experience during combat and interaction.
- **`player/` 🏃**: Contains the different player animations and sprites for movement and actions (e.g., walking, attacking, idling) in various directions (up, down, left, right).
- **`ui/` 💻**: Holds assets for the user interface, including dialogs and emotes that enhance interactions between the player and the game world.
- **`weapons/` ⚔️**: Stores the assets for weapon animations such as `axe`, `hammer`, `sword`, and more, which are used during combat.

Each of these folders serves a distinct purpose in the game, providing the necessary visuals for gameplay, interactions, and storytelling.


---


audio/ Directory 🎵
This directory contains all the audio files for the game, categorized into attack sounds and menu sounds.
```bash
audio/
├── attack/ # sounds for attacking
├── npc/ # sounds for npc speak
└── menu/ # sounds sonore for menu
```

### Explanation:
- **`attack/`**: Contains sound files related to the player's and enemies' actions during combat. This includes sounds for various attack types, like sword swings, magic casting, and monster roars. These sounds enhance the combat experience by providing audio feedback to the player.

- **`menu/`**: This section contains sound effects for the user interface. These sounds are played when interacting with the menu, such as button clicks, selections, and background music. These auditory cues contribute to the overall user experience and atmosphere of the game.

- **`npc/`**: This section contains sound effects for the npc dialog. These sounds are played when interacting with the npc.

---

### `settings.py` 🛠️

This file contains important configuration settings for the game, including screen resolution, FPS (frames per second), and chunk settings. These settings help optimize the game's performance and user experience.

```json
{
  settings.py: {
    "WIDTH": 1280,
    "HEIGHT": 720,
    "FPS": 60,
    "TILESIZE": 64,
    "CHUNKSIZE": 32,
    "VISIBLE_CHUNKS": 3,
    "CHUNKS_FOLDER": "../chunks"
  }
}
```

### Explanation:

- **`WIDTH`**: Defines the width of the game window in pixels. Set to `1280`, which is a standard width for a smooth gaming experience. 🌐
- **`HEIGHT`**: Defines the height of the game window in pixels. Set to `720`, giving the game a 16:9 aspect ratio. 📐
- **`FPS`**: Specifies the number of frames per second the game should run at. Set to `60` for a smooth visual experience. 🎮
- **`TILESIZE`**: Defines the size of each tile in the game world. Set to `64` pixels, which provides a good balance between detail and performance. 🔲
- **`CHUNKSIZE`**: The size of each chunk of the game world that is loaded into memory. Set to `32`, this determines how much of the world is actively loaded at once. 🌍
- **`VISIBLE_CHUNKS`**: The number of chunks that are visible at any given time. Set to `3` to control how many chunks are rendered around the player. 👀
- **`CHUNKS_FOLDER`**: This defines the folder where the chunks are stored. The value `"../chunks"` points to a directory one level up from the game directory. 📂

---

### Chunks and Memory Management 💾

The game uses **chunks** to manage the game world and optimize memory usage. As the player moves through the world, chunks that have been explored are stored in memory to prevent reloading them from scratch each time the player returns to an area. This system reduces loading times and prevents lag, allowing the game to run smoothly. 🚀

- **Persistent Chunks**: As the player progresses, chunks that have been explored and passed through are saved temporarily. These chunks are not reloaded when the player revisits areas they've already explored, which saves memory and ensures a smooth experience when traveling between locations. 🛣️
- **Deletion on Exit**: Once the player exits the game, the stored chunks are deleted. This prevents unnecessary storage usage, as only the active game data is retained during gameplay. 🗑️

By managing chunks this way, the game ensures it only loads necessary data into memory, reducing the risk of performance issues or lag. ⚡


---

### Game Settings Logic ⚙️

The `apply_game_settings` function in `main.py` is responsible for adjusting the game's settings based on the selected performance mode. There are three modes to choose from: **optimized**, **normal**, and **extreme performance**. Each mode changes certain game parameters to ensure the best performance depending on the player's system. ⚡🎮

```json
{
  main.py: {
    "apply_game_settings": {
      "game_mode": "This function adjusts the game settings based on the selected mode: optimized, normal, or extreme performance.",
      "optimized_mode": {
        "TILESIZE": 32,
        "CHUNKSIZE": 16,
        "VISIBLE_CHUNKS": 1,
        "wind_effect_interval": 30000,
        "wind_effect_duration": 5000
      },
      "normal_mode": {
        "TILESIZE": 64,
        "CHUNKSIZE": 32,
        "VISIBLE_CHUNKS": 3,
        "wind_effect_interval": 10000,
        "wind_effect_duration": 5000
      },
      "extreme_mode": {
        "TILESIZE": 128,
        "CHUNKSIZE": 64,
        "VISIBLE_CHUNKS": 6,
        "wind_effect_interval": 10000,
        "wind_effect_duration": 5000
      }
    }
  }
}
```
### Explanation:

- **Tiles Regeneration**: 
  - In **Optimized Mode** 🏞️, the tile size (`TILESIZE`) is smaller, and fewer chunks are loaded, which results in fewer resources being used by the game, helping it run smoothly on lower-performance systems. This reduces the visual detail of the environment, but the player still experiences a playable and optimized version of the game.
  - In **Normal Mode** 🎮, the tile size and the number of visible chunks are set to medium values. This strikes a balance between performance and visual quality, allowing the game to run well while providing a good level of detail.
  - In **Extreme Mode** ⚡, larger tiles and more visible chunks are rendered, making the game look more detailed but demanding more resources from the system.

- **Wind Effects** 🌬️:
  - The wind effects, such as their interval (`wind_effect_interval`) and duration (`wind_effect_duration`), are also modified depending on the performance mode.
    - In **Optimized Mode** 🛠️, the wind effects appear less frequently and last for a shorter duration to reduce the strain on the system.
    - In **Normal Mode** 🌿, the wind effects occur more regularly and last a bit longer, balancing performance and realism.
    - In **Extreme Mode** 🌪️, wind effects are more frequent and longer, adding to the immersive experience with enhanced visual effects.

By adjusting these settings based on the player's choice, the game optimizes its performance, ensuring it can run efficiently on various systems while providing a suitable visual experience for each mode. 🌬️🖥️🎮


This ensures that the game runs efficiently on various systems while providing an enjoyable experience.

<br><br>

## Credits 💡
Developed by
```bash
  - GabrielNat1
  - ClearCode
```

<br>

Pack Tile used:
```
  - NinjaAdventurePack
```

---
