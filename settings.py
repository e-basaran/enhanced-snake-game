import pygame

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GAME_SPEED = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)

# Power-up settings
SPEED_BOOST_DURATION = 5000  # 5 seconds
GHOST_MODE_DURATION = 3000   # 3 seconds
SHRINK_DURATION = 4000      # 4 seconds
SHIELD_DURATION = 6000      # 6 seconds
POWER_UP_SPAWN_CHANCE = 0.02  # 2% chance per frame

# Obstacle settings
OBSTACLE_COUNT = 15  # Increased number of obstacles
MIN_OBSTACLE_SPACING = 3  # Minimum spacing between obstacles in grid units

# Score settings
NORMAL_FOOD_SCORE = 1
SPEED_BOOST_SCORE = 3
GHOST_MODE_SCORE = 5
SHRINK_SCORE = 4
SHIELD_SCORE = 4

# Sound settings
MUSIC_VOLUME = 0.3
EFFECT_VOLUME = 0.4

# Menu settings
MENU_BUTTON_WIDTH = 200
MENU_BUTTON_HEIGHT = 50
MENU_BUTTON_PADDING = 20

# Player controls
P1_CONTROLS = {
    pygame.K_UP: "UP",
    pygame.K_DOWN: "DOWN",
    pygame.K_LEFT: "LEFT",
    pygame.K_RIGHT: "RIGHT"
}

P2_CONTROLS = {
    pygame.K_w: "UP",
    pygame.K_s: "DOWN",
    pygame.K_a: "LEFT",
    pygame.K_d: "RIGHT"
}
 