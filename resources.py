import pygame 
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

# Game mechanics
if True:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

# Sound 
if True:
    pygame.mixer.init(44100, -16, 2, 2048)
    shot_sound = pygame.mixer.Sound("sound/shot.mp3")
    crack_lump = pygame.mixer.Sound("sound/crack.mp3")
    crack_lump.set_volume(0.2)
    crack_main = pygame.mixer.Sound("sound/explosion.mp3")
    crack_main.set_volume(0.4)
    level_up_sound = pygame.mixer.Sound("sound/shroom_up.mp3")
    player_death_sound = pygame.mixer.Sound("sound/crash.mp3")

# Fonts
if True:
    pygame.font.init()
    font48 = pygame.font.Font(None, 48)  
    font36 = pygame.font.Font(None, 36)
    font24 = pygame.font.Font(None, 24)
    font20 = pygame.font.Font(None, 20)

# Images
if True:
    def load_frames(number_of_frames, frame_names, extension):
        frames = []
        for i in range(number_of_frames): # load 5 instead of available 9 for shorter animation
            frame_path = f"{frame_names}{i:02d}.{extension}"
            frame = pygame.image.load(frame_path).convert_alpha()
            frame = pygame.transform.scale(frame, (frame.get_width() / 4, frame.get_height() / 4))  # originals are too big, repplace by smaller ones later
            frames.append(frame)
        return frames
    
    background = pygame.image.load("image/space.jpg")
    explosion_frames = load_frames(9, "image/explosion/explosion", "png")
    player_explosion_frames = load_frames(25, "image/explosion/whitePuff", "png")
