import pygame
import sys
from snake import Snake
from food import Food
from power_up import PowerUp
from obstacle import Obstacle
from sound_manager import SoundManager
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Enhanced Snake Game")
        self.clock = pygame.time.Clock()
        self.sound_manager = SoundManager()
        self.game_state = "MENU"  # MENU, PLAYING, GAME_OVER
        self.game_mode = "1P"     # 1P or 2P
        self.reset_game()
        
    def reset_game(self):
        self.score = [0, 0]  # [P1_score, P2_score]
        self.game_font = pygame.font.Font(None, 42)
        self.snake1 = Snake(player_number=1)
        self.snake2 = Snake(player_number=2) if self.game_mode == "2P" else None
        self.food = Food()
        self.power_up = PowerUp()
        self.obstacles = Obstacle()
        
    def handle_menu_input(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 1P button
                if WINDOW_WIDTH/2 - 100 <= mouse_pos[0] <= WINDOW_WIDTH/2 + 100:
                    if WINDOW_HEIGHT/2 - 60 <= mouse_pos[1] <= WINDOW_HEIGHT/2 - 20:
                        self.game_mode = "1P"
                        self.game_state = "PLAYING"
                        self.reset_game()
                    # 2P button
                    elif WINDOW_HEIGHT/2 <= mouse_pos[1] <= WINDOW_HEIGHT/2 + 40:
                        self.game_mode = "2P"
                        self.game_state = "PLAYING"
                        self.reset_game()
                    # Quit button
                    elif WINDOW_HEIGHT/2 + 60 <= mouse_pos[1] <= WINDOW_HEIGHT/2 + 100:
                        pygame.quit()
                        sys.exit()
        
    def handle_game_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Player 1 controls
                if event.key in P1_CONTROLS and self.snake1.direction != self.get_opposite_direction(P1_CONTROLS[event.key]):
                    self.snake1.direction = P1_CONTROLS[event.key]
                # Player 2 controls
                if self.game_mode == "2P" and event.key in P2_CONTROLS and self.snake2.direction != self.get_opposite_direction(P2_CONTROLS[event.key]):
                    self.snake2.direction = P2_CONTROLS[event.key]
    
    def get_opposite_direction(self, direction):
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        return opposites.get(direction, "")
    
    def check_collision(self, snake, player_num):
        # Snake eats food
        if snake.body[0] == self.food.position:
            snake.grow()
            self.food.randomize_position()
            self.score[player_num-1] += NORMAL_FOOD_SCORE
            self.sound_manager.play_collect_sound()
        
        # Snake collects power-up
        if self.power_up.active and snake.body[0] == self.power_up.position:
            power_up_type = self.power_up.collect()
            snake.activate_power_up(power_up_type, pygame.time.get_ticks())
            self.score[player_num-1] += SPEED_BOOST_SCORE
            self.sound_manager.play_power_up_sound()
            
        # Snake hits wall
        if not snake.ghost_mode:
            if not (0 <= snake.body[0][0] < WINDOW_WIDTH and 0 <= snake.body[0][1] < WINDOW_HEIGHT):
                return True
            
        # Snake hits obstacles
        if not snake.ghost_mode and not snake.shield_mode and snake.body[0] in self.obstacles.positions:
            return True
            
        # Snake hits itself or other snake
        if snake.body[0] in snake.body[1:]:
            return True
            
        if self.game_mode == "2P":
            other_snake = self.snake2 if player_num == 1 else self.snake1
            if snake.body[0] in other_snake.body:
                return True
                
        return False
    
    def draw_menu(self):
        self.screen.fill(BLACK)
        title = self.game_font.render("Snake Game", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 120))
        self.screen.blit(title, title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # 1P button
        self.draw_button("1 Player", 
            (WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 - 60),
            WINDOW_WIDTH/2 - 100 <= mouse_pos[0] <= WINDOW_WIDTH/2 + 100 and \
            WINDOW_HEIGHT/2 - 60 <= mouse_pos[1] <= WINDOW_HEIGHT/2 - 20)
            
        # 2P button
        self.draw_button("2 Players", 
            (WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2),
            WINDOW_WIDTH/2 - 100 <= mouse_pos[0] <= WINDOW_WIDTH/2 + 100 and \
            WINDOW_HEIGHT/2 <= mouse_pos[1] <= WINDOW_HEIGHT/2 + 40)
            
        # Quit button
        self.draw_button("Quit", 
            (WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 + 60),
            WINDOW_WIDTH/2 - 100 <= mouse_pos[0] <= WINDOW_WIDTH/2 + 100 and \
            WINDOW_HEIGHT/2 + 60 <= mouse_pos[1] <= WINDOW_HEIGHT/2 + 100)
    
    def draw_button(self, text, position, hover=False):
        button_rect = pygame.Rect(position[0], position[1], MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
        color = GRAY if hover else (80, 80, 80)
        pygame.draw.rect(self.screen, color, button_rect)
        pygame.draw.rect(self.screen, WHITE, button_rect, 2)
        
        button_text = self.game_font.render(text, True, WHITE)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, text_rect)
        return button_rect
    
    def draw_game_over_screen(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        if self.game_mode == "1P":
            game_over_text = self.game_font.render(f"Game Over! Score: {self.score[0]}", True, WHITE)
        else:
            winner = "Player 1" if self.score[0] > self.score[1] else "Player 2" if self.score[1] > self.score[0] else "Tie"
            game_over_text = self.game_font.render(f"Game Over! {winner} wins!", True, WHITE)
            scores_text = self.game_font.render(f"P1: {self.score[0]} - P2: {self.score[1]}", True, WHITE)
            scores_rect = scores_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
            self.screen.blit(scores_text, scores_rect)
        
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 60))
        self.screen.blit(game_over_text, text_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Menu button
        self.draw_button("Menu", 
            (WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 + 20),
            WINDOW_WIDTH/2 - 100 <= mouse_pos[0] <= WINDOW_WIDTH/2 + 100 and \
            WINDOW_HEIGHT/2 + 20 <= mouse_pos[1] <= WINDOW_HEIGHT/2 + 60)
        
        # Quit button
        self.draw_button("Quit", 
            (WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 + 80),
            WINDOW_WIDTH/2 - 100 <= mouse_pos[0] <= WINDOW_WIDTH/2 + 100 and \
            WINDOW_HEIGHT/2 + 80 <= mouse_pos[1] <= WINDOW_HEIGHT/2 + 120)
    
    def draw_score(self):
        if self.game_mode == "1P":
            score_text = self.game_font.render(f"Score: {self.score[0]}", True, WHITE)
            self.screen.blit(score_text, (20, 20))
        else:
            p1_score = self.game_font.render(f"P1: {self.score[0]}", True, GREEN)
            p2_score = self.game_font.render(f"P2: {self.score[1]}", True, RED)
            self.screen.blit(p1_score, (20, 20))
            self.screen.blit(p2_score, (WINDOW_WIDTH - 120, 20))
        
        # Draw power-up status for P1
        y_offset = 60
        if self.snake1.speed_boost:
            status_text = self.game_font.render("Speed Boost!", True, BLUE)
            self.screen.blit(status_text, (20, y_offset))
            y_offset += 40
        if self.snake1.ghost_mode:
            status_text = self.game_font.render("Ghost Mode!", True, PURPLE)
            self.screen.blit(status_text, (20, y_offset))
            y_offset += 40
        if self.snake1.shield_mode:
            status_text = self.game_font.render("Shield!", True, CYAN)
            self.screen.blit(status_text, (20, y_offset))
        
        # Draw power-up status for P2 if in 2P mode
        if self.game_mode == "2P":
            y_offset = 60
            if self.snake2.speed_boost:
                status_text = self.game_font.render("Speed Boost!", True, BLUE)
                self.screen.blit(status_text, (WINDOW_WIDTH - 200, y_offset))
                y_offset += 40
            if self.snake2.ghost_mode:
                status_text = self.game_font.render("Ghost Mode!", True, PURPLE)
                self.screen.blit(status_text, (WINDOW_WIDTH - 200, y_offset))
                y_offset += 40
            if self.snake2.shield_mode:
                status_text = self.game_font.render("Shield!", True, CYAN)
                self.screen.blit(status_text, (WINDOW_WIDTH - 200, y_offset))
    
    def handle_game_over_input(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Menu button
                if WINDOW_WIDTH/2 - 100 <= mouse_pos[0] <= WINDOW_WIDTH/2 + 100 and \
                   WINDOW_HEIGHT/2 + 20 <= mouse_pos[1] <= WINDOW_HEIGHT/2 + 60:
                    self.game_state = "MENU"
                # Quit button
                elif WINDOW_WIDTH/2 - 100 <= mouse_pos[0] <= WINDOW_WIDTH/2 + 100 and \
                     WINDOW_HEIGHT/2 + 80 <= mouse_pos[1] <= WINDOW_HEIGHT/2 + 120:
                    pygame.quit()
                    sys.exit()
    
    def run(self):
        while True:
            # Initialize game_speed with default value
            game_speed = 60  # Default FPS for MENU and GAME_OVER states

            if self.game_state == "MENU":
                self.handle_menu_input()
                self.draw_menu()
            
            elif self.game_state == "PLAYING":
                self.handle_game_input()
                
                # Update game_speed based on power-ups
                game_speed = GAME_SPEED * 2 if self.snake1.speed_boost else GAME_SPEED
                
                # Update snakes
                self.snake1.move()
                self.snake1.update_power_ups(pygame.time.get_ticks())
                if self.game_mode == "2P":
                    self.snake2.move()
                    self.snake2.update_power_ups(pygame.time.get_ticks())
                
                self.power_up.spawn_power_up()
                
                # Check collisions
                if self.check_collision(self.snake1, 1) or \
                   (self.game_mode == "2P" and self.check_collision(self.snake2, 2)):
                    self.sound_manager.play_game_over_sound()
                    self.game_state = "GAME_OVER"
                
                # Draw game elements
                self.screen.fill(BLACK)
                self.snake1.draw(self.screen)
                if self.game_mode == "2P":
                    self.snake2.draw(self.screen)
                self.food.draw(self.screen)
                self.power_up.draw(self.screen)
                self.obstacles.draw(self.screen)
                self.draw_score()
            
            elif self.game_state == "GAME_OVER":
                self.handle_game_over_input()
                self.draw_game_over_screen()
            
            pygame.display.flip()
            self.clock.tick(game_speed)

if __name__ == "__main__":
    game = Game()
    game.run() 