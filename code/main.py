import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        
        pygame.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.RESIZABLE)
        pygame.display.set_caption('RPG Eldoria')
        self.clock = pygame.time.Clock()

        self.level = Level()

        main_sound = pygame.mixer.Sound('../audio/main.ogg')
        main_sound.set_volume(0.5)
        main_sound.play(loops=-1)

        self.fullscreen = False

    def toggle_fullscreen(self):
        if not self.fullscreen:
         
            self.screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.FULLSCREEN)
        else:
            
            self.screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.RESIZABLE)
        self.fullscreen = not self.fullscreen

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()
                    if event.key == pygame.K_f:  
                        self.toggle_fullscreen()

                if event.type == pygame.VIDEORESIZE:
                    
                    WIDTH, HEIGTH = event.size
                    self.screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.RESIZABLE)

            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
