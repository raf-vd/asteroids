import pygame

class Explosion(pygame.sprite.Sprite):
    __animation_frames = None  # Class variable to store frames

    @classmethod
    def load_frames(cls):
        if cls.__animation_frames is None:  # Only load if not already loaded
            frames = []
            for i in range(5): # load 5 instead of available 9 for shorter animation
                frame_path = f"image/explosion/explosion{i:02d}.png"
                frame = pygame.image.load(frame_path).convert_alpha()
                frame = pygame.transform.scale(frame, (frame.get_width() / 4, frame.get_height() / 4))  # originals are too big, repplace by smaller ones later
                frames.append(frame)
            cls.__animation_frames = frames
        return cls.__animation_frames

    def __init__(self, position, shrinkfactor):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.__shrinkfactor = shrinkfactor
        self.frames = self.load_frames()
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

    def draw(self, screen):
        screen.blit(self.image, self.rect)

