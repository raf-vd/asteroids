import pygame
from resources import explosion_frames, screen

class Explosion(pygame.sprite.Sprite):

    def __init__(self, position, shrinkfactor, frames=explosion_frames):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.__shrinkfactor = shrinkfactor
        self.frames = frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.image = self.__resize_image()
        self.rect = self.image.get_rect(center=position)
        self.animation_speed = 0.05
        self.timer = 0

    def __resize_image(self):
        rs_w = self.image.get_width() * self.__shrinkfactor
        rs_h = self.image.get_height() * self.__shrinkfactor
        img = pygame.transform.scale(self.image, (rs_w, rs_h)) 
        return img

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.animation_speed:
            self.timer = 0
            self.current_frame += 1
            if self.current_frame < len(self.frames):
                self.image = self.frames[self.current_frame]
                self.image = self.__resize_image()
            else:
                self.kill()  # Remove the explosion sprite when the animation ends

    def draw(self):
        screen.blit(self.image, self.rect)

