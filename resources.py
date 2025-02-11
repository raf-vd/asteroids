import pygame
import os
import sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

# Ensure dynamic pathing works
def resource_path(relative_path):
    """ Get absolute path to resource; works for development and PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

# Game mechanics
if True:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    clock = pygame.time.Clock()

# Sound 
if True:
    pygame.mixer.init(44100, -16, 2, 2048)
    alert_channel = pygame.mixer.Channel(1)
    shield_channel = pygame.mixer.Channel(2)
    shot_channel = pygame.mixer.Channel(3)
    asteroid_break_channel = pygame.mixer.Channel(4)
    game_sounds = pygame.mixer.Channel(5)
    # Sounds
  # relative location
    alert_sound_path = resource_path("sound/alarm.mp3")
    crack_lump_sound_path = resource_path("sound/crack.wav")
    crack_main_sound_path = resource_path("sound/explosion.mp3")
    game_over_sound_path = resource_path("sound/game_over.mp3")
    level_up_sound_path = resource_path("sound/shroom_up.mp3")
    player_death_sound_path = resource_path("sound/crash.mp3")
    shield_hit_sound_path = resource_path("sound/buzz.mp3")
    shot_sound_path = resource_path("sound/shot.wav")
    hitboss_path = resource_path("sound/hitboss.wav")
    # Music
    background_music = resource_path("sound/space_music.mp3")

  # dynamic pathing
    alert_sound = pygame.mixer.Sound(alert_sound_path) 
    crack_lump_sound = pygame.mixer.Sound(crack_lump_sound_path)
    crack_main_sound = pygame.mixer.Sound(crack_main_sound_path)
    game_over_sound = pygame.mixer.Sound(game_over_sound_path)
    level_up_sound = pygame.mixer.Sound(level_up_sound_path)
    player_death_sound = pygame.mixer.Sound(player_death_sound_path)
    shield_hit_sound = pygame.mixer.Sound(shield_hit_sound_path)
    shot_sound = pygame.mixer.Sound(shot_sound_path)
    hitboss_sound = pygame.mixer.Sound(hitboss_path)
    # Music
    background_music = pygame.mixer.music.load(background_music)
  # Volume control  
    alert_sound.set_volume(0.5)
    crack_lump_sound.set_volume(0.3)
    crack_main_sound.set_volume(0.6)
    shot_sound.set_volume(0.2)
    hitboss_sound.set_volume(0.2)
    pygame.mixer.music.set_volume(0.10)

# Fonts
if True:
    # FreeSans_otf = resource_path("font/FreeSans.otf")
    FreeSansBold_otf = resource_path("font/FreeSansBold.otf")

    pygame.font.init()
    font64 = pygame.font.Font(None, 64)
    font48 = pygame.font.Font(None, 48)  
    font36 = pygame.font.Font(None, 36)
    font32 = pygame.font.Font(None, 32)
    font24 = pygame.font.Font(None, 24)
    font20 = pygame.font.Font(None, 20)
    # font20_fs = pygame.font.Font(FreeSans_otf, 20)  # For unicode characters support (arrow keys)
    font20_fsb = pygame.font.Font(FreeSansBold_otf, 20)  # For unicode characters support (arrow keys)

# Frame loading mechanic (dynamic pathing included)
if True:
    def load_frames(number_of_frames, frame_names, extension):
        frames = []
        for i in range(number_of_frames): # load 5 instead of available 9 for shorter animation
            frame_path = resource_path(f"{frame_names}{i:02d}.{extension}")
            frame = pygame.image.load(frame_path).convert_alpha()
            frame = pygame.transform.scale(frame, (frame.get_width() / 4, frame.get_height() / 4))  # originals are too big, repplace by smaller ones later
            frames.append(frame)
        return frames

# Images    
  # relative location
    background_path = resource_path("image/space.jpg")
    boss_image_path = resource_path("image/boss_try2.png")
    player_image_path = resource_path("image/ship2.png")
    speedometer_image_path = resource_path("image/speedometer.png")
    needle_image_path = resource_path("image/needle_centered.png")
    broken_speedometer_path = resource_path("image/broken_glass_circle.png")

  # dynamic pathing
    background = pygame.image.load(background_path)
    boss_image = pygame.image.load(boss_image_path).convert_alpha()
    boss_image = pygame.transform.scale(boss_image, (500, 150))
    player_image = pygame.image.load(player_image_path).convert_alpha()
    player_image = pygame.transform.scale(player_image, (40, 55))
    speedometer_image = pygame.image.load(speedometer_image_path).convert_alpha()
    speedometer_image = pygame.transform.scale(speedometer_image, (225, 105))
    needle_image = pygame.image.load(needle_image_path).convert_alpha()
    needle_image = pygame.transform.scale(needle_image, (160, 10))
    broken_speedometer = pygame.image.load(broken_speedometer_path).convert_alpha()
    broken_speedometer = pygame.transform.scale(broken_speedometer, (220, 100))

# Frames
    asteroid_frames = load_frames(6, "image/asteroid/asteroid", "png")
    boss_bullet_frames = load_frames(8, "image/bullet/bbullet", "png")
    explosion_frames = load_frames(9, "image/explosion/explosion", "png")
    piercing_shot_frames = load_frames(9, "image/explosion/flash", "png")
    player_explosion_frames = load_frames(25, "image/explosion/whitePuff", "png")
    shot_frames = load_frames(9, "image/explosion/fart", "png")
