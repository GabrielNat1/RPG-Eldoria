import pygame
import os
from settings import WIDTH, HEIGTH, AUDIO_PATHS

class NPC(pygame.sprite.Sprite):
    shared_frames = {}

    def __init__(self, pos, groups, player, display_surface, mission_system=None):
        super().__init__(groups)
        self.load_frames()
        self.dialogue_images = {
            0: pygame.image.load('../graphics/dialog/OldManDialog/OldManBox_0.png').convert_alpha(),
            1: pygame.image.load('../graphics/dialog/OldManDialog/OldManBox_1.png').convert_alpha(),
            2: pygame.image.load('../graphics/dialog/OldManDialog/OldManBox_2.png').convert_alpha()
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

        # Direction normal for npc
        self.facing = "down"  # normal down

        # Sound npc talking
        self.speech_sound = pygame.mixer.Sound(AUDIO_PATHS['npc_talk'])
        self.is_playing_speech = False
        self.is_sound_playing = False  

        # System Missions
        self.mission_system = mission_system if mission_system else MissionSystem()

    def load_frames(self):
        if not NPC.shared_frames:
            NPC.shared_frames['up'] = [
                pygame.image.load(os.path.join("../", "graphics", "npc", "oldman", "idle_up", f"idle_up_{i}.png")).convert_alpha()
                for i in range(3)
            ]
            NPC.shared_frames['down'] = [
                pygame.image.load(os.path.join("../", "graphics", "npc", "oldman", "idle_down", f"idle_down_{i}.png")).convert_alpha()
                for i in range(3)
            ]
            NPC.shared_frames['left'] = [
                pygame.image.load(os.path.join("../", "graphics", "npc", "oldman", "idle_left", f"idle_left_{i}.png")).convert_alpha()
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
        if self.dialogue_stage == 0:
            self.dialogue_text = "Hello dear player!!"
        elif self.dialogue_stage == 1:
            self.dialogue_text = "Could you get 100 points for me? please."
            self.mission_system.start_mission()
        elif self.dialogue_stage == 2:
            if self.player.exp >= 100:
                self.dialogue_text = "Thank you very much! Here your prize: Lance."
                self.player.exp -= 100
                self.player.weapons.append("lance")
                self.quest_given = True
                self.mission_system.complete_mission()
                self.dialogue_stage += 1 
            else:
                self.dialogue_text = "Go, player! Get those 1000 points for me."
        elif self.dialogue_stage == 3:
            self.dialogue_text = 'Please, get 200 exp!'
            self.mission_system.start_mission()
            self.dialogue_stage += 1 
        elif self.dialogue_stage == 4:
            if self.player.exp >= 200:
                self.dialogue_text = "Congratulation, + 200 exp and Axe!"
                self.player.exp += 200 
                self.player.weapons.append('axe')
                self.quest_given = True
                self.mission_system.complete_mission()
                self.dialogue_stage += 1
            else:
                self.dialogue_text = "Go collect 200 exp!"
        elif self.dialogue_stage == 5:
            self.dialogue_text = 'get 200 exp!'
            self.mission_system.start_mission()
            self.dialogue_stage += 1
        elif self.dialogue_stage == 6:
            if self.player.exp >= 200:
                self.dialogue_text = "Congratulation, Get lance!"
                self.player.exp -= 200
                self.player.weapons.append('lance')
                self.quest_given = True
                self.mission_system.complete_mission()
                self.dialogue_stage += 1
            else:
                self.dialogue_text = "Get 200 exp!"
        elif self.dialogue_stage == 7:
            self.dialogue_text = "Please, kill 5 enemies for me."

            self.mission_system.start_mission()
            self.dialogue_stage += 1
        elif self.dialogue_stage == 8:
            if self.mission_system.enemies_killed >= 5:
                self.dialogue_text = "Please, kill 5 enemies for me."
                self.player.exp += 100
                self.player.weapons.append('rapier')
                self.quest_given = True
                self.mission_system.complete_mission()
                self.dialogue_stage += 1
            else:
                self.dialogue_text = "You need to kill 5 enemies."
                
                
        elif self.dialogue_stage == 9:
            self.dialogue_text = "Final mission, find and kill the boss RACCOON."
            self.mission_system.start_mission()
            self.dialogue_stage += 1
        elif self.dialogue_stage == 10:
            if self.mission_system.boss_killed:
                self.dialogue_text = "Thank you!! Here is your prize: sai and 100xp."
                self.player.exp += 100
                self.player.weapons.append('sai')
                self.quest_given = True
                self.mission_system.complete_mission()
                self.dialogue_stage += 1
            else:
                self.dialogue_text = "You need to kill the boss RACCOON."
        elif self.dialogue_stage == 11:
            self.dialogue_text = "Thanks for helping me, you are a good person!"
            self.interaction_completed = True

        self.typing_effect_index = 0  
        
        if not self.is_playing_speech:
            self.speech_sound.play() 
            self.is_playing_speech = True
            self.is_sound_playing = True

    def display_dialogue(self):
        dialogue_box = pygame.image.load('../graphics/dialog/UI/DialogBoxFaceset.png').convert_alpha()
        
        npc_image = self.dialogue_images.get(self.dialogue_stage, self.dialogue_images[0])

        dialogue_box_rect = pygame.Rect(WIDTH // 2 - 400, HEIGTH // 1.3, 800, 200)
        npc_rect = pygame.Rect(dialogue_box_rect.left + 16, dialogue_box_rect.top + 36, 105, 114)

        self.display_surface.blit(dialogue_box, dialogue_box_rect)
        self.display_surface.blit(npc_image, npc_rect)

        font = pygame.font.Font(None, 40)
        current_time = pygame.time.get_ticks()

        if current_time - self.typing_effect_last_update > self.typing_effect_speed:
            self.typing_effect_last_update = current_time
            if self.typing_effect_index < len(self.dialogue_text):
                self.typing_effect_index += 1

        text_surface = font.render(
            self.dialogue_text[: self.typing_effect_index], True, (0, 0, 0)
        )
        text_rect = text_surface.get_rect(
            topleft=(dialogue_box_rect.left + 140, dialogue_box_rect.top + 50)
        )
        self.display_surface.blit(text_surface, text_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.is_sound_playing:
                self.speech_sound.stop()
                self.is_sound_playing = False

        if self.typing_effect_index == len(self.dialogue_text):
            if self.dialogue_close_time is None:
                self.dialogue_close_time = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self.dialogue_close_time > 1000:
                self.close_dialogue()

    def close_dialogue(self):
        self.show_dialogue = False
        if self.dialogue_stage < 2:
            self.dialogue_stage += 1
        self.dialogue_close_time = None  

        if self.is_playing_speech:
            self.speech_sound.stop()  
            self.is_playing_speech = False
            self.is_sound_playing = False

    def update(self):
        keys = pygame.key.get_pressed()

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

    def boss_killed(self):
        self.boss_killed = True