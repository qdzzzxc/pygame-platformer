import pygame
from os.path import join

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None, image_name='player.png'):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height
        self.name = name

        self.x_vel = 0
        self.y_vel = 0
        self.direction = "left"
        self.animation_count = 0

        image = pygame.image.load(join("assets", name, image_name))
        self.image = pygame.transform.scale(image, (width, height))

    
    def draw(self, win, offset_x, offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

    def reverse_direction(self):
        if self.direction == 'left':
            self.direction = 'right'
        else:
            self.direction = 'left'

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def move_up(self, vel):
        self.y_vel = -vel

    def move_down(self, vel):
        self.y_vel = vel

    def update(self):
        self.move(self.x_vel, self.y_vel)
        self.update_rect()

    def update_rect(self):
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))


class FloatingEnemy(Character):
    def __init__(self, x, y, width, height, name=None, image_name='player.png', x_range = (200, 200), y_range = None,  x_vel=3, y_vel=2):
        super().__init__(x, y, width, height, name, image_name)

        if x_range:
            self.left_pos_x = x - x_range[0]
            self.right_pos_x = x + x_range[1]
            self.x_ranged = True
        else:
            self.x_ranged = False

        if y_range:
            self.left_pos_y = y - y_range[0]
            self.right_pos_y = y + y_range[1]
            self.direction_y = 'up'
        else:
            self.direction_y = None

        self.velocity_x = x_vel
        self.velocity_y = y_vel

    def update_range_mov_x(self):
        self.x_vel = 0
        
        if not(self.left_pos_x <= self.rect.x <=self.right_pos_x):
            self.reverse_direction()
  
        if self.direction == "left":
            self.move_left(self.velocity_x)
        else:
            self.move_right(self.velocity_x)
    
    def update_range_mov_y(self):
        self.y_vel = 0

        if not(self.left_pos_y <= self.rect.y <= self.right_pos_y):
            if self.direction_y == "up":
                self.direction_y = 'down'
            else:
                self.direction_y = "up"
            
        if self.direction_y == "up":
            self.move_up(self.velocity_y)
        else:
            self.move_down(self.velocity_y)
            
        

    def update(self):
        if self.x_ranged:
            self.update_range_mov_x()
        if self.direction_y:
            self.update_range_mov_y()
        
        self.move(self.x_vel, self.y_vel)
        self.update_rect()


