# Technical Details 🛠️

## Technologies Used
- **Python 3.x** 🐍
- **Pygame**: For graphical rendering and gameplay control 🎮
- **Tiled Map Editor**: For map creation and editing 🗺️
- **SQLite** (future): For implementing the save system 💾

## System Requirements
- Operating System: Windows 10/11, Linux, or macOS
- Processor: 1.5 GHz or faster
- Memory: 250 - 500 MB RAM minimum
- Graphics: DirectX 9 compatible graphics card
- Storage: 100 MB available space
- Python 3.x or higher

## Dependencies
- pygame-2.6.1
- pillow-11.1.0

## Installation
1. Clone the repository
```bash
git clone https://github.com/GabrielNat1/RPG-Eldoria.git
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the game
```bash
python main.py
```

## Development Setup
1. Set up virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

2. Install development dependencies
```bash
pip install -r requirements-dev.txt
```

3. Install pre-commit hooks
```bash
pre-commit install
```

## Building from Source
1. Clone with submodules
```bash
git clone --recursive https://github.com/GabrielNat1/RPG-Eldoria.git
```


## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
