import pygame
import random
from enum import Enum
from constants import *
from functions import *
from resources import *
from slider import Slider
from particle import ExplosionParticleCloud

def factorial(x):
    if x ==1:
        return 1
    return x * factorial(x-1)

def main():
    pygame.init()
    dt = 0
    frame = 1
    explosions = []

    c_slider1 = Slider(400, 100, 400, 20, base_color=(100,150,100,150), highlight_border=2)
    c_slider2 = Slider(400, 150, 400, 20, base_color=(150,100,100,150), border=5)
    while True:
        surface.fill((0, 0, 0, 0))                          # reset surface
        screen.blit(background, (0,0))                      # show background

        c_slider1.set_value(30)
        c_slider2.set_value(60)
        c_slider1.draw(surface, True)
        c_slider2.draw(surface, True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_PLUS:
                    explosions.append(ExplosionParticleCloud(SCREEN_WIDTH / 2, SCREEN_HEIGHT /2, 1))

        for explosion in explosions:
            explosion.update(dt)

        for explosion in explosions:
            explosion.draw()

        explosions = [e for e in explosions if e.is_active()] 


        screen.blit(surface, (0, 0))  
        pygame.display.flip()

        dt = clock.tick(FRAME_RATE) / 1000
        frame += 1

    # pygame.font.init()
    # font32 = pygame.font.Font(None,32)
    # print(font20_fsb.get_linesize())

    # pygame.init()
    # screen = pygame.display.set_mode((800, 600))
    # font = pygame.font.Font(None, 36)
    # text = u"\u2193 Use the arrow keys: ↑ ↓ ← →"
    # text_surface = font32_fs.render(text, True, (255, 255, 255))
    # screen.blit(text_surface, (50, 50))
    # pygame.display.flip()

    # # Keep the window open for a few seconds
    # pygame.time.wait(3000)
    # pygame.quit()


main()