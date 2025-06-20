# 🧮 Performance Management

## FPS Targets and Dynamic Cap
The game targets 60 FPS by default (see `settings.py`). Performance modes can adjust visible chunks and enemy spawn distances for optimization.

## CPU/GPU Profiling
There is no built-in profiler, but you can use external tools (e.g., cProfile, Py-Spy) to analyze performance. Manual garbage collection (`gc.collect()`) is called after unloading chunks.

## Memory Cleanup
Memory is freed by unloading distant chunks and calling `gc.collect()` (see `chunk_manager.py`).

---
