import pygame
from settings import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.selected = 0
        self.options = ['1 Player', '2 Players', 'Quit']
        
    def draw_button(self, text, position, selected):
        button_rect = pygame.Rect(
            position[0],
            position[1],
            MENU_BUTTON_WIDTH,
            MENU_BUTTON_HEIGHT
        )
        
        # Draw button background
        color = (100, 100, 100) if selected else (80, 80, 80)
        pygame.draw.rect(self.screen, color, button_rect)
        pygame.draw.rect(self.screen, WHITE, button_rect, 2)
        
        # Draw text
        text_surface = self.font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        
        return button_rect
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw title
        title = self.font.render("Snake Game", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/4))
        self.screen.blit(title, title_rect)
        
        # Draw menu options
        button_y = WINDOW_HEIGHT/2
        self.button_rects = []
        
        for i, option in enumerate(self.options):
            button_rect = self.draw_button(
                option,
                (WINDOW_WIDTH/2 - MENU_BUTTON_WIDTH/2, button_y),
                i == self.selected
            )
            self.button_rects.append(button_rect)
            button_y += MENU_BUTTON_HEIGHT + MENU_BUTTON_PADDING
        
        pygame.display.flip()
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected]
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, rect in enumerate(self.button_rects):
                if rect.collidepoint(mouse_pos):
                    return self.options[i]
        
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for i, rect in enumerate(self.button_rects):
                if rect.collidepoint(mouse_pos):
                    self.selected = i
        
        return None 