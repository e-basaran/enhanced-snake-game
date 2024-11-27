import pygame
from settings import *

class Snake:
    def __init__(self, player_number=1):
        self.player_number = player_number
        self.reset()
        
    def reset(self):
        # Different starting positions for different players
        if self.player_number == 1:
            self.body = [(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2)]
            self.direction = "RIGHT"
        else:
            self.body = [(3 * WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2)]
            self.direction = "LEFT"
            
        self.grow_pending = False
        self.speed_boost = False
        self.ghost_mode = False
        self.shield_mode = False
        self.is_shrunk = False
        self.speed_boost_time = 0
        self.ghost_mode_time = 0
        self.shield_mode_time = 0
        self.shrink_time = 0
        
    def move(self):
        x, y = self.body[0]
        
        if self.direction == "UP":
            y -= GRID_SIZE
        elif self.direction == "DOWN":
            y += GRID_SIZE
        elif self.direction == "LEFT":
            x -= GRID_SIZE
        elif self.direction == "RIGHT":
            x += GRID_SIZE
            
        # Wrap around screen if in ghost mode
        if self.ghost_mode:
            x = x % WINDOW_WIDTH
            y = y % WINDOW_HEIGHT
            
        new_head = (x, y)
        
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False
            
        self.body.insert(0, new_head)
        
    def grow(self):
        if not self.is_shrunk:
            self.grow_pending = True
        
    def activate_power_up(self, power_up_type, current_time):
        if power_up_type == 'speed':
            self.speed_boost = True
            self.speed_boost_time = current_time + SPEED_BOOST_DURATION
        elif power_up_type == 'ghost':
            self.ghost_mode = True
            self.ghost_mode_time = current_time + GHOST_MODE_DURATION
        elif power_up_type == 'shield':
            self.shield_mode = True
            self.shield_mode_time = current_time + SHIELD_DURATION
        elif power_up_type == 'shrink':
            self.is_shrunk = True
            self.shrink_time = current_time + SHRINK_DURATION
            # Remove half of the snake's body
            if len(self.body) > 1:
                self.body = self.body[:len(self.body)//2]
    
    def update_power_ups(self, current_time):
        if self.speed_boost and current_time >= self.speed_boost_time:
            self.speed_boost = False
        if self.ghost_mode and current_time >= self.ghost_mode_time:
            self.ghost_mode = False
        if self.shield_mode and current_time >= self.shield_mode_time:
            self.shield_mode = False
        if self.is_shrunk and current_time >= self.shrink_time:
            self.is_shrunk = False
        
    def draw(self, screen):
        for i, segment in enumerate(self.body):
            color = self.get_snake_color(i == 0)  # i == 0 means it's the head
            
            if self.ghost_mode:
                s = pygame.Surface((GRID_SIZE - 1, GRID_SIZE - 1))
                s.set_alpha(128)
                s.fill(color)
                screen.blit(s, (segment[0], segment[1]))
            else:
                pygame.draw.rect(screen, color, (segment[0], segment[1], GRID_SIZE - 1, GRID_SIZE - 1))
                
            # Draw shield effect
            if self.shield_mode and i == 0:
                pygame.draw.rect(screen, CYAN, (segment[0], segment[1], GRID_SIZE - 1, GRID_SIZE - 1), 2)
    
    def get_snake_color(self, is_head):
        if is_head:
            if self.ghost_mode:
                return PURPLE
            elif self.speed_boost:
                return BLUE
            elif self.shield_mode:
                return CYAN
            elif self.is_shrunk:
                return ORANGE
        
        # Body color depends on player number
        return GREEN if self.player_number == 1 else RED