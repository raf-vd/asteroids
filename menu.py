import pygame
import sys
from resources import background, font32, font64, surface
from functions import exit_msg

class Menu:
    def __init__(self, title, options):
        self.title = title                      # title at the top of menu
        self.options = options                  # options as list of tuples: [(label, action), ...]
        self.current_selection = 0              # first option highlighted
        self.title_font = font64                # larger for title
        self.option_font = font32               # smaller for menu items

    def handle_menu_loop(self, screen):
        menu_active = True
        while menu_active:                                                                          # Loop to keep menu active
            for event in pygame.event.get():                                                        # Get user input & process it
                if event.type == pygame.QUIT: exit_msg()                                            # Game killed with x on window
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.current_selection = (self.current_selection - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.current_selection = (self.current_selection + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        return self.options[self.current_selection][1]                              # Return the action
                    elif event.key == pygame.K_ESCAPE and self.title != "ASTEROIDS":
                        return "back"                                                               # Only allow escape to work in submenus
                        
            self.draw_menu(screen)
            pygame.display.flip()

    def draw_menu(self, screen):
        # First, ensure the game is still visible
        screen.blit(background, (0,0))
        screen.blit(surface, (0,0))  # This shows your game objects        

        menu_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)                       # Create a surface for the menu to be drawn upon
        menu_surface.fill((0, 0, 0, 128))                                                       # Fill surface with transparent 50£ transaprent black
        title_surface = self.title_font.render(self.title, True, (255, 255, 255))               # Render title (full white)
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 100))              # Create title surface, x:centre of screen, 100 pixels from top
        menu_surface.blit(title_surface, title_rect)                                            # Blit title to menu surface
        
        # Draw options
        option_y = 250                                                                          # Starting y position for first option
        for i, (option_text, _) in enumerate(self.options):
            color = (255, 255, 0) if i == self.current_selection else (255, 255, 255)           # Highlight selected option
            option_surface = self.option_font.render(option_text, True, color)                  # Render the option text
            option_rect = option_surface.get_rect(center=(screen.get_width() // 2, option_y))   # Create option surface, x:centre of screen, 250+i*50 pixels from top
            menu_surface.blit(option_surface, option_rect)                                      # Blit option to the menu surface
            option_y += 50                                                                      # Space between options                                             

        screen.blit(menu_surface, (0, 0))                                                       # Blit the complete menu to the screen

    @classmethod
    def create_main_menu(cls, is_game_paused=False):
        if is_game_paused:
            options = [
                ("Resume", "resume"),                       # When paused, new game is replaced by resume
                ("Controls", "controls"),
                ("Exit", "quit")
            ]
        else:
            options = [
                ("New Game", "start"),                      # When not in game, new game is available and not resume
                ("Controls", "controls"),
                ("Exit", "quit")
            ]
        return cls("ASTEROIDS", options)

    @classmethod
    def create_controls_menu(cls):
        options = [
            ("Back", "back")
        ]
        return cls("CONTROLS", options)