import pygame
from constants import *
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        if self.is_off_screen(screen):
            self.kill()
        else:
            pygame.draw.circle(screen, "blue", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt
            
