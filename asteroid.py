import pygame
import random
import math
from constants import *
from functions import apply_tint, scale_to_circle
from resources import asteroid_frames, asteroid_break_channel, crack_lump_sound, crack_main_sound, surface
from circleshape import CircleShape
from explosion import Explosion

class LumpyAsteroid(CircleShape):
    def __init__(self, x, y, radius, special=False, max_lumps=6):
        super().__init__(x, y, radius)
        self.special = special
        self.image = asteroid_frames[random.randint(0,5)]
        self.lumps = self.generate_random_lumps(max_lumps)
        if self.special:
            self.score_value = 0                                # Special asteroids are smaller and have no value => nasty
        else:
            self.score_value = 1800 / self.radius
        self.colour = self.get_colour(random.randint(190, 200))

    def draw(self):
        self.wrap_screen()                                                              # Handle asteroid wrapping around screen

        scaled_asteroid = scale_to_circle(self.image, self.radius)                      # Resize base image to match radius
        image_rect = scaled_asteroid.get_rect()
        image_rect.center = (self.position.x, self.position.y)
        tinted_asteroid = apply_tint(scaled_asteroid, self.colour)                      # Tint the image to match asteroid kind
        surface.blit(tinted_asteroid, image_rect)                                       # Blit the image to the surface
        # pygame.draw.circle(surface, (255, 0, 0), (self.position.x, self.position.y), self.radius, 1)      #### VISUAL CHECK, REMOVE WHEN WORKING AS INTENDED  ####
        # pygame.draw.circle(surface, self.colour, self.position, self.radius, 0)                           #### OLD SYSTEM FOR DRAWING ASTEROID                ####

        for lump in self.lumps:
            scaled_lump = scale_to_circle(lump.image, lump.radius)                       # Resize base image to match radius
            image_rect = scaled_lump.get_rect()
            image_rect.center = (lump.position.x, lump.position.y)
            tinted_lump = apply_tint(scaled_lump, lump.colour)                          # Tint the image to match asteroid kind
            surface.blit(tinted_lump, image_rect)                                       # Blit the image to the surface
            # pygame.draw.circle(surface, (255, 0, 0), (lump.position.x, lump.position.y), lump.radius, 1)  #### VISUAL CHECK, REMOVE WHEN WORKING AS INTENDED  ####
            # pygame.draw.circle(surface, lump.colour, lump.position, lump.radius, 0)                       #### OLD SYSTEM FOR DRAWING ASTEROID                ####

    def update(self, dt):
        self.position +=  self.velocity * dt * LumpyAsteroid.velocity_multiplier
        for lump in self.lumps:
            lump.position +=  self.velocity * dt * LumpyAsteroid.velocity_multiplier

    def get_colour(self, transparency=255):
        if self.special:
            return (random.randint(200, 210), random.randint(0, 10), random.randint(200, 210), transparency)

        if self.radius == ASTEROID_MAX_RADIUS:
            # return "yellow"
            return (random.randint(200, 255), random.randint(200, 255), random.randint(0, 50), transparency)
        elif self.radius > ASTEROID_MIN_RADIUS:
            # return "orange"
            return (random.randint(200, 255), random.randint(100, 150), random.randint(0, 50), transparency)
        else:
            # return "red"
            return (random.randint(200,255), random.randint(0, 50), random.randint(0, 50), transparency)

    def generate_random_lumps(self, max_lumps=6):
        num_lumps = random.randint(3, max_lumps)
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
            lumps[-1].colour = self.get_colour(random.randint(180, 210))
            lumps[-1].image = asteroid_frames[random.randint(0,5)]

        # return list of lumps
        return lumps

    def split(self):
        Explosion(self.position, self.radius / ASTEROID_MAX_RADIUS) 
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
        # Note: allow for overlapping sounds, destruction sounds are just cool!
        if super().check_collision(other):
            asteroid_break_channel.play(crack_main_sound)
            return -1
        for lump in self.lumps:
            if lump.check_collision(other):
                asteroid_break_channel.play(crack_lump_sound)
                return self.lumps.index(lump)
        return -2

    def wrap_screen(self):
        # Store original position
        old_x = self.position.x
        old_y = self.position.y

        # Wrap main body
        super().wrap_screen()
        
        # If position changed, update all lumps by the same amount
        if old_x != self.position.x or old_y != self.position.y:
            dx = self.position.x - old_x
            dy = self.position.y - old_y
            for lump in self.lumps:
                lump.position.x += dx
                lump.position.y += dy

