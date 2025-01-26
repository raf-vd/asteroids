import pygame
from constants import *
from resources import screen, piercing_shot_frames, shot_frames, shot_channel, shot_sound
from circleshape import CircleShape

class Shot(CircleShape):

    piercing_active = False
    shot_size_multiplier = 1

    def __init__(self, x, y, frames=shot_frames):
        super().__init__(x, y, SHOT_RADIUS * Shot.shot_size_multiplier)
        if shot_channel.get_busy: shot_sound.stop()
        shot_channel.play(shot_sound)
        self.pierce = Shot.piercing_active
        self.frames = frames
        self.current_frame = 0
        self.image = pygame.transform.scale(self.frames[self.current_frame], (10, 10))


    def reset_class_variables():            # Method to be able to reset Shot class variables
        Shot.piercing_active = False
        Shot.shot_size_multiplier = 1

    def draw(self):
        if self.is_off_screen():
            self.kill()
        else:
            # pygame.draw.circle(screen, "lightcyan" if self.pierce else "cyan", self.position, self.radius , 0 if self.pierce else 2)
            rect = self.image.get_rect()
            rect.center = self.position
            screen.blit(self.image, rect)

    def update(self, dt):
        self.position += self.velocity * dt
        if self.current_frame < len(self.frames)-1:
            self.current_frame += 1
        else:
            self.current_frame = 0
        bulletsize = Shot.shot_size_multiplier * 15
        if self.piercing_active:
            self.frames = piercing_shot_frames
        else:
            self.frames = shot_frames
        self.image = pygame.transform.scale(self.frames[self.current_frame], (bulletsize, bulletsize))
