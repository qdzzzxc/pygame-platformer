import pygame

from graphics import get_background, draw
from player import Character, FloatingEnemy

WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))

def handle_move(player):
    player.x_vel = 0
    player.y_vel = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)
    if keys[pygame.K_UP]:
        player.move_up(PLAYER_VEL)
    if keys[pygame.K_DOWN]:
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

    player = Character(200, 200, 100, 180, name='player', image_name='valorant.png')

    enemies = pygame.sprite.Group()

    miku1 = FloatingEnemy(200, 200, 120, 150, name='enemy', image_name='miku.webp', x_range = (200, 200), y_range = (200, 250), x_vel=5, y_vel=2)

    enemies.add(miku1)

    objects = [miku1]

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        player.update()
        enemies.update()

        handle_move(player)

        draw(window, background, bg_image, player, objects, offset_x, offset_y, (1, 1))

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
