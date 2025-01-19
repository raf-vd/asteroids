import pygame
import sys
import os
from constants import *
from explosion import Explosion
from scoreboard import ScoreBoard
from player import Player
from asteroid import LumpyAsteroid
from asteroidfield import AsteroidField
from shot import Shot

def main(): 
    print("Starting asteroids!")

    pygame.init()
    pygame.font.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background = pygame.image.load("image/space.jpg")

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    LumpyAsteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (explosions, updatable, drawable)

    asteroidfield = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    scoreboard = ScoreBoard(player.lives, STARTING_LEVEL)
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for obj in updatable:    
            obj.update(dt)

        for obj in asteroids:

            for bullet in shots:

                # Check returns -2 for miss,-1 for body hit, index of lump for lump hit
                rc = obj.check_collision(bullet)
                if rc >= -1:
                    score_hit = 0
                    if not bullet.pierce:
                        bullet.kill()
                    if rc > -1:
                        score_hit = (obj.score_value / len(obj.lumps)) / 2
                        del obj.lumps[rc]
                    else:
                        if obj.split():
                            player.activate_upgrade("PIERCING")      # centre of asteroid hit => enable piercing shots
                        else:
                            player.activate_upgrade("BIGGER_SHOT")      # smallest size asteroid centre hit => enable larger shots
                        score_hit = obj.score_value

                    # When add returns True, a new level was reached, and Asteroids will speed up
                    if scoreboard.add(score_hit):                           
                        LumpyAsteroid.velocity_multiplier *= 1 + ASTEROID_VELOCITY_MULTIPLIER
  
            if player.collides(obj):
                if player.lives < 1:
                    print(f"Game over with final score {int(scoreboard.score)} ")
                    sys.exit()
                scoreboard.lose_life()
                print(f"player collided with object at {obj.position.x}, {obj.position.y} and lost a life, new lives: {player.lives}")

        screen.blit(background, (0,0))
        for obj in drawable:
            if not isinstance(obj, Explosion):
                obj.draw(screen)
        for exp in explosions:
            exp.draw(screen)
        scoreboard.update(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
