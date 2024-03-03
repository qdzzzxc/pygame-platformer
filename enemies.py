import pygame
import math
from graphics import load_sprite_sheets
from character import Character

class NinjaFrog(Character):
    VELOCITY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "frog")
        self.sprites = load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)

        self.animation_count = 0

        self.direction = "left"
        self.image = self.sprites["idle_" + self.direction][0]

        self.rect = pygame.Rect(x, y, width, height)
        self.mask = pygame.mask.from_surface(self.image)

        self.attack_delay = 1000

        self.melee_attack_range = 100
        self.attacking = False
        self.attack_timer = 0
    
    def player_around(self, player):
        range_to_player = math.sqrt((self.rect.x - player.rect.x)**2 + (self.rect.y - player.rect.y)**2)
        if range_to_player < self.aggro_range:
            if range_to_player < self.melee_attack_range:
                self.melee_attack()

            if player.rect.right < self.rect.left:
                self.move_left(self.VELOCITY)

            elif player.rect.left > self.rect.right:
                self.move_right(self.VELOCITY)
        else:
            self.x_vel = 0
    
    def melee_attack(self):
        self.attack_timer = pygame.time.get_ticks()
        self.attacking = True

    def attack_check(self):
        if pygame.time.get_ticks() - self.attack_timer > self.attack_delay:
            self.attacking = False
    
    def update(self):
        if self.attacking:
            sprite_sheet = "attack"
        elif self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"
        elif self.fall_count > 5:
            sprite_sheet = "jump"
        else:
            sprite_sheet = "idle"

        sprites = self.sprites[sprite_sheet + "_" + self.direction]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

        if self.attacking:
            self.attack_check()
        else:
            self.move(self.x_vel, self.y_vel)
