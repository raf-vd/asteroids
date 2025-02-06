import pygame
from constants import *
from resources import *
from asteroid import LumpyAsteroid
from boss import Boss, BossBullet
from explosion import Explosion
from asteroidfield import AsteroidField
from shot import Shot
from player import Player
from speedometer import Speedometer

def scale_to_circle(image, circle_radius):
    # Calculate the new size (maintain aspect ratio)
    original_size = image.get_size()
    scale = (circle_radius * 2) / max(original_size)
    new_width = int(original_size[0] * scale)
    new_height = int(original_size[1] * scale)
    
    # Scale the image
    scaled_image = pygame.transform.smoothscale(image, (new_width, new_height))
    return scaled_image
  
def main():
    
    pygame.init()

    updatable = pygame.sprite.Group()                                                           # groups
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    Player.containers = (updatable, drawable)                                                   # containers
    LumpyAsteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (explosions, updatable, drawable)

    # l_asts = [LumpyAsteroid(200,200,50),LumpyAsteroid(500,200,50),LumpyAsteroid(800,200,50),LumpyAsteroid(1100,200,50)]
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    speedometer = Speedometer()

    # boss = Boss((SCREEN_WIDTH - boss_image.get_width())/ 2, -boss_image.get_height() - 10, boss_image)
    boss = None
    dt = 0

    while True:

        surface.fill((0, 0, 0, 0))                          # reset surface
        screen.blit(background, (0,0))                      # show background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:   
                    player.toggle_strafe()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F8:   
                    player.toggle_boss_mode()
                    print(f"F8 pressed boss mode active = {player.boss_active()}")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_PLUS:
                    boss = boss = Boss((SCREEN_WIDTH - boss_image.get_width())/ 2, -boss_image.get_height() - 10, boss_image)
                    # print(f"boss(x,y)={boss.position}\tboss target(x,y)=[{SCREEN_WIDTH / 2}, 125]")
                    # rect = boss.image.get_rect(topleft=boss.position)
                    # print(f"bossCenter(x,y)={rect.center}\tboss target(x,y)=[{SCREEN_WIDTH / 2}, 125]")
                    player.toggle_boss_mode()
                    # print(f"player(x,y)={player.position}\t player target(x,y)=[{SCREEN_WIDTH / 2}, {SCREEN_HEIGHT * 0.9}]")

        if not boss is None:
            boss.update(dt)

        player.update(dt, boss)
        player.draw()

        if not boss is None:
            boss.draw()

        screen.blit(surface, (0, 0))  
        pygame.display.flip()

        dt = clock.tick(FRAME_RATE) / 1000


main()