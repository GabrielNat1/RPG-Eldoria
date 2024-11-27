import pygame, sys
from gameplay.level import *
from gameplay.settings import *

sys.path.append(r'C:\RPG Eldoria\source')

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH ))
        pygame.display.set_caption('Rpg Eldoria')
        self.clock = pygame.time.Clock()
        
        self.level = Level()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
            
if __name__ == '__main__':
    game = Game()
    game.run()