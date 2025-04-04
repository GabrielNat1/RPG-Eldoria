import pygame
from settings import *
from entity import Entity
from support import *

class Enemy(Entity):
    shared_animations = {}

    # Adiciona controle de remoção global (definir no início do arquivo ou logo após a definição da classe)
    MAX_DESPAWNS_PER_FRAME = 1
    last_despawn_frame = 0
    despawn_count = 0

    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp, mission_system=None):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics setup
        self.load_animations(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed'] * 0.5  # Reduzir a velocidade dos inimigos
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        if self.monster_name == 'raccoon':
            self.health *= 2  # Double the health of the raccoon

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp

        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

        # sounds
        self.death_sound = pygame.mixer.Sound('../audio/death.wav')
        self.hit_sound = pygame.mixer.Sound('../audio/hit.wav')
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.death_sound.set_volume(0.6)
        self.hit_sound.set_volume(0.6)
        self.attack_sound.set_volume(0.6)

        # respawn - atualize para 60.000ms
        self.respawn_time = 60000  
        self.death_time = None
        self.alive = True  
        self.initial_position = pos  

        # mission system
        self.mission_system = mission_system
        self.player_near = False
        self.fight_music_playing = False
        self.fight_music = pygame.mixer.Sound('../audio/fight.ogg')  # Preload fight music
        self.main_music_path = '../audio/main.ogg'  # Path to main music
        self.music_channel = pygame.mixer.Channel(1)  # Use a separate channel for music

    def load_animations(self, name):
        if name not in Enemy.shared_animations:
            animations = {'idle': [], 'move': [], 'attack': []}
            main_path = f'../graphics/monsters/{name}/'
            for animation in animations.keys():
                animations[animation] = import_folder(main_path + animation)
            Enemy.shared_animations[name] = animations

        self.animations = Enemy.shared_animations[name]

    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        if self.monster_name == 'raccoon':
            if distance <= 750 and not self.fight_music_playing:  # Increased distance
                self.start_fight_music()
            elif distance > 750 and self.fight_music_playing:
                self.stop_fight_music()

        return (distance,direction)

    def start_fight_music(self):
        self.fight_music_playing = True
        pygame.mixer.music.pause()  # Pause the main music
        self.music_channel.play(self.fight_music, loops=-1, fade_ms=500)  # Reduce fade-in time to minimize lag

    def stop_fight_music(self):
        self.fight_music_playing = False
        self.music_channel.fadeout(500)  # Reduce fadeout time to minimize lag
        pygame.mixer.music.unpause()  # Resume the main music

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self,player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage,self.attack_type)
            self.attack_sound.play()
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self,player,attack_type):
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0 and self.alive:
            self.alive = False
            self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.add_exp(self.exp)
            self.death_sound.play()
            self.death_time = pygame.time.get_ticks()
            if self.mission_system:
                self.mission_system.enemy_killed()
                if self.monster_name == 'raccoon':
                    self.mission_system.boss_killed = True
                    self.stop_fight_music()

    def respawn(self):
        if not self.alive and self.death_time and pygame.time.get_ticks() - self.death_time >= self.respawn_time:
            # Cache o dicionário do monstro para melhor performance
            data = monster_data[self.monster_name]
            self.health = data['health']
            self.alive = True
            # Verifica se já não está no grupo para evitar alocações duplicadas
            if self not in self.groups():
                self.add(self.groups())
            self.death_time = None
            self.rect.topleft = self.initial_position
            self.hitbox.topleft = self.initial_position

    def check_despawn(self, player):
        distance = self.get_player_distance_direction(player)[0]
        if distance > ENEMY_DESPAWN_DISTANCE:
            current_time = pygame.time.get_ticks()
            # Se ainda não iniciou o timer, inicia-o
            if not hasattr(self, 'despawn_timer'):
                self.despawn_timer = current_time
            else:
                # Se já passou o tempo de espera (3000ms), efetua o despawn
                if current_time - self.despawn_timer >= 3000:
                    if current_time != Enemy.last_despawn_frame:
                        Enemy.last_despawn_frame = current_time
                        Enemy.despawn_count = 0
                    if Enemy.despawn_count < Enemy.MAX_DESPAWNS_PER_FRAME:
                        Enemy.despawn_count += 1
                        self.kill()
                        self.alive = False
        else:
            # Se o inimigo volta para perto, reseta o timer
            if hasattr(self, 'despawn_timer'):
                del self.despawn_timer

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()
        self.respawn()  

    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)
        self.check_despawn(player)
        self.update()