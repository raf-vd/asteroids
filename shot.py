import pygame
from constants import *
from resources import screen, shot_sound
from circleshape import CircleShape

class Shot(CircleShape):

    piercing_active = False
    shot_size_multiplier = 1

    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS * Shot.shot_size_multiplier)
        shot_sound.play()
        self.pierce = Shot.piercing_active

    def reset_class_variables():            # Method to be able to reset Shot class variables
        Shot.piercing_active = False
        Shot.shot_size_multiplier = 1

    def draw(self):
        if self.is_off_screen():
            self.kill()
        else:
            pygame.draw.circle(screen, "lightcyan" if self.pierce else "cyan", self.position, self.radius , 0 if self.pierce else 2)

    def update(self, dt):
        self.position += self.velocity * dt

