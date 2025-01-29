import pygame
import os
import random
from settings import WIDTH, HEIGTH

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, display_surface, mission_system=None):
        super().__init__(groups)

        # Carregar sprites do NPC para diferentes direções
        self.frames_up = [
            pygame.image.load(os.path.join("../", "graphics", "npc", "oldman", "idle_up", f"idle_up_{i}.png")).convert_alpha()
            for i in range(3)
        ]
        self.frames_down = [
            pygame.image.load(os.path.join("../", "graphics", "npc", "oldman", "idle_down", f"idle_down_{i}.png")).convert_alpha()
            for i in range(3)
        ]
        self.frames_left = [
            pygame.image.load(os.path.join("../", "graphics", "npc", "oldman", "idle_left", f"idle_left_{i}.png")).convert_alpha()
            for i in range(3)
        ]
        self.frames_right = [
            pygame.image.load(os.path.join("../", "graphics", "npc", "oldman", "idle_right", f"idle_right_{i}.png")).convert_alpha()
            for i in range(3)
        ]

        # Variáveis de animação
        self.current_frame = 0
        self.animation_speed = 1
        self.last_update = pygame.time.get_ticks()

        # Inicializar imagem do NPC
        self.image = self.frames_down[self.current_frame]  # Começa voltado para baixo
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)

        self.player = player
        self.display_surface = display_surface
        self.dialogue_text = ""
        self.typing_effect_index = 0
        self.typing_effect_speed = 40  
        self.typing_effect_last_update = pygame.time.get_ticks()
        self.dialogue_stage = 0
        self.quest_given = False
        self.show_dialogue = False
        self.interaction_completed = False
        self.player_near = False
        self.dialogue_complete_time = None
        self.dialogue_close_time = None
        self.menu_open = False

        # Direção inicial
        self.facing = "down"  # Inicialmente voltado para baixo

        # Som do NPC falando
        self.speech_sound = pygame.mixer.Sound('../audio/npc/talking_sfx/Talking.mp3')
        self.is_playing_speech = False
        self.is_sound_playing = False  

        # Sistema de missões
        self.mission_system = mission_system if mission_system else MissionSystem()

    def update_direction(self):
        """Atualiza a direção do NPC com base na posição do jogador, mas apenas se o jogador estiver perto o suficiente."""
        # Distância mínima de interação
        interaction_distance = 200  # Ajuste o valor conforme necessário

        # Calculando a diferença absoluta entre as posições do jogador e do NPC
        distance_x = self.rect.centerx - self.player.rect.centerx
        distance_y = self.rect.centery - self.player.rect.centery

        # Calculando a distância total entre o NPC e o jogador
        distance_to_player = pygame.math.Vector2(distance_x, distance_y).length()

        # Só atualiza a direção se o jogador estiver dentro da distância de interação
        if distance_to_player <= interaction_distance:
            # Verifica se o jogador está à esquerda ou à direita
            if abs(distance_x) > abs(distance_y):  # Mais distante no eixo X
                if distance_x > 0:
                    self.facing = "left"  # Jogador está à esquerda
                elif distance_x < 0:
                    self.facing = "right"  # Jogador está à direita

            # Verifica se o jogador está acima ou abaixo
            if abs(distance_y) > abs(distance_x):  # Mais distante no eixo Y
                if distance_y > 0:
                    self.facing = "up"  # Jogador está acima
                elif distance_y < 0:
                    self.facing = "down"  # Jogador está abaixo

    def animate(self):
        """Anima o NPC com base na direção atual."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_speed * 100:
            self.last_update = current_time
            self.current_frame = (self.current_frame + 1) % len(self.frames_down)

            if self.facing == "up":
                self.image = self.frames_up[self.current_frame]
            elif self.facing == "down":
                self.image = self.frames_down[self.current_frame]
            elif self.facing == "left":
                self.image = self.frames_left[self.current_frame]
            elif self.facing == "right":
                self.image = self.frames_right[self.current_frame]

    def check_player_distance(self):
        """Verifica a distância entre o NPC e o jogador."""
        player_distance = pygame.math.Vector2(
            self.rect.centerx - self.player.rect.centerx,
            self.rect.centery - self.player.rect.centery,
        ).length()

        self.player_near = player_distance <= 100  # Distância para interação

        if self.player_near and not self.show_dialogue and not self.interaction_completed:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:  # Ativa o diálogo quando Enter é pressionado
                self.show_dialogue = True
                self.start_dialogue()
    
    def update_direction(self):
        """Atualiza a direção do NPC com base na posição do jogador, mas apenas se o jogador estiver perto o suficiente."""
        # Distância mínima de interação
        interaction_distance = 200  # Ajuste o valor conforme necessário

        # Calculando a diferença absoluta entre as posições do jogador e do NPC
        distance_x = self.rect.centerx - self.player.rect.centerx
        distance_y = self.rect.centery - self.player.rect.centery

        # Calculando a distância total entre o NPC e o jogador
        distance_to_player = pygame.math.Vector2(distance_x, distance_y).length()

        # Só atualiza a direção se o jogador estiver dentro da distância de interação
        if distance_to_player <= interaction_distance:
            # Verifica se o jogador está à esquerda ou à direita
            if abs(distance_x) > abs(distance_y):  # Mais distante no eixo X
                if distance_x > 0:
                    self.facing = "left"  # Jogador está à esquerda
                elif distance_x < 0:
                    self.facing = "right"  # Jogador está à direita

            # Verifica se o jogador está acima ou abaixo
            if abs(distance_y) > abs(distance_x):  # Mais distante no eixo Y
                if distance_y > 0:
                    self.facing = "up"  # Jogador está acima
                elif distance_y < 0:
                    self.facing = "down"  # Jogador está abaixo

    def start_dialogue(self):
        """Inicia o diálogo com base no estágio atual."""
        if self.dialogue_stage == 0:
            self.dialogue_text = "Hello dear player!!"
        elif self.dialogue_stage == 1:
            self.dialogue_text = "Could you get 1000 points for me? please."
            self.mission_system.start_mission()
        elif self.dialogue_stage == 2:
            if self.player.exp >= 1000:
                self.dialogue_text = "Thank you very much! Here your prize: Lance."
                self.player.exp -= 1000
                self.player.weapons.append("lance")
                self.quest_given = True
                self.interaction_completed = True
                self.mission_system.complete_mission()
            else:
                self.dialogue_text = "Go, player! Get those 1000 points for me."

        self.typing_effect_index = 0  # Inicia o efeito de digitação

        # Inicia o som de fala, garantindo que ele toque uma vez.
        if not self.is_playing_speech:
            self.speech_sound.play()  # Toca o som uma vez
            self.is_playing_speech = True
            self.is_sound_playing = True

    def display_dialogue(self):
        """Exibe o texto do diálogo na tela, agora com a imagem do NPC à esquerda e a caixa de diálogo bem maior e centralizada."""
        # Carregar as imagens
        dialogue_box = pygame.image.load('../graphics/dialog/UI/DialogBoxFaceset.png').convert_alpha()
        npc_image = pygame.image.load('../graphics/dialog/OldManDialog/OldManBox.png').convert_alpha()
        
        # Aumentar o tamanho da caixa de diálogo para 800x200 e centralizá-la
        dialogue_box_rect = pygame.Rect(WIDTH // 2 - 400, HEIGTH // 1.3, 800, 200)  # Caixa ainda maior, centralizada e mais abaixo
        
        # Aumentar a imagem do NPC para 120x120 (ajustado para combinar com a caixa maior)
        npc_rect = pygame.Rect(dialogue_box_rect.left + 16, dialogue_box_rect.top + 36, 105, 114)
        
        # Desenhar a caixa de diálogo
        self.display_surface.blit(dialogue_box, dialogue_box_rect)
        
        # Desenhar a imagem do NPC à esquerda dentro da caixa
        self.display_surface.blit(npc_image, npc_rect)

        # Texto do diálogo
        font = pygame.font.Font(None, 40)  # Aumentei o tamanho da fonte ainda mais
        current_time = pygame.time.get_ticks()

        # Efeito de digitação
        if current_time - self.typing_effect_last_update > self.typing_effect_speed:
            self.typing_effect_last_update = current_time
            if self.typing_effect_index < len(self.dialogue_text):
                self.typing_effect_index += 1

        # Desenhar o texto dentro da caixa, à direita da imagem do NPC
        text_surface = font.render(
            self.dialogue_text[: self.typing_effect_index], True, (0, 0, 0)  # Texto preto
        )
        text_rect = text_surface.get_rect(
            topleft=(dialogue_box_rect.left + 140, dialogue_box_rect.top + 50)  # Espaçamento ajustado para a nova caixa
        )
        self.display_surface.blit(text_surface, text_rect)

        # Pausa o som quando a barra de espaço é pressionada
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.is_sound_playing:
                self.speech_sound.stop()  # Para o som
                self.is_sound_playing = False

        # Verifica se o jogador terminou de digitar
        if self.typing_effect_index == len(self.dialogue_text):
            if self.dialogue_close_time is None:
                self.dialogue_close_time = pygame.time.get_ticks()  # Registra quando o diálogo termina
            elif pygame.time.get_ticks() - self.dialogue_close_time > 1000:  # Espera 1 segundo depois do diálogo
                self.close_dialogue()

    def close_dialogue(self):
        """Fecha o diálogo e para o som de fala."""
        self.show_dialogue = False
        if self.dialogue_stage < 2:
            self.dialogue_stage += 1
        self.dialogue_close_time = None  # Reseta o tempo de fechamento do diálogo

        # Para o som de fala quando o diálogo é fechado
        if self.is_playing_speech:
            self.speech_sound.stop()  # Para o som imediatamente
            self.is_playing_speech = False
            self.is_sound_playing = False

    def update(self):
        """Atualiza o NPC, incluindo direção e animação."""
        keys = pygame.key.get_pressed()

        # Verifica se o menu foi aberto (supondo que a tecla ESC seja usada para abrir o menu)
        if keys[pygame.K_ESCAPE]:  # Se o jogador pressionou ESC
            if not self.menu_open:  # Se o menu não estava aberto antes
                self.menu_open = True
                self.close_dialogue()  # Fecha o diálogo, se aberto
                if self.is_playing_speech:  # Se o NPC estiver falando
                    self.speech_sound.stop()  # Para o som imediatamente
                    self.is_playing_speech = False
                    self.is_sound_playing = False
        else:
            if self.menu_open:  # Se o menu estava aberto antes e foi fechado
                self.menu_open = False
                # Retoma o som apenas se o NPC estiver falando e o diálogo estiver aberto
                if self.show_dialogue and not self.is_playing_speech:
                    self.speech_sound.play(-1)  # Retoma o som se o NPC estiver falando
                    self.is_playing_speech = True
                    self.is_sound_playing = True
                    
        self.update_direction()  # Atualiza a direção do NPC com base na posição do jogador
        self.animate()  # Anima o NPC com base na direção
        self.check_player_distance()  # Verifica a distância entre o NPC e o jogador

    #def show_emote(self):
    #    """Exibe um emote aleatório acima da cabeça do NPC a cada 40 segundos."""
    #    current_time = pygame.time.get_ticks()
    #    if current_time - self.emote_last_update > 40000:  # 40 segundos
    #        emote_files = os.listdir('../graphics/ui/emote')
    #        emote_file = random.choice(emote_files)  # Escolhe aleatoriamente um emote
    #        self.current_emote = pygame.image.load(f'../graphics/ui/emote/{emote_file}').convert_alpha()
    #        self.emote_last_update = current_time  # Reseta o timer para o próximo emote

    #def draw_emote(self):
    #    """Desenha o emote acima do NPC."""        
    #    if self.current_emote:  
    #        emote_rect = self.current_emote.get_rect(midbottom=self.rect.midtop)
    #        self.display_surface.blit(self.current_emote, emote_rect)

class MissionSystem:
    def __init__(self):
        self.mission_state = "not_start"

    def get_mission_state(self):
        return self.mission_state

    def set_mission_state(self, state):
        self.mission_state = state
        #print(f"Mission Update: {self.mission_state}")

    def start_mission(self):
        self.set_mission_state("in_progress")

    def complete_mission(self):
        self.set_mission_state("completed")