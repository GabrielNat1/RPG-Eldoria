import pygame
from csv import reader
from os import walk

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
        #print(f"Erro: O arquivo {path} não foi encontrado.")
        return []
    except Exception as e:
        #print(f"Erro ao importar {path}: {e}")
        return []
    
def import_folder(path):
    surface_list = []
    try:
        for _, __, img_files in walk(path):
            for image in img_files:
                full_path = path + '/' + image
                try:
                    image_surf = pygame.image.load(full_path).convert_alpha()
                    surface_list.append(image_surf)
                     #print(f"Imagem carregada: {full_path}")  # Mensagem de depuração
                except pygame.error as e:
                    #print(f"Erro ao carregar imagem {full_path}: {e}")
                    pass
        if not surface_list:
            print(f"AVISO: Nenhuma imagem foi carregada de {path}")
        return surface_list
    except Exception as e:
        print(f"Erro ao acessar o diretório {path}: {e}")
        return []
