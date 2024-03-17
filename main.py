import pygame

from graphics import get_background, draw
from character import Player, FloatingEnemy

WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))

def handle_move(player):
    player.x_vel = 0
    player.y_vel = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.move_right(PLAYER_VEL)
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.move_up(PLAYER_VEL)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.move_down(PLAYER_VEL)

def main(window):
    pygame.init()
    pygame.display.set_caption("Platformer")

    offset_x = 0
    offset_y = 0 
    scroll_area_height = HEIGHT//6
    scroll_area_width = WIDTH//4

    clock = pygame.time.Clock()
    background, bg_image = get_background("fon.png", WIDTH, HEIGHT)

    player = Player(200, 200, 100, 180, name='player', image_name='valorant.png')

    enemies = pygame.sprite.Group()
    objects = pygame.sprite.Group() #for static

    miku1 = FloatingEnemy(200, 200, 120, 150, name='enemy', image_name='miku.webp', x_range = (200, 200), y_range = (200, 250), x_vel=5, y_vel=2)

    enemies.add(miku1)

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.range_attack()

        player.update()
        enemies.update()

        handle_move(player)

        draw(window, background, bg_image, player, objects, offset_x, offset_y, enemies, bg_slow=(1, 1))

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

        if ((player.rect.bottom - offset_y >= HEIGHT - scroll_area_height) and player.y_vel > 0) or (
                (player.rect.top - offset_y <= scroll_area_height) and player.y_vel < 0):
            offset_y += player.y_vel

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
