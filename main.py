import pygame

from player import Player
from blocks import Block, Fire
from enemies import NinjaFrog
from graphics import get_background, draw

WIDTH, HEIGHT = 1920, 1080
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        # +- 12 чтобы не обрезать спрайт, +1 чтобы не падал под землю
        if player.rect.left + 10 < obj.rect.right and \
           player.rect.right - 10 > obj.rect.left and \
           player.rect.top < obj.rect.bottom and \
           player.rect.bottom + 1 > obj.rect.top:
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            if dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    dx = int(dx)
    player.move(dx, 0)
    player.update()
    collided_object = None

    for obj in objects:
        if player.rect.colliderect(obj.rect):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects, last_press, damage, enemies):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL//4)
    collide_right = collide(player, objects, PLAYER_VEL//4)
    if collide_left == collide_right != None:
        collide_left = collide(player, objects, -PLAYER_VEL*2)
        collide_right = collide(player, objects, PLAYER_VEL*2)

    if keys[pygame.K_LEFT] and not collide_left and keys[pygame.K_RIGHT] and not collide_right:
        if last_press == 'R':
            player.move_right(PLAYER_VEL)
        else:
            player.move_left(PLAYER_VEL)
    elif (keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]) and (collide_left or collide_right):
        pass
    else:
        if keys[pygame.K_LEFT] and not collide_left:
                player.move_left(PLAYER_VEL)

        if keys[pygame.K_RIGHT] and not collide_right:
            player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]
    
    for obj in to_check:
        if obj and obj in damage:
            player.make_hit()

    for enemy in enemies:
        enemy.player_around(player)

    return keys[pygame.K_LEFT], keys[pygame.K_RIGHT]

def main(window):
    pygame.init()
    pygame.display.set_caption("Platformer")

    offset_x = 0
    scroll_area_width = WIDTH//4

    last_press = 'R'

    clock = pygame.time.Clock()
    background, bg_image = get_background("t1.png", WIDTH, HEIGHT)

    block_size = 96

    damage = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    player = Player(200, 100, 50, 50)
    damage.add(Fire(100, HEIGHT - block_size - 64, 16, 32))
    damage.add(Fire(-100, HEIGHT - block_size - 64, 16, 32))

    nf = NinjaFrog(300, HEIGHT - block_size - 64, 64, 64)
    damage.add(nf)
    enemies.add(nf)

    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-2*WIDTH // block_size, (WIDTH * 2) // block_size)]
    
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size), 
               Block(block_size * 4, HEIGHT - block_size * 4, block_size), 
               *damage,]

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.jump_count < 2:
                    player.jump()

                if event.key == pygame.K_LEFT:
                    last_press = 'L'
                elif event.key == pygame.K_RIGHT:
                    last_press = 'R'

        player.loop(FPS)
        damage.update()

        handle_move(player, objects, last_press, damage, enemies)

        draw(window, background, bg_image, player, objects, offset_x, 8)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width*2) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
