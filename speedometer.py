import math
import pygame
from constants import PLAYER_MAXIMUM_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH
from resources import surface

class Speedometer:
    def __init__(self):
        # Position in bottom-right corner (adjust as needed)
        self.center_x = SCREEN_WIDTH - 60
        self.center_y = SCREEN_HEIGHT - 60
        self.radius = 50
        
        # Angle ranges for the needle
        self.min_angle = math.pi * 0.75  # 135 degrees
        self.max_angle = math.pi * 0.25  # 45 degrees
        
    def draw(self, velocity):
        # Draw the static background arc
        pygame.draw.arc(surface, (100, 100, 100), 
                       (self.center_x - self.radius, 
                        self.center_y - self.radius,
                        self.radius * 2, self.radius * 2),
                        self.min_angle, self.max_angle, 3)
        
        # Calculate needle angle based on velocity
        speed_ratio = min(1.0, velocity.length() / PLAYER_MAXIMUM_SPEED)
        current_angle = self.min_angle + (self.max_angle - self.min_angle) * speed_ratio
        
        # Draw needle
        end_x = self.center_x + math.cos(current_angle) * (self.radius - 10)
        end_y = self.center_y + math.sin(current_angle) * (self.radius - 10)
        pygame.draw.line(surface, (255, 0, 0), 
                        (self.center_x, self.center_y),
                        (end_x, end_y), 2)