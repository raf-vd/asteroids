import pygame
from functions import create_circle_mask
from constants import *
from resources import screen

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
        self.mask = create_circle_mask(self.radius)             # Create a mask from the non-transparent pixel on the circle, better match than animated images mask

    def draw(self, screen): # sub-classes must override
        pass

    def update(self, dt): # sub-classes must override
        pass

    def check_collision(self, other): # Circle ti circle collision check
        distance = self.position.distance_to(other.position)
        return distance <= self.radius + other.radius

    def circle_vs_rect(self, rect): # Circle to Rectangle collision check
        expanded_rect = rect.inflate(self.radius * 2,self.radius * 2)           # Expanded rectangle to include the circle’s radius
        return expanded_rect.collidepoint(self.position.x, self.position.y)     # Returns true if point is on rect

    def circle_vs_mask(self, mask, mask_rect):
        offset_x = int(self.position.x - mask_rect.x - self.radius)     # Offset for the overlap: center the bullet relative to the boss rect
        offset_y = int(self.position.y - mask_rect.y - self.radius)        
        point = mask.overlap(self.mask, (offset_x, offset_y))           # Check for overlap between the bullet's circle mask and the given mask
        return point is not None                                        # True if hitpoint is returned
    
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
        if self.position.x < x:     self.position.x = min(self.position.x + speed, x)               #  50 < 100 =>  53 = min( 50 + 3, 100)
        elif self.position.x > x:   self.position.x = max(self.position.x - speed, x)               # 150 > 100 => 147 = max(150 - 3, 100)
        if self.position.y < y:     self.position.y = min(self.position.y + speed, y ) 
        elif self.position.y > y:   self.position.y = max(self.position.y - speed, y)            
        # print(f"MAIN: Started at: ({old_x},{old_y} \t moved to: ({old_x},{old_y}) \t destination: ({x},{y})")
        # ASTEROIDS
        if hasattr(self, "lumps"):          # Asteroid move lumps according to main body
            for lump in self.lumps:
                if old_x < x:       lump.position.x = lump.position.x + (self.position.x - old_x)   #  50 < 100 =>  63 =  60 + ( 53 -  50) 
                elif old_x > x:     lump.position.x = lump.position.x - (old_x - self.position.x)   # 150 > 100 => 157 = 160 - (150 - 147) 
                if old_y < y:       lump.position.y = lump.position.y + (self.position.y - old_y)
                elif old_y > y:     lump.position.y = lump.position.y - (old_y - self.position.y)

        # PLAYERS
        if hasattr(self, "angle"):          # Face player upwards (work on base angle (<360) by using %)
            self.angle %= 360
            if self.angle < angle:    self.angle = min(self.angle + 1, angle)
            elif self.angle > angle:  self.angle = max(self.angle - 1, angle)

        # Reset velocity
        self.velocity = pygame.Vector2(0, 0)        
