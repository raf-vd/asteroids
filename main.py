import pygame
import sys
import os
from scoreboard import ScoreBoard
from player import Player
from asteroid import LumpyAsteroid
from asteroidfield import AsteroidField
from shot import Shot
from constants import *

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

    Player.containers = (updatable, drawable)
    LumpyAsteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

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
                if obj.check_collision(bullet):
                    obj.split()
                    bullet.kill()
                    # When add returns True, a new level was reached, and Asteroids will speed up
                    if scoreboard.add(obj.score_value):   
                        LumpyAsteroid.velocity_multiplier *= 1 + ASTEROID_VELOCITY_MULTIPLIER

            if player.collides(obj):
                if player.lives < 1:
                    print(f"Game over with final score {int(scoreboard.score)} ")
                    sys.exit()
                scoreboard.lose_life()
                print(f"player collided with object at {obj.position.x}, {obj.position.y} and lost a life, new lives: {player.lives}")

        screen.blit(background, (0,0))
        scoreboard.update(screen)

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
