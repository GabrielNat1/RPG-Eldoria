import pygame
import sys
import time
from settings import *
from level import Level


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(UI_FONT, 40)
        self.options = ["Resume Game", "Settings", "Quit Game"]
        self.selected = 0

    def display(self):
        self.screen.fill(WATER_COLOR)
        for idx, option in enumerate(self.options):
            color = TEXT_COLOR if idx == self.selected else UI_BG_COLOR
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, 200 + idx * 50))
            self.screen.blit(text, text_rect)
        pygame.display.flip()

    def navigate(self, direction):
        self.selected = (self.selected + direction) % len(self.options)

    def select(self):
        if self.selected == 0:  # Resume Game
            return "resume"
        elif self.selected == 1:  # Settings
            return "settings"
        elif self.selected == 2:  # Quit Game
            return "quit"


class SettingsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(UI_FONT, 40)
        self.options = [
            {"name": "Fullscreen", "type": "toggle", "value": False},
            {"name": "Borderless", "type": "toggle", "value": False},
            {"name": "Resolution", "type": "choice", "choices": [(1280, 720), (1920, 1080), (800, 600)], "value": 0},
            {"name": "Back", "type": "action"}
        ]
        self.selected = 0

    def display(self):
        self.screen.fill(WATER_COLOR)
        for idx, option in enumerate(self.options):
            color = TEXT_COLOR if idx == self.selected else UI_BG_COLOR
            text = option["name"]
            if option["type"] == "toggle":
                text += f": {'On' if option['value'] else 'Off'}"
            elif option["type"] == "choice":
                current_res = option["choices"][option["value"]]
                text += f": {current_res[0]}x{current_res[1]}"
            rendered_text = self.font.render(text, True, color)
            text_rect = rendered_text.get_rect(center=(WIDTH // 2, 200 + idx * 50))
            self.screen.blit(rendered_text, text_rect)
        pygame.display.flip()

    def navigate(self, direction):
        self.selected = (self.selected + direction) % len(self.options)

    def toggle_option(self):
        option = self.options[self.selected]
        if option["type"] == "toggle":
            option["value"] = not option["value"]
            return option["name"], option["value"]
        elif option["type"] == "choice":
            option["value"] = (option["value"] + 1) % len(option["choices"])
            return option["name"], option["choices"][option["value"]]
        elif option["type"] == "action" and option["name"] == "Back":
            return "Back", None
        return None, None


class Intro:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(UI_FONT, 60)
        self.text = "RPG ELDORIA"

    def display(self):
        self.screen.fill(WATER_COLOR)
        displayed_text = ""

        for char in self.text:
            displayed_text += char
            rendered_text = self.font.render(displayed_text, True, TEXT_COLOR)
            text_rect = rendered_text.get_rect(center=(WIDTH // 2, HEIGTH // 2))
            self.screen.fill(BLACK_COLOR)
            self.screen.blit(rendered_text, text_rect)
            pygame.display.flip()
            time.sleep(0.2)  # Adjust speed of the typing effect

        time.sleep(1)  # Pause after the full text appears


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.RESIZABLE)
        pygame.display.set_caption('RPG Eldoria')
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.main_menu = MainMenu(self.screen)
        self.settings_menu = SettingsMenu(self.screen)
        self.fullscreen = False
        self.in_menu = False
        self.in_settings = False
        self.intro_played = False

        # Background music
        main_sound = pygame.mixer.Sound("../audio/main.ogg")
        main_sound.set_volume(0.5)
        main_sound.play(loops=-1)

    def toggle_fullscreen(self, borderless=False):
        if borderless:
            self.screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.NOFRAME)
        else:
            if not self.fullscreen:
                self.screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.RESIZABLE)
        self.fullscreen = not self.fullscreen

    def apply_resolution(self, resolution):
        global WIDTH, HEIGTH
        WIDTH, HEIGTH = resolution
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.RESIZABLE)

    def run(self):
        if not self.intro_played:
            intro = Intro(self.screen)
            intro.display()
            self.intro_played = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.in_menu:  # Main menu
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.main_menu.navigate(-1)
                        elif event.key == pygame.K_DOWN:
                            self.main_menu.navigate(1)
                        elif event.key == pygame.K_RETURN:
                            action = self.main_menu.select()
                            if action == "resume":
                                self.in_menu = False
                            elif action == "settings":
                                self.in_menu = False
                                self.in_settings = True
                            elif action == "quit":
                                pygame.quit()
                                sys.exit()
                        elif event.key == pygame.K_ESCAPE:
                            self.in_menu = False

                elif self.in_settings:  # Settings menu
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.settings_menu.navigate(-1)
                        elif event.key == pygame.K_DOWN:
                            self.settings_menu.navigate(1)
                        elif event.key == pygame.K_RETURN:
                            option, value = self.settings_menu.toggle_option()
                            if option == "Fullscreen":
                                self.toggle_fullscreen(borderless=False)
                            elif option == "Borderless":
                                self.toggle_fullscreen(borderless=True)
                            elif option == "Resolution":
                                self.apply_resolution(value)
                            elif option == "Back":
                                self.in_settings = False
                                self.in_menu = True
                        elif event.key == pygame.K_ESCAPE:
                            self.in_settings = False
                            self.in_menu = True

                else:  # Game controls
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.in_menu = True
                        elif event.key == pygame.K_f:
                            self.toggle_fullscreen()

                    if event.type == pygame.VIDEORESIZE:
                        global WIDTH, HEIGTH
                        WIDTH, HEIGTH = event.size
                        self.screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.RESIZABLE)

            if self.in_menu:
                self.main_menu.display()
            elif self.in_settings:
                self.settings_menu.display()
            else:
                self.screen.fill(WATER_COLOR)
                self.level.run()
                pygame.display.update()

            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
