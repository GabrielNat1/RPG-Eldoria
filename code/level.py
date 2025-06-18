import pygame
import asyncio
from settings import *
from tile import Tile
from player import Player
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer, WindEffect, RainEffect, LeafEffect
from magic import MagicPlayer
from upgrade import Upgrade
from npc import NPC, MissionSystem
from chunk_manager import *
from paths import get_asset_path
import os
import gc
import pygame._sdl2

class Level:
	shared_wind_frames = None

	def __init__(self, mission_system=None):
		try:
			# mission
			self.mission_system = mission_system if mission_system else MissionSystem()
  
			# get the display surface 
			self.display_surface = get_main_surface()
			self.game_surface = pygame.Surface((WIDTH, HEIGTH))
			self.game_paused = False 
			self.upgrade_menu_active = False
			self.in_settings = False  # Add this line
			self.in_pause = False  # Add this line
			self.in_menu = False  # Add this line for main menu state

			# Estado do jogo
			self.game_active = False  
			self.paused = False
			self.game_state = 'gameplay' 

			try:
				window = pygame._sdl2.Window.from_display_module()
				self.renderer = window.renderer
			except:
				self.renderer = None

			# sprite group setup
			self.visible_sprites = YSortCameraGroup()
			self.obstacle_sprites = pygame.sprite.Group()

			# attack sprites
			self.current_attack = None
			self.attack_sprites = pygame.sprite.Group()
			self.attackable_sprites = pygame.sprite.Group()
	    
			# create map
			self.initial_position = None 
			self.create_map()

			# user interface - move this after player creation
			self.ui = UI()
			
			# Initialize upgrade menu with player
			self.upgrade = Upgrade(self.player)
			self.upgrade_menu_active = False

			# particles
			self.animation_player = AnimationPlayer()
			self.magic_player = MagicPlayer(self.animation_player)

			# chunks
			self.chunks = {}
			self.current_chunk = None
			
			if PERFORMANCE_MODE == 'optimized':
				self.visible_chunks = VISIBLE_CHUNKS    
				self.wind_effect_interval = 6000         
				self.wind_effect_duration = 2000        
			else:
				self.visible_chunks = VISIBLE_CHUNKS
				self.wind_effect_interval = 4000
				self.wind_effect_duration = 3000
			self.load_initial_chunks()
			os.makedirs(CHUNKS_FOLDER, exist_ok=True)  

			self.max_wind_effects = 4 
			self.wind_effects = pygame.sprite.Group()
			self.wind_effect_last_spawn_time = pygame.time.get_ticks()
			self.load_wind_frames()
			self.spawn_wind_effects()

			self.floor_surf = pygame.image.load(get_asset_path('graphics', 'tilemap', 'ground.png')).convert()
			self.floor_surf = pygame.transform.scale(self.floor_surf, (WIDTH, HEIGTH)) 
			self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

			# Add a delay before enemies can attack the player
			self.enemy_attack_delay = 3000  
			self.game_start_time = pygame.time.get_ticks()

			self.last_respawn_time = pygame.time.get_ticks()
			self.raccoon_respawn_time = 600000  # 10 minutes
			self.last_raccoon_respawn_time = pygame.time.get_ticks()

			# Instance for NPC
			self.npc = NPC(
   			 (self.initial_position[0] + 840, self.initial_position[1]),
   			 [self.visible_sprites, self.obstacle_sprites],
    		 self.player,
   			 self.display_surface,
      		 self.mission_system)
		  
			# Initialize rain effect at the initial position
			self.rain_effect = RainEffect(self.initial_position, [self.visible_sprites])
			if hasattr(self, 'player'):
				self.rain_effect.set_player(self.player)  
			self.rain_effect.set_obstacle_sprites(self.obstacle_sprites)  

			self.leaf_effects = pygame.sprite.Group()  
		except Exception as e:
			print(f"Erro na inicialização do Level: {e}")
			raise

	def create_map(self):
		layouts = {
			'boundary': import_csv_layout(get_asset_path('map', 'map_FloorBlocks.csv')),
			'grass': import_csv_layout(get_asset_path('map', 'map_Grass.csv')),
			'object': import_csv_layout(get_asset_path('map', 'map_Objects.csv')),
			'entities': import_csv_layout(get_asset_path('map', 'map_Entities.csv'))
		}
		graphics = {
			'grass': import_folder(get_asset_path('graphics', 'Grass')),
			'objects': import_folder(get_asset_path('graphics', 'objects'))
		}

		self.enemy_spawn_points = [] 

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
							object_index = int(col)
							if object_index < len(graphics['objects']):
								surf = graphics['objects'][object_index]
								Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)

						if style == 'entities':
							if col == '394' and not hasattr(self, 'player'):
								self.player = Player(
									(x, y),
									[self.visible_sprites],
									self.obstacle_sprites,
									self.create_attack,
									self.destroy_attack,
									self.create_magic,
			                        self.mission_system
                                    )
								self.initial_position = (x, y)  
								self.player.can_move = True  
							else:
								if col == '390': monster_name = 'bamboo'
								elif col == '391': monster_name = 'spirit'
								elif col == '392': monster_name = 'raccoon'
								else: monster_name = 'squid'
								enemy = Enemy(
									monster_name,
									(x, y),
									[self.visible_sprites, self.attackable_sprites],
									self.obstacle_sprites,
									self.damage_player,
									self.trigger_death_particles,
									self.add_exp,
									self.mission_system)
								self.visible_sprites.add(enemy)  
								
								if (monster_name, (x, y)) not in self.enemy_spawn_points:
									self.enemy_spawn_points.append((monster_name, (x, y)))  
         

	def get_chunk(self, position):
			return (position[0] // (TILESIZE * CHUNKSIZE), position[1] // (TILESIZE * CHUNKSIZE))

	def load_initial_chunks(self):
			player_chunk = self.initial_position  
			self.load_chunks_around(self.get_chunk(player_chunk))
   
	def load_chunks_around(self, center_chunk):
		for dx in range(-1, 2):
			for dy in range(-1, 2):
				chunk_pos = (center_chunk[0] + dx, center_chunk[1] + dy)
				if chunk_pos not in self.chunks:
					self.chunks[chunk_pos] = self.load_chunk(chunk_pos)

	def load_chunk(self, chunk):
		chunk_data = load_chunk_data(chunk)
		if chunk_data is None:
			chunk_data = generate_chunk_data(chunk)
			save_chunk_data(chunk, chunk_data)
		return chunk_data

	def update_chunks(self):
		new_chunk = self.get_chunk(self.player.rect.center)
		if new_chunk != self.current_chunk:
			self.current_chunk = new_chunk
			for dx in range(-1, 2):
				for dy in range(-1, 2):
					chunk_pos = (new_chunk[0] + dx, new_chunk[1] + dy)
					if chunk_pos not in self.chunks:
						self.chunks[chunk_pos] = self.load_chunk(chunk_pos)
			unload_chunks(self.chunks, new_chunk, visibility_radius=self.visible_chunks)

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
		current_time = pygame.time.get_ticks()
		if self.player.vulnerable and current_time - self.game_start_time > self.enemy_attack_delay:
			self.player.health -= amount
			self.player.vulnerable = False
			self.player.hurt_time = pygame.time.get_ticks()
			self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])
			if self.player.health <= 0:
				self.player.kill()
				self.player.alive = False
				if self.current_attack:
					self.destroy_attack()
     
				self.respawn_player()

	def respawn_player(self):
		self.player = Player(
			self.initial_position,  
			[self.visible_sprites],
			self.obstacle_sprites,
			self.create_attack,
			self.destroy_attack,
			self.create_magic,
   			self.mission_system)
		self.player.health = self.player.stats['health']
		self.player.blinking = True
		self.player.blink_start_time = pygame.time.get_ticks()
		self.player.vulnerable = False
		if hasattr(self, 'npc'):
			self.npc.player = self.player

		# Update the player reference in RainEffect
		self.rain_effect.set_player(self.player)

	def respawn_enemies(self):
		current_time = pygame.time.get_ticks()
		if not hasattr(self, 'last_spawn_times'):
			self.last_spawn_times = {spawn_point: 0 for _, spawn_point in self.enemy_spawn_points}
		LOAD_IMMEDIATE_DISTANCE = 500 
		MAX_SPAWNS_PER_FRAME = 2     
		MAX_NEARBY_ENEMIES = 1  # Limit to 1 enemy near the player
		NEARBY_DISTANCE = 300  # Distance to check nearby enemies
		RESPAWN_DELAY_AFTER_DEATH = 5000  # 5 seconds delay after death
		spawns_this_frame = 0

		for monster_name, spawn_point in self.enemy_spawn_points:
			delay = 60000 
			if current_time - self.last_spawn_times.get(spawn_point, 0) < delay:
				continue

			spawn_vec = pygame.math.Vector2(spawn_point)
			player_vec = pygame.math.Vector2(self.player.rect.center)
			distance = (player_vec - spawn_vec).magnitude()

			# Skip respawn if player is too close to the spawn point
			if distance < NEARBY_DISTANCE:
				continue

			# Check nearby enemies
			nearby_enemies = [
				sprite for sprite in self.visible_sprites
				if isinstance(sprite, Enemy) and
				(pygame.math.Vector2(sprite.rect.center) - player_vec).magnitude() < NEARBY_DISTANCE
			]
			if len(nearby_enemies) > MAX_NEARBY_ENEMIES:
				continue

			# Skip respawn if too far from the player
			if distance > ENEMY_SPAWN_DISTANCE:
				continue

			enemy_exists = any(
				isinstance(sprite, Enemy) and 
				sprite.monster_name == monster_name and 
				sprite.alive and
				(pygame.math.Vector2(sprite.rect.center) - pygame.math.Vector2(spawn_point)).magnitude() < 50
				for sprite in self.visible_sprites
			)
			if enemy_exists:
				continue

			# Ensure the enemy has been dead for at least the respawn delay
			if hasattr(self, 'enemy_death_times') and spawn_point in self.enemy_death_times:
				if current_time - self.enemy_death_times[spawn_point] < RESPAWN_DELAY_AFTER_DEATH:
					continue

			enemy = Enemy(
				monster_name,
				spawn_point,
				[self.visible_sprites, self.attackable_sprites],
				self.obstacle_sprites,
				self.damage_player,
				self.trigger_death_particles,
				self.add_exp,
				self.mission_system
			)
			self.visible_sprites.add(enemy)
			self.last_spawn_times[spawn_point] = current_time
			spawns_this_frame += 1

			if distance > LOAD_IMMEDIATE_DISTANCE or spawns_this_frame >= MAX_SPAWNS_PER_FRAME:
				break

	def add_enemy_death_time(self, spawn_point):
		if not hasattr(self, 'enemy_death_times'):
			self.enemy_death_times = {}
		self.enemy_death_times[spawn_point] = pygame.time.get_ticks()

	def trigger_death_particles(self, pos, particle_type):
		self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

	def add_exp(self, amount):
		self.player.exp += amount

	def toggle_menu(self):
		if hasattr(self, 'player'):
			self.game_paused = not self.game_paused
			self.upgrade_menu_active = self.game_paused
			if self.upgrade is None:
				self.upgrade = Upgrade(self.player)
			self.upgrade.is_opening = self.upgrade_menu_active
			self.upgrade.animation_progress = 0 if self.upgrade_menu_active else 1
		

	def clear_wind_effects(self):
		self.wind_effects.empty()

	def spawn_wind_effects(self):
		for _ in range(self.max_wind_effects):
			x = randint(int(self.player.rect.left) - 400, int(self.player.rect.right) + 400)
			y = randint(int(self.player.rect.top) - 400, int(self.player.rect.bottom) + 400)
			WindEffect((x, y), [self.visible_sprites, self.wind_effects], self.wind_frames, self.wind_effect_duration)

	def update_wind_effects(self):
		current_time = pygame.time.get_ticks()

		# Stop wind effects if it's raining
		if self.rain_effect.is_raining:
			for wind_effect in self.wind_effects:
				wind_effect.kill()
			return

		# Resume wind effects if not raining
		if current_time - self.wind_effect_last_spawn_time >= self.wind_effect_interval:
			self.wind_effect_last_spawn_time = current_time
			self.spawn_wind_effects()

		# Remove finished wind effects
		for wind_effect in self.wind_effects:
			if wind_effect.finished:
				wind_effect.kill()

	def update_wind_effects_settings(self):
		self.wind_effects.empty()  # Clear existing wind effects
		self.wind_effect_last_spawn_time = pygame.time.get_ticks()  # Reset spawn time
		self.spawn_wind_effects()

	def load_wind_frames(self):
		if Level.shared_wind_frames is None:
			Level.shared_wind_frames = import_folder(get_asset_path('graphics', 'environment', 'wind'))
		self.wind_frames = Level.shared_wind_frames

	def clear_leaf_effects(self):
		self.leaf_effects.empty()  # Clear all leaf effects

	def spawn_leaf_effects(self):
		for _ in range(self.max_wind_effects):  # Reuse max_wind_effects for consistency
			x = randint(int(self.player.rect.left) - 400, int(self.player.rect.right) + 400)
			y = randint(int(self.player.rect.top) - 400, int(self.player.rect.bottom) + 400)
			LeafEffect((x, y), [self.visible_sprites, self.leaf_effects], self.animation_player.frames['leaf'][0])  # Use first leaf frame set

	def update_leaf_effects(self):
		current_time = pygame.time.get_ticks()

		# Remove all leaf effects if rain stops
		if not self.rain_effect.is_raining:
			self.clear_leaf_effects()  # Clear all leaf effects imediatamente
			return

		# Spawn new leaf effects periodically
		if current_time - self.wind_effect_last_spawn_time >= self.wind_effect_interval:
			self.wind_effect_last_spawn_time = current_time
			self.spawn_leaf_effects()

		# Remove leaf effects that are too far from the player
		for leaf_effect in self.leaf_effects:
			if leaf_effect.rect.centerx < self.player.rect.left - 1000 or \
			   leaf_effect.rect.centerx > self.player.rect.right + 1000 or \
			   leaf_effect.rect.centery < self.player.rect.top - 1000 or \
			   leaf_effect.rect.centery > self.player.rect.bottom + 1000:
				leaf_effect.kill()

	def update_leaf_effects_settings(self):
		self.leaf_effects.empty()  # Clear existing leaf effects
		self.wind_effect_last_spawn_time = pygame.time.get_ticks()  # Reset spawn time
		self.spawn_leaf_effects()
  
	def handle_input(self, event):
		if event.type == pygame.KEYDOWN:
			# Menu Principal
			if self.in_menu:
				if event.key == pygame.K_UP:
					self.main_menu.navigate(-1)
				elif event.key == pygame.K_DOWN:
					self.main_menu.navigate(1)
				elif event.key == pygame.K_RETURN:
					action = self.main_menu.select()
					if action == "new_game":
						self.in_menu = False
						self.in_gameplay = True
						self.audio_manager.stop_music()
						self.audio_manager.play_music(AUDIO_PATHS['main_game'], loops=-1)
					elif action == "settings":
						self.in_menu = False
						self.in_settings = True
			
			# Gameplay
			elif self.in_gameplay:
				if event.key == pygame.K_ESCAPE:
					self.in_pause = not self.in_pause  # Toggle pause state
					self.game_paused = self.in_pause  # Sync with game_paused
				elif event.key == pygame.K_u and not self.in_pause:  # Only allow upgrade menu if not paused
					self.upgrade_menu_active = not self.upgrade_menu_active
					self.game_paused = self.upgrade_menu_active

	def cleanup(self):
			try:
				# Limpa grupos de sprites
				if hasattr(self, 'visible_sprites'):
					self.visible_sprites.empty()
				if hasattr(self, 'obstacle_sprites'):
					self.obstacle_sprites.empty()
				if hasattr(self, 'attack_sprites'):
					self.attack_sprites.empty()
				if hasattr(self, 'attackable_sprites'):
					self.attackable_sprites.empty()
				if hasattr(self, 'wind_effects'):
					self.wind_effects.empty()
				if hasattr(self, 'leaf_effects'):
					self.leaf_effects.empty()

				# Remove referências
				self.player = None
				self.current_attack = None
				self.npc = None
				self.upgrade = None
				
				# Força coleta de lixo
				gc.collect()
			except Exception as e:
				print(f"Erro ao limpar recursos do Level: {e}")

	def run(self, game_state='gameplay'):
		try:
			if not self.game_active:
				return self.game_surface

			self.display_surface = get_main_surface()
			
			# Only fill with WATER_COLOR if not in dialog
			if not (hasattr(self, 'npc') and self.npc.show_dialogue):
				self.game_surface.fill(WATER_COLOR)
				
			self.game_state = game_state

			if hasattr(self, 'visible_sprites') and hasattr(self, 'player') and self.player:
				# Impede atualização do player se estiver travado (em diálogo)
				if not hasattr(self.player, "can_move") or self.player.can_move:
					self.visible_sprites.custom_draw(self.player, self.game_surface)
					if game_state == 'gameplay':
						self.visible_sprites.update()
						self.visible_sprites.enemy_update(self.player)
						self.player_attack_logic()
				else:
					self.visible_sprites.custom_draw(self.player, self.game_surface)
					

			self.ui.display(self.player, self.game_surface)

			# Display NPC dialogue
			if hasattr(self, 'npc') and self.npc.show_dialogue:
				if self.npc.dialogue_text:
					self.npc.display_dialogue(self.game_surface)

			if self.upgrade_menu_active and self.upgrade:
				if self.upgrade.display(self.game_surface):
					self.toggle_menu()

			return self.game_surface

		except Exception as e:
			print(f"Error during level execution: {e}")
			return self.game_surface

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		# general setup 
		super().__init__()
		self.display_surface = pygame.Surface((WIDTH, HEIGTH))
		self.half_width = WIDTH // 2
		self.half_height = HEIGTH // 2
		self.offset = pygame.math.Vector2()

		# creating the floor
		self.floor_surf = pygame.image.load(get_asset_path('graphics', 'tilemap', 'ground.png')).convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

	def draw_shadows(self, player, target_surface):
		light_source = pygame.math.Vector2(player.rect.centerx, player.rect.centery - 100)  # Light source above the player
		shadow_color = (0, 0, 0, 100)  # Semi-transparent black for shadows

		for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
			if hasattr(sprite, 'shadow') and self.is_sprite_visible(sprite):
				offset_pos = sprite.rect.topleft - self.offset
				shadow_offset = pygame.math.Vector2(offset_pos) - light_source
				shadow_offset.scale_to_length(20)  # Shadow length
				shadow_rect = sprite.rect.move(shadow_offset.x, shadow_offset.y)
				shadow_surface = pygame.Surface(sprite.image.get_size(), pygame.SRCALPHA)
				shadow_surface.fill(shadow_color)
				target_surface.blit(shadow_surface, shadow_rect.topleft)

	def custom_draw(self, player, target_surface):
		# Update camera position
		self.half_width = target_surface.get_size()[0] // 2
		self.half_height = target_surface.get_size()[1] // 2
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		# Draw floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		target_surface.blit(self.floor_surf, floor_offset_pos)

		# Draw shadows
		self.draw_shadows(player, target_surface)

		# Draw sprites
		for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
			if self.is_sprite_visible(sprite):
				offset_pos = sprite.rect.topleft - self.offset
				target_surface.blit(sprite.image, offset_pos)

	def is_sprite_visible(self, sprite):
		buffer = TILESIZE * 3  # Buffer to ensure objects and enemies are fully off-screen before disappearing
		return (self.offset.x - buffer <= sprite.rect.right <= self.offset.x + self.display_surface.get_width() + buffer and
				self.offset.y - buffer <= sprite.rect.bottom <= self.offset.y + self.display_surface.get_height() + buffer)

	def enemy_update(self,player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
		for enemy in enemy_sprites:
			enemy.enemy_update(player)