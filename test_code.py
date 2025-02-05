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

    boss = Boss((SCREEN_WIDTH - boss_image.get_width())/ 2, -boss_image.get_height() - 10, boss_image)

    dt = 0

    # In your initialization
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
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_KP_PLUS:
            #         for i in range(10):
            #             particles.append(Particle(50 + random.randint(1, 10),500 + random.randint(10, 20)))

        # for l_ast in l_asts:
        #     l_ast.draw()

        # Check bos-bullet collisions (remeber to do player to LATER)
        # pygame.draw.rect(surface, (255,255,255), boss.image.get_rect(topleft=(boss.position.x, boss.position.y)))
        boss.update(dt)
        for obj in updatable:
            obj.update(dt)
            if isinstance(obj, Shot):
                rect = boss.image.get_rect(topleft=(boss.position.x, boss.position.y))
                if obj.circle_vs_rect(rect):    # naast hitbox (quick check) => geen mask check
                    # if boss.check_collision(obj): 
                    if obj.circle_vs_mask(boss.mask, rect):
                        crack_lump_sound.play()
                        obj.kill()
                        # print("Collision detected!")

        for obj in asteroids:
            if player.collides(obj):                                            # PLAYER COLLISION DETECTION
                if player.lives < 1:                                            
                    pass

        for obj in drawable:
            # if isinstance(obj, Player):
                obj.draw()

        for expl in explosions:
            expl.draw()

        speedometer.update(player.velocity)
        speedometer.draw()

        boss.draw()

        screen.blit(surface, (0, 0))  
        pygame.display.flip()

        dt = clock.tick(FRAME_RATE) / 1000


main()