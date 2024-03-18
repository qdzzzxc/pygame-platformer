import pygame
import numpy as np

def health_bar_decorator(character_class, width=100, height=10, color_full=(0, 255, 0), color_damaged=(255, 165, 0), y_offset=20):
    class HealthBar(character_class):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.max_health = self.health

            self.hb_width = width
            self.hb_height = height

            self.ticks = np.linspace(0, width, self.health+1)[1:-1]
            self.tick = pygame.Surface((width//25, height))
            self.tick.fill((0, 0, 0))

            print(self.ticks)

            self.full_rect = pygame.Surface((width, height))
            self.full_rect.fill(color_full)

            self.damaged_rect = pygame.Surface((width//self.max_health+1, height))
            self.damaged_rect.fill(color_damaged)

            self.y_offset = y_offset
        
        def display_health(self, win, offset_x, offset_y):
            win.blit(self.full_rect, (self.rect.centerx - offset_x - self.hb_width//2, self.rect.top - offset_y - y_offset))
            
            for i in range(self.max_health - self.health):
                win.blit(self.damaged_rect, (self.rect.centerx - offset_x - self.hb_width//2 + self.damaged_rect.get_width()*(self.max_health - i - 1), self.rect.top - offset_y - y_offset))

            if self.max_health <= 8:
                for i in self.ticks:
                    win.blit(self.tick, (self.rect.centerx - offset_x - self.hb_width//2 + i, self.rect.top - offset_y - y_offset))

    return HealthBar