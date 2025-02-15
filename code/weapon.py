import pygame 

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        direction = player.status.split('_')[0]

        # Carrega a imagem padrão (direita)
        full_path = f'../graphics/weapons/{player.weapon}/right.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        # Modifica a imagem conforme a direção
        if direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)  # Inverte horizontalmente
        elif direction == 'up':
            self.image = pygame.transform.rotate(self.image, 90)  # Rotaciona 90° sentido horário
        elif direction == 'down':
            self.image = pygame.transform.rotate(self.image, -90)  # Rotaciona -90° sentido horário

        # Posicionamento
        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0))
        else:  # 'up'
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-10, 0))
