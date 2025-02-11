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

    mv_ast = LumpyAsteroid(100,0,25)
    track = 0

    homing_ast = LumpyAsteroid(-24,SCREEN_HEIGHT / 2 , 40)

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
                    boss = Boss((SCREEN_WIDTH - boss_image.get_width())/ 2, -boss_image.get_height() - 10, boss_image)
                    player.toggle_boss_mode()

        if not boss is None:
            boss.update(dt)

        player.update(dt, boss)
        player.draw()

        if not boss is None:
            boss.draw()

        # match track:
        #     case 0: 
        #         mv_ast.guide_to_location(25, 100,speed=1)
        #         if mv_ast.position == (25, 100) : track += 1 
        #     case 1: 
        #         mv_ast.guide_to_location(25,300,speed=3)
        #         if mv_ast.position == (25, 300): track += 1
        #     case 2: 
        #         mv_ast.guide_to_location(125,400,speed=1)
        #         if mv_ast.position == (125, 400): track += 1
        #     case 3: 
        #         mv_ast.guide_to_location(525,600,speed=5)
        #         if mv_ast.position == (525, 600): track += 1
        #     case _: pass
        # mv_ast.draw()

        homing_ast.guide_to_location(player.position.x, player.position.y, speed=1)
        homing_ast.draw()


        screen.blit(surface, (0, 0))  
        pygame.display.flip()

        dt = clock.tick(FRAME_RATE) / 1000


main()