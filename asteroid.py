import pygame
import random
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.score_value = 1800 / self.radius

    def draw(self, screen):
        self.wrap_screen(screen)
        pygame.draw.circle(screen, self.get_colour(), self.position, self.radius, 2)

    def update(self, dt):
        self.position +=  self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        random_angle = random.uniform(20, 50)
        direction_1 = self.velocity.rotate(random_angle)
        direction_2 = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        new_asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid_1.velocity = direction_1 * 1.2
        new_asteroid_2.velocity = direction_2 * 1.2

    def get_colour(self):
        if self.radius == ASTEROID_MAX_RADIUS:
            return "yellow"
        elif self.radius > ASTEROID_MIN_RADIUS:
            return "orange"
        else:
            return "red"