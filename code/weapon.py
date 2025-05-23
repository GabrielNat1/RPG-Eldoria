import pygame
from paths import get_asset_path

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        direction = player.status.split('_')[0]

        full_path = get_asset_path('graphics', 'weapons', player.weapon, 'right.png')
        self.image = pygame.image.load(full_path).convert_alpha()

        if direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)  
        elif direction == 'up':
            self.image = pygame.transform.rotate(self.image, 90)  
        elif direction == 'down':
            self.image = pygame.transform.rotate(self.image, -90)  

        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0))
        else:  # 'up'
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-10, 0))
