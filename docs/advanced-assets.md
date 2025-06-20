# 📦 Asset Management

## Texture Streaming / Lazy Loading
Assets (graphics, audio) are loaded dynamically as needed, especially for map chunks and UI elements. The chunk system loads only visible regions to optimize memory usage.

## Recommended Organization
- `graphics/characters/`
- `graphics/ui/`
- `audio/music/`
- `graphics/environment/`
- `graphics/monsters/`

## Internal Cache
Dictionaries and LRU caches are used to avoid repeated loading of the same files (see `chunk_manager.py`).

---
