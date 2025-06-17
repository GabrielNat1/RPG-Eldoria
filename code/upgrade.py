import pygame
import pygame._sdl2.video as sdl2
from settings import *

class Upgrade:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.font = pygame.font.Font(UI_FONT, 48)  # Fonte maior para "Coming Soon"
        self.small_font = pygame.font.Font(UI_FONT, 24)
        self.is_opening = True
        self.animation_progress = 0
        self.last_update = pygame.time.get_ticks()

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] or keys[pygame.K_u]:
            self.is_opening = False
            return True
        return False

    def animate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= 16:
            if self.is_opening:
                self.animation_progress = min(1, self.animation_progress + 0.2)
            else:
                self.animation_progress = max(0, self.animation_progress - 0.2)
            self.last_update = current_time

    def display(self, surface=None):
        # surface pode ser passado pelo Level, se não, usa display_surface
        if surface is None:
            surface = self.display_surface

        if self.input():
            if self.animation_progress <= 0:
                return True

        self.animate()

        # Fundo semi-transparente
        bg_color = (0, 0, 0, int(180 * self.animation_progress))
        temp_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        temp_surface.fill(bg_color)

        # Texto "Coming Soon"
        text = "Coming Soon"
        text_surf = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 20))
        temp_surface.blit(text_surf, text_rect)

        # Texto menor de instrução
        info = "O sistema de upgrades estará disponível em breve!"
        info_surf = self.small_font.render(info, True, (200, 200, 200))
        info_rect = info_surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 40))
        temp_surface.blit(info_surf, info_rect)

        surface.blit(temp_surface, (0, 0))
        return False

class Item:
    def __init__(self, l, t, w, h, index, font):
        self.original_rect = pygame.Rect(l, t, w, h)
        self.rect = self.original_rect.copy()
        self.index = index
        self.font = font

    def display(self, surface, selection_num, name, value, max_value, cost, animation_progress):
        # Apply animation
        offset = 50 * (1 - animation_progress)
        self.rect.y = self.original_rect.y + offset
        alpha = int(255 * animation_progress)

        # Create temporary surface with transparency
        temp_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        
        # Draw background
        if self.index == selection_num:
            bg_color = (*UPGRADE_BG_COLOR_SELECTED[:3], alpha)  # Convert to RGBA
            border_color = (*UI_BORDER_COLOR[:3], alpha)  # Convert to RGBA
        else:
            bg_color = (*UI_BG_COLOR[:3], alpha)  # Convert to RGBA
            border_color = (*UI_BORDER_COLOR[:3], alpha)  # Convert to RGBA
            
        pygame.draw.rect(temp_surf, bg_color, temp_surf.get_rect())
        pygame.draw.rect(temp_surf, border_color, temp_surf.get_rect(), 4)

        # Draw content
        self.display_names(temp_surf, name, cost, self.index == selection_num, alpha)
        self.display_bar(temp_surf, value, max_value, self.index == selection_num, alpha)
        
        # Blit to main surface
        surface.blit(temp_surf, self.rect)

    def display_names(self, surface, name, cost, selected, alpha):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        text_color = (*color[:3], alpha)  # Convert to RGBA
        
        title_surf = self.font.render(name, True, text_color)
        title_rect = title_surf.get_rect(midtop=(self.rect.width//2, 20))
        surface.blit(title_surf, title_rect)
        
        cost_surf = self.font.render(f'{int(cost)}', True, text_color)
        cost_rect = cost_surf.get_rect(midbottom=(self.rect.width//2, self.rect.height-20))
        surface.blit(cost_surf, cost_rect)

    def display_bar(self, surface, value, max_value, selected, alpha):
        if selected:
            color = (*BAR_COLOR_SELECTED[:3], alpha)  # Convert to RGBA
        else:
            color = (*BAR_COLOR[:3], alpha)  # Convert to RGBA
        
        top = pygame.math.Vector2(self.rect.width//2, 60)
        bottom = pygame.math.Vector2(self.rect.width//2, self.rect.height-60)
        
        full_height = bottom.y - top.y
        relative_number = (value / max_value) * full_height
        value_rect = pygame.Rect(top.x - 15, bottom.y - relative_number, 30, 10)
        
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

    def trigger(self, player):
        upgrade_attribute = list(player.stats.keys())[self.index]
        
        if player.exp >= player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
            player.exp -= player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] += 1
            player.upgrade_cost[upgrade_attribute] *= 1.4
        
        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]