import pygame
import random
import math
from constants import *
from circleshape import CircleShape
from explosion import Explosion


class LumpyAsteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.lumps = self.generate_random_lumps()
        self.score_value = 1800 / self.radius

    def draw(self, screen):
        self.wrap_screen(screen)
        pygame.draw.circle(screen, self.get_colour(), self.position, self.radius, 0)
        for lump in self.lumps:
            pygame.draw.circle(screen, self.get_colour(), lump.position, lump.radius, 0)

    def update(self, dt):
        self.position +=  self.velocity * dt * LumpyAsteroid.velocity_multiplier
        for lump in self.lumps:
            lump.position +=  self.velocity * dt * LumpyAsteroid.velocity_multiplier

    def get_colour(self):
        if self.radius == ASTEROID_MAX_RADIUS:
            return "yellow"
        elif self.radius > ASTEROID_MIN_RADIUS:
            return "orange"
        else:
            return "red"

    def generate_random_lumps(self):
        num_lumps = random.randint(3, 6)
        lumps = []

        # base angle for even spacing of lumps
        angle_step = (2 * math.pi) / num_lumps

        for i in range(num_lumps):
            # base angle + small random variation
            angle = (i * angle_step) + random.uniform(-0.2, 0.2)
            # calculate offset from centre of main body's centre
            offset_distance = self.radius * 0.8  
            dx = offset_distance * math.cos(angle)
            dy = offset_distance * math.sin(angle)
            # make sure the lump sticks out (enough)
            distance_to_edge = self.radius - offset_distance
            min_lump_radius = distance_to_edge + 10
            max_lump_radius = self.radius * ASTEROID_MAX_LUMP_SIZE
            lump_radius = random.uniform(min_lump_radius, max_lump_radius)

            # create the lump
            lumps.append(CircleShape(self.position.x + dx, self.position.y + dy, lump_radius))

        # return list of lumps
        return lumps

    def split(self):
        Explosion(self.position)  # asteroid.rect.center gives the position
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return False #asteroid destroyed
        random_angle = random.uniform(20, 50)
        direction_1 = self.velocity.rotate(random_angle)
        direction_2 = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        new_asteroid_1 = LumpyAsteroid(self.position.x, self.position.y, new_radius)
        new_asteroid_2 = LumpyAsteroid(self.position.x, self.position.y, new_radius)
        new_asteroid_1.velocity = direction_1 * 1.2
        new_asteroid_2.velocity = direction_2 * 1.2
        return True #asteroid split

    def check_collision(self, other):
        if super().check_collision(other):
            return -1
        for lump in self.lumps:
            if lump.check_collision(other):
                return self.lumps.index(lump)
        return -2

    def wrap_screen(self, screen):
        # Store original position
        old_x = self.position.x
        old_y = self.position.y

        # Wrap main body
        super().wrap_screen(screen)
        
        # If position changed, update all lumps by the same amount
        if old_x != self.position.x or old_y != self.position.y:
            dx = self.position.x - old_x
            dy = self.position.y - old_y
            for lump in self.lumps:
                lump.position.x += dx
                lump.position.y += dy

