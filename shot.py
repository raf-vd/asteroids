import pygame
from constants import *
from resources import piercing_shot_frames, shot_frames, shot_channel, shot_sound, surface
from circleshape import CircleShape

class Shot(CircleShape):

    def __init__(self, x, y, radius=SHOT_RADIUS, piercing=False):
        super().__init__(x, y, radius)
        if shot_channel.get_busy: shot_sound.stop()
        shot_channel.play(shot_sound)
        self.__bulletsize = self.radius * 3.75                   # conversion of the frame to pixels size
        self.pierce = piercing
        self.frames =  piercing_shot_frames if self.pierce else shot_frames
        self.current_frame = 0
        self.image = pygame.transform.scale(self.frames[self.current_frame], (self.__bulletsize, self.__bulletsize))

    def reset_class_variables():            # Method to be able to reset Shot class variables
        Shot.piercing_active = False
        Shot.shot_size_multiplier = 1

    def draw(self):
        if self.is_off_screen():
            self.kill()
        else:
            # keeping this commented out to verify collision with actual radius vs image size
            # pygame.draw.circle(screen, "lightcyan" if self.pierce else "cyan", self.position, self.radius , 0 if self.pierce else 2)
            rect = self.image.get_rect()
            rect.center = self.position
            surface.blit(self.image, rect)

    def update(self, dt):
        self.position += self.velocity * dt
        self.current_frame = (self.current_frame + 1) % len(self.frames)        # Cycle through frames
        self.image = pygame.transform.scale(self.frames[self.current_frame], (self.__bulletsize, self.__bulletsize))    

