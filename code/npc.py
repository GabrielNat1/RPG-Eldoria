import pygame
import time
from settings import WIDTH, HEIGTH
from player import Player

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, display_surface, npc=None):
        super().__init__(groups)
        self.frames = [
            pygame.image.load(f'../graphics/npc/oldman/npc_{i}.png').convert_alpha() for i in range(1, 5)
        ]
        self.current_frame = 0
        self.animation_speed = 1
        self.last_update = pygame.time.get_ticks()

        self.image = self.frames[self.current_frame]
        self.npc = npc
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.player = player  
        self.quest_given = False
        self.dialogue_completed = False
        self.display_surface = display_surface

        # Caixa de diálogo
        self.dialogue_box = pygame.Surface((WIDTH - 200, 150))
        self.dialogue_box.fill((0, 0, 0))
        self.dialogue_box_rect = self.dialogue_box.get_rect(center=(WIDTH // 2, HEIGTH // 1.5))
        self.dialogue_border_color = (255, 165, 0) 
        self.dialogue_text = ""
        self.show_dialogue = False
        self.typing_effect_index = 0
        self.typing_effect_speed = 5  
        self.typing_effect_last_update = pygame.time.get_ticks()
        self.dialogue_finished = False
        self.dialogue_stage = 0  
        self.dialogue_timer = None
        self.initial_dialogue_done = False 

    def update(self):
        
        self.animate()

       
        player_distance = pygame.math.Vector2(self.rect.centerx - self.player.rect.centerx, self.rect.centery - self.player.rect.centery).length()
        if player_distance <= 100:
            self.handle_npc_interaction()

       
        if self.show_dialogue:
            self.display_dialogue()

    def animate(self):
      
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_speed * 100:
            self.last_update = current_time
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def handle_npc_interaction(self):
       
        player_distance = pygame.math.Vector2(self.rect.centerx - self.player.rect.centerx, self.rect.centery - self.player.rect.centery).length()
        if player_distance <= 100: 
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                if not self.show_dialogue: 
                    self.show_dialogue = True
                    self.dialogue_stage = 0
                    self.start_dialogue()
                elif self.dialogue_finished:  
                    self.show_dialogue = False  

    def start_dialogue(self):
       
        if self.dialogue_stage == 0:
            self.dialogue_text = "Olá caro jogador..."
            self.initial_dialogue_done = True  
        self.typing_effect_index = 0
        self.dialogue_finished = False
        self.dialogue_timer = pygame.time.get_ticks()

    def advance_dialogue(self):
       
        self.show_dialogue = False  

    def display_dialogue(self):
       
        pygame.draw.rect(self.display_surface, self.dialogue_border_color, self.dialogue_box_rect.inflate(10, 10), border_radius=10)
        self.display_surface.blit(self.dialogue_box, self.dialogue_box_rect)

        font = pygame.font.Font(None, 30)
        current_time = pygame.time.get_ticks()

   
        if current_time - self.typing_effect_last_update > self.typing_effect_speed:
            self.typing_effect_last_update = current_time
            if self.typing_effect_index < len(self.dialogue_text):
                self.typing_effect_index += 1
            else:
                self.dialogue_finished = True

      
        text_surface = font.render(self.dialogue_text[:self.typing_effect_index], True, (255, 255, 255))
        text_rect = text_surface.get_rect(topleft=(self.dialogue_box_rect.x + 20, self.dialogue_box_rect.y + 20))
        self.display_surface.blit(text_surface, text_rect)

      
        if self.dialogue_finished:
            self.advance_dialogue()
