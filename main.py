import pygame
import sys
import os
from constants import *
from resources import clock, background, player_death_sound, player_explosion_frames, screen
from explosion import Explosion
from scoreboard import ScoreBoard
from player import Player
from asteroid import LumpyAsteroid
from asteroidfield import AsteroidField
from shot import Shot

def end_game(surface, scoreboard, player):      # End game with a bang & final scores

    player_death_sound.play()                           # BANG
    player_explosion = Explosion(player.position, 1, player_explosion_frames)

    dt = 0
    # while dt < 10:                                      # 10s ending
    while True:
        
        for event in pygame.event.get():                # make close button work
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                sys.exit()

        surface.fill((0, 0, 0, 0))                  
        screen.blit(background, (0,0))              
        player_explosion.update(dt)
        player_explosion.draw()                         # Animate player explosion
        if player_explosion.current_frame == len(player_explosion.frames) -1:
            player_explosion.current_frame = 0
        scoreboard.game_over()                          # Show final score
        pygame.display.flip()
        dt += clock.tick(30)/1000

    print("Asteroids ended!")                           # Th-Th-That's it folks!
    sys.exit()
 
def main(): 
    print("Starting asteroids!")

    pygame.init()
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

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
        for event in pygame.event.get():                                # make close button work
            if event.type == pygame.QUIT:
                return

        for obj in updatable:    
            obj.update(dt)

        for obj in asteroids:

            for bullet in shots:                                        # SHOT HIT DETECTION

                rc = obj.check_collision(bullet)                        # Check returns -2 for miss,-1 for body hit, index of lump for lump hit
                if rc >= -1:
                    score_hit = 0
                    if not bullet.pierce:
                        bullet.kill()
                    if rc > -1:
                        score_hit = (obj.score_value / len(obj.lumps)) / 2
                        del obj.lumps[rc]
                    else:
                        if obj.split():
                            player.activate_upgrade("PIERCING")         # centre of asteroid hit => enable piercing shots
                        else:
                            player.activate_upgrade("BIGGER_SHOT")      # smallest size asteroid centre hit => enable larger shots
                        score_hit = obj.score_value

                    player.non_hit_scoring_streak += score_hit          # increase scoring streak
                    if scoreboard.add(score_hit):                       # When add returns True, a new level was reached, and Asteroids will speed up
                        LumpyAsteroid.velocity_multiplier *= 1 + ASTEROID_VELOCITY_MULTIPLIER
  
            if player.collides(obj):                                    # PLAYER COLLISION DETECTION
                if player.lives < 1:                                    
                    end_game(surface, scoreboard, player)               # Player dies: finish game

        surface.fill((0, 0, 0, 0))                                      # reset surface
        screen.blit(background, (0,0))                                  # show background

        #### Revisit this to figuere out screen/surface use and conform drawing methods
        for obj in drawable:                                            # draw all objects but explosions
            if (isinstance(obj, Player) or 
                isinstance(obj, LumpyAsteroid)):
                obj.draw(surface)                                       # player & asteroid need surface for transpart objects
            elif not isinstance(obj, Explosion):                        # draw explosions last, exclude here
                    obj.draw() 
                    
        for exp in explosions:                                          # draw explosions last (to be on top)
            exp.draw()

        scoreboard.update(player)                                       # Scoreboard updated (and drawn) on top of all
        screen.blit(surface, (0, 0))                                    # overlay surface
        pygame.display.flip()                                           # refresh display

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
