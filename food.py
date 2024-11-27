import pygame
import random
from settings import *

class Food:
    def __init__(self):
        self.randomize_position()
        
    def randomize_position(self):
        columns = WINDOW_WIDTH // GRID_SIZE
        rows = WINDOW_HEIGHT // GRID_SIZE
        self.position = (
            random.randint(0, columns - 1) * GRID_SIZE,
            random.randint(0, rows - 1) * GRID_SIZE
        )
        
    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], GRID_SIZE - 1, GRID_SIZE - 1)) 