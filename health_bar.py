import pygame
from functions import rect_surface
from resources import surface

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, width, height, max_value, color=(0,75,25,100)):
        super().__init__(self.containers) 
        self.color = color                                                                  # Can be used to set/get a fixed initial color
        # self.image = rect_surface(width, height, (75,0,0,100))
        self.surface = rect_surface(width, height, (0,0,0,0))                               # Surface to rectangle/draw bar on
        self.surfacebar = rect_surface(width, height, self.color)                           # Bar to hold the actual value
        self.rect = self.surface.get_rect()
        self.vertical_offset = -20                                                          # Draw bar a bit above target
        self.max_value = max_value                                                      
        self.current_value = self.max_value                                             

    def update(self, _):
        bar_width = self.surface.get_width() * self.bar_percentage()                            # Recalculate the bar_with in % of max
        self.surfacebar = rect_surface(bar_width, self.surface.get_height(), self.calc_color()) # Recreate bar with new width

    def calc_color(self):                                                                       # Calculate color based on bar
        p = self.bar_percentage()
        red = 255 * (1 - p)
        if p < 0.5:                                                                             # mess with green a bit more at 50%
            green = 150 * p
        else: 
            green = 100 * p                                                                         
        
        return (red, green, 0, 100)

    def bar_percentage(self):
        return self.current_value / self.max_value

    def draw(self, position):
        pygame.draw.rect(self.surface, (255,255,255,50), self.rect, 1)                  # Draw boundary of bar to indicate 'max/total' value
        surface.blit(self.surfacebar, (position.x, position.y + self.vertical_offset))  # Draw actual value inside rectangle
        surface.blit(self.surface, (position.x, position.y + self.vertical_offset))     # Draw surface containing value and rectangle

    def increase(self, value):
        self.current_value = min(self.current_value + value, self.max_value)

    def decrease(self, value):
        self.current_value = max(self.current_value - value, 0)