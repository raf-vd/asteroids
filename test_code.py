import pygame
from constants import *
from asteroid import LumpyAsteroid
from explosion import Explosion
from player import Player

def main():
    
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Explosion.containers = (explosions, updatable, drawable)

    l_asts = [LumpyAsteroid(200,200,50),LumpyAsteroid(500,200,50),LumpyAsteroid(800,200,50),LumpyAsteroid(1100,200,50)]
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black") 

        for l_ast in l_asts:
            l_ast.draw(screen)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_KP_PLUS]:
            e=Explosion(pygame.Vector2(600,600))

        for obj in updatable:
             obj.update(dt)

        for obj in drawable:
            if isinstance(obj, Player):
                obj.draw(screen)

        for expl in explosions:
            expl.draw(screen)


        pygame.display.flip()

        dt = clock.tick(60) / 1000
        
# x=2
# print(x)
# print("ja") if x==1 else print("nee")
# print("JA" if x==1 else "NEE")
# y = "yes" if x == 1 else "no"
# print(y)
main()