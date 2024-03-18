import pygame

from game import Game

def main(game):
    game.level_1()

    run = True
    while run:
        game.clock.tick(game.fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game.player.range_attack()

        game.loop()
    
        if game.player.health <= 0:
            game.reset()
            pass

            # while run:
            #     for event in pygame.event.get():
            #         if event.type == pygame.QUIT:
            #             run = False
            #             game.reset()
            #             break

    pygame.quit()
    quit()


if __name__ == "__main__":
    game = Game(WIDTH=800, HEIGHT=600, FPS=60, sec_after_hit=0) 
    main(game)
