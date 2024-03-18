import pygame
from os.path import join
from graphics import flip

class MovingObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None, image_name='player.png', direction = "right", health=3, fps=60):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height
        self.name = name

        self.x_vel = 0
        self.y_vel = 0
        self.direction = direction
        self.health = health

        image = pygame.image.load(join("assets", name, image_name))
        self.image = pygame.transform.scale(image, (width, height))

        self.after_hit = 0
        self.fps = fps

    
    def draw(self, win, offset_x, offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

    def reverse_direction(self):
        self.image = flip(self.image)

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
            self.image = flip(self.image)
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.image = flip(self.image)
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

    def make_hit(self):
        self.health -= 1
        if self.health <= 0:
            self.delete_object()

    def delete_object(self):
        self.kill()


bullet_width = 70
bullet_height = 20
bullet_x_vel = 15
class Player(MovingObject):
    def __init__(self, x, y, width, height, name='player', image_name='player.png', direction='right', health=5, fps=60):
        super().__init__(x, y, width, height, name, image_name, direction, health, fps)
        self.bullets = pygame.sprite.Group()

    def update(self):
        self.move(self.x_vel, self.y_vel)
        self.bullets.update()
        self.update_rect()

    def range_attack(self):
        if self.direction == 'right':
            bullet = Bullet(self.rect.right, self.rect.top + 0.25*self.height, bullet_width, bullet_height, parent=self, direction=self.direction, x_vel=bullet_x_vel)
        else:
            bullet = Bullet(self.rect.left-bullet_width, self.rect.top + 0.25*self.height, bullet_width, bullet_height, parent=self, direction=self.direction, x_vel=bullet_x_vel)

        self.bullets.add(bullet)

class Bullet(MovingObject):
    def __init__(self, x, y, width, height, parent, name='projectile', image_name='bullet.png', direction='right', x_vel=15):
        super().__init__(x, y, width, height, name, image_name, direction)
        self.parent = parent
        self.bullet_x_vel = x_vel
        if self.direction == 'left':
            self.image = flip(self.image)
            self.bullet_x_vel *= -1


    def update(self):
        self.move(self.bullet_x_vel, 0)
        self.update_rect()

    def draw(self, win, offset_x, offset_y, w, h):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

        x, y = self.rect.x, self.rect.y
        if x - offset_x > 2*w or x - offset_x< - w or y - offset_y > 2*h or y - offset_y < - h:
            self.parent.bullets.remove(self)

            self.delete_object()

class FloatingEnemy(MovingObject):
    def __init__(self, x, y, width, height, name='enemy', image_name='default_enemy.png', direction='right', x_range = (200, 200), y_range = None,  x_vel=3, y_vel=2, health=3, fps=60):
        super().__init__(x, y, width, height, name, image_name, direction, health, fps)

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


