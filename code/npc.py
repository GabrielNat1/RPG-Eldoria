import pygame
from settings import WIDTH, HEIGTH
from player import Player


class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, display_surface, npc=None):
        super().__init__(groups)
        self.frames = [
            pygame.image.load(f'../graphics/npc/oldman/npc_{i}.png').convert_alpha()
            for i in range(1, 5)
        ]
        self.current_frame = 0
        self.animation_speed = 1
        self.last_update = pygame.time.get_ticks()

        self.image = self.frames[self.current_frame]
        self.npc = npc
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.player = player
        self.display_surface = display_surface

     
        self.dialogue_box = pygame.Surface((WIDTH - 200, 150))
        self.dialogue_box.fill((0, 0, 0))
        self.dialogue_box_rect = self.dialogue_box.get_rect(
            center=(WIDTH // 2, HEIGTH // 1.5)
        )
        self.dialogue_border_color = (255, 165, 0)
        self.dialogue_text = ""
        self.typing_effect_index = 0
        self.typing_effect_speed = 5
        self.typing_effect_last_update = pygame.time.get_ticks()
        self.dialogue_stage = 0
        self.quest_given = False
        self.show_dialogue = False
        self.interaction_completed = False
        self.player_near = False 

    def update(self):
    
        self.animate()

        self.check_player_distance()

        if self.show_dialogue:
            self.display_dialogue()

    def animate(self):
   
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_speed * 100:
            self.last_update = current_time
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def check_player_distance(self):
        
        player_distance = pygame.math.Vector2(
            self.rect.centerx - self.player.rect.centerx,
            self.rect.centery - self.player.rect.centery,
        ).length()

        self.player_near = player_distance <= 100  

       
        if self.player_near and not self.show_dialogue and not self.interaction_completed:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:  
                self.show_dialogue = True
                self.start_dialogue()

    def start_dialogue(self):
        """Inicia o diálogo de acordo com o estágio atual."""
        if self.dialogue_stage == 0:
            self.dialogue_text = "Olá caro jogador..."
        elif self.dialogue_stage == 1:
            self.dialogue_text = "Poderia pegar 100 pontos para mim? porfavor "
        elif self.dialogue_stage == 2:
            if self.player.exp >= 100:  # Jogador tem os pontos necessários
                self.dialogue_text = "Muito obrigado, jogador! Aqui está sua recompensa!!!"
                self.player.exp -= 100
                self.player.weapons.append("sai")  # Recompensa
                self.quest_given = True
                self.interaction_completed = True  # Bloqueia futuras interações
            else:
                self.dialogue_text = "Vá, jogador! Pegue os 100 pontos para mim."

        self.typing_effect_index = 0

    def display_dialogue(self):
        
        pygame.draw.rect(
            self.display_surface,
            self.dialogue_border_color,
            self.dialogue_box_rect.inflate(10, 10),
            border_radius=10,
        )
        self.display_surface.blit(self.dialogue_box, self.dialogue_box_rect)

        font = pygame.font.Font(None, 30)
        current_time = pygame.time.get_ticks()

       
        if current_time - self.typing_effect_last_update > self.typing_effect_speed:
            self.typing_effect_last_update = current_time
            if self.typing_effect_index < len(self.dialogue_text):
                self.typing_effect_index += 1

        text_surface = font.render(
            self.dialogue_text[: self.typing_effect_index], True, (255, 255, 255)
        )
        text_rect = text_surface.get_rect(
            topleft=(self.dialogue_box_rect.x + 20, self.dialogue_box_rect.y + 20)
        )
        self.display_surface.blit(text_surface, text_rect)

      
        if self.typing_effect_index == len(self.dialogue_text):
            self.close_dialogue()

    def close_dialogue(self):
      
        pygame.time.delay(500)  
        self.show_dialogue = False
        if self.dialogue_stage < 2:
            self.dialogue_stage += 1 
