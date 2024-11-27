import pygame
import random
from settings import *

class Obstacle:
    def __init__(self):
        self.positions = []
        self.generate_obstacles()
    
    def is_valid_position(self, pos, all_positions):
        """Check if a position is valid (not too close to other obstacles)"""
        x, y = pos
        
        # Check minimum spacing between obstacles
        for other_pos in all_positions:
            ox, oy = other_pos
            if abs(x - ox) < MIN_OBSTACLE_SPACING * GRID_SIZE and \
               abs(y - oy) < MIN_OBSTACLE_SPACING * GRID_SIZE:
                return False
        
        # Check if this position would create a surrounded area
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        count_adjacent = 0
        for dx, dy in directions:
            check_pos = (x + dx * GRID_SIZE, y + dy * GRID_SIZE)
            if check_pos in all_positions:
                count_adjacent += 1
        
        return count_adjacent < 2  # Prevent more than 2 adjacent obstacles
    
    def generate_obstacles(self):
        columns = WINDOW_WIDTH // GRID_SIZE - 2  # Leave space at edges
        rows = WINDOW_HEIGHT // GRID_SIZE - 2
        center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        
        attempts = 0
        while len(self.positions) < OBSTACLE_COUNT and attempts < 1000:
            pos = (
                (random.randint(1, columns) * GRID_SIZE),
                (random.randint(1, rows) * GRID_SIZE)
            )
            
            # Ensure obstacles don't spawn at snake's starting position or too close to center
            if abs(pos[0] - center[0]) < 3 * GRID_SIZE and \
               abs(pos[1] - center[1]) < 3 * GRID_SIZE:
                continue
                
            if self.is_valid_position(pos, self.positions):
                self.positions.append(pos)
            
            attempts += 1
    
    def draw(self, screen):
        for pos in self.positions:
            pygame.draw.rect(screen, YELLOW, (pos[0], pos[1], GRID_SIZE - 1, GRID_SIZE - 1)) 