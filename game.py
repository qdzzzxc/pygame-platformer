import pygame
from decorators import health_bar_decorator
from graphics import get_background, draw
from character import Player, FloatingEnemy


class Game():
    def __init__(self, WIDTH, HEIGHT, FPS, sec_after_hit):
        pygame.init()
        pygame.display.set_caption("Platformer")

        self.width = WIDTH
        self.height = HEIGHT

        self.clock = pygame.time.Clock()

        self.offset_x = 0
        self.offset_y = 0 
        self.scroll_area_height = self.width//6
        self.scroll_area_width = self.height//4

        self.enemies = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()

        self.window = pygame.display.set_mode((self.width, self.height))

        self.run = True

        self.fps= FPS

        self.player_velocity = 5

        self.player = None

        self.sec_after_hit = sec_after_hit

    def update_offset(self, player):
        if ((player.rect.right - self.offset_x >= self.width - self.scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - self.offset_x <= self.scroll_area_width) and player.x_vel < 0):
            self.offset_x += player.x_vel

        if ((player.rect.bottom - self.offset_y >= self.height - self.scroll_area_height) and player.y_vel > 0) or (
                (player.rect.top - self.offset_y <= self.scroll_area_height) and player.y_vel < 0):
            self.offset_y += player.y_vel

    def level_1(self):
        self.background, self.bg_image = get_background("fon.png", self.width, self.height)

        hb_player = health_bar_decorator(Player)
        self.player = hb_player(200, 200, 100, 180, name='player', image_name='valorant.png', health=5, fps=self.fps)

        hb_enemy = health_bar_decorator(FloatingEnemy)
        miku1 = hb_enemy(400, 200, 120, 150, name='enemy', image_name='miku.webp', x_range = (200, 200), y_range = (200, 250), x_vel=5, y_vel=2, health=8, fps=self.fps)

        self.enemies.add(miku1)

    def reset(self):
        self.player.delete_object()

        for enemy in self.enemies:
            enemy.delete_object()
            del enemy

        for obj in self.objects:
            obj.kill()
            del obj

    def loop(self):
        self.player.update()
        self.enemies.update()

        self.handle_move()

        draw(self.window, self.background, self.bg_image, self.player, self.objects, self.offset_x, self.offset_y, self.enemies, bg_slow=(1, 1), sec_after_hit=self.sec_after_hit)

        self.update_offset(self.player)

    def handle_move(self):
        self.player.x_vel = 0
        self.player.y_vel = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left(self.player_velocity)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right(self.player_velocity)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.move_up(self.player_velocity)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.move_down(self.player_velocity)
        