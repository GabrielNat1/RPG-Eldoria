import pygame
import random
import os
from settings import WIDTH, HEIGTH
from player import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, display_surface, mission_system=None):
        super().__init__(groups)

        # NPC frames
        self.frames = [
            pygame.image.load(os.path.join("../", "graphics", "npc", "oldman", f"npc_{i}.png")).convert_alpha()
            for i in range(1, 5)
        ]
        self.current_frame = 0
        self.animation_speed = 1
        self.last_update = pygame.time.get_ticks()
        

        # "Speaking" animation
        self.dialogue_indicator_frames = [
            pygame.image.load(os.path.join("../", "graphics", "ui", "dialog", f"DialogInfo_{i}.png")).convert_alpha()
            for i in range(1, 3)  # 3 frames in the folder
        ]
        self.dialogue_indicator_current_frame = 0
        self.dialogue_indicator_speed = 0.2  # Animation speed
        self.dialogue_indicator_last_update = pygame.time.get_ticks()

        # Image and hitbox
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)

        # Other attributes
        self.player = player
        self.display_surface = display_surface
        self.dialogue_text = ""
        self.typing_effect_index = 0
        self.typing_effect_speed = 40  # Slow down typing speed for better audio sync
        self.typing_effect_last_update = pygame.time.get_ticks()
        self.dialogue_stage = 0
        self.quest_given = False
        self.show_dialogue = False
        self.interaction_completed = False
        self.player_near = False
        self.dialogue_complete_time = None  # Time when the dialogue finishes

        # Emote management
        self.emote_last_update = pygame.time.get_ticks()
        self.current_emote = None

        # Directional facing
        self.facing_right = False  # Start facing left

        # Time delay to close dialogue automatically
        self.dialogue_close_time = None

        # Talking Sound NPC 
        self.speech_sound = pygame.mixer.Sound('../audio/npc/talking_sfx/Talking.mp3')
        self.is_playing_speech = False
        self.is_sound_playing = False  
        
        #mission definded
        self.mission_system = mission_system if mission_system else MissionSystem()

    def animate(self):
        """Animate the NPC"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_speed * 100:
            self.last_update = current_time
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def animate_dialogue_indicator(self):
        """Updates the dialogue indicator animation."""  
        current_time = pygame.time.get_ticks()
        if current_time - self.dialogue_indicator_last_update > self.dialogue_indicator_speed * 100:
            self.dialogue_indicator_last_update = current_time
            self.dialogue_indicator_current_frame = (self.dialogue_indicator_current_frame + 1) % len(self.dialogue_indicator_frames)

    def draw_dialogue_indicator(self):
        """Draws the animated sprite above the NPC's head."""  
        if self.show_dialogue:  # Only shows if the dialogue is active
            self.animate_dialogue_indicator()
            indicator_image = self.dialogue_indicator_frames[self.dialogue_indicator_current_frame]
            indicator_rect = indicator_image.get_rect(midbottom=self.rect.midtop)  # Above the NPC's head
            self.display_surface.blit(indicator_image, indicator_rect)

    def check_player_distance(self):
        """Checks the distance between the NPC and the player"""
        player_distance = pygame.math.Vector2(
            self.rect.centerx - self.player.rect.centerx,
            self.rect.centery - self.player.rect.centery,
        ).length()

        self.player_near = player_distance <= 100  # Interaction distance

        if self.player_near and not self.show_dialogue and not self.interaction_completed:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:  # Activates dialogue when pressing Enter
                self.show_dialogue = True
                self.start_dialogue()
        print(f"NPC reconhecendo player: {self.player}")  # Debug
        print(f"Missão atual: {self.mission_system.get_mission_state()}")  # Debug

    def start_dialogue(self):
        """Starts the dialogue based on the current stage"""
        if self.dialogue_stage == 0:
            self.dialogue_text = "Hello dear player!!"
        elif self.dialogue_stage == 1:
            self.dialogue_text = "Could you get 1000 points for me? please."
            self.mission_system.start_mission()
        elif self.dialogue_stage == 2:
            if self.player.exp >= 1000:
                self.dialogue_text = "Thank you very much, player! Here your prize: Lance"
                self.player.exp -= 1000
                self.player.weapons.append("lance")
                self.quest_given = True
                self.interaction_completed = True
                self.mission_system.complete_mission()
            else:
                self.dialogue_text = "Go, player! Get those 1000 points for me."

        self.typing_effect_index = 0  # Start typing effect from the beginning

        if not self.is_playing_speech:
            self.speech_sound.play(-1)  
            self.is_playing_speech = True
            self.is_sound_playing = True

    def display_dialogue(self):
        """Displays the dialogue text with black background and orange borders"""
        # Draw black background with orange border
        pygame.draw.rect(
            self.display_surface,
            (255, 165, 0),  # Border color (orange)
            pygame.Rect(WIDTH // 2 - (WIDTH - 200) // 2, HEIGTH // 1.5, WIDTH - 200, 150),
            border_radius=10,  # Rounded corners
            width=5  # Border thickness
        )  # Draw the orange border
        
        pygame.draw.rect(
            self.display_surface,
            (0, 0, 0),  # Background color (black)
            pygame.Rect(WIDTH // 2 - (WIDTH - 200) // 2 + 5, HEIGTH // 1.5 + 5, WIDTH - 210, 140),  # Adjusted size so the black background doesn't overlap with the border
            border_radius=10  # Rounded corners
        )  # Draw the black background

        font = pygame.font.Font(None, 30)
        current_time = pygame.time.get_ticks()

        # Typing effect
        if current_time - self.typing_effect_last_update > self.typing_effect_speed:
            self.typing_effect_last_update = current_time
            if self.typing_effect_index < len(self.dialogue_text):
                self.typing_effect_index += 1

        text_surface = font.render(
            self.dialogue_text[: self.typing_effect_index], True, (255, 255, 255)  # White text
        )
        text_rect = text_surface.get_rect(
            topleft=(WIDTH // 2 - (WIDTH - 200) // 2 + 20, HEIGTH // 1.5 + 20)  # Margin for the text
        )
        self.display_surface.blit(text_surface, text_rect)

        # Pause sound when space is pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.is_sound_playing:
                self.speech_sound.stop()  # Stop the sound
                self.is_sound_playing = False

        # Check if the player has finished typing
        if self.typing_effect_index == len(self.dialogue_text):
            if self.dialogue_close_time is None:
                self.dialogue_close_time = pygame.time.get_ticks()  # Record when dialogue finishes
            elif pygame.time.get_ticks() - self.dialogue_close_time > 1000:  # Wait 1 second after dialogue finishes
                self.close_dialogue()

    def close_dialogue(self):
        """Closes the dialogue and stops speech sound"""
        self.show_dialogue = False
        if self.dialogue_stage < 2:
            self.dialogue_stage += 1
        self.dialogue_close_time = None  # Reset dialogue completion time

        # Stop the speech sound when the dialogue is closed
        self.speech_sound.stop()
        self.is_playing_speech = False
        self.is_sound_playing = False

    def show_emote(self):
        """Show a random emote above the NPC's head every 40 seconds"""
        current_time = pygame.time.get_ticks()
        if current_time - self.emote_last_update > 40000:  # 40 seconds
            emote_files = os.listdir('../graphics/ui/emote')
            emote_file = random.choice(emote_files)  # Randomly choose an emote
            self.current_emote = pygame.image.load(f'../graphics/ui/emote/{emote_file}').convert_alpha()
            self.emote_last_update = current_time  # Reset timer for the next emote

    def draw_emote(self):
        """Draws the emote above the NPC"""
        if self.current_emote:  # If there's a valid emote
            emote_rect = self.current_emote.get_rect(midbottom=self.rect.midtop)
            self.display_surface.blit(self.current_emote, emote_rect)

class MissionSystem:
    def __init__(self):
        self.mission_state = "not_start"

    def get_mission_state(self):
        return self.mission_state

    def set_mission_state(self, state):
        self.mission_state = state
        print(f"Estado da missão atualizado para: {self.mission_state}")

    def start_mission(self):
        self.set_mission_state("in_progress")

    def complete_mission(self):
        self.set_mission_state("completed")
