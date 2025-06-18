import pygame
import sys
import time
import shutil  
import os
import random
import math
from settings import *  
from level import *
from PIL import Image, ImageSequence   # type: ignore
from debug import *
from support import check_os_and_limit_memory
from paths import get_asset_path
import gc  
from pygame._sdl2 import Window, Renderer, Texture
from dev_args import dev_mode
from verify_resources import ResourceVerifier

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

class Intro:
    def __init__(self, screen, renderer):
        self.screen = screen
        self.renderer = renderer
        self.font = pygame.font.Font(UI_FONT, 60)
        self.text = "RPG ELDORIA"
        self.version_text = "v2.1.0"
        self.audio_manager = AudioManager() 

    def fade_to_black(self, delay=10, alpha_step=8): 
        fade_surface = pygame.Surface((WIDTH, HEIGTH))
        fade_surface.fill((0, 0, 0)) 
        for alpha in range(0, 256, alpha_step): 
            fade_surface.set_alpha(alpha)
            self.screen.fill(WATER_COLOR)  
            self.screen.blit(fade_surface, (0, 0))
            
            # Update SDL2 window
            texture = Texture.from_surface(self.renderer, self.screen)
            self.renderer.clear()
            self.renderer.blit(texture)
            self.renderer.present()
            
            pygame.time.delay(delay)

    def fade_in(self, delay=10, alpha_step=8):
        fade_surface = pygame.Surface((WIDTH, HEIGTH))
        fade_surface.fill((0, 0, 0))  
        for alpha in range(255, -1, -alpha_step):  
            fade_surface.set_alpha(alpha)
            self.screen.fill(WATER_COLOR)
            self.screen.blit(fade_surface, (0, 0))
            
            # Update SDL2 window
            texture = Texture.from_surface(self.renderer, self.screen)
            self.renderer.clear()
            self.renderer.blit(texture)
            self.renderer.present()
            
            pygame.time.delay(delay)
            
    def type_text(self, text, color, center_x, center_y, delay=0.05): 
        displayed_text = ""
        for char in text:
            displayed_text += char
            rendered_text = self.font.render(displayed_text, True, color)
            text_rect = rendered_text.get_rect(center=(center_x, center_y))
            self.screen.fill(WATER_COLOR)  
            self.screen.blit(rendered_text, text_rect)
            
            # Update SDL2 window
            texture = Texture.from_surface(self.renderer, self.screen)
            self.renderer.clear()
            self.renderer.blit(texture)
            self.renderer.present()
            
            time.sleep(delay)  

    def display(self):
        pygame.mouse.set_visible(False)
        pygame.event.set_blocked(None)  
        
        try:
            pygame.event.clear()
            
            self.audio_manager.play_music(AUDIO_PATHS['intro'], loops=-1, volume=VOLUME_SETTINGS['music'])
            self.screen.fill((0, 0, 0))
            pygame.display.flip()
            time.sleep(0.5)

            self.fade_in()
            self.type_text(self.text, TEXT_COLOR, WIDTH // 2, HEIGTH // 2)
            time.sleep(1)
            self.fade_to_black()

            self.fade_in()
            self.type_text(self.version_text, TEXT_COLOR, WIDTH // 2, HEIGTH // 2)
            time.sleep(1)
            self.fade_to_black()

            time.sleep(0.5)
            self.audio_manager.stop_music()
            
        finally:
            pygame.event.set_allowed(None)
            pygame.event.clear()
            
            self.audio_manager.stop_music()
            self.font = None
            self.screen = None
            gc.collect()  

class MainMenu:
    shared_background_frames = None 

    def __init__(self, screen, renderer): 
        self.screen = screen
        self.renderer = renderer  # Store renderer
        self.font_title = pygame.font.Font(UI_FONT, 60)
        self.font_options = pygame.font.Font(UI_FONT, 40)
        self.title = "RPG ELDORIA"
        self.options = ["New Game", "Settings", "Quit Game"]
        self.selected_option = 0
        self.audio_manager = AudioManager()
        self.load_background_frames()
        self.animation_speed = 180 
        self.current_frame = 0
        self.last_frame_time = pygame.time.get_ticks()

        self.screen.blit(self.background_frames[self.current_frame], (0, 0))
        
        # Convert to texture and render with SDL2
        texture = Texture.from_surface(self.renderer, self.screen)
        self.renderer.clear()
        self.renderer.blit(texture)
        self.renderer.present()

        # Play menu music
        self.audio_manager.play_music(AUDIO_PATHS['main_menu'], loops=-1, volume=VOLUME_SETTINGS['music'])

    def load_background_frames(self):
        if MainMenu.shared_background_frames is None:
            gif_path = get_asset_path('graphics', 'background', 'background.gif')
            gif = Image.open(gif_path)
            frames = []

            for frame in ImageSequence.Iterator(gif):
                img = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode).convert_alpha()
                scaled_img = pygame.transform.scale(img, (WIDTH, HEIGTH))
                frames.append(scaled_img)

            frames = [frame for frame in frames if not self.is_white_frame(frame)]
            MainMenu.shared_background_frames = frames

        self.background_frames = MainMenu.shared_background_frames

    def is_white_frame(self, frame):
        avg_color = pygame.transform.average_color(frame)
        return avg_color == (255, 255, 255, 255)  

    def display(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time > self.animation_speed:  # Usar animation_speed aqui
            self.current_frame = (self.current_frame + 1) % len(self.background_frames)
            self.last_frame_time = current_time

        self.screen.blit(self.background_frames[self.current_frame], (0, 0))

        # Render title
        title_surface = self.font_title.render(self.title, True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGTH // 4))
        self.screen.blit(title_surface, title_rect)

        # Render menu options
        for i, option in enumerate(self.options):
            color = TEXT_COLOR if i != self.selected_option else "blue"
            option_surface = self.font_options.render(option, True, color)
            option_rect = option_surface.get_rect(center=(WIDTH // 2, HEIGTH // 2 + i * 50))
            self.screen.blit(option_surface, option_rect)

        # Convert to texture and render with SDL2
        texture = Texture.from_surface(self.renderer, self.screen)
        self.renderer.clear()
        self.renderer.blit(texture)
        self.renderer.present()

    def navigate(self, direction):
        self.selected_option = (self.selected_option + direction) % len(self.options)

    def select(self):
        if self.selected_option == 0:
            self.audio_manager.play_sound(AUDIO_PATHS['menu_select'], volume=VOLUME_SETTINGS['menu_effects'])
            return "new_game"
        elif self.selected_option == 1:
            self.audio_manager.play_sound(AUDIO_PATHS['menu_select'], volume=VOLUME_SETTINGS['menu_effects'])
            return "settings"
        elif self.selected_option == 2:
            self.audio_manager.play_sound(AUDIO_PATHS['menu_back'], volume=VOLUME_SETTINGS['menu_effects'])
            time.sleep(1)
            pygame.quit()
            sys.exit()

        return None

class Settings:
    def __init__(self):
        self.options = [
            {"name": "Fullscreen", "type": "toggle", "value": True}, 
            {"name": "Borderless", "type": "toggle", "value": False},
            {"name": "Resolution", "type": "choice", "choices": [(1280, 720), (1920, 1080), (800, 600), (1024, 768), (1280, 720), (1366, 768)], "value": 1},  
            {"name": "Game", "type": "choice", "choices": ["optimized", "normal", "ultra"], "value": 1}, 
            {"name": "Volume", "type": "slider", "min": 0, "max": 100, "value": 50},  
            {"name": "Gamma", "type": "slider", "min": 0, "max": 100, "value": 50},  
            {"name": "Back", "type": "action"}
        ]
        self.selected = 0

    def navigate(self, direction):
        self.selected = (self.selected + direction) % len(self.options)

    def toggle_option(self):
        option = self.options[self.selected]

        if option["type"] == "toggle":
            option["value"] = not option["value"]
            if option["name"] == "Fullscreen" and option["value"]:
                self.set_option("Borderless", False)

            elif option["name"] == "Borderless" and option["value"]:
                self.set_option("Fullscreen", False)

            return option["name"], option["value"]

        elif option["type"] == "choice":
            option["value"] = (option["value"] + 1) % len(option["choices"])
            return option["name"], option["choices"][option["value"]]

        elif option["type"] == "slider":
            return option["name"], option["value"]

        elif option["type"] == "action" and option["name"] == "Back":
            return "Back", None

        return None, None

    def set_option(self, name, value):
        for opt in self.options:
            if opt["name"] == name:
                opt["value"] = value
                break

    def adjust_gamma(self, direction):
        option = self.options[self.selected]
        if option["type"] == "slider":
            option["value"] = max(option["min"], min(option["max"], option["value"] + direction))
            return option["name"], option["value"]
        return None, None

class MainMenuSettings:
    def __init__(self, screen, settings):
        self.screen = screen
        self.font = pygame.font.Font(UI_FONT, 40)  
        self.settings = settings
        self.audio_manager = AudioManager()  

    def display(self):
        self.screen.fill(WATER_COLOR)
        for idx, option in enumerate(self.settings.options):
            color = TEXT_COLOR if idx == self.settings.selected else UI_BG_COLOR
            text = option["name"]
            
            if option["type"] == "toggle":
                text += f": {'On' if option['value'] else 'Off'}"
            elif option["type"] == "choice":
                current_res = option["choices"][option["value"]]
                text += f": {current_res[0]}x{current_res[1]}" if option["name"] == "Resolution" else f": {current_res}"
            elif option["type"] == "slider":
                text += f": {option['value']}"

            rendered_text = self.font.render(text, True, color)
            text_rect = rendered_text.get_rect(center=(WIDTH // 2, 200 + idx * 50))
            self.screen.blit(rendered_text, text_rect)

        # Display buttons
        enter_img = pygame.image.load(get_asset_path('graphics', 'environment', 'sprite_buttons_menu', 'ENTER.png')).convert_alpha()
        y_img = pygame.image.load(get_asset_path('graphics', 'environment', 'sprite_buttons_menu', 'Y.png')).convert_alpha()
        esc_img = pygame.image.load(get_asset_path('graphics', 'environment', 'sprite_buttons_menu', 'ESC.png')).convert_alpha()

        enter_img = pygame.transform.scale(enter_img, (20, 20))
        y_img = pygame.transform.scale(y_img, (20, 20))
        esc_img = pygame.transform.scale(esc_img, (20, 20))

        small_font = pygame.font.Font(UI_FONT, 20)
        enter_text = small_font.render("Toggle", True, BLACK_COLOR)
        y_text = small_font.render("Reset", True, BLACK_COLOR)
        esc_text = small_font.render("Back", True, BLACK_COLOR)

        self.screen.blit(enter_img, (WIDTH - 370, HEIGTH - 30))
        self.screen.blit(enter_text, (WIDTH - 340, HEIGTH - 30))
        self.screen.blit(y_img, (WIDTH - 230, HEIGTH - 30))
        self.screen.blit(y_text, (WIDTH - 200, HEIGTH - 30))
        self.screen.blit(esc_img, (WIDTH - 110, HEIGTH - 30))
        self.screen.blit(esc_text, (WIDTH - 80, HEIGTH - 30))

        pygame.display.flip()

    def navigate(self, direction):
        self.settings.navigate(direction)

    def toggle_option(self):
        option, value = self.settings.toggle_option()
        if option == "Volume":
            self.audio_manager.update_volume(value)
        if option:
            self.audio_manager.play_sound(AUDIO_PATHS['menu_select'], volume=VOLUME_SETTINGS['menu_effects'])
        return option, value

    def adjust_gamma(self, direction):
        option, value = self.settings.adjust_gamma(direction)
        if option == "Volume":
            self.audio_manager.update_volume(value)
        elif option == "Gamma":
            self.apply_gamma(value)
        if option:
            self.audio_manager.play_sound(AUDIO_PATHS['menu_select'], volume=VOLUME_SETTINGS['menu_effects'])
        return option, value

    def apply_gamma(self, value):
        gamma = value / 100.0
        pygame.display.set_gamma(gamma)

    def reset_settings(self):
        fullscreen_before_reset = self.settings.options[0]["value"]
        self.settings = Settings()
        self.settings.set_option("Fullscreen", fullscreen_before_reset)
        if fullscreen_before_reset:
            self.settings.set_option("Borderless", False)
            game.toggle_fullscreen(borderless=False)
        else:
            game.toggle_fullscreen(borderless=True)

class MainMenu:
    shared_background_frames = None 

    def __init__(self, screen, renderer):  # Add renderer parameter
        self.screen = screen
        self.renderer = renderer  # Store renderer
        self.font_title = pygame.font.Font(UI_FONT, 60)
        self.font_options = pygame.font.Font(UI_FONT, 40)
        self.title = "RPG ELDORIA"
        self.options = ["New Game", "Settings", "Quit Game"]
        self.selected_option = 0
        self.audio_manager = AudioManager()
        self.load_background_frames()
        self.animation_speed = 180  
        self.current_frame = 0
        self.last_frame_time = pygame.time.get_ticks()

        self.screen.blit(self.background_frames[self.current_frame], (0, 0))
        
        # Convert to texture and render with SDL2
        texture = Texture.from_surface(self.renderer, self.screen)
        self.renderer.clear()
        self.renderer.blit(texture)
        self.renderer.present()

        # Play menu music
        self.audio_manager.play_music(AUDIO_PATHS['main_menu'], loops=-1, volume=VOLUME_SETTINGS['music'])

    def load_background_frames(self):
        if MainMenu.shared_background_frames is None:
            gif_path = get_asset_path('graphics', 'background', 'background.gif')
            gif = Image.open(gif_path)
            frames = []

            for frame in ImageSequence.Iterator(gif):
                img = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode).convert_alpha()
                scaled_img = pygame.transform.scale(img, (WIDTH, HEIGTH))
                frames.append(scaled_img)

            frames = [frame for frame in frames if not self.is_white_frame(frame)]
            
            MainMenu.shared_background_frames = frames

        self.background_frames = MainMenu.shared_background_frames

    def is_white_frame(self, frame):
        avg_color = pygame.transform.average_color(frame)
        return avg_color == (255, 255, 255, 255)  

    def display(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time > self.animation_speed:  # Usar animation_speed aqui
            self.current_frame = (self.current_frame + 1) % len(self.background_frames)
            self.last_frame_time = current_time

        self.screen.blit(self.background_frames[self.current_frame], (0, 0))

        # Render title
        title_surface = self.font_title.render(self.title, True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGTH // 4))
        self.screen.blit(title_surface, title_rect)

        # Render menu options
        for i, option in enumerate(self.options):
            color = TEXT_COLOR if i != self.selected_option else "blue"
            option_surface = self.font_options.render(option, True, color)
            option_rect = option_surface.get_rect(center=(WIDTH // 2, HEIGTH // 2 + i * 50))
            self.screen.blit(option_surface, option_rect)

        # Convert to texture and render with SDL2
        texture = Texture.from_surface(self.renderer, self.screen)
        self.renderer.clear()
        self.renderer.blit(texture)
        self.renderer.present()

    def navigate(self, direction):
        self.selected_option = (self.selected_option + direction) % len(self.options)

    def select(self):
        if self.selected_option == 0:
            self.audio_manager.play_sound(AUDIO_PATHS['menu_select'], volume=VOLUME_SETTINGS['menu_effects'])
            return "new_game"
        elif self.selected_option == 1:
            self.audio_manager.play_sound(AUDIO_PATHS['menu_select'], volume=VOLUME_SETTINGS['menu_effects'])
            return "settings"
        elif self.selected_option == 2:
            self.audio_manager.play_sound(AUDIO_PATHS['menu_back'], volume=VOLUME_SETTINGS['menu_effects'])
            time.sleep(1)
            pygame.quit()
            sys.exit()

        return None

class Settings:
    def __init__(self):
        self.options = [
            {"name": "Fullscreen", "type": "toggle", "value": True}, 
            {"name": "Borderless", "type": "toggle", "value": False},
            {"name": "Resolution", "type": "choice", "choices": [(1280, 720), (1920, 1080), (800, 600), (1024, 768), (1280, 720), (1366, 768)], "value": 1},  
            {"name": "Game", "type": "choice", "choices": ["optimized", "normal", "ultra"], "value": 1}, 
            {"name": "Volume", "type": "slider", "min": 0, "max": 100, "value": 50},  
            {"name": "Gamma", "type": "slider", "min": 0, "max": 100, "value": 50},  
            {"name": "Back", "type": "action"}
        ]
        self.selected = 0

    def navigate(self, direction):
        self.selected = (self.selected + direction) % len(self.options)

    def toggle_option(self):
        option = self.options[self.selected]

        if option["type"] == "toggle":
            option["value"] = not option["value"]
            if option["name"] == "Fullscreen" and option["value"]:
                self.set_option("Borderless", False)

            elif option["name"] == "Borderless" and option["value"]:
                self.set_option("Fullscreen", False)

            return option["name"], option["value"]

        elif option["type"] == "choice":
            option["value"] = (option["value"] + 1) % len(option["choices"])
            return option["name"], option["choices"][option["value"]]

        elif option["type"] == "slider":
            return option["name"], option["value"]

        elif option["type"] == "action" and option["name"] == "Back":
            return "Back", None

        return None, None

    def set_option(self, name, value):
        for opt in self.options:
            if opt["name"] == name:
                opt["value"] = value
                break

    def adjust_gamma(self, direction):
        option = self.options[self.selected]
        if option["type"] == "slider":
            option["value"] = max(option["min"], min(option["max"], option["value"] + direction))
            return option["name"], option["value"]
        return None, None

class MainMenuSettings:
    def __init__(self, screen, settings):
        self.screen = screen
        self.font = pygame.font.Font(UI_FONT, 40)  
        self.settings = settings
        self.audio_manager = AudioManager()  

    def display(self):
        self.screen.fill(WATER_COLOR)
        for idx, option in enumerate(self.settings.options):
            color = TEXT_COLOR if idx == self.settings.selected else UI_BG_COLOR
            text = option["name"]
            
            if option["type"] == "toggle":
                text += f": {'On' if option['value'] else 'Off'}"
            elif option["type"] == "choice":
                current_res = option["choices"][option["value"]]
                text += f": {current_res[0]}x{current_res[1]}" if option["name"] == "Resolution" else f": {current_res}"
            elif option["type"] == "slider":
                text += f": {option['value']}"

            rendered_text = self.font.render(text, True, color)
            text_rect = rendered_text.get_rect(center=(WIDTH // 2, 200 + idx * 50))
            self.screen.blit(rendered_text, text_rect)

        # Display buttons
        enter_img = pygame.image.load(get_asset_path('graphics', 'environment', 'sprite_buttons_menu', 'ENTER.png')).convert_alpha()
        y_img = pygame.image.load(get_asset_path('graphics', 'environment', 'sprite_buttons_menu', 'Y.png')).convert_alpha()
        esc_img = pygame.image.load(get_asset_path('graphics', 'environment', 'sprite_buttons_menu', 'ESC.png')).convert_alpha()

        enter_img = pygame.transform.scale(enter_img, (20, 20))
        y_img = pygame.transform.scale(y_img, (20, 20))
        esc_img = pygame.transform.scale(esc_img, (20, 20))

        small_font = pygame.font.Font(UI_FONT, 20)
        enter_text = small_font.render("Toggle", True, BLACK_COLOR)
        y_text = small_font.render("Reset", True, BLACK_COLOR)
        esc_text = small_font.render("Back", True, BLACK_COLOR)

        self.screen.blit(enter_img, (WIDTH - 370, HEIGTH - 30))
        self.screen.blit(enter_text, (WIDTH - 340, HEIGTH - 30))
        self.screen.blit(y_img, (WIDTH - 230, HEIGTH - 30))
        self.screen.blit(y_text, (WIDTH - 200, HEIGTH - 30))
        self.screen.blit(esc_img, (WIDTH - 110, HEIGTH - 30))
        self.screen.blit(esc_text, (WIDTH - 80, HEIGTH - 30))

        pygame.display.flip()

    def navigate(self, direction):
        self.settings.navigate(direction)

    def toggle_option(self):
        option, value = self.settings.toggle_option()
        if option == "Volume":
            self.audio_manager.update_volume(value)
        if option:
            self.audio_manager.play_sound(AUDIO_PATHS['menu_select'], volume=VOLUME_SETTINGS['menu_effects'])
        return option, value

    def adjust_gamma(self, direction):
        option, value = self.settings.adjust_gamma(direction)
        if option == "Volume":
            self.audio_manager.update_volume(value)
        elif option == "Gamma":
            self.apply_gamma(value)
        if option:
            self.audio_manager.play_sound(AUDIO_PATHS['menu_select'], volume=VOLUME_SETTINGS['menu_effects'])
        return option, value

    def apply_gamma(self, value):
        gamma = value / 100.0
        pygame.display.set_gamma(gamma)

    def reset_settings(self):
        fullscreen_before_reset = self.settings.options[0]["value"]
        self.settings = Settings()
        self.settings.set_option("Fullscreen", fullscreen_before_reset)
        if fullscreen_before_reset:
            self.settings.set_option("Borderless", False)
            game.toggle_fullscreen(borderless=False)
        else:
            game.toggle_fullscreen(borderless=True)

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(UI_FONT, 40)
        self.options = ["Resume Game", "Settings", "Quit Game"]
        self.selected = 0
        self.menu_surface = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA) 
        self.menu_surface.fill((0, 0, 0, 150))  
        self.audio_manager = AudioManager() 

    def display(self):
        self.menu_surface = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)  
        self.menu_surface.fill((0, 0, 0, 150))  
        self.screen.blit(self.menu_surface, (0, 0))
        
        for idx, option in enumerate(self.options):
            color = TEXT_COLOR if idx == self.selected else UI_BG_COLOR
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, 200 + idx * 50))
            self.screen.blit(text, text_rect)
            
        pygame.display.flip()

    def navigate(self, direction):
        self.selected = (self.selected + direction) % len(self.options)

    def select(self):
        if self.selected == 0:  
            self.audio_manager.play_sound(AUDIO_PATHS['menu_select'], volume=VOLUME_SETTINGS['menu_effects'])
            return "resume"
        elif self.selected == 1:  
            self.audio_manager.play_sound(AUDIO_PATHS['menu_select'], volume=VOLUME_SETTINGS['menu_effects'])
            return "settings"
        elif self.selected == 2:  
            self.audio_manager.play_sound(AUDIO_PATHS['menu_back'], volume=VOLUME_SETTINGS['menu_effects'])
            time.sleep(0.5)
            return "quit"
        
class PauseMenuSettings:
    def __init__(self, screen, settings):
        self.screen = screen
        self.font = pygame.font.Font(UI_FONT, 40) 
        self.settings = settings
        self.audio_manager = AudioManager()  

    def display(self):
        self.screen.fill(WATER_COLOR)
        
        for idx, option in enumerate(self.settings.options):
            color = TEXT_COLOR if idx == self.settings.selected else UI_BG_COLOR
            text = option["name"]
            
            if option["type"] == "toggle":
                text += f": {'On' if option['value'] else 'Off'}"
            elif option["type"] == "choice":
                current_res = option["choices"][option["value"]]
                text += f": {current_res[0]}x{current_res[1]}" if option["name"] == "Resolution" else f": {current_res}"
            elif option["type"] == "slider":
                text += f": {option['value']}"

            rendered_text = self.font.render(text, True, color)
            text_rect = rendered_text.get_rect(center=(WIDTH // 2, 200 + idx * 50))
            self.screen.blit(rendered_text, text_rect)

        # Display buttons
        enter_img = pygame.image.load(get_asset_path('graphics', 'environment', 'sprite_buttons_menu', 'ENTER.png')).convert_alpha()
        y_img = pygame.image.load(get_asset_path('graphics', 'environment', 'sprite_buttons_menu', 'Y.png')).convert_alpha()
        esc_img = pygame.image.load(get_asset_path('graphics', 'environment', 'sprite_buttons_menu', 'ESC.png')).convert_alpha()

        enter_img = pygame.transform.scale(enter_img, (20, 20))
        y_img = pygame.transform.scale(y_img, (20, 20))
        esc_img = pygame.transform.scale(esc_img, (20, 20))

        small_font = pygame.font.Font(UI_FONT, 20)
        enter_text = small_font.render("Toggle", True, BLACK_COLOR)
        y_text = small_font.render("Reset", True, BLACK_COLOR)
        esc_text = small_font.render("Back", True, BLACK_COLOR)

        self.screen.blit(enter_img, (WIDTH - 370, HEIGTH - 30))
        self.screen.blit(enter_text, (WIDTH - 340, HEIGTH - 30))
        self.screen.blit(y_img, (WIDTH - 230, HEIGTH - 30))
        self.screen.blit(y_text, (WIDTH - 200, HEIGTH - 30))
        self.screen.blit(esc_img, (WIDTH - 110, HEIGTH - 30))
        self.screen.blit(esc_text, (WIDTH - 80, HEIGTH - 30))

        pygame.display.flip()

    def navigate(self, direction):
        self.settings.navigate(direction)

    def toggle_option(self):
        option, value = self.settings.toggle_option()
        if option == "Volume":
            self.audio_manager.update_volume(value)
        if option:
            self.audio_manager.play_sound(AUDIO_PATHS['menu_select'], volume=VOLUME_SETTINGS['menu_effects'])
        return option, value

    def adjust_gamma(self, direction):
        option, value = self.settings.adjust_gamma(direction)
        if option == "Volume":
            self.audio_manager.update_volume(value)
        elif option == "Gamma":
            self.apply_gamma(value)
        if option:
            self.audio_manager.play_sound(AUDIO_PATHS['menu_select'], volume=VOLUME_SETTINGS['menu_effects'])
        return option, value

    def apply_gamma(self, value):
        gamma = value / 100.0
        pygame.display.set_gamma(gamma)

    def reset_settings(self):
        fullscreen_before_reset = self.settings.options[0]["value"]
        self.settings = Settings()
        self.settings.set_option("Fullscreen", fullscreen_before_reset)
        if fullscreen_before_reset:
            self.settings.set_option("Borderless", False)
            game.toggle_fullscreen(borderless=False)
        else:
            game.toggle_fullscreen(borderless=True)

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.update_volume(50)  

    def update_volume(self, value):
        volume = value / 100
        pygame.mixer.music.set_volume(volume)
        VOLUME_SETTINGS['music'] = volume
        VOLUME_SETTINGS['menu_effects'] = volume * 5  
        VOLUME_SETTINGS['enemy_effects'] = volume

    def play_music(self, filename, loops=0, volume=None):
        try:
            pygame.mixer.music.load(filename)
            final_volume = volume if volume is not None else VOLUME_SETTINGS['music']
            pygame.mixer.music.set_volume(final_volume)
            pygame.mixer.music.play(loops)
        except pygame.error:
            pass

    def play_sound(self, filename, volume=None):
        try:
            sound = pygame.mixer.Sound(filename)
            final_volume = volume if volume is not None else VOLUME_SETTINGS['menu_effects']
            sound.set_volume(final_volume)
            sound.play()
        except pygame.error:
            pass

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_music_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

class LoadingWindow:
    def __init__(self):
        self.width = 600
        self.height = 200
        
        screen_info = pygame.display.Info()
        user_width = screen_info.current_w
        user_height = screen_info.current_h
        
        window_x = (user_width - self.width) // 2
        window_y = (user_height - self.height) // 2
        
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{window_x},{window_y}"
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME | pygame.SHOWN)
        pygame.display.set_caption('Loading RPG Eldoria')
        
        icon_path = get_asset_path('graphics', 'icon', 'game.ico')
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
        
        self.font = pygame.font.Font(UI_FONT, 20)
        self.progress = 0
        self.resource_progress = None  # (current, total)
        self.resource_message = None

    def update(self, progress, message="loading...", resource_progress=None, resource_message=None):
        self.screen.fill((0, 0, 0))
        
        border_thickness = 3
        border_color = (255, 255, 255)
        pygame.draw.rect(self.screen, border_color, 
                        (0, 0, self.width, self.height), border_thickness)
        icon = pygame.image.load(get_asset_path('graphics', 'icon', 'game.ico'))
        icon = pygame.transform.scale(icon, (48, 48))
        icon_rect = icon.get_rect(midtop=(self.width // 2, 20))
        self.screen.blit(icon, icon_rect)
        text = self.font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.width // 2, 100))
        self.screen.blit(text, text_rect)

        if resource_progress is not None and resource_message:
            res_text = self.font.render(
                f"{resource_message}: {resource_progress[0]}/{resource_progress[1]}", True, (200, 220, 255)
            )
            res_rect = res_text.get_rect(center=(self.width // 2, 130))
            self.screen.blit(res_text, res_rect)

        bar_width = 400
        bar_height = 25
        bar_x = (self.width - bar_width) // 2
        bar_y = 140
        
        pygame.draw.rect(self.screen, border_color,
                        (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4), 2)
        fill_width = int(bar_width * (progress / 100))
        pygame.draw.rect(self.screen, border_color,
                        (bar_x, bar_y, fill_width, bar_height))
        
        pygame.display.flip()
        
        if progress >= 100:
            pygame.time.wait(500) 
            self.cleanup()
            
    def cleanup(self):
        """Properly cleanup the loading window"""
        pygame.display.quit()  # Close the current display
        pygame.display.init()  # Reinitialize the display
        self.screen = None     # Remove reference to screen
        pygame.event.clear()   # Clear any pending events

class Game:
    def __init__(self):
        pygame.init()
        
        # Get screen info for centering
        screen_info = pygame.display.Info()
        window_x = (screen_info.current_w - WIDTH) // 2
        window_y = (screen_info.current_h - HEIGTH) // 2
        
        # Carregar ícone
        icon_path = get_asset_path('graphics', 'icon', 'game.ico')
        icon = pygame.image.load(icon_path)
        
        # Inicializar loading window com simulação de carregamento
        loading = LoadingWindow()
        
        loading.update(5, "Verificando recursos do jogo...", resource_progress=(0, 0), resource_message="Carregando recursos")
        pygame.time.wait(300)

        def loading_callback(verified, total):
            loading.update(5, "Verificando recursos do jogo...", resource_progress=(verified, total), resource_message="Carregando recursos")
        verifier = ResourceVerifier()
        verifier.verify_all(loading_callback=loading_callback)
        loading.update(15, "Recursos verificados com sucesso!", resource_progress=(1, 1), resource_message="Carregando recursos")
        pygame.time.wait(300)

        for i in range(20, 101, 5):  
            loading_message = "Starting..." if i < 30 else "Loading assets..." if i < 60 else "Preparing game..."
            loading.update(i, loading_message)
            pygame.time.wait(200)  # 200ms * 20 steps = 4 s
        
        self.window = Window(title='RPG Eldoria', size=(WIDTH, HEIGTH))
        self.window.position = (window_x, window_y)
        self.renderer = Renderer(self.window, accelerated=1, vsync=True)
        self.window.set_icon(icon)
        self.window.set_fullscreen(True)  
        
        pygame.display.set_mode((1, 1), flags=pygame.HIDDEN)
        pygame.mouse.set_visible(False)
        
        self.texture = None
        self.screen = pygame.Surface((WIDTH, HEIGTH))
        self.fullscreen = True
        
        # Initialize clock
        self.clock = pygame.time.Clock()
        
        # Game states
        self.in_menu = True
        self.in_settings = False
        self.in_pause = False
        self.in_pause_settings = False
        self.in_gameplay = False
        self.in_upgrade = False

        # Inicialize intro_played 
        self.intro_played = False
        
        # Initialize settings and game components
        self.settings = Settings()
        self.level = None
        self.game_settings = {
            0: {"tilesize": 10,
                "chunksize": 10, 
                "visible_chunks": 1, 
                "wind_interval": 30000, "wind_duration": 5000,
                "max_wind": 1},
            
            1: {"tilesize": 25,
                "chunksize": 25,
                "visible_chunks": 5,
                "wind_interval": 20000, "wind_duration": 5000,
                "max_wind": 3},
            
            2: {"tilesize": 30,
                "chunksize": 30,
                "visible_chunks": 10,
                "wind_interval": 10000, "wind_duration": 5000,
                "max_wind": 5},
        }
        
        # Initialize menu objects
        self.main_menu = MainMenu(self.screen, self.renderer)  # Pass renderer
        self.main_menu_settings = MainMenuSettings(self.screen, self.settings)
        self.pause_menu = PauseMenu(self.screen)
        self.pause_menu_settings = PauseMenuSettings(self.screen, self.settings)
        
        self.audio_manager = AudioManager()


        if dev_mode:
            # Pula intro e menu, vai direto para o jogo
            self.intro_played = True
            self.in_menu = False
            self.in_settings = False
            self.in_pause = False
            self.in_pause_settings = False
            self.in_gameplay = True
            self.start_new_game()
        else:
            if not self.intro_played:
                intro = Intro(self.screen, self.renderer)
                intro.display()
                self.intro_played = True
                # Start menu music after intro
                self.audio_manager.play_music(AUDIO_PATHS['main_menu'], loops=-1, volume=VOLUME_SETTINGS['music'])

    def apply_game_settings(self):
        if self.level is None:
            return
        
        game_mode = self.settings.options[3]["value"]
        if game_mode in self.game_settings:
            self._apply_level_settings(self.game_settings[game_mode])

    def start_new_game(self):
        try:
            if self.level:
                self.level.cleanup()
                self.level = None
                gc.collect()
            
            # Create mystical loading background with particles
            loading_bg = pygame.Surface((WIDTH, HEIGTH))
            particles = [(random.randint(0, WIDTH), random.randint(0, HEIGTH), random.random()) 
                        for _ in range(50)]
            
            # Load and scale game icon with glow effect
            icon = pygame.image.load(get_asset_path('graphics', 'icon', 'game.ico'))
            icon = pygame.transform.scale(icon, (96, 96))  # Smaller icon
            icon_rect = icon.get_rect(center=(WIDTH // 2, HEIGTH // 2 - 30))
            
            # Loading bar parameters - stone texture style
            bar_width = 300
            bar_height = 15
            border_width = 3
            bar_rect = pygame.Rect((WIDTH - bar_width) // 2, HEIGTH // 2 + 80, bar_width, bar_height)
            
            # Font setup
            font = pygame.font.Font(UI_FONT, 16)
            loading_text = font.render("Loading...", True, (180, 180, 200))
            text_rect = loading_text.get_rect(center=(WIDTH // 2, bar_rect.bottom + 25))
            
            # Tip text
            tip_font = pygame.font.Font(UI_FONT, 14)
            tip_text = tip_font.render(" Tip: NPCs with glowing eyes guard valuable secrets.", True, (150, 150, 170))
            tip_rect = tip_text.get_rect(center=(WIDTH // 2, HEIGTH - 30))

            # Initialize configuration before the loading loop
            game_mode = self.settings.options[3]["value"]
            config = self.game_settings[game_mode]
            global TILESIZE, CHUNKSIZE, VISIBLE_CHUNKS
            TILESIZE = config["tilesize"]
            CHUNKSIZE = config["chunksize"]
            VISIBLE_CHUNKS = config["visible_chunks"]
            
            loading_steps = {
                25: "Initializing game state...",
                50: "Loading resources...",
                75: "Creating game world..."
            }

            # Loading animation
            for progress in range(101):
                # Dark purple background with fog effect
                loading_bg.fill((20, 10, 30))
                
                # Update and draw particles
                for i, (x, y, speed) in enumerate(particles):
                    # Move particles up slowly
                    y = (y - speed) % HEIGTH
                    particles[i] = (x, y, speed)
                    
                    # Draw particle with fade effect
                    alpha = int(255 * (0.5 + math.sin(y / 30) * 0.5))
                    particle_color = (100, 80, 120, alpha)
                    pygame.draw.circle(loading_bg, particle_color, (int(x), int(y)), 1)
                
                # Draw icon with pulsing glow
                glow = math.sin(pygame.time.get_ticks() * 0.003) * 0.3 + 0.7
                glow_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (80, 60, 100, 50), (50, 50), 48 * glow)
                loading_bg.blit(glow_surf, (icon_rect.centerx - 50, icon_rect.centery - 50))
                loading_bg.blit(icon, icon_rect)
                
                # Draw stone-textured loading bar
                border_color = (100, 90, 120)
                fill_color = (80, 60, 100)
                glow_color = (140, 100, 180, 50)
                
                # Bar border with texture
                pygame.draw.rect(loading_bg, border_color, 
                               bar_rect.inflate(border_width * 2, border_width * 2), border_width)
                
                # Progress fill with magical glow
                fill_width = int((bar_width - border_width * 2) * (progress / 100))
                if fill_width > 0:
                    # Glow effect
                    glow_rect = pygame.Rect(bar_rect.left + border_width, 
                                          bar_rect.top + border_width,
                                          fill_width,
                                          bar_height - border_width * 2)
                    pygame.draw.rect(loading_bg, glow_color, glow_rect.inflate(4, 4))
                    pygame.draw.rect(loading_bg, fill_color, glow_rect)
                
                # Draw texts
                loading_bg.blit(loading_text, text_rect)
                loading_bg.blit(tip_text, tip_rect)
                
                # Convert to texture and render
                self.renderer.clear()
                texture = Texture.from_surface(self.renderer, loading_bg)
                self.renderer.blit(texture)
                self.renderer.present()
                
                # Handle loading steps at specific progress points
                if progress in loading_steps:
                    try:
                        if progress == 25:
                            # Reset game states
                            self.in_menu = False
                            self.in_settings = False
                            self.in_pause = False
                            self.in_pause_settings = False
                            self.in_upgrade = False
                            pygame.event.clear()
                            
                        elif progress == 50:
                            # Load resources and prepare level initialization
                            pygame.display.flip()
                            pygame.time.wait(100)  
                            
                        elif progress == 75:
                            # Create level instance
                            self.level = Level()
                            if not self.level:
                                raise Exception("Failed to create Level instance")
                            
                            # Configure level
                            self.level.game_active = True
                            self.level.paused = False
                            self.level.wind_effect_interval = config["wind_interval"]
                            self.level.wind_effect_duration = config["wind_duration"]
                            self.level.max_wind_effects = config["max_wind"]
                            self.level.update_wind_effects_settings()
                            
                            # Update game state
                            self.in_gameplay = True
                            
                            # Start game music
                            self.audio_manager.stop_music()
                            self.audio_manager.play_music(AUDIO_PATHS['main_game'], loops=-1, volume=VOLUME_SETTINGS['music'])
                            
                    except Exception as e:
                        print(f"Error during loading step {progress}: {e}")
                        raise
                
                # Update loading screen
                pygame.time.wait(20)  
                
            if not self.level:
                raise Exception("Level initialization failed")
                
            return True
            
        except Exception as e:
            print(f"Critical error starting new game: {e}")
            self.in_menu = True
            self.in_gameplay = False
            if self.level:
                self.level.cleanup()
                self.level = None
            gc.collect()

    def _apply_level_settings(self, config):
        if self.level is None:
            return
            
        self.level.clear_wind_effects()
        
        global TILESIZE, CHUNKSIZE, VISIBLE_CHUNKS
        TILESIZE = config["tilesize"]
        CHUNKSIZE = config["chunksize"]
        VISIBLE_CHUNKS = config["visible_chunks"]
        
        self.level.wind_effect_interval = config["wind_interval"]
        self.level.wind_effect_duration = config["wind_duration"]
        self.level.max_wind_effects = config["max_wind"]
        self.level.update_wind_effects_settings()
        
    def run(self):
        try:
            key_hold_time = 0
            pygame.mouse.set_visible(False)
            
            if not self.intro_played:
                intro = Intro(self.screen, self.renderer)
                intro.display()
                self.intro_played = True

            
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if self.in_menu:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                self.main_menu.navigate(-1)
                            elif event.key == pygame.K_DOWN:
                                self.main_menu.navigate(1)
                            elif event.key == pygame.K_RETURN:
                                action = self.main_menu.select()
                                if action == "new_game":
                                    self.audio_manager.stop_music()  # Stop menu music before starting game
                                    if not self.start_new_game():
                                        print("Failed to start new game - returning to menu")
                                        self.in_menu = True
                                        
                                        # Restart menu music if game failed to start
                                        self.audio_manager.play_music(AUDIO_PATHS['main_menu'], loops=-1, volume=VOLUME_SETTINGS['music'])
                                        continue
                                elif action == "settings":
                                    self.in_menu = False
                                    self.in_settings = True
                                elif action == "quit":
                                    pygame.quit()
                                    sys.exit()
                                    del CHUNKS_FOLDER
                            elif event.key == pygame.K_ESCAPE:
                                pygame.quit()
                                sys.exit()

                    elif self.in_pause:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                self.pause_menu.navigate(-1)
                            elif event.key == pygame.K_DOWN:
                                self.pause_menu.navigate(1)
                            elif event.key == pygame.K_RETURN:
                                action = self.pause_menu.select()
                                if action == "resume":
                                    self.in_pause = False
                                    self.level.paused = False
                                    self.audio_manager.stop_music()
                                    self.audio_manager.play_music(AUDIO_PATHS['main_game'], loops=-1, volume=VOLUME_SETTINGS['music'])
                                elif action == "settings":
                                    self.in_pause = False
                                    self.in_pause_settings = True
                                elif action == "quit":
                                    pygame.quit()
                                    sys.exit()
                                    del CHUNKS_FOLDER
                            elif event.key == pygame.K_ESCAPE:
                                self.in_pause = False
                                self.level.paused = False
                                self.audio_manager.stop_music()
                                self.audio_manager.play_music(AUDIO_PATHS['main_game'], loops=-1, volume=VOLUME_SETTINGS['music'])

                    elif self.in_settings:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                self.main_menu_settings.navigate(-1)
                            elif event.key == pygame.K_DOWN:
                                self.main_menu_settings.navigate(1)
                            elif event.key == pygame.K_LEFT:
                                self.main_menu_settings.adjust_gamma(-1)
                                key_hold_time = pygame.time.get_ticks()
                            elif event.key == pygame.K_RIGHT:
                                self.main_menu_settings.adjust_gamma(1)
                                key_hold_time = pygame.time.get_ticks()
                            elif event.key == pygame.K_RETURN:
                                option, value = self.main_menu_settings.toggle_option()
                                if option == "Fullscreen":
                                    self.toggle_fullscreen(borderless=False)
                                elif option == "Borderless":
                                    self.toggle_fullscreen(borderless=True)
                                elif option == "Resolution":
                                    self.apply_resolution(value)
                                    self.settings.set_option("Fullscreen", False) 
                                elif option == "Back":
                                    self.in_settings = False
                                    self.in_menu = True
                            elif event.key == pygame.K_y:
                                fullscreen_before_reset = self.settings.options[0]["value"]
                                self.main_menu_settings.reset_settings()  
                                self.pause_menu_settings.reset_settings()  
                                self.settings.set_option("Fullscreen", fullscreen_before_reset)
                            elif event.key == pygame.K_ESCAPE:
                                self.in_settings = False
                                self.in_menu = True
                        elif event.type == pygame.KEYUP:
                            key_hold_time = 0

                    elif self.in_pause_settings:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                self.pause_menu_settings.navigate(-1)
                            elif event.key == pygame.K_DOWN:
                                self.pause_menu_settings.navigate(1)
                            elif event.key == pygame.K_LEFT:
                                self.pause_menu_settings.adjust_gamma(-1)
                                key_hold_time = pygame.time.get_ticks()
                            elif event.key == pygame.K_RIGHT:
                                self.pause_menu_settings.adjust_gamma(1)
                                key_hold_time = pygame.time.get_ticks()
                            elif event.key == pygame.K_RETURN:
                                option, value = self.pause_menu_settings.toggle_option()
                                if option == "Fullscreen":
                                    self.toggle_fullscreen(borderless=False)
                                elif option == "Borderless":
                                    self.toggle_fullscreen(borderless=True)
                                elif option == "Resolution":
                                    self.apply_resolution(value)
                                    self.settings.set_option("Fullscreen", False) 
                                elif option == "Back":
                                    self.in_pause_settings = False
                                    self.in_pause = True
                            elif event.key == pygame.K_y:
                                fullscreen_before_reset = self.settings.options[0]["value"]
                                self.main_menu_settings.reset_settings()  #
                                self.pause_menu_settings.reset_settings()  
                                self.settings.set_option("Fullscreen", fullscreen_before_reset)
                            elif event.key == pygame.K_ESCAPE:
                                self.in_pause_settings = False
                                self.in_pause = True

                    elif self.in_gameplay:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                self.in_pause = True
                                self.level.paused = True
                                self.audio_manager.stop_music()
                                self.audio_manager.play_music(AUDIO_PATHS['pause_menu'], loops=-1, volume=VOLUME_SETTINGS['music'])
                            elif event.key == pygame.K_f:
                                self.toggle_fullscreen()
                            elif event.key == pygame.K_u:
                                self.in_upgrade = True
                                self.level.toggle_menu()

                        if event.type == pygame.VIDEORESIZE:
                            global WIDTH, HEIGTH
                            WIDTH, HEIGTH = event.size
                            self.screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.RESIZABLE)
                            ground_path = get_asset_path('graphics', 'tilemap', 'ground.png')
                            self.level.floor_surf = pygame.transform.scale(pygame.image.load(ground_path).convert(), (WIDTH, HEIGTH))  # Scale the background image

                    elif self.in_upgrade:
                        if event.type == pygame.KEYDOWN and (event.key == pygame.K_u or event.key == pygame.K_ESCAPE):
                            self.in_upgrade = False
                            self.level.toggle_menu()

                    # Restart menu music when returning to menu from settings
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if self.in_settings:
                                self.in_settings = False
                                self.in_menu = True
                                self.audio_manager.play_music(AUDIO_PATHS['main_menu'], loops=-1, volume=VOLUME_SETTINGS['music'])

                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    if pygame.time.get_ticks() - key_hold_time > 100:
                        self.main_menu_settings.adjust_gamma(-1)
                        key_hold_time = pygame.time.get_ticks()
                elif keys[pygame.K_RIGHT]:
                    if pygame.time.get_ticks() - key_hold_time > 100:
                        self.main_menu_settings.adjust_gamma(1)
                        key_hold_time = pygame.time.get_ticks()

                # Clear the screen surface
                self.screen.fill(WATER_COLOR)

                # Regular game rendering to self.screen
                if self.in_menu:
                    self.main_menu.display()
                elif self.in_pause:
                    if self.last_game_surface is not None:
                        self.screen.blit(self.last_game_surface, (0, 0))
                    self.pause_menu.display()
                elif self.in_settings:
                    self.main_menu_settings.display()
                elif self.in_pause_settings:
                    self.pause_menu_settings.display()
                elif self.in_gameplay:
                    try:
                        game_surface = self.level.run()
                        self.screen.blit(game_surface, (0, 0))
                        self.last_game_surface = game_surface.copy()
                    except Exception as e:
                        print(f"Erro durante renderização do jogo: {e}")
                        self.in_menu = True
                        self.in_gameplay = False
                        if self.level:
                            self.level.cleanup()
                            self.level = None
                        gc.collect()
                elif self.in_upgrade:
                    try:
                        game_surface = self.level.run(game_state='upgrade')
                        self.screen.blit(game_surface, (0, 0))
                        self.last_game_surface = game_surface.copy()
                    except Exception as e:
                        print(f"Erro durante renderização do upgrade: {e}")
                        self.in_menu = True
                        self.in_upgrade = False
                        if self.level:
                            self.level.cleanup()
                            self.level = None
                        gc.collect()
                
                # Convert pygame surface to SDL2 texture and render
                self.renderer.clear()
                texture = Texture.from_surface(self.renderer, self.screen)
                self.renderer.blit(texture)
                self.renderer.present()

                self.clock.tick(FPS)

        finally:
            self.cleanup()

    def cleanup(self):
        if os.path.exists(CHUNKS_FOLDER):
            shutil.rmtree(CHUNKS_FOLDER)
        
        # Properly clean up SDL2 resources
        if hasattr(self, 'window'):
            self.renderer = None  # Release renderer reference
            self.window = None    # Release window reference
        
        self.main_menu = None
        self.level = None
        self.screen = None
        pygame.mixer.quit()
        pygame.quit()
        gc.collect()

    def toggle_fullscreen(self, borderless=False):
        if borderless:
            self.window.set_windowed()
            self.window.resizable = True
            self.window.borderless = True
            self.fullscreen = False
        else:
            if self.fullscreen:
                self.window.set_windowed()
                self.window.resizable = True
                self.window.borderless = False
                self.fullscreen = False
            else:
                self.window.set_fullscreen(True)
                self.fullscreen = True

        # Only update level floor_surf if level exists
        if self.level is not None:
            self.level.floor_surf = pygame.transform.scale(
                pygame.image.load(get_asset_path('graphics', 'tilemap', 'ground.png')).convert(), 
                (WIDTH, HEIGTH)
            )
            self.level.visible_sprites.offset = pygame.math.Vector2(0, 0)

    def apply_resolution(self, resolution):
        global WIDTH, HEIGTH
        WIDTH, HEIGTH = resolution
        
        # Update window size
        self.window.size = (WIDTH, HEIGTH)
        self.screen = pygame.Surface((WIDTH, HEIGTH))
        
        self.level.floor_surf = pygame.transform.scale(
            pygame.image.load(get_asset_path('graphics', 'tilemap', 'ground.png')).convert(), 
            (WIDTH, HEIGTH)
        )
        
    def start_new_game(self):
        try:
            if self.level:
                self.level.cleanup()
                self.level = None
                gc.collect()
            
            # Create mystical loading background with particles
            loading_bg = pygame.Surface((WIDTH, HEIGTH))
            particles = [(random.randint(0, WIDTH), random.randint(0, HEIGTH), random.random()) 
                        for _ in range(50)]
            
            # Load and scale game icon with glow effect
            icon = pygame.image.load(get_asset_path('graphics', 'icon', 'game.ico'))
            icon = pygame.transform.scale(icon, (96, 96))  # Smaller icon
            icon_rect = icon.get_rect(center=(WIDTH // 2, HEIGTH // 2 - 30))
            
            # Loading bar parameters - stone texture style
            bar_width = 300
            bar_height = 15
            border_width = 3
            bar_rect = pygame.Rect((WIDTH - bar_width) // 2, HEIGTH // 2 + 80, bar_width, bar_height)
            
            # Font setup
            font = pygame.font.Font(UI_FONT, 16)
            loading_text = font.render("Loading...", True, (180, 180, 200))
            text_rect = loading_text.get_rect(center=(WIDTH // 2, bar_rect.bottom + 25))
            
            # Tip text
            tip_font = pygame.font.Font(UI_FONT, 14)
            tip_text = tip_font.render(" Tip: NPCs with glowing eyes guard valuable secrets.", True, (150, 150, 170))
            tip_rect = tip_text.get_rect(center=(WIDTH // 2, HEIGTH - 30))

            # Initialize configuration before the loading loop
            game_mode = self.settings.options[3]["value"]
            config = self.game_settings[game_mode]
            global TILESIZE, CHUNKSIZE, VISIBLE_CHUNKS
            TILESIZE = config["tilesize"]
            CHUNKSIZE = config["chunksize"]
            VISIBLE_CHUNKS = config["visible_chunks"]
            
            loading_steps = {
                25: "Initializing game state...",
                50: "Loading resources...",
                75: "Creating game world..."
            }

            # Loading animation
            for progress in range(101):
                # Dark purple background with fog effect
                loading_bg.fill((20, 10, 30))
                
                # Update and draw particles
                for i, (x, y, speed) in enumerate(particles):
                    # Move particles up slowly
                    y = (y - speed) % HEIGTH
                    particles[i] = (x, y, speed)
                    
                    # Draw particle with fade effect
                    alpha = int(255 * (0.5 + math.sin(y / 30) * 0.5))
                    particle_color = (100, 80, 120, alpha)
                    pygame.draw.circle(loading_bg, particle_color, (int(x), int(y)), 1)
                
                # Draw icon with pulsing glow
                glow = math.sin(pygame.time.get_ticks() * 0.003) * 0.3 + 0.7
                glow_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (80, 60, 100, 50), (50, 50), 48 * glow)
                loading_bg.blit(glow_surf, (icon_rect.centerx - 50, icon_rect.centery - 50))
                loading_bg.blit(icon, icon_rect)
                
                # Draw stone-textured loading bar
                border_color = (100, 90, 120)
                fill_color = (80, 60, 100)
                glow_color = (140, 100, 180, 50)
                
                # Bar border with texture
                pygame.draw.rect(loading_bg, border_color, 
                               bar_rect.inflate(border_width * 2, border_width * 2), border_width)
                
                # Progress fill with magical glow
                fill_width = int((bar_width - border_width * 2) * (progress / 100))
                if fill_width > 0:
                    # Glow effect
                    glow_rect = pygame.Rect(bar_rect.left + border_width, 
                                          bar_rect.top + border_width,
                                          fill_width,
                                          bar_height - border_width * 2)
                    pygame.draw.rect(loading_bg, glow_color, glow_rect.inflate(4, 4))
                    pygame.draw.rect(loading_bg, fill_color, glow_rect)
                
                # Draw texts
                loading_bg.blit(loading_text, text_rect)
                loading_bg.blit(tip_text, tip_rect)
                
                # Convert to texture and render
                self.renderer.clear()
                texture = Texture.from_surface(self.renderer, loading_bg)
                self.renderer.blit(texture)
                self.renderer.present()
                
                # Handle loading steps at specific progress points
                if progress in loading_steps:
                    try:
                        if progress == 25:
                            # Reset game states
                            self.in_menu = False
                            self.in_settings = False
                            self.in_pause = False
                            self.in_pause_settings = False
                            self.in_upgrade = False
                            pygame.event.clear()
                            
                        elif progress == 50:
                            # Load resources and prepare level initialization
                            pygame.display.flip()
                            pygame.time.wait(100)  
                            
                        elif progress == 75:
                            # Create level instance
                            self.level = Level()
                            if not self.level:
                                raise Exception("Failed to create Level instance")
                            
                            # Configure level
                            self.level.game_active = True
                            self.level.paused = False
                            self.level.wind_effect_interval = config["wind_interval"]
                            self.level.wind_effect_duration = config["wind_duration"]
                            self.level.max_wind_effects = config["max_wind"]
                            self.level.update_wind_effects_settings()
                            
                            # Update game state
                            self.in_gameplay = True
                            
                            # Start game music
                            self.audio_manager.stop_music()
                            self.audio_manager.play_music(AUDIO_PATHS['main_game'], loops=-1, volume=VOLUME_SETTINGS['music'])
                            
                    except Exception as e:
                        print(f"Error during loading step {progress}: {e}")
                        raise
                
                # Update loading screen
                pygame.time.wait(20)  
                
            if not self.level:
                raise Exception("Level initialization failed")
                
            return True
            
        except Exception as e:
            print(f"Critical error starting new game: {e}")
            self.in_menu = True
            self.in_gameplay = False
            if self.level:
                self.level.cleanup()
                self.level = None
            gc.collect()

if __name__ == '__main__':
    check_os_and_limit_memory(356)  
    game = Game()
    game.run()