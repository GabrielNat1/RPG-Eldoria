import os
import pickle
import gzip  
from random import randint
from settings import TILESIZE, CHUNKSIZE, CHUNKS_FOLDER, REGION_SIZE, LRU_CACHE_SIZE, CHUNK_DATA_VERSION  
from support import import_csv_layout, import_folder
from paths import get_asset_path
import gc  
import asyncio
import queue
import threading
import concurrent.futures
from collections import OrderedDict

_executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

def get_region_coords(chunk):
    return (chunk[0] // REGION_SIZE, chunk[1] // REGION_SIZE)

def get_region_file(region_coords):
    return os.path.join(CHUNKS_FOLDER, f"region_{region_coords[0]}_{region_coords[1]}.region")

def get_chunk_key(chunk):
    return (chunk[0], chunk[1])

def get_chunk_file(chunk):
    return os.path.join(CHUNKS_FOLDER, f"chunk_{chunk[0]}_{chunk[1]}.region")

def generate_chunk_data(chunk):
    chunk_data = {
        'version': CHUNK_DATA_VERSION,  
        'boundary': [],
        'grass': [],
        'object': [],
        'entities': []
    }
    
    layouts = {
        'boundary': import_csv_layout(get_asset_path('map', 'map_FloorBlocks.csv')),
        'grass': import_csv_layout(get_asset_path('map', 'map_Grass.csv')),
        'object': import_csv_layout(get_asset_path('map', 'map_Objects.csv')),
        'entities': import_csv_layout(get_asset_path('map', 'map_Entities.csv'))
    }
    graphics = {
        'grass': import_folder(get_asset_path('graphics', 'Grass')),
        'objects': import_folder(get_asset_path('graphics', 'Objects'))
    }
    
    for style, layout in layouts.items():
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col != '-1':
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE
                   
                    chunk_x = x // (TILESIZE * CHUNKSIZE)
                    chunk_y = y // (TILESIZE * CHUNKSIZE)
                    
                    if (chunk_x, chunk_y) == chunk:
                        if style == 'boundary':
                            chunk_data['boundary'].append({
                                'x': x,
                                'y': y,
                                'sprite_type': 'invisible'
                            })
                        elif style == 'grass':
                            random_index = randint(0, len(graphics['grass']) - 1)
                            chunk_data['grass'].append({
                                'x': x,
                                'y': y,
                                'sprite_type': 'grass',
                                'image_index': random_index
                            })
                        elif style == 'object':
                            chunk_data['object'].append({
                                'x': x,
                                'y': y,
                                'sprite_type': 'object',
                                'object_index': int(col)
                            })
                        elif style == 'entities':
                            if col == '394':
                                chunk_data.setdefault("player", {"x": x, "y": y})
                            else:
                                if col == '390': 
                                    monster_name = 'bamboo'
                                elif col == '391': 
                                    monster_name = 'spirit'
                                elif col == '392': 
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                chunk_data['entities'].append({
                                    'x': x,
                                    'y': y,
                                    'monster_name': monster_name })
    return chunk_data

def load_region(region_coords):
    region_file = get_region_file(region_coords)
    if os.path.exists(region_file) and os.path.getsize(region_file) > 0:
        try:
            with gzip.open(region_file, "rb") as f:
                region_data = pickle.load(f)
                return region_data
        except Exception:
            return {}
    else:
        return {}

def save_region(region_coords, region_data):
    os.makedirs(CHUNKS_FOLDER, exist_ok=True)
    region_file = get_region_file(region_coords)
    with gzip.open(region_file, "wb") as f:
        pickle.dump(region_data, f)

def save_chunk_data(chunk, data):
    region_coords = get_region_coords(chunk)
    region_data = load_region(region_coords)
    region_data[get_chunk_key(chunk)] = data
    save_region(region_coords, region_data)

def load_chunk_data(chunk):
    region_coords = get_region_coords(chunk)
    region_data = load_region(region_coords)
    return region_data.get(get_chunk_key(chunk), None)

def unload_chunks(chunks_dict, current_chunk, visibility_radius=2):
    chunks_to_unload = []
    for chunk_pos in list(chunks_dict.keys()):
        dx = abs(chunk_pos[0] - current_chunk[0])
        dy = abs(chunk_pos[1] - current_chunk[1])
        if dx > visibility_radius or dy > visibility_radius:
            chunks_to_unload.append(chunk_pos)
    for chunk_pos in chunks_to_unload:
        data = chunks_dict[chunk_pos]
        # Save chunk data asynchronously in a thread
        loop = asyncio.get_event_loop()
        loop.run_in_executor(_executor, save_chunk_data, chunk_pos, data)
        del chunks_dict[chunk_pos]
    gc.collect()  # Trigger garbage collection after unloading chunks

class ChunkPriorityQueue:
    def __init__(self):
        self.q = queue.PriorityQueue()
        self.set = set()
        self.lock = threading.Lock()

    def put(self, priority, chunk):
        with self.lock:
            if chunk not in self.set:
                self.q.put((priority, chunk))
                self.set.add(chunk)

    def get(self):
        with self.lock:
            if not self.q.empty():
                priority, chunk = self.q.get()
                self.set.remove(chunk)
                return priority, chunk
            return None, None

    def empty(self):
        with self.lock:
            return self.q.empty()

chunk_queue = ChunkPriorityQueue()

async def async_load_chunk(chunk, chunks_dict):
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, load_chunk_data, chunk)
    if data is None:
        data = await loop.run_in_executor(None, generate_chunk_data, chunk)
    chunks_dict[chunk] = data

def get_prefetch_chunks(player_chunk, direction, speed, radius=2, prefetch_distance=2):
    dx, dy = direction
    prefetch_chunks = set()
    
    for step in range(1, int(prefetch_distance * max(1, speed)) + 1):
        target_chunk = (player_chunk[0] + dx * step, player_chunk[1] + dy * step)
        prefetch_chunks.add((int(round(target_chunk[0])), int(round(target_chunk[1]))))

    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            prefetch_chunks.add((player_chunk[0] + x, player_chunk[1] + y))
    return list(prefetch_chunks)

async def chunk_streamer(player_chunk, chunks_dict, radius=2, max_concurrent=2, direction=(0,0), speed=0):
    prefetch_chunks = get_prefetch_chunks(player_chunk, direction, speed, radius=radius, prefetch_distance=2)
    for chunk in prefetch_chunks:
        dist = abs(chunk[0] - player_chunk[0]) + abs(chunk[1] - player_chunk[1])
     
        chunk_queue.put(dist, chunk)
    sem = asyncio.Semaphore(max_concurrent)
    async def worker():
        while not chunk_queue.empty():
            _, chunk = chunk_queue.get()
            if chunk is not None and chunk not in chunks_dict:
                async with sem:
                    await async_load_chunk(chunk, chunks_dict)
    workers = [asyncio.create_task(worker()) for _ in range(max_concurrent)]
    await asyncio.gather(*workers)

def generate_chunk_mesh(chunk_data):
    mesh = []
    
    for layer in ['boundary', 'grass', 'object']:
        tiles = chunk_data.get(layer, [])
      
        tiles_by_row = {}
        for tile in tiles:
            row = tile['y']
            tiles_by_row.setdefault(row, []).append(tile)
        for row, row_tiles in tiles_by_row.items():
            row_tiles.sort(key=lambda t: t['x'])
            start = None
            last_x = None
            for tile in row_tiles:
                if start is None:
                    start = tile
                    last_x = tile['x']
                elif tile['x'] == last_x + TILESIZE:
                    last_x = tile['x']
                else:
                    width = last_x - start['x'] + TILESIZE
                    mesh.append({
                        'x': start['x'],
                        'y': start['y'],
                        'w': width,
                        'h': TILESIZE,
                        'sprite_type': start.get('sprite_type', layer),
                        'layer': layer
                    })
                    start = tile
                    last_x = tile['x']
                    
            if start is not None:
                width = last_x - start['x'] + TILESIZE
                mesh.append({
                    'x': start['x'],
                    'y': start['y'],
                    'w': width,
                    'h': TILESIZE,
                    'sprite_type': start.get('sprite_type', layer),
                    'layer': layer
                })
                
    return mesh

def occlusion_culling(mesh, camera_rect):
    visible = []
    cam_x, cam_y, cam_w, cam_h = camera_rect
    for rect in mesh:
        rx, ry, rw, rh = rect['x'], rect['y'], rect['w'], rect['h']
        if (rx + rw > cam_x and rx < cam_x + cam_w and
            ry + rh > cam_y and ry < cam_y + cam_h):
            visible.append(rect)
    return visible

class ChunkLRUCache:
    def __init__(self, max_size=LRU_CACHE_SIZE):
        self.cache = OrderedDict()
        self.max_size = max_size

    def get(self, chunk):
        if chunk in self.cache:
            self.cache.move_to_end(chunk)
            return self.cache[chunk]
        return None

    def put(self, chunk, data):
        self.cache[chunk] = data
        self.cache.move_to_end(chunk)
        if len(self.cache) > self.max_size:
            old_chunk, old_data = self.cache.popitem(last=False)
           
            loop = asyncio.get_event_loop()
            loop.run_in_executor(_executor, save_chunk_data, old_chunk, old_data)

    def remove(self, chunk):
        if chunk in self.cache:
            del self.cache[chunk]

    def __contains__(self, chunk):
        return chunk in self.cache

    def __getitem__(self, chunk):
        return self.get(chunk)

    def __setitem__(self, chunk, data):
        self.put(chunk, data)

    def keys(self):
        return self.cache.keys()

    def items(self):
        return self.cache.items()

chunk_cache = ChunkLRUCache()

def unload_chunks(chunks_dict, current_chunk, visibility_radius=2):
    chunks_to_unload = []
    for chunk_pos in list(chunk_cache.keys()):
        dx = abs(chunk_pos[0] - current_chunk[0])
        dy = abs(chunk_pos[1] - current_chunk[1])
        if dx > visibility_radius or dy > visibility_radius:
            chunks_to_unload.append(chunk_pos)
    for chunk_pos in chunks_to_unload:
        data = chunk_cache[chunk_pos]
        loop = asyncio.get_event_loop()
        loop.run_in_executor(_executor, save_chunk_data, chunk_pos, data)
        chunk_cache.remove(chunk_pos)
    gc.collect()

def load_chunk_data_with_cache(chunk):
    data = chunk_cache.get(chunk)
    if data is not None:
    
        if isinstance(data, dict) and data.get('version') == CHUNK_DATA_VERSION:
            return data
      
        chunk_cache.remove(chunk)
        data = None
    if data is None:
        region_coords = get_region_coords(chunk)
        region_data = load_region(region_coords)
        data = region_data.get(get_chunk_key(chunk), None)
   
        if isinstance(data, dict) and data.get('version') == CHUNK_DATA_VERSION:
            chunk_cache.put(chunk, data)
            return data
        else:
            return None
        
    return data

def save_chunk_data_with_cache(chunk, data):
    chunk_cache.put(chunk, data)
   
async def async_load_chunk(chunk, chunks_dict):
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, load_chunk_data_with_cache, chunk)
    if data is None:
        data = await loop.run_in_executor(None, generate_chunk_data, chunk)
        await loop.run_in_executor(_executor, save_chunk_data_with_cache, chunk, data)
    chunk_cache.put(chunk, data)
    chunks_dict[chunk] = data