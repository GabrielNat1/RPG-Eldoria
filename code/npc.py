import pygame
from paths import get_asset_path
from settings import WIDTH, HEIGTH, AUDIO_PATHS

# Helper para obter a surface correta, independente do backend
def get_main_surface():
	if hasattr(pygame.display, "get_window"):
		try:
			return pygame.display.get_window().get_surface()
		except Exception:
			pass
	return pygame.display.get_surface()

class NPC(pygame.sprite.Sprite):
    shared_frames = {}

    def __init__(self, pos, groups, player, display_surface, mission_system=None):
        super().__init__(groups)
        self.load_frames()
        # Fallback para imagem transparente se faltar alguma
        fallback_img = pygame.Surface((128, 128), pygame.SRCALPHA)
        self.dialogue_images = {
            0: self.safe_load_dialog_img('OldManBox_0.png', fallback_img),
            1: self.safe_load_dialog_img('OldManBox_1.png', fallback_img),
            2: self.safe_load_dialog_img('OldManBox_2.png', fallback_img)
        }

        # Animation Npc
        self.current_frame = 0
        self.animation_speed = 1
        self.last_update = pygame.time.get_ticks()

        # Img Npc
        self.image = self.frames_down[self.current_frame]  
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)

        self.player = player
        # SDL2: use always the correct display surface
        self.display_surface = get_main_surface()
        self.dialogue_text = ""
        self.displayed_text = ""  # Novo: texto que está sendo exibido
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

        # Direction normal for npc
        self.facing = "down"  # normal down

        # Sound npc talking
        self.speech_sound = pygame.mixer.Sound(AUDIO_PATHS['npc_talk'])
        self.typing_sound = pygame.mixer.Sound(get_asset_path('audio', 'effects', 'Talking.mp3'))  # Efeito de digitação
        self.typing_sound.set_volume(0.3)
        self.is_playing_speech = False
        self.is_sound_playing = False  

        # System Missions
        self.mission_system = mission_system if mission_system else MissionSystem()

        # Interaction control
        self.interaction_cooldown = 300  # Add cooldown time
        self.last_interaction = 0  # Track last interaction time
        self.can_interact = True  # Flag to control interaction

        # Cache dialogue box
        self._dialogue_box = pygame.image.load(get_asset_path('graphics', 'dialog', 'UI', 'DialogBoxFaceset.png')).convert_alpha()
        self._dialogue_font = pygame.font.Font(None, 40)

        # Novos controles de diálogo
        self.dialogue_active = False  # Novo: controle adicional para diálogo
        self.dialogue_initialized = False  # Novo: garante que o diálogo foi iniciado

    def load_frames(self):
        if not NPC.shared_frames:
            NPC.shared_frames['up'] = [
                pygame.image.load(get_asset_path('graphics', 'npc', 'oldman', 'idle_up', f'idle_up_{i}.png')).convert_alpha()
                for i in range(3)
            ]
            NPC.shared_frames['down'] = [
                pygame.image.load(get_asset_path('graphics', 'npc', 'oldman', 'idle_down', f'idle_down_{i}.png')).convert_alpha()
                for i in range(3)
            ]
            NPC.shared_frames['left'] = [
                pygame.image.load(get_asset_path('graphics', 'npc', 'oldman', 'idle_left', f'idle_left_{i}.png')).convert_alpha()
                for i in range(3)
            ]
            NPC.shared_frames['right'] = [pygame.transform.flip(frame, True, False) for frame in NPC.shared_frames['left']]

        self.frames_up = NPC.shared_frames['up']
        self.frames_down = NPC.shared_frames['down']
        self.frames_left = NPC.shared_frames['left']
        self.frames_right = NPC.shared_frames['right']

    def update_direction(self):
        """Update Direction for npc"""
        interaction_distance = 200 

        distance_x = self.rect.centerx - self.player.rect.centerx
        distance_y = self.rect.centery - self.player.rect.centery

        distance_to_player = pygame.math.Vector2(distance_x, distance_y).length()
        if distance_to_player <= interaction_distance:
            if abs(distance_x) > abs(distance_y):
                if distance_x > 0:
                    self.facing = "left" 
                elif distance_x < 0:
                    self.facing = "right"  
            else:
                if distance_y > 0:
                    self.facing = "up"  
                elif distance_y < 0:
                    self.facing = "down"  

    def animate(self):
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

    def safe_load_dialog_img(self, filename, fallback):
        try:
            return pygame.image.load(get_asset_path('graphics', 'dialog', 'OldManDialog', filename)).convert_alpha()
        except Exception:
            return fallback

    def start_dialogue(self):
        if self.dialogue_active:
            return

        self.dialogue_active = True
        self.dialogue_initialized = True
        self.show_dialogue = True
        self.typing_effect_index = 0
        self.displayed_text = ""
        self.set_dialogue_text(self.get_current_dialogue())
        self.dialogue_finished_time = None  # Marca quando o texto terminou

        if not self.is_playing_speech:
            self.speech_sound.play()
            self.is_playing_speech = True
            self.is_sound_playing = True

        if hasattr(self.player, "can_move"):
            self.player.can_move = False

    def get_current_dialogue(self):
        # Retorna o texto correto baseado no estágio atual
        if self.dialogue_stage == 0:
            #print("start dialogue")
            self.dialogue_stage += 1
            return "Hello dear player!!"
            
        elif self.dialogue_stage == 1:
            #print("dialogue_stage 1")
            self.mission_system.start_mission()
            self.dialogue_stage += 1
            return "Could you get 100 points for me? please."
        
        elif self.dialogue_stage == 2:
            if self.player.exp >= 100:
                self.player.exp -= 100
                self.player.weapons.append("lance")
                self.quest_given = True
                self.mission_system.complete_mission()
                self.dialogue_stage += 1 
                return "Thank you very much! Here your prize: Lance."
            else:
                return "Go, player! Get those 1000 points for me."
        elif self.dialogue_stage == 3:
            self.mission_system.start_mission()
            self.dialogue_stage += 1 
            return 'Please, get 200 exp!'
        elif self.dialogue_stage == 4:
            if self.player.exp >= 200:
                self.player.exp += 200 
                self.player.weapons.append('axe')
                self.quest_given = True
                self.mission_system.complete_mission()
                self.dialogue_stage += 1
                return "Congratulation, + 200 exp and Axe!"
            else:
                return "Go collect 200 exp!"
        elif self.dialogue_stage == 5:
            self.mission_system.start_mission()
            self.dialogue_stage += 1
            return 'get 200 exp!'
        elif self.dialogue_stage == 6:
            if self.player.exp >= 200:
                self.player.exp -= 200
                self.player.weapons.append('lance')
                self.quest_given = True
                self.mission_system.complete_mission()
                self.dialogue_stage += 1
                return "Congratulation, Get lance!"
            else:
                return "Get 200 exp!"
        elif self.dialogue_stage == 7:
            self.mission_system.start_mission()
            self.dialogue_stage += 1
            return "Please, kill 5 enemies for me."
        elif self.dialogue_stage == 8:
            if self.mission_system.enemies_killed >= 5:
                self.player.exp += 100
                self.player.weapons.append('rapier')
                self.quest_given = True
                self.mission_system.complete_mission()
                self.dialogue_stage += 1
                return "Thank you!! Here is your prize: rapier and 100xp."
            else:
                return "You need to kill 5 enemies."
        elif self.dialogue_stage == 9:
            self.mission_system.start_mission()
            self.dialogue_stage += 1
            return "Final mission, find and kill the boss RACCOON."
        elif self.dialogue_stage == 10:
            if self.mission_system.boss_killed:
                self.player.exp += 100
                self.player.weapons.append('sai')
                self.quest_given = True
                self.mission_system.complete_mission()
                self.dialogue_stage += 1
                return "Thank you!! Here is your prize: sai and 100xp."
            else:
                return "You need to kill the boss RACCOON."
        elif self.dialogue_stage == 11:
            return "Thanks for helping me, you are a good person!"
        
        return "..." 

    def update_dialog(self):
        now = pygame.time.get_ticks()
        if self.typing_effect_index < len(self.dialogue_text):
            if now - self.typing_effect_last_update > self.typing_effect_speed:
                next_char = self.dialogue_text[self.typing_effect_index]
                self.displayed_text += next_char
                self.typing_effect_index += 1
                self.typing_effect_last_update = now
                # Toca o som de digitação apenas para letras visíveis
                if next_char not in (' ', '\n', '\t'):
                    if not self.typing_sound.get_num_channels():
                        self.typing_sound.play()
        elif self.dialogue_finished_time is None:
            self.dialogue_finished_time = pygame.time.get_ticks()

    def display_dialogue(self, target_surface):
        if not self.dialogue_active or not self.dialogue_initialized:
            return
            
        try:
            # Calculate dialog box position and size
            dialogue_box_rect = pygame.Rect(WIDTH // 2 - 400, HEIGTH // 1.3, 800, 200)
            
            # Draw the dialog box image instead of the semi-transparent box
            target_surface.blit(self._dialogue_box, dialogue_box_rect)
            
            # Draw NPC portrait
            npc_rect = pygame.Rect(dialogue_box_rect.left + 16, dialogue_box_rect.top + 36, 105, 114)
            img_idx = min(self.dialogue_stage, max(self.dialogue_images.keys()))
            target_surface.blit(self.dialogue_images[img_idx], npc_rect)

            # Update typing effect
            self.update_dialog()

            # Render text with typing effect
            text = self.displayed_text if self.displayed_text else "..."
            # Using darker color for better contrast
            text_surface = self._dialogue_font.render(text, True, (20, 20, 20))
            # Adjusted text position to be more visible in the dialog box
            text_rect = text_surface.get_rect(topleft=(target_surface.get_width() // 2 - 400 + 140, int(HEIGTH // 1.3) + 80))
            target_surface.blit(text_surface, text_rect)

            # Fecha automaticamente após 2 segundos do texto terminar
            if self.typing_effect_index >= len(self.dialogue_text) and self.dialogue_finished_time is not None:
                if pygame.time.get_ticks() - self.dialogue_finished_time >= 2000:
                    self.give_reward()
                    self.close_dialogue()

            # Permite pular o efeito digitando pressionando ENTER
            keys = pygame.key.get_pressed()
            if self.typing_effect_index < len(self.dialogue_text) and keys[pygame.K_RETURN]:
                self.displayed_text = self.dialogue_text
                self.typing_effect_index = len(self.dialogue_text)
                self.dialogue_finished_time = pygame.time.get_ticks()
                self.typing_sound.stop()
            # ...existing code...
        except Exception as e:
            print(f"Error displaying dialogue: {e}")
            self.close_dialogue()

    def give_reward(self):
        # Dá recompensas conforme o estágio do diálogo/missão
        # Exemplo: adicionar armas ou experiência ao jogador
        if self.dialogue_stage == 2 and self.player.exp >= 100:
            # Dar lança e experiência
            if hasattr(self.player, "inventory"):
                self.player.inventory.append("Lance")
            self.player.exp += 50  # Exemplo de recompensa
        elif self.dialogue_stage == 4 and self.player.exp >= 200:
            if hasattr(self.player, "inventory"):
                self.player.inventory.append("Axe")
            self.player.exp += 200
        elif self.dialogue_stage == 10 and self.mission_system.boss_killed:
            if hasattr(self.player, "inventory"):
                self.player.inventory.append("Sai")
            self.player.exp += 100

    def close_dialogue(self):
        self.show_dialogue = False
        self.dialogue_active = False
        self.dialogue_initialized = False
        self.typing_effect_index = 0
        self.displayed_text = ""
        self.dialogue_finished_time = None

        if hasattr(self.player, "can_move"):
            self.player.can_move = True

        if self.is_playing_speech:
            self.speech_sound.stop()
            self.is_playing_speech = False
            self.is_sound_playing = False

        if self.typing_sound.get_num_channels() > 0:
            self.typing_sound.stop()

        if self.typing_effect_index >= len(self.dialogue_text):
            if self.dialogue_stage < max(self.dialogue_images.keys()):
                self.dialogue_stage += 1

    def check_player_distance(self):
        if not self.can_interact:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_interaction > self.interaction_cooldown:
                self.can_interact = True

        # Only check for interaction if not already in dialogue
        if not self.show_dialogue:
            player_distance = pygame.math.Vector2(
                self.rect.centerx - self.player.rect.centerx,
                self.rect.centery - self.player.rect.centery,
            ).length()

            self.player_near = player_distance <= 100

            if self.player_near and not self.interaction_completed and self.can_interact:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    self.show_dialogue = True
                    self.start_dialogue()
                    self.last_interaction = pygame.time.get_ticks()
                    self.can_interact = False

    def update(self, game_state='gameplay'):
        keys = pygame.key.get_pressed()

        # Só permite interação se o estado for gameplay ou dialog
        if game_state not in ('gameplay', 'dialog'):
            return

        if keys[pygame.K_ESCAPE]:  
            if not self.menu_open: 
                self.menu_open = True
                self.close_dialogue()  
                if self.is_playing_speech: 
                    self.speech_sound.stop()  
                    self.is_playing_speech = False
                    self.is_sound_playing = False
        else:
            if self.menu_open: 
                self.menu_open = False
                if self.show_dialogue and not self.is_playing_speech:
                    self.speech_sound.play(-1)  
                    self.is_playing_speech = True
                    self.is_sound_playing = True
                    
        self.update_direction() 
        self.animate()  
        self.check_player_distance() 

    def set_dialogue_text(self, text):
        self.dialogue_text = text
        self.typing_effect_index = 0
        self.typing_effect_last_update = pygame.time.get_ticks()

    def display(self, surface):
        # Remove debug text display - function can stay empty or be removed
        pass
            
class MissionSystem:
    def __init__(self):
        self.mission_state = "not_start"
        self.enemies_killed = 0
        self.boss_killed = False

    def get_mission_state(self):
        return self.mission_state

    def set_mission_state(self, state):
        self.mission_state = state
        #print(f"Mission Update: {self.mission_state}")

    def start_mission(self):
        self.set_mission_state("in_progress")
        self.enemies_killed = 0
        self.boss_killed = False

    def complete_mission(self):
        self.set_mission_state("completed")

    def enemy_killed(self):
        self.enemies_killed += 1

    def boss_killed_event(self):
        self.boss_killed = True
