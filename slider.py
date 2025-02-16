from functions import get_lighter_color
from resources import font20

import pygame

class Slider:
    def __init__(self, x, y, width, text_value, value=100, max_value=100, height=30, base_color=(100,100,100), border=2, highlight_border=1):
        # Base attributes
        self.__current_value = value
        self.__max_value = max_value
        self.__text_value = text_value
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border = border
        self.hlw = highlight_border
        self.highlighted = False
        self.base_color = base_color
        self.value_color = get_lighter_color(base_color)
        self.highlight_color = get_lighter_color(base_color, 0.8)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

    def draw(self, surface):
        self.surface.fill((0, 0, 0, 0))                                                                                 # Clear with transparent color since we're using SRCALPHA
        pygame.draw.rect(self.surface, self.base_color, self.surface.get_rect(), self.border)                           # Draw a ractangle inside/at the edge of the base surface
        value_surface = pygame.Surface((self.get_value_width(), self.height - 2* self.border), pygame.SRCALPHA)         # Create surface for value with same height as base surface minus the space needed for the border
        value_surface.fill(self.value_color)                                                                            # Fill surface for value with lighter color derived from base color
        self.surface.blit(value_surface, (self.border, self.border))                                                    # Blit the value on the base surface inside the border rectangle
        self.surface.blit(font20.render(self.text_value(), True, (0,0,0)), (self.border+5, self.border+5))              # Blit the text value and the numeric value inside the slider
        surface.blit(self.surface, (self.x, self.y))                                                                    # Blit the finished base surface on the target surface at the desired coordinates
        if self.highlighted:
            rect = pygame.Rect(self.x - self.hlw, self.y - self.hlw,                                                    
                               self.width + self.hlw * 2, self.height + self.hlw * 2)                                   # Get the correct rect dimensions
            pygame.draw.rect(surface, self.highlight_color, rect, self.hlw)                                             # Create highlight rectangle
            
        
    def get_value(self):
        return self.__current_value
    
    def get_value_width(self):
        return (self.__current_value / self.__max_value) * (self.width - 2 * self.border)
    
    def set_value(self, value):
        self.__current_value = max(0, min(value, self.__max_value))     # Limit the values for the slider to it's limits

    def text_value(self):
        return f"{self.__text_value}: {int(100* self.get_value())}"

    def handle_event(self, event):
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):                      # Handle mouse events
            mouse_pos = pygame.mouse.get_pos()                                              # Get cursor position
            self.highlighted = False                                                        # Reset highlighted parameter
            if (self.x <= mouse_pos[0] <= self.x + self.width and                           # Check if mouse is within slider bounds
                self.y <= mouse_pos[1] <= self.y + self.height):
                if event.type == pygame.MOUSEMOTION:                                        # Show highlight border when mouseover
                    self.highlighted = True
                if event.type == pygame.MOUSEBUTTONDOWN:                                    # Adjust value when clicking inside the slider
                    relative_x = mouse_pos[0] - self.x
                    new_value = (relative_x / self.width) * self.__max_value
                    if new_value > self.__max_value * 0.95: new_value = self.__max_value    # 'Snap to' 100% to deal with narrow slider edge
                    if new_value < self.__max_value * 0.05: new_value = 0                   # 'Snap to' 0%   to deal with narrow slider edge   
                    self.set_value(new_value)

