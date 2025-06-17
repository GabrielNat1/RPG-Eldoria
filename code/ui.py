import pygame
from settings import * 

class UI:
	def __init__(self):
		# general 
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

		# bar setup 
		self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
		self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)
		self.stamina_bar_rect = pygame.Rect(10,58,ENERGY_BAR_WIDTH,BAR_HEIGHT) 

		# convert weapon dictionary
		self.weapon_graphics = []
		self.weapons_data = []
		for weapon in weapon_data.values():
			path = weapon['graphic']
			weapon_surf = pygame.image.load(path).convert_alpha()
			self.weapon_graphics.append(weapon_surf)
			self.weapons_data.append(weapon)

		# convert magic dictionary
		self.magic_graphics = []
		for magic in magic_data.values():
			magic = pygame.image.load(magic['graphic']).convert_alpha()
			self.magic_graphics.append(magic)

	def show_bar(self,current,max_amount,bg_rect,color,target_surface):
		# draw bg 
		pygame.draw.rect(target_surface,UI_BG_COLOR,bg_rect)

		# converting stat to pixel
		ratio = current / max_amount
		current_width = bg_rect.width * ratio
		current_rect = bg_rect.copy()
		current_rect.width = current_width

		# drawing the bar
		pygame.draw.rect(target_surface,color,current_rect)
		pygame.draw.rect(target_surface,UI_BORDER_COLOR,bg_rect,3)

	def show_exp(self,exp,target_surface):
		text_surf = self.font.render(str(int(exp)),False,TEXT_COLOR)
		x = self.display_surface.get_size()[0] - 250  # Moved closer to right edge
		y = self.display_surface.get_size()[1] - 250  # Moved closer to bottom edge
		text_rect = text_surf.get_rect(bottomright = (x,y))  

		pygame.draw.rect(target_surface,UI_BG_COLOR,text_rect.inflate(20,20))
		target_surface.blit(text_surf,text_rect)
		pygame.draw.rect(target_surface,UI_BORDER_COLOR,text_rect.inflate(20,20),3)

	def selection_box(self, left, top, has_switched, target_surface):
		bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
		pygame.draw.rect(target_surface, UI_BG_COLOR, bg_rect)  # Draw background on target_surface
		if has_switched:
			pygame.draw.rect(target_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
		else:
			pygame.draw.rect(target_surface, UI_BORDER_COLOR, bg_rect, 3)
		return bg_rect

	def weapon_overlay(self, weapon_index, has_switched, target_surface):
		if weapon_index is None:
			return
			
		bg_rect = self.selection_box(10, 630, has_switched, target_surface)  # Pass target_surface
		weapon_surf = self.weapon_graphics[weapon_index]
		weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
		target_surface.blit(weapon_surf, weapon_rect)

	def magic_overlay(self, magic_index, has_switched, target_surface):
		bg_rect = self.selection_box(80, 635, has_switched, target_surface)  # Pass target_surface
		magic_surf = self.magic_graphics[magic_index]
		magic_rect = magic_surf.get_rect(center=bg_rect.center)
		target_surface.blit(magic_surf, magic_rect)

	def display(self,player, target_surface):
		self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR, target_surface)
		self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR, target_surface)
		self.show_bar(player.stamina, player.stats['stamina'], self.stamina_bar_rect, ENERGY_COLOR, target_surface) 

		self.show_exp(player.exp, target_surface)

		self.weapon_overlay(player.weapon_index, not player.can_switch_weapon, target_surface)
		self.magic_overlay(player.magic_index, not player.can_switch_magic, target_surface)