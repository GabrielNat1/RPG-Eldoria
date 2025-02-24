import pygame
from csv import reader
from os import walk

image_cache = {}

def import_csv_layout(path):
    terrain_map = []
    try:
        with open(path) as level_map:
            layout = reader(level_map, delimiter=',')
            for row in layout:
                terrain_map.append(list(row))
        if not terrain_map:
            print(f"AVISO: O arquivo {path} não contém dados válidos.")
        return terrain_map
    except FileNotFoundError:
        return []
    except Exception as e:
        return []

def import_folder(path):
    surface_list = []
    try:
        for _, __, img_files in walk(path):
            for image in img_files:
                full_path = path + '/' + image
                if full_path not in image_cache:
                    try:
                        image_surf = pygame.image.load(full_path).convert_alpha()
                        image_cache[full_path] = image_surf
                    except pygame.error as e:
                        continue
                surface_list.append(image_cache[full_path])
        if not surface_list:
            print(f"AVISO: Nenhuma imagem foi carregada de {path}")
        return surface_list
    except Exception as e:
        print(f"Erro ao acessar o diretório {path}: {e}")
        return []
