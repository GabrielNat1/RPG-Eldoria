import os
import pickle
from random import randint
from settings import TILESIZE, CHUNKSIZE, CHUNKS_FOLDER
from support import import_csv_layout, import_folder
import gc  

def get_chunk_file(chunk):
    return os.path.join(CHUNKS_FOLDER, f"chunk_{chunk[0]}_{chunk[1]}.dat")

def generate_chunk_data(chunk):
    chunk_data = {
        'boundary': [],
        'grass': [],
        'object': [],
        'entities': []
    }
    
    layouts = {
        'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
        'grass': import_csv_layout('../map/map_Grass.csv'),
        'object': import_csv_layout('../map/map_Objects.csv'),
        'entities': import_csv_layout('../map/map_Entities.csv')
    }
    graphics = {
        'grass': import_folder('../graphics/Grass'),
        'objects': import_folder('../graphics/Objects')
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

def save_chunk_data(chunk, data):
    os.makedirs(CHUNKS_FOLDER, exist_ok=True)
    chunk_file = get_chunk_file(chunk)
    
    with open(chunk_file, "wb") as f:
        pickle.dump(data, f)

def load_chunk_data(chunk):
    chunk_file = get_chunk_file(chunk)
    if os.path.exists(chunk_file) and os.path.getsize(chunk_file) > 0:
        with open(chunk_file, "rb") as f:
            try:
                data = pickle.load(f)
                return data
            except Exception as e:
                return None
    else:
        return None

def unload_chunks(chunks_dict, current_chunk, visibility_radius=2):
    chunks_to_unload = []
    for chunk_pos in list(chunks_dict.keys()):
        dx = abs(chunk_pos[0] - current_chunk[0])
        dy = abs(chunk_pos[1] - current_chunk[1])
        if dx > visibility_radius or dy > visibility_radius:
            chunks_to_unload.append(chunk_pos)
    
    for chunk_pos in chunks_to_unload:
        data = chunks_dict[chunk_pos]
        save_chunk_data(chunk_pos, data)
        del chunks_dict[chunk_pos]
    gc.collect()