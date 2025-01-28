from csv import reader
from os import walk
import os
import pygame
import warnings
from PIL import Image
import sys

# Caminho para o diretório de imagens
folder_path = "../graphics/environment/wind"

# Suprimir mensagens no stderr
class SuppressOutput:
    def __enter__(self):
        self._original_stderr = sys.stderr
        self._null = open(os.devnull, 'w')  # Abre um "buraco negro" para mensagens
        sys.stderr = self._null  # Redireciona o stderr para o null

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stderr = self._original_stderr  # Restaura o stderr
        self._null.close()

# Processar as imagens sem mensagens no terminal
with SuppressOutput():  # Tudo dentro desse bloco não terá mensagens no stderr
    for filename in os.listdir(folder_path):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            image_path = os.path.join(folder_path, filename)
            try:
                image = Image.open(image_path)
                image.load()  # Garante o carregamento da imagem
            except Exception as e:
                pass  # Ignora erros se necessário

def import_csv_layout(path):
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map

def import_folder(path):
	surface_list = []

	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list

