import pygame
from resources import screen
from constants import *

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):

    velocity_multiplier =  1

    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.colour = (255, 255 , 255 , 255)
        self.image = None

    def draw(self, screen): # sub-classes must override
        pass

    def update(self, dt): # sub-classes must override
        pass

    def check_collision(self, other): # Circle ti circle collision check
        distance = self.position.distance_to(other.position)
        return distance <= self.radius + other.radius

    def circle_vs_rect(self, rect): # Circle to Rectangle collision check
        expanded_rect = rect.inflate(self.radius * 2,self.radius * 2)           # Expanded rectangle to include the circle’s radius
        return expanded_rect.collidepoint(self.position.x, self.position.y)

    # used for killing shots
    def is_off_screen(self):
         return (self.position.x < -ASTEROID_MAX_RADIUS or self.position.x > screen.get_width() + ASTEROID_MAX_RADIUS or
                 self.position.y < -ASTEROID_MAX_RADIUS or self.position.y > screen.get_height() + ASTEROID_MAX_RADIUS) 
    
    # basic circle off-screen wrap
    def wrap_screen(self):
        if self.position.x < 0 - self.radius:
            self.position.x = screen.get_width() + self.radius * 0.9
        elif self.position.x > screen.get_width() + self.radius:
            self.position.x = 0 - self.radius * 0.9
        
        if self.position.y < 0 - self.radius:
            self.position.y = screen.get_height() + self.radius * 0.9
        elif self.position.y > screen.get_height() + self.radius:
            self.position.y = 0 - self.radius * 0.9

    # Move self to a coordinate
    def guide_to_location(self, x, y, angle=180, speed=3): 

        # Code to help with multipart objects
        old_x = self.position.x
        old_y = self.position.y

        # Move CircleShape towards target coordinate
        if self.position.x < x:     self.position.x = min(self.position.x + speed, x) 
        elif self.position.x > x:   self.position.x = max(self.position.x - speed, x)
        if self.position.y < y:     self.position.y = min(self.position.y + speed, y ) 
        elif self.position.y > y:   self.position.y = max(self.position.y - speed, y)            

        # ASTEROIDS
        if hasattr(self, "lumps"):          # Asteroid move lumps according to main body
            for lump in self.lumps:
                if old_x < x:       lump.position.x = lump.position.x + speed
                elif old_x > x:     lump.position.x = lump.position.x - speed
                if old_y < y:       lump.position.y = lump.position.y + speed
                elif old_y > y:     lump.position.y = lump.position.y - speed

        # PLAYERS
        if hasattr(self, "angle"):          # Face player upwards (work on base angle (<360) by using %)
            self.angle %= 360
            if self.angle < angle:    self.angle = min(self.angle + 1, angle)
            elif self.angle > angle:  self.angle = max(self.angle - 1, angle)

        # Remset velocity
        self.velocity = pygame.Vector2(0, 0)        
