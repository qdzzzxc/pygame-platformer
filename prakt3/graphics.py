import pygame
from os.path import join

def get_background(name, WIDTH, HEIGHT):
    image = pygame.image.load(join("assets", "background", name))
    image = pygame.transform.scale(image, (WIDTH, HEIGHT))

    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(-1, WIDTH // width + 1):
        for j in range(-1, HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x, offset_y, bg_slow=(1, 1)):
    _, _, w, h = bg_image.get_rect()
    bg_slow_x, bg_slow_y = bg_slow

    for i, tile in enumerate(background):
        x, y = tile
        if x - offset_x//bg_slow_x > 2 * w:
            background[i] =  (x - 3 * w, y)
        elif x - offset_x//bg_slow_x < - w:
            background[i] =  (x + 3 * w, y)
        
        if y - offset_y//bg_slow_y > 2 * h:
            background[i] =  (x, y - 3 * h,)
        elif y - offset_y//bg_slow_y < - h:
            background[i] =  (x, y + 3 * h)
        
        window.blit(bg_image, (x - offset_x//bg_slow_x, y - offset_y//bg_slow_y))

    for obj in objects:
        obj.draw(window, offset_x, offset_y)

    player.draw(window, offset_x, offset_y)

    pygame.display.update()