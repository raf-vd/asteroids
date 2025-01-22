import pygame
import random
from asteroid import LumpyAsteroid
from constants import *

class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y, z: pygame.Vector2(-ASTEROID_MIN_RADIUS * z, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y, z: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MIN_RADIUS * z, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x, z: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MIN_RADIUS * z),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x, z: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MIN_RADIUS * z
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity, special=False, max_lumps=6):
        asteroid = LumpyAsteroid(position.x, position.y, radius, special, max_lumps)
        asteroid.velocity = velocity

    def super_spawn(self, count, factor):
        if count < 2: count = 2                                         # Force at least double spawn 
        for i in range(count):
            # Asteroid will have a radius that is half the min size and will have more lumps
            # This will make them much harder to kill at higher levels
            self.__generate_asteroid(True, 6 + int(count / 3))   

    def __generate_asteroid(self, special=False, max_lumps=6):
        edge = random.choice(self.edges)
        speed = random.randint(40, 100)
        velocity = edge[0] * speed
        velocity = velocity.rotate(random.randint(-30, 30))
        if special: 
            kind = 0.5
        else:
            kind = random.randint(1, ASTEROID_KINDS)
        position = edge[1](random.uniform(0, 1), kind)
        self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity, special, max_lumps)

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            self.__generate_asteroid()
