import pygame
import os
import sys
from constants import MASTER_VOLUME_MAX, SCREEN_HEIGHT, SCREEN_WIDTH
from gamedata import settings

# Ensure dynamic pathing works
def resource_path(relative_path):
    """ Get absolute path to resource; works for development and PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

# Game mechanics
if True:
    clock = pygame.time.Clock()                                                     # Gameloop clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))                 # Game screen
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)        # Game Surface

# Sound 
if True:
    pygame.mixer.init(44100, -16, 2, 2048)
    asteroid_break_channel = pygame.mixer.Channel(1)
    alert_channel = pygame.mixer.Channel(2)
    boss_laser_channel = pygame.mixer.Channel(3)
    game_sounds = pygame.mixer.Channel(4)
    shield_channel = pygame.mixer.Channel(5)
    shot_channel = pygame.mixer.Channel(6)
    # Sounds
  # relative location
    alert_sound_path = resource_path("sound/alarm.mp3")
    boss_bullet_sound_path = resource_path('sound/boss_bullet.wav')
    boss_laser_sound_path = resource_path('sound/boss_laser.wav')
    crack_lump_sound_path = resource_path("sound/crack.wav")
    crack_main_sound_path = resource_path("sound/explosion.mp3")
    game_over_sound_path = resource_path("sound/game_over.mp3")
    game_won_sound_path = resource_path("sound/game_won.wav")
    level_up_sound_path = resource_path("sound/shroom_up.mp3")
    player_death_sound_path = resource_path("sound/crash.mp3")
    shield_hit_sound_path = resource_path("sound/buzz.mp3")
    shot_sound_path = resource_path("sound/shot.wav")
    hitboss_path = resource_path("sound/hitboss.wav")
    # Music
    background_music = resource_path("sound/space_music.mp3")

  # dynamic pathing
    alert_sound = pygame.mixer.Sound(alert_sound_path) 
    boss_bullet_sound = pygame.mixer.Sound(boss_bullet_sound_path)
    boss_laser_sound = pygame.mixer.Sound(boss_laser_sound_path)
    crack_lump_sound = pygame.mixer.Sound(crack_lump_sound_path)
    crack_main_sound = pygame.mixer.Sound(crack_main_sound_path)
    game_over_sound = pygame.mixer.Sound(game_over_sound_path)
    game_won_sound = pygame.mixer.Sound(game_won_sound_path)
    hitboss_sound = pygame.mixer.Sound(hitboss_path)
    level_up_sound = pygame.mixer.Sound(level_up_sound_path)
    player_death_sound = pygame.mixer.Sound(player_death_sound_path)
    shield_hit_sound = pygame.mixer.Sound(shield_hit_sound_path)
    shot_sound = pygame.mixer.Sound(shot_sound_path)
    # Music
    background_music = pygame.mixer.music.load(background_music)
    # Volume balancing
    balanced_volumes = {
        alert_sound: 0.5,
        boss_bullet_sound: 0.4,
        boss_laser_sound: 0.8,
        crack_lump_sound: 0.3,
        crack_main_sound: 0.6,
        game_over_sound: 1.0,
        game_won_sound: 1.0,
        hitboss_sound: 0.2,
        level_up_sound: 1.0,
        player_death_sound: 1.0,
        shield_hit_sound: 1.0,
        shot_sound: 0.2,
    }
    # Function to handle a master volume setting
    def apply_master_volume(factor=1.0, music=True, sounds=True):           # optional parameters to reuse code for sound/music control only
        factor = min(factor, 1.0)                                           # Cap factor at 100%
        if sounds:                                                          # Apply to sounds
            for sound, base_volume in balanced_volumes.items():             # Loop sounds in dict
                sound.set_volume(base_volume * factor)                      # Apply new factored volume setting
        if music: pygame.mixer.music.set_volume(0.10 * factor)              # Apply to music mixer
        return factor                                                       # Return factor for storing
    
    def apply_music_volume(factor=1.0):                                     # Adjust only music
        return apply_master_volume(factor, sounds=False)                    # Return value for storing

    def apply_sounds_volume(factor=1.0):                                    # Adjust only sounds
        return apply_master_volume(factor, music=False)                     # Return value for storing

    apply_master_volume(MASTER_VOLUME_MAX * settings.get("master volume"))# Apply initial master volume (90% of max) 
    global_sounds_volume = 1.0                                              # Set 1.0 (already affected by master volume)
    global_music_volume = 1.0                                               # Set 1.0 (already affected by master volume)

    
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
