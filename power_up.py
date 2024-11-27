import pygame
import random
from settings import *

class PowerUp:
    def __init__(self):
        self.active = False
        self.position = (0, 0)
        self.type = None
        self.spawn_power_up()
    
    def spawn_power_up(self):
        if random.random() < POWER_UP_SPAWN_CHANCE and not self.active:
            self.active = True
            columns = WINDOW_WIDTH // GRID_SIZE
            rows = WINDOW_HEIGHT // GRID_SIZE
            self.position = (
                random.randint(0, columns - 1) * GRID_SIZE,
                random.randint(0, rows - 1) * GRID_SIZE
            )
            self.type = random.choice(['speed', 'ghost', 'shrink', 'shield'])
    
    def collect(self):
        self.active = False
        return self.type
    
    def draw(self, screen):
        if self.active:
            color = self.get_power_up_color()
            pygame.draw.rect(screen, color, (self.position[0], self.position[1], GRID_SIZE - 1, GRID_SIZE - 1))
    
    def get_power_up_color(self):
        colors = {
            'speed': BLUE,
            'ghost': PURPLE,
            'shrink': ORANGE,
            'shield': CYAN
        }
        return colors.get(self.type, WHITE)