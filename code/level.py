import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
import json
import os

class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()
		self.game_paused = False

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		# attack sprites
		self.current_attack = None
		self.attack_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()

		# sprite setup
		self.create_map()

		# user interface 
		self.ui = UI()
		self.upgrade = Upgrade(self.player)

		# particles
		self.animation_player = AnimationPlayer()
		self.magic_player = MagicPlayer(self.animation_player)

		# chunks
		self.chunks = {}
		self.current_chunk = None
		self.visible_chunks = VISIBLE_CHUNKS
		self.load_initial_chunks()

		

	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
			'grass': import_csv_layout('../map/map_Grass.csv'),
			'object': import_csv_layout('../map/map_Objects.csv'),
			'entities': import_csv_layout('../map/map_Entities.csv')
		}
		graphics = {
			'grass': import_folder('../graphics/Grass'),
			'objects': import_folder('../graphics/objects')
		}

		for style, layout in layouts.items():
			for row_index, row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x, y), [self.obstacle_sprites], 'invisible')
						if style == 'grass':
							random_grass_image = choice(graphics['grass'])
							Tile(
								(x, y),
								[self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
								'grass',
								random_grass_image)

						if style == 'object':
							surf = graphics['objects'][int(col)]
							Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)

						if style == 'entities':
							if col == '394' and not hasattr(self, 'player'):
								self.player = Player(
									(x, y),
									[self.visible_sprites],
									self.obstacle_sprites,
									self.create_attack,
									self.destroy_attack,
									self.create_magic)
								self.initial_position = (x, y)  # Armazene a posição inicial do jogador
							else:
								if col == '390': monster_name = 'bamboo'
								elif col == '391': monster_name = 'spirit'
								elif col == '392': monster_name = 'raccoon'
								else: monster_name = 'squid'
								Enemy(
									monster_name,
									(x, y),
									[self.visible_sprites, self.attackable_sprites],
									self.obstacle_sprites,
									self.damage_player,
									self.trigger_death_particles,
									self.add_exp)

	def load_initial_chunks(self):
		player_chunk = self.get_chunk(self.player.rect.center)
		self.load_chunks_around(player_chunk)

	def get_chunk(self, position):
		return (position[0] // (TILESIZE * CHUNKSIZE), position[1] // (TILESIZE * CHUNKSIZE))

	def load_chunks_around(self, chunk):
		for x in range(chunk[0] - self.visible_chunks, chunk[0] + self.visible_chunks + 1):
			for y in range(chunk[1] - self.visible_chunks, chunk[1] + self.visible_chunks + 1):
				if (x, y) not in self.chunks:
					self.chunks[(x, y)] = self.load_chunk((x, y))

	def load_chunk(self, chunk):
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
			'objects': import_folder('../graphics/objects')
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
								chunk_data['boundary'].append(Tile((x, y), [self.obstacle_sprites], 'invisible'))
							if style == 'grass':
								random_grass_image = choice(graphics['grass'])
								chunk_data['grass'].append(Tile(
									(x, y),
									[self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
									'grass',
									random_grass_image))
							if style == 'object':
								surf = graphics['objects'][int(col)]
								chunk_data['object'].append(Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf))
							if style == 'entities':
								if col == '394' and not hasattr(self, 'player'):
									self.player = Player(
										(x, y),
										[self.visible_sprites],
										self.obstacle_sprites,
										self.create_attack,
										self.destroy_attack,
										self.create_magic)
									self.initial_position = (x, y)  # Armazene a posição inicial do jogador
								elif col != '394':
									if col == '390': monster_name = 'bamboo'
									elif col == '391': monster_name = 'spirit'
									elif col == '392': monster_name = 'raccoon'
									else: monster_name = 'squid'
									# Verifique se já existe um inimigo na mesma posição
									if not any(enemy.rect.topleft == (x, y) for enemy in self.attackable_sprites):
										chunk_data['entities'].append(Enemy(
											monster_name,
											(x, y),
											[self.visible_sprites, self.attackable_sprites],
											self.obstacle_sprites,
											self.damage_player,
											self.trigger_death_particles,
											self.add_exp))
		return chunk_data

	def unload_chunks(self, chunk):
		for x in range(chunk[0] - self.visible_chunks - 1, chunk[0] + self.visible_chunks + 2):
			for y in range(chunk[1] - self.visible_chunks - 1, chunk[1] + self.visible_chunks + 2):
				if (x, y) in self.chunks and not self.is_chunk_visible((x, y), chunk):
					
					self.save_chunk((x, y))
					del self.chunks[(x, y)]

	def is_chunk_visible(self, chunk, current_chunk):
		return (current_chunk[0] - self.visible_chunks <= chunk[0] <= current_chunk[0] + self.visible_chunks and
				current_chunk[1] - self.visible_chunks <= chunk[1] <= current_chunk[1] + self.visible_chunks)

	def update_chunks(self):
		new_chunk = self.get_chunk(self.player.rect.center)
		if new_chunk != self.current_chunk:
			self.current_chunk = new_chunk
			self.load_chunks_around(new_chunk)
			self.unload_chunks(new_chunk)

	def save_chunk(self, chunk):
		chunk_data = self.chunks[chunk]
		chunk_file = f'../chunks/chunk_{chunk[0]}_{chunk[1]}.json'
		os.makedirs(os.path.dirname(chunk_file), exist_ok=True)  # Certifique-se de que o diretório exista
		with open(chunk_file, 'w') as f:
			json.dump(chunk_data, f)

	def load_chunk_from_file(self, chunk):
		chunk_file = f'../chunks/chunk_{chunk[0]}_{chunk[1]}.json'
		if os.path.exists(chunk_file):
			with open(chunk_file, 'r') as f:
				chunk_data = json.load(f)
			return chunk_data
		else:
			return self.load_chunk(chunk)

	def create_attack(self):
		self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

	def destroy_attack(self):
		if self.current_attack:
			self.current_attack.kill()
		self.current_attack = None

	def create_magic(self, style, strength, cost):
		if style == 'heal':
			self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

		if style == 'flame':
			self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

	def player_attack_logic(self):
		if self.attack_sprites:
			for attack_sprite in self.attack_sprites:
				collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
				if collision_sprites:
					for target_sprite in collision_sprites:
						if target_sprite.sprite_type == 'grass':
							pos = target_sprite.rect.center
							offset = pygame.math.Vector2(0, 75)
							for leaf in range(randint(3, 6)):
								self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
							target_sprite.kill()
						else:
							target_sprite.get_damage(self.player, attack_sprite.sprite_type)

	def damage_player(self, amount, attack_type):
		if self.player.vulnerable:
			self.player.health -= amount
			self.player.vulnerable = False
			self.player.hurt_time = pygame.time.get_ticks()
			self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])
			if self.player.health <= 0:
				self.player.kill()
				self.respawn_player()

	def respawn_player(self):
		# Reposicione o jogador no ponto inicial correto
		self.player = Player(
			self.initial_position,  # Ponto inicial correto
			[self.visible_sprites],
			self.obstacle_sprites,
			self.create_attack,
			self.destroy_attack,
			self.create_magic)
		self.player.health = self.player.stats['health']  # Restaure a saúde do jogador

	def trigger_death_particles(self, pos, particle_type):
		self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

	def add_exp(self, amount):
		self.player.exp += amount

	def toggle_menu(self):
		self.game_paused = not self.game_paused 

	def run(self):
		self.update_chunks()
		self.visible_sprites.custom_draw(self.player)
		self.ui.display(self.player)
		
		if self.game_paused:
			self.upgrade.display()
		else:
			self.visible_sprites.update()
			self.visible_sprites.enemy_update(self.player)
			self.player_attack_logic()

		

	def is_chunk_within_visibility_radius(self, chunk):
		player_pos = self.player.rect.center
		visibility_radius = 300  # Adjust as needed
		chunk_center = (chunk[0] * TILESIZE * CHUNKSIZE + TILESIZE * CHUNKSIZE // 2, chunk[1] * TILESIZE * CHUNKSIZE + TILESIZE * CHUNKSIZE // 2)
		distance = ((chunk_center[0] - player_pos[0]) ** 2 + (chunk_center[1] - player_pos[1]) ** 2) ** 0.5
		return distance < visibility_radius

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):

		# general setup 
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		# creating the floor
		self.floor_surf = pygame.image.load('../graphics/tilemap/ground.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

	def custom_draw(self,player):

		# getting the offset 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		# drawing the floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf,floor_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			# Verifique se o sprite está dentro da área visível
			if self.is_sprite_visible(sprite):
				offset_pos = sprite.rect.topleft - self.offset
				self.display_surface.blit(sprite.image,offset_pos)

	def is_sprite_visible(self, sprite):
		# Verifique se o sprite está dentro da área visível
		return (self.offset.x - TILESIZE <= sprite.rect.x <= self.offset.x + self.display_surface.get_width() + TILESIZE and
				self.offset.y - TILESIZE <= sprite.rect.y <= self.offset.y + self.display_surface.get_height() + TILESIZE)

	def enemy_update(self,player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
		for enemy in enemy_sprites:
			enemy.enemy_update(player)
