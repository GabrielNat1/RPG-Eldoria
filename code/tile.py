import pygame 
from settings import *

class Tile(pygame.sprite.Sprite):
    shared_surfaces = {}

    def __init__(self, pos, groups, sprite_type, surface=None):
        unique_groups = list(set(groups))
        super().__init__(unique_groups)
        self.sprite_type = sprite_type
        y_offset = HITBOX_OFFSET[sprite_type]

        if surface is None:
            if sprite_type not in Tile.shared_surfaces:
                Tile.shared_surfaces[sprite_type] = pygame.Surface((TILESIZE, TILESIZE))
            self.image = Tile.shared_surfaces[sprite_type]
        else:
            self.image = surface

        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.inflate(0, y_offset)