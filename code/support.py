from csv import reader
from os import walk
import os
import pygame
import warnings

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
			with warnings.catch_warnings(record=True) as caught_warnings:
				warnings.simplefilter("always")
				image_surf = pygame.image.load(full_path).convert_alpha()
				for warning in caught_warnings:
					if "iCCP: known incorrect sRGB profile" in str(warning.message):
						continue
					warnings.showwarning(warning.message, warning.category, warning.filename, warning.lineno)
			surface_list.append(image_surf)

	return surface_list

