import pygame
from constants import SCREEN_WIDTH
from functions import exit_msg
from gamedata import settings
from resources import background, font32, font64, screen, surface

class Menu:
    def __init__(self, title, options=None):
        self.title = title                      # title at the top of menu
        self.options = []                       # List of tuples: [(label, action_or_tuple), ...]
        self.current_selection = 0              # first option highlighted
        self.title_font = font64                # larger for title
        self.option_font = font32               # smaller for menu items
        self.parent = None                      # Reference to parent menu
        if options:
            self.add_options(options)                   # need to define the add_options method

    def add_options(self, options):
        for option in options:
            if isinstance(option[1], Menu):
                option[1].parent = self  # Set parent reference
            self.options.append(option)

    def update_visibility(self, is_paused=False):
        new_options = []
        for label, action, _ in self.options:                           # Update visibility flags based on game state
            visible = True                                              # Set default (visible)
            if is_paused and action == "start": visible = False         # Hide "New Game" when paused
            if is_paused and action == "quit": visible = False          # Hide "Exit" when paused
            if not is_paused and action == "resume": visible = False    # Hide "Resume" when not paused
            if not is_paused and action == "end": visible = False       # Hide "Resume" when not paused
            new_options.append((label, action, visible))
        self.options = new_options                                      

    def get_visible_options(self):                                      # Return a list of (label, action) tuples with only visible options
        return [(label, action) for label, action, visible in self.options if visible]

    def adjust_selection(self):
        self.current_selection = 0
        while not self.options[self.current_selection][2]:
            self.current_selection += 1

    def handle_menu_loop(self):
        self.current_selection=0
        menu_active = True
        while menu_active:                                                                          # Loop to keep menu active
            for event in pygame.event.get():                                                        # Get user input & process it
                if event.type == pygame.QUIT:                                                       # Game killed with x on window
                    exit_msg(settings)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:                      # Move selection
                        direction = -1 if event.key == pygame.K_UP else 1                           # Previous or next
                        visible_options = self.get_visible_options()                                # Consider only visible options
                        self.current_selection = (self.current_selection + direction) % len(visible_options)
                    elif event.key == pygame.K_RETURN:
                        visible_options = self.get_visible_options()
                        selected_option = visible_options[self.current_selection][1]                        
                        if isinstance(selected_option, Menu):
                            return selected_option.handle_menu_loop()                              # Enter submenu (recursively call handler)
                        elif callable(selected_option):
                            selected_option()
                        else:
                            return selected_option                                                  # Return the action
                    elif event.key == pygame.K_ESCAPE and self.parent:
                        return "back"

                self.draw_menu()
                pygame.display.flip()

    def draw_menu(self):
        
        screen.blit(background, (0,0))                                                          # First, ensure the game is still visible
        screen.blit(surface, (0,0))                                                             # This shows your game objects behind the transparent menu

        menu_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)                       # Create a surface for the menu to be drawn upon
        menu_surface.fill((0, 0, 0, 128))                                                       # Fill surface with transparent 50% transaprent black
        title_surface = self.title_font.render(self.title, True, (255, 255, 255))               # Render title (full white)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))                    # Create title surface, x:centre of screen, 100 pixels from top
        menu_surface.blit(title_surface, title_rect)                                            # Blit title to menu surface

        visible_options = self.get_visible_options()                                            # Get only visible options for drawing

        option_y = 250                                                                          # Starting y position for first option
        for i, option in enumerate(visible_options):                                            # Draw options in a loop
            color = (255, 255, 0) if i == self.current_selection else (255, 255, 255)           # Highlight selected option
            text = f"< {option[0]} >" if isinstance(option[1], Menu) else option[0]             # Put < ... > around submenu's
            option_surface = self.option_font.render(text, True, color)                         # Render the option text
            option_rect = option_surface.get_rect(center=(screen.get_width() // 2, option_y))   # Create option surface, x:centre of screen, 250+i*50 pixels from top
            menu_surface.blit(option_surface, option_rect)                                      # Blit option to the menu surface
            option_y += 50                                                                      # Space between options                                             

        screen.blit(menu_surface, (0, 0))                                                       # Blit the complete menu to the screen

