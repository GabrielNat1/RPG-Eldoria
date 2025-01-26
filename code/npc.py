import pygame
import time

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, display_surface):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/npc/npc.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.player = player
        self.quest_given = False
        self.display_surface = display_surface  # Para mostrar o diálogo
        self.dialogue_stage = 0
        self.dialogue_text = ""
        self.typing_effect_index = 0
        self.typing_effect_speed = 50
        self.typing_effect_last_update = 0
        self.dialogue_finished = False
        self.dialogue_timer = 0
        self.show_dialogue = False

    def update(self):
        # Verifica se o jogador está perto do NPC e permite interação
        player_distance = pygame.math.Vector2(self.rect.centerx - self.player.rect.centerx, self.rect.centery - self.player.rect.centery).length()
        if player_distance <= 100 and not self.quest_given:
            if pygame.key.get_pressed()[pygame.K_KP_ENTER]:
                self.give_quest()

        # Atualiza o diálogo quando necessário
        if self.show_dialogue:
            self.display_dialogue()

    def give_quest(self):
        if self.player.exp >= 100:
            self.player.exp -= 100  # Deduz 100 de experiência
            self.quest_given = True
            self.dialogue_stage = 1
            self.dialogue_text = "Missão concluída! Como recompensa, você recebeu uma nova arma."
            self.typing_effect_index = 0
            self.dialogue_finished = False
            self.dialogue_timer = pygame.time.get_ticks()
            self.show_dialogue = True
        else:
            self.dialogue_stage = 1
            self.dialogue_text = "Você precisa de 100 pontos de experiência para completar a missão."
            self.typing_effect_index = 0
            self.dialogue_finished = False
            self.dialogue_timer = pygame.time.get_ticks()
            self.show_dialogue = True

    def display_dialogue(self):
        pygame.draw.rect(self.display_surface, (0, 0, 0), pygame.Rect(50, 400, 600, 150), border_radius=10)
        font = pygame.font.Font(None, 30)
        current_time = pygame.time.get_ticks()

        if current_time - self.typing_effect_last_update > self.typing_effect_speed:
            self.typing_effect_last_update = current_time
            if self.typing_effect_index < len(self.dialogue_text):
                self.typing_effect_index += 1
            else:
                self.dialogue_finished = True

        text_surface = font.render(self.dialogue_text[:self.typing_effect_index], True, (255, 255, 255))
        text_rect = text_surface.get_rect(topleft=(60, 420))
        self.display_surface.blit(text_surface, text_rect)

        if self.dialogue_finished and current_time - self.dialogue_timer > 1000:
            if self.dialogue_stage == 1:
                self.dialogue_stage = 2
                self.dialogue_text = "Agora você pode equipar sua nova arma!"
                self.typing_effect_index = 0
                self.dialogue_finished = False
                self.dialogue_timer = pygame.time.get_ticks()
            elif self.dialogue_stage == 2:
                self.dialogue_stage = 0
                self.show_dialogue = False
              
                self.player.weapon = self.player.add_weapon('sai')
                print('arma adicionada')
                print(self.player.weapon)
