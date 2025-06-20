# 🧩 Internal Module System

## Dynamic Loading
Some systems (e.g., chunk loading, enemy/NPC instantiation) are loaded dynamically as the player moves or interacts with the world. Python's importlib is not used for hot-reloading, but modules are structured for separation.

## Isolated and Testable Systems
Each system (inventory, player, enemy, UI, chunk manager) is implemented as a separate class/module and can be tested in isolation.

## Communication Patterns
Game systems communicate via method calls and state checks. Some state machines (FSMs) are used for event/trigger logic (see `level.py`).

---
