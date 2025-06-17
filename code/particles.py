import pygame
from support import import_folder
from random import choice, randint
import gc
from paths import get_asset_path
from settings import AUDIO_PATHS

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic
            'flame': import_folder(get_asset_path('graphics', 'particles', 'flame', 'frames')),
            'aura': import_folder(get_asset_path('graphics', 'particles', 'aura')),
            'heal': import_folder(get_asset_path('graphics', 'particles', 'heal', 'frames')),

            # attacks
            'claw': import_folder(get_asset_path('graphics', 'particles', 'claw')),
            'slash': import_folder(get_asset_path('graphics', 'particles', 'slash')),
            'sparkle': import_folder(get_asset_path('graphics', 'particles', 'sparkle')),
            'leaf_attack': import_folder(get_asset_path('graphics', 'particles', 'leaf_attack')),
            'thunder': import_folder(get_asset_path('graphics', 'particles', 'thunder')),

            # monster deaths
            'squid': import_folder(get_asset_path('graphics', 'particles', 'smoke_orange')),
            'raccoon': import_folder(get_asset_path('graphics', 'particles', 'raccoon')),
            'spirit': import_folder(get_asset_path('graphics', 'particles', 'nova')),
            'bamboo': import_folder(get_asset_path('graphics', 'particles', 'bamboo')),

            # leaves 
            'leaf': (
                import_folder(get_asset_path('graphics', 'particles', 'leaf1')),
                import_folder(get_asset_path('graphics', 'particles', 'leaf2')),
                import_folder(get_asset_path('graphics', 'particles', 'leaf3')),
                import_folder(get_asset_path('graphics', 'particles', 'leaf4')),
                import_folder(get_asset_path('graphics', 'particles', 'leaf5')),
                import_folder(get_asset_path('graphics', 'particles', 'leaf6')),
                self.reflect_images(import_folder(get_asset_path('graphics', 'particles', 'leaf1'))),
                self.reflect_images(import_folder(get_asset_path('graphics', 'particles', 'leaf2'))),
                self.reflect_images(import_folder(get_asset_path('graphics', 'particles', 'leaf3'))),
                self.reflect_images(import_folder(get_asset_path('graphics', 'particles', 'leaf4'))),
                self.reflect_images(import_folder(get_asset_path('graphics', 'particles', 'leaf5'))),
                self.reflect_images(import_folder(get_asset_path('graphics', 'particles', 'leaf6')))
            )
        }
        self.wind_frames = import_folder(get_asset_path('graphics', 'environment', 'wind'))
    
    def reflect_images(self, frames):
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)

    def create_wind_effect(self, pos, groups, duration):
        WindEffect(pos, groups, self.wind_frames, duration)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()

class WindEffect(pygame.sprite.Sprite):
    def __init__(self, pos, groups, frames, duration):
        super().__init__(groups)
        self.frames = [pygame.transform.scale(frame, (frame.get_width() // 2, frame.get_height() // 2)) for frame in frames]  # Reduce size
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.start_time = pygame.time.get_ticks()
        self.duration = duration  # Use the provided duration
        self.finished = False

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
        if pygame.time.get_ticks() - self.start_time >= self.duration:
            self.finished = True
        if self.finished:
            self.kill()

class RainDrop(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups, player):
        super().__init__(groups)
        self.sprite_type = 'rain'
        self.image = pygame.transform.scale(surf, (12, 22))
        self.frame_index = 0
        self.frames = import_folder(get_asset_path('graphics', 'environment', 'drops'))
        self.animation_speed = 0.15
        self.rect = self.image.get_rect(topleft=pos)
        self.initial_pos = pygame.math.Vector2(pos)
        self.player = player  # Store player reference
        self.relative_pos = self.initial_pos - pygame.math.Vector2(self.player.rect.center)
        self.direction = pygame.math.Vector2(0.5, 3)
        self.speed = randint(1, 2)

    def update(self):
        # Animation
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

        # Update relative position with falling motion
        self.relative_pos.y += self.direction.y * self.speed
        self.relative_pos.x += self.direction.x * self.speed

        # Follow player's movement by updating position
        new_pos = pygame.math.Vector2(self.player.rect.center) + self.relative_pos
        self.rect.topleft = (round(new_pos.x), round(new_pos.y))

        # Kill if too far from player
        if abs(self.relative_pos.y) > 1000 or abs(self.relative_pos.x) > 1000:
            self.kill()
            gc.collect()  # Trigger garbage collection for optimization

class FloorDrop(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)
        self.sprite_type = 'floor_drop'
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        
        # Fade effect
        self.spawn_time = pygame.time.get_ticks()
        self.duration = 3000  # Total duration before disappearing
        self.alpha = 255

    def update(self):
        # Animation
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        
        # Fade out effect
        time_alive = pygame.time.get_ticks() - self.spawn_time
        if time_alive > self.duration - 1000:  # Start fading out in the last second
            self.alpha = max(0, int(255 * (self.duration - time_alive) / 1000))
            self.image.set_alpha(self.alpha)
        
        if time_alive > self.duration:
            self.kill()
            gc.collect()  # Trigger garbage collection for optimization

class LeafEffect(pygame.sprite.Sprite):
    def __init__(self, pos, groups, frames):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 0.05  # Slower animation speed
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.loop_completed = False  # Track if the first loop is completed

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.loop_completed = True  # Mark loop as completed
            self.kill()  # Delete the sprite after the first loop
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()

class RainEffect:
    def __init__(self, initial_position, groups):
        self.position = pygame.math.Vector2(initial_position)  # Use initial position as a starting point
        self.groups = groups
        self.rain_drops = import_folder(get_asset_path('graphics', 'environment', 'drops'))  # Load drop sprites
        self.floor_frames = import_folder(get_asset_path('graphics', 'environment', 'floor'))  # Load floor sprites
        self.spawn_interval = 60  # Reduced frequency of drops
        self.floor_spawn_interval = 300  # Adjusted for floor drops
        self.last_spawn_time = pygame.time.get_ticks()
        self.last_floor_spawn = pygame.time.get_ticks()

        # Load rain sound
        self.rain_sound = pygame.mixer.Sound(AUDIO_PATHS['rain']) 
        self.rain_sound.set_volume(1.0)  # Adjust volume
        self.player = None  # Initialize player as None
        self.obstacle_sprites = None  # Placeholder for obstacle sprites
        self.is_raining = False  # Flag to track if it's raining
        self.rain_start_time = None
        self.rain_duration = 80000  
        self.rain_interval = 80000  
        self.last_rain_check = pygame.time.get_ticks()
        self.leaf_frames = import_folder(get_asset_path('graphics', 'particles', 'leaf4'))  # Use only leaf4 frames
        self.leaf_effects = pygame.sprite.Group()
        self.leaf_spawn_interval = 5000  # Interval for spawning leaf effects
        self.last_leaf_spawn_time = pygame.time.get_ticks()

    def create_drops(self):
        screen = pygame.display.get_surface()
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Spawn drops across the entire visible area
        for _ in range(4):  # Reduced number of drops
            x = randint(int(self.position.x - screen_width // 2 - 100),  # Extend to the left
                        int(self.position.x + screen_width // 2))
            y = int(self.position.y - screen_height // 2 - 100)
            
            drop = RainDrop(
                surf=self.rain_drops[0],  # Use first frame
                pos=(x, y),
                groups=self.groups,
                player=self.player  # Pass player reference
            )
            drop.frames = self.rain_drops  # Pass all frames for animation

    def create_floor_drops(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_floor_spawn > self.floor_spawn_interval:
            screen = pygame.display.get_surface()
            screen_width = screen.get_width()
            screen_height = screen.get_height()
            
            # Create floor drops across the visible area
            for _ in range(2):  # Reduced number of floor drops
                x = randint(int(self.position.x - screen_width // 2), 
                           int(self.position.x + screen_width // 2))
                y = randint(int(self.position.y - screen_height // 2), 
                           int(self.position.y + screen_height // 2))
                drop_position = pygame.Rect(x, y, 1, 1)  # Create a small rect for collision check

                # Check if the position collides with any obstacle
                if self.obstacle_sprites and any(sprite.rect.colliderect(drop_position) for sprite in self.obstacle_sprites):
                    continue  # Skip this position if it collides with an obstacle

                FloorDrop(
                    pos=(x, y),
                    frames=self.floor_frames,
                    groups=self.groups
                )
            self.last_floor_spawn = current_time

    def create_leaf_effects(self):
        screen = pygame.display.get_surface()
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        for _ in range(4):  # Ensure at least 4 leaf effects
            x = randint(int(self.position.x - screen_width // 2), int(self.position.x + screen_width // 2))
            y = randint(int(self.position.y - screen_height // 2), int(self.position.y + screen_height // 2))
            LeafEffect((x, y), self.groups, self.leaf_frames)  # Pass player reference

    def update(self):
        current_time = pygame.time.get_ticks()

        # Check if it's time to start or stop the rain
        if not self.is_raining and current_time - self.last_rain_check >= self.rain_interval:
            self.last_rain_check = current_time
            if randint(1, 100) <= 50:  # 50% chance to start raining
                self.is_raining = True
                self.rain_start_time = current_time
                self.rain_sound.play(loops=-1)  # Start rain sound

        if self.is_raining and current_time - self.rain_start_time >= self.rain_duration:
            self.is_raining = False
            self.rain_sound.stop()  # Stop rain sound
            self.leaf_effects.empty()  # Kill all leaf effects when rain stops

        # Update rain drops and floor drops only if it's raining
        if self.is_raining:
            if self.player is not None:  # Ensure player is associated
                self.position = pygame.math.Vector2(self.player.rect.center)

            if current_time - self.last_spawn_time > self.spawn_interval:
                self.create_drops()
                self.create_floor_drops()
                self.last_spawn_time = current_time

            # Handle leaf effects
            if current_time - self.last_leaf_spawn_time >= self.leaf_spawn_interval:
                self.last_leaf_spawn_time = current_time
                self.create_leaf_effects()

        self.leaf_effects.update()
        gc.collect()  # Trigger garbage collection for optimization

    def stop_rain_sound(self):
        self.rain_sound.stop()

    def set_player(self, player):
        self.player = player
        self.position = pygame.math.Vector2(player.rect.center)

    def set_obstacle_sprites(self, obstacle_sprites):
        self.obstacle_sprites = obstacle_sprites

    def is_raining(self):
        return self.is_raining