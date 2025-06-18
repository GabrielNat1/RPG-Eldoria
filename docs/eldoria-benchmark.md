<h2 align="left">
   <br>
   <strong>🖥️ System Requirements</strong>
   <br>
</h2>

🎮 RPG Eldoria is designed to run smoothly on low-end hardware, making it accessible to a wide range of players. Below are the minimum and recommended requirements:

---

## ✅ Minimum Requirements

- CPU: 1.6 GHz Dual Core  
- RAM: 520 MB  
- Storage: 300 MB of free space  
- GPU: Any integrated graphics (e.g. Intel HD)  
- OS: Windows 7 / Linux / macOS  
- Dependencies: Python 3.10+, Pygame 2.x  

---

## 💡 Recommended Requirements

- CPU: 2.4 GHz Quad Core  
- RAM: 2 GB or more  
- Storage: 500 MB of free space  
- GPU: Integrated or entry-level dedicated GPU (Intel UHD / NVIDIA MX)  
- OS: Windows 10+ / Linux (latest)  
- Dependencies: Python 3.10+, **Pygame-CE with SDL2**

---

## ⚙️ Performance Comparison – Pygame vs Pygame-CE (SDL2 GPU)

| Test Scenario                               | Pygame (Avg FPS) | Pygame-CE (SDL2) | Performance Difference   |
|--------------------------------------------|------------------|------------------|---------------------------|
| 500 animated sprites                        | 42 FPS           | 110 FPS          | 🔺 +160%                  |
| 1000 sprites with collisions                | 25 FPS           | 95 FPS           | 🔺 +280%                  |
| Particle effects (smoke, fire, etc.)       | 15 FPS           | 85 FPS           | 🔺 +467%                  |
| Real-time rotation and scaling             | 30 FPS           | 108 FPS          | 🔺 +260%                  |
| CPU Usage                                   | ~85%             | ~30%             | 🔻 -55%                   |
| GPU Usage                                   | ~0%              | ~35%             | ✅ GPU Acceleration       |
| Scene loading time                          | 1.8s             | 0.6s             | 🔺 +200% faster           |

> 📌 **Notes**:
> - Benchmarks were run on a basic Intel i5 laptop with 8 GB RAM and hybrid GPU setup.
> - Even low-end systems benefit significantly from GPU offloading with Pygame-CE + SDL2.
> - This configuration is now the default as of version **2.1.0**.

---

🎯 **Conclusion**: With Pygame-CE and SDL2 now fully integrated, Eldoria delivers smoother gameplay, richer effects, and better performance across a broad range of hardware — all while maintaining its lightweight and accessible nature.
