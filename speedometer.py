import pygame
from constants import PLAYER_MAXIMUM_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH
from resources import broken_speedometer, needle_image, speedometer_image, surface

class Speedometer:
    def __init__(self, speed=0):
        self.meter_x = SCREEN_WIDTH - speedometer_image.get_width()                         # Coords for the dial background
        self.meter_y = SCREEN_HEIGHT - speedometer_image.get_height()
        self.center_x = SCREEN_WIDTH - 35 - (needle_image.get_width() / 2)                  # Coords for the centre of the needle 
        self.center_y = SCREEN_HEIGHT - needle_image.get_height()
        self.speed = speed                                                                  # Speed = 0 at start
        self.angle = 0                                                                      # Angle = 0 at start

    def update(self, speed):
        self.speed = speed.magnitude()                                                      # Receive the new speed
        self.angle = - (180 * (self.speed / PLAYER_MAXIMUM_SPEED))                          # Calculate sppeed as % of angle

    def draw(self, broken=False):
        back = pygame.Surface((speedometer_image.get_width(), speedometer_image.get_height() + 7), pygame.SRCALPHA) # Create surface to draw red background (slightly larger than the image to create some room for drawing around it)
        intensity = int(75 * (self.speed / PLAYER_MAXIMUM_SPEED))                                                   # Scale intensity from 0 to 75

        center = (back.get_width() // 2, back.get_height())                                 # Draw a filled circle on the background
        radius = (0.97 * back.get_width()) // 2 
        pygame.draw.circle(back, (255, 0, 0, intensity), center, radius)                    
        pygame.draw.circle(back, (25, 25, 0, 128), center, radius + 2, 4)                    # Draw a border circle on the background
        surface.blit(back, (self.meter_x, self.meter_y))

        surface.blit(speedometer_image, (self.meter_x, self.meter_y))                       # Draw the background dial
        rotated_needle = pygame.transform.rotate(needle_image, self.angle)                  # Rotate the needle image based on the current angle
        rotated_rect = rotated_needle.get_rect(center=(self.center_x, self.center_y))       # Get the rotated image's rect
        surface.blit(rotated_needle, rotated_rect.topleft)                                  # Blit the rotated needle on the surface

        if broken:                                                                          
            surface.blit(broken_speedometer, (self.meter_x + 5, self.meter_y + 5))          # Overlay broken glass       

