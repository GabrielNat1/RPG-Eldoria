import pygame 
from settings import *
from support import import_folder
from entity import Entity
from ui import UI
from npc import NPC, MissionSystem

class Player(Entity):
    shared_animations = {}

    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic, mission_system):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])
        self.initial_position = pos

        # graphics setup
        self.import_player_assets()
        self.status = 'down'
        self.ui = UI()

        # movement 
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # weapons
        self.weapons = ['sword']  # Initial weapons
        self.weapon_index = 0
        self.weapon = self.weapons[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # magic 
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5, 'stamina': 100}
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic' : 10, 'speed': 10, 'stamina': 100}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic' : 100, 'speed': 100, 'stamina': 100}
        self.health = self.stats['health']  
        self.energy = self.stats['energy'] * 0.8
        self.exp = 0
        self.speed = self.stats['speed']
        self.stamina = self.stats['stamina']
        self.running = False
        self.stamina_recovery_time = 2000  
        self.last_run_time = pygame.time.get_ticks()

        # damage timer
        self.vulnerable = True
        self.hurt_time = pygame.time.get_ticks()  
        self.invulnerability_duration = 500
        self.blinking = False
        self.blink_start_time = None

        # import a sound
        self.weapon_attack_sound = pygame.mixer.Sound('../audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)

        # animation speed
        self.animation_speed = 0.2  

        # attack methods
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack

        # fade effect
        self.fade_effect = False
        self.fade_start_time = None
        self.fade_duration = 1000  # 1 second
        
    def weapon_data(self):
            self.weapon_data = weapon_data 
            #print("Loaded weapons data.")
   
    def add_weapon(self, weapon_name):
            if weapon_name not in self.weapons:  
                self.weapons.append(weapon_name)
                #print(f'Weapon {weapon_name} Added!')
    
            self.weapon = weapon_name  
            self.weapon_index = self.weapons.index(weapon_name) 
            #print(f'Equipped Weapon : {self.weapon}, Index: {self.weapon_index}')

            self.ui.display(self)
             
    def import_player_assets(self):
        character_path = '../graphics/player/'
        if not Player.shared_animations:
            animations = {
                'up': [], 'down': [], 'left': [],
                'left_idle': [], 'up_idle': [], 'down_idle': [],
                'left_attack': [], 'up_attack': [], 'down_attack': []
            }

            for animation in animations.keys():
                full_path = character_path + animation
                animations[animation] = import_folder(full_path)

            animations['right'] = [pygame.transform.flip(img, True, False) for img in animations['left']]
            animations['right_idle'] = [pygame.transform.flip(img, True, False) for img in animations['left_idle']]
            animations['right_attack'] = [pygame.transform.flip(img, True, False) for img in animations['left_attack']]

            Player.shared_animations = animations

        self.animations = Player.shared_animations

    
    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # movement input
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # running input
            if keys[pygame.K_LSHIFT] and self.stamina > 0:
                self.running = True
                self.speed = self.stats['speed'] * 1.5
                self.stamina -= 0.5
                self.last_run_time = pygame.time.get_ticks()
            else:
                self.running = False
                self.speed = self.stats['speed']

            # attack input 
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()

            # magic input 
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style,strength,cost)

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                self.weapon_index += 1
                if self.weapon_index >= len(self.weapons):
                    self.weapon_index = 0
                self.weapon = self.weapons[self.weapon_index]

            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0

                self.magic = list(magic_data.keys())[self.magic_index]
    
            # // mouse input //
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0]: # Left mouse button
                if not self.attacking:
                    self.attacking = True
                    self.attack_time = pygame.time.get_ticks()
                    self.create_attack()
                    self.weapon_attack_sound.play()

            if mouse_buttons[2]:  # Right mouse button
                if not self.attacking:
                    self.attacking = True
                    self.attack_time = pygame.time.get_ticks()
                    style = list(magic_data.keys())[self.magic_index]
                    strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                    cost = list(magic_data.values())[self.magic_index]['cost']
                    self.create_magic(style, strength, cost)
    
    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
        elif self.running:
            if 'idle' in self.status:
                self.status = self.status.replace('_idle','')
            elif 'attack' in self.status:
                self.status = self.status.replace('_attack','')
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.weapon is None:
            return
    
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if self.hurt_time is not None and current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

        # Stamina recovery
        if not self.running and current_time - self.last_run_time >= self.stamina_recovery_time:
            if self.stamina < self.stats['stamina']:
                self.stamina += 0.5

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flicker 
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
  
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
  
        return base_damage + spell_damage

    def get_value_by_index(self,index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self,index):
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def blink(self):
        current_time = pygame.time.get_ticks()
  
        if current_time - self.blink_start_time >= 500:
            self.blinking = False
            self.vulnerable = True
            self.image.set_alpha(255)
        else:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
   
    def restore_mission_state(self):
            self.mission_state = self.mission_system.get_mission_state()

    def check_death(self):
        if self.health <= 0:
            self.health = self.stats['health']
            self.energy = self.stats['energy']
            self.rect.topleft = self.initial_position
            self.hitbox.topleft = self.initial_position
            self.blinking = True
            self.blink_start_time = pygame.time.get_ticks()
            self.vulnerable = False
            self.restore_mission_state()
            self.start_fade_effect()

    def start_fade_effect(self):
        self.fade_effect = True
        self.fade_start_time = pygame.time.get_ticks()

    def apply_fade_effect(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.fade_start_time >= self.fade_duration:
            self.fade_effect = False
        else:
            alpha = 255 * (1 - (current_time - self.fade_start_time) / self.fade_duration)
            self.image.set_alpha(alpha)

    def update(self):
        if not self.blinking:
            self.input()
            self.move(self.speed)
        self.cooldowns()
        self.get_status()
        self.animate()
        self.energy_recovery()
        self.check_death()
        if self.blinking:
            self.blink()
        if self.fade_effect:
            self.apply_fade_effect()