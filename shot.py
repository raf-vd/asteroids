import pygame
from constants import *
from circleshape import CircleShape

pygame.mixer.init(44100, -16, 2, 2048)
shot_sound = pygame.mixer.Sound("sound/shot.mp3")

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        shot_sound.play()

    def draw(self, screen):
        if self.is_off_screen(screen):
            self.kill()
        else:
            pygame.draw.circle(screen, "cyan", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt
            
