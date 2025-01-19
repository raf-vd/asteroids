import pygame 

pygame.mixer.init(44100, -16, 2, 2048)
shot_sound = pygame.mixer.Sound("sound/shot.mp3")
crack_lump = pygame.mixer.Sound("sound/crack.mp3")
crack_lump.set_volume(0.2)
crack_main = pygame.mixer.Sound("sound/explosion.mp3")
crack_main.set_volume(0.4)
level_up_sound = pygame.mixer.Sound("sound/shroom_up.mp3")
player_death_sound = pygame.mixer.Sound("sound/crash.mp3")

