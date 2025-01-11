# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
import sys
import os
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from constants import *

def main():
    print("Starting asteroids!")

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    score = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    asteroidfield = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

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
                    score += obj.score_value
            if player.collides(obj):
                if player.lives < 1:
                    print(f"Game over with final score {int(score)} ")
                    sys.exit()
                # coding flow help
                print(f"player collided with object at {obj.position.x}, {obj.position.y} and lost a life, new lives: {player.lives}")

        screen.fill("black")

        score_text = font.render(f"Score: {int(score)}", True, "green")
        lives_text = font.render(f"Lives: {player.lives}", True, "green")
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 35))

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
