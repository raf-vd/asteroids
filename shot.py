import pygame
from constants import *
from resources import shot_sound
from circleshape import CircleShape

class Shot(CircleShape):

    piercing_active = False
    shot_size_multiplier = 1

    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS * Shot.shot_size_multiplier)
        shot_sound.play()
        self.pierce = Shot.piercing_active

    def draw(self, screen):
        if self.is_off_screen(screen):
            self.kill()
        else:
            pygame.draw.circle(screen, "lightcyan" if self.pierce else "cyan", self.position, self.radius , 0 if self.pierce else 2)
            #pygame.draw.circle(screen, "cyan", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

