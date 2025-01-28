import pygame
from settings import WIDTH, HEIGTH
from player import Player

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, display_surface, npc=None):
        super().__init__(groups)

        # NPC frames
        self.frames = [
            pygame.image.load(f'../graphics/npc/oldman/npc_{i}.png').convert_alpha()
            for i in range(1, 5)
        ]
        self.current_frame = 0
        self.animation_speed = 1
        self.last_update = pygame.time.get_ticks()

        # "Speaking" animation
        self.dialogue_indicator_frames = [
            pygame.image.load(f'../graphics/ui/dialog/DialogInfo_{i}.png').convert_alpha()
            for i in range(0, 3)  # Assuming you have 3 frames in the folder
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
        self.typing_effect_speed = 5
        self.typing_effect_last_update = pygame.time.get_ticks()
        self.dialogue_stage = 0
        self.quest_given = False
        self.show_dialogue = False
        self.interaction_completed = False
        self.player_near = False
        self.dialogue_complete_time = None  # Time when the dialogue finishes

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

    def start_dialogue(self):
        """Starts the dialogue based on the current stage"""
        if self.dialogue_stage == 0:
            self.dialogue_text = "Hello dear player!!"
        elif self.dialogue_stage == 1:
            self.dialogue_text = "Could you get 100 points for me? please."
        elif self.dialogue_stage == 2:
            if self.player.exp >= 100:
                self.dialogue_text = "Thank you very much, player! Here's your reward!!!"
                self.player.exp -= 100
                self.player.weapons.append("sai")
                self.quest_given = True
                self.interaction_completed = True
            else:
                self.dialogue_text = "Go, player! Get those 100 points for me."

        self.typing_effect_index = 10

    def display_dialogue(self):
        """Displays the dialogue text with black background and orange borders"""
        # Draw the black background with orange borders
        pygame.draw.rect(
            self.display_surface,
            (255, 165, 0),  # Border color (orange)
            pygame.Rect(WIDTH // 2 - (WIDTH - 200) // 2, HEIGTH // 1.5, WIDTH - 200, 150),
            border_radius=10,  # Rounded borders
            width=5  # Border thickness
        )  # Draw the orange border
        
        pygame.draw.rect(
            self.display_surface,
            (0, 0, 0),  # Background color (black)
            pygame.Rect(WIDTH // 2 - (WIDTH - 200) // 2 + 5, HEIGTH // 1.5 + 5, WIDTH - 210, 140),  # Adjusting the size so the black background doesn't overlap the border
            border_radius=10  # Rounded borders
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

        # Checks if the text is fully displayed
        if self.typing_effect_index == len(self.dialogue_text):
            # If dialogue is complete and 1 second has passed, close the dialogue automatically
            if self.dialogue_complete_time is None:
                self.dialogue_complete_time = pygame.time.get_ticks()  # Start the timer

            # Close the dialogue after 1 second
            if pygame.time.get_ticks() - self.dialogue_complete_time > 1000:
                self.close_dialogue()

    def close_dialogue(self):
        """Closes the dialogue"""
        pygame.time.delay(500)  # Adds a small delay to give the player time to see the final message
        self.show_dialogue = False
        self.dialogue_complete_time = None  # Reset the timer
        if self.dialogue_stage < 2:
            self.dialogue_stage += 1

    def update(self):
        """NPC update method"""
        self.animate()
        self.check_player_distance()
        if self.show_dialogue:
            self.display_dialogue()
        self.draw_dialogue_indicator()  # Updates the drawing of the dialogue indicator