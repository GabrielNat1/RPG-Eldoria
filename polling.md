# 🎮 Input System – Polling (Coming Soon)

As Eldoria evolves toward a faster and more responsive combat system, we are migrating to a **polling-based input system**.

---

## 🧠 What Is Polling?

**Polling** is a method where the game continuously checks the state of keys (or other inputs) every frame, rather than waiting for discrete input events like key presses or releases.

This approach is ideal for real-time games that require precise, continuous input.

### 🔤 Code Example

```python
enemies = [
    Enemy(100, 100),
    Enemy(400, 300),
    Enemy(600, 150)
]

for enemy in enemies:
    enemy.update(player.get_position()) 

for enemy in enemies:
    if enemy.active:
        screen.blit(enemy.image, enemy.rect)
```

---

## ⚔️ Polling Tests

| Feature/Aspect                 | Event-Driven (pygame.event.get()) | Polling (pygame.key.get_pressed())     |
|-------------------------------|-----------------------------------|----------------------------------------|
| Style                         | Reactive                          | Continuous checking                    |
| Input latency                 | Low                               | Very low                               |
| Multi-key support             | ⚠️ Manual handling required        | ✅ Native and easy                      |
| Suited for Menus / UI         | ✅ Yes                             | ⚠️ Needs extra logic                   |
| Suited for Real-Time Gameplay | ⚠️ OK, but less fluid              | ✅ Excellent for combat and movement    |
| CPU usage                     | Slightly lower                    | Slightly higher (but negligible)       |
| RAM usage                     | Slightly lower                    | Slightly higher (but negligible)       |
| Key repeat on hold            | OS-controlled delays              | Full control & faster reaction         |
| Implementation complexity     | Medium                            | ✅ Simpler for gameplay logic           |

---

## ✅ Why Polling for Eldoria?

- 🎯 **Improved responsiveness** during fast-paced actions like dodging, attacking, or casting spells.
- 🧩 **Simpler logic** for handling multiple simultaneous keys (like moving diagonally while sprinting).
- 🔁 **Consistent input detection** across all frames, without relying on OS key repeat timings.
- 🧪 Better suited for upcoming **combat-focused mechanics**.

---

## 🛠️ Current Plan

Polling will be used for:

- Movement  
- Combat actions (attack, dash, spell)  
- Charged or hold-based abilities  
- Real-time interactions with NPCs or world elements  

Event-driven input will still be used for:

- Menus (pause, inventory)  
- Mouse interactions (clicks, UI)  
- System events (quit, resize)  

---

## 🔚 Final Notes

> Polling isn't "better" in every situation — but for **real-time gameplay**, it's a massive upgrade.  
> This hybrid model (polling + events) gives Eldoria the best of both worlds: fluid controls and precise UI handling.
