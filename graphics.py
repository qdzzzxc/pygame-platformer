import pygame
from os.path import join

def flip(sprite):
    return pygame.transform.flip(sprite, True, False)

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


def draw(window, background, bg_image, player, objects, offset_x, offset_y, enemies, bg_slow=(1, 1), sec_after_hit=1):
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

    for obj in enemies:
        if hasattr(obj, 'display_health'):
            obj.display_health(window, offset_x, offset_y)
        obj.draw(window, offset_x, offset_y)

    if hasattr(player, 'display_health'):
        player.display_health(window, offset_x, offset_y)
    player.draw(window, offset_x, offset_y)

    player_attacked_by = pygame.sprite.spritecollide(player, enemies, False)
    for i in player_attacked_by:
        if not player.after_hit:
            player.after_hit = sec_after_hit*player.fps
            player.make_hit()
        break
    if player.after_hit:
         player.after_hit -= 1
    
    for bullet in player.bullets:
        damaged_by_player = pygame.sprite.spritecollide(bullet, enemies, False)
        for obj in damaged_by_player:
            if obj in enemies:
                obj.make_hit()
                bullet.delete_object()
        bullet.draw(window, offset_x, offset_y, w, h)

    pygame.display.update()