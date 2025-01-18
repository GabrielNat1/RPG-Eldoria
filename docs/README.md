<div align="center">
  <h1><strong>🎮RPG Eldoria🎮</strong></h1>
</div>
<br>
<img src='https://github.com/user-attachments/assets/29986fe7-23d2-4662-bc62-96244db0e1c7'>

---

## 🛠️ Technologies Used

<ul>
    <li><strong>Python</strong> 🐍</li>
    <li><strong>PyGame</strong> 🎮</li>
</ul>

<br>
<hr>

## 🖥️ How to Install and Run

To play **Eldoria** on your computer, follow the steps below:

### 1. Clone the repository

```bash  
git clone https://github.com/GabrielNat1/RPG-Eldoria.git  
```

2. Navigate to the project directory  
```bash   
cd {rpgeldoria/code}  
```

3. Install dependencies  
Make sure you have PyGame installed:  
```bash  
python -m pip install pygame  
```
4. Run the game  
Run the game with the following command:  
```bash 
python main.py  
```

---

## 🚀 How to Play

### 🏃‍♂️ Movement

- **W**, **A**, **S**, **D**, or the **Arrow Keys**: Move the character on the map.

### ⚔️ Combat

- **Spacebar**: Attack enemies.
- **Ctrl**: Special abilities (when available).
- **Q** or **E**: Switch items.

---

## 📂 Directory Structure  

The project directory structure is organized as follows:

```bash 
RPG-ELDORIA/  
├── assets/  
│   ├── audio/                   # Game audio files  
│   │   ├── attack/              # Attack sounds  
│   │   ├── death.wav            # Death sound  
│   │   ├── Fire.wav             # Fire sound  
│   │   ├── heal.wav             # Healing sound  
│   │   ├── hit.wav              # Hit sound  
│   │   ├── main_menu.wav        # Main menu music  
│   │   ├── main.wav             # Main game music  
│   │   └── sword.wav            # Sword sound  
│   ├── code/                    # Game scripts and code  
│   ├── docs/                    # Project documentation  
│   ├── graphics/                # Game visual assets  
│   │   ├── font/                # Fonts used in the game  
│   │   ├── grass/               # Grass images  
│   │   ├── icon/                # Game icons  
│   │   ├── monsters/            # Monster sprites  
│   │   ├── movies/              # Videos and cutscenes  
│   │   ├── objects/             # Interactive game objects  
│   │   ├── particles/           # Particle effects  
│   │   ├── player/              # Main character sprites  
│   │   ├── test/                # Test assets for development  
│   │   ├── tilemap/             # Game maps and tilesets  
│   │   └── weapons/             # Weapon sprites  
├── map/                         # Game map-related files  
├── requirements.txt             # Project dependencies  
```

---

## 🌍 Chunk-Based Rendering System  

The project uses a **chunk-based rendering system** to optimize performance, avoiding overloading the application and saving memory during execution.  

### 🔧 How It Works  
- The game map is divided into **small regions called chunks**, which are dynamically loaded and rendered based on the player's position.  
- Only the chunks near the player are loaded into memory, while others are unloaded or kept in a low-priority state.  

### 🛠️ Benefits  
- **Improved Performance:** Reduces system resource usage, ensuring a smoother experience.  
- **Memory Management:** Only necessary data is kept in memory, allowing the game to run on devices with limited specifications.  
- **Scalability:** Supports larger maps without negatively impacting performance.  

<br>

---

🏆 Credits  
Developers:

```bash   
GabrielNat1  

ClearCode  

Pack: NinjaAdventurePack  
```
