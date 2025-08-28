import pygame
from csv import reader
from os import walk
import platform
import os  

if platform.system() in ["Linux", "Darwin"]: 
    import resource

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
                full_path = os.path.join(path, image)  
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

def check_os_and_limit_memory(memory_limit_mb):
    """
    Scans the operating system and applies a RAM limiter
    on macOS or Linux systems.

    :p aram memory_limit_mb: Memory limit in MB.
    """
    os_name = platform.system()
    if os_name in ["Linux", "Darwin"]:
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        memory_limit_bytes = memory_limit_mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (memory_limit_bytes, hard))
        #print(f"Limite de memória definido para {memory_limit_mb} MB no {os_name}.")
    else:
        #print(f"Sistema operacional {os_name} não suporta limitador de memória.")
        pass

def get_main_surface():
	if hasattr(pygame.display, "get_window"):
		try:
			return pygame.display.get_window().get_surface()
		except Exception:
			pass
	
	return pygame.display.get_surface()