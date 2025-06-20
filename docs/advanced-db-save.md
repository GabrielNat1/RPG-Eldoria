# 🗃️ Internal Save System and Data Storage

## Save File Format
RPG Eldoria uses a region-based chunk system for world persistence. Each region is stored as a compressed `.region` file (using Python's `pickle` and `gzip`), containing chunk data such as terrain, objects, and entities.

- Save files are located in the folder defined by `CHUNKS_FOLDER` (see `settings.py`).
- Each region file is named `region_X_Y.region` where X and Y are region coordinates.
- Data is serialized with `pickle` and compressed with `gzip` for efficiency.

### Example: Saving a Chunk
```python
import pickle, gzip
with gzip.open('region_0_0.region', 'wb') as f:
    pickle.dump(region_data, f)
```

### Data Structure Example
```python
{
  'version': 1,
  'boundary': [...],
  'grass': [...],
  'object': [...],
  'entities': [...],
  'player': {'x': 100, 'y': 200}
}
```

## Save Editor
There is no official save editor. Modifying `.region` files is not recommended and may corrupt your game. Use at your own risk.

---
