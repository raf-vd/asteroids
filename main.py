import pygame
import sys
from constants import *
from resources import clock, background, game_over_sound, player_explosion_frames, screen, surface
from explosion import Explosion
from scoreboard import ScoreBoard
from player import Player
from asteroid import LumpyAsteroid
from asteroidfield import AsteroidField
from shot import Shot

def game_over_screen(scoreboard, player):                                       # End game with a bang & final scores

    game_over_sound.play()                                                   # BANG
    player_explosion = Explosion(player.position, 1, player_explosion_frames)

    dt = 0
    while True:                                                                 # Display final score untill player choice
        
        for event in pygame.event.get():                
            if event.type == pygame.QUIT: return False                          # make close button work
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_F5]:  return True                              # F5  = Restart game
                if keys[pygame.K_F10]: return False                             # F10 = Exit game (same as x-button)

        clear_screen()             
        player_explosion.update(dt)
        player_explosion.draw()                                                 # Animate final player explosion (continues version)
        if player_explosion.current_frame == len(player_explosion.frames) -1:
            player_explosion.current_frame = 0
        scoreboard.game_over()                                                  # Show final score
        pygame.display.flip()
        dt += clock.tick(30)/1000

def exit_msg():
    print("Asteroids ended!")                           # Th-Th-That's it folks!
    sys.exit()

def update_objects(updatable, dt):
    for obj in updatable: 
        obj.update(dt)

def draw_objects(drawable):
    for obj in drawable:                                        # draw explosions last, skip them here
        if (isinstance(obj, Player) or                          
            isinstance(obj, LumpyAsteroid)):
            obj.draw()                                              
        elif not isinstance(obj, Explosion):                    
                obj.draw() 
                
    for exp in drawable:                                        # draw explosions last (to be on top)
        if isinstance(exp, Explosion):   
            exp.draw()

def clear_screen():
    surface.fill((0, 0, 0, 0))                      # reset surface
    screen.blit(background, (0,0))                  # show background

def refresh_screen(player, scoreboard):
    scoreboard.update(player)                           # Scoreboard updated (and drawn) on top of all
    screen.blit(surface, (0, 0))                        # overlay surface
    pygame.display.flip()                               # refresh display

def game_mechanics(asteroidfield, asteroids, shots, player, scoreboard):

    game_over, start_new_game = False, False                                # Init game flow variables

    for obj in asteroids:

        if game_over: return game_over, start_new_game                      # Abort loop when game has ended

        for bullet in shots:                                                # SHOT HIT DETECTION

            rc = obj.check_collision(bullet)                                # Check returns -2 for miss,-1 for body hit, index of lump for lump hit
            if rc >= -1:
                score_hit = 0
                if not bullet.pierce:
                    bullet.kill()
                if rc > -1:
                    score_hit = (obj.score_value / len(obj.lumps)) / 2
                    del obj.lumps[rc]
                else:
                    if obj.split():
                        player.activate_upgrade("PIERCING")                 # Centre of asteroid hit => enable piercing shots
                    else:
                        player.activate_upgrade("BIGGER_SHOT")              # Smallest size asteroid centre hit => enable larger shots
                    score_hit = obj.score_value

                player.non_hit_scoring_streak += score_hit                  # Increase scoring streak
                if scoreboard.add(score_hit):                               # When add returns True, a new level was reached, and Asteroids will speed up
                    LumpyAsteroid.velocity_multiplier *= 1 + ASTEROID_VELOCITY_MULTIPLIER
                    if not scoreboard.level % 3:                            # Spawn several special asteroids each 3 levels
                        asteroidfield.super_spawn(scoreboard.level, 1 + scoreboard.level / 10) 

        if player.collides(obj):                                            # PLAYER COLLISION DETECTION
            if player.lives < 1:                                            
                game_over = True                                            # Track that game is over
                start_new_game = game_over_screen(scoreboard, player)       # Show endscore (receive newgame variable)

    return game_over, start_new_game                                        # Pass on game flow variables

def game_loop(asteroidfield, drawable, updatable, asteroids, shots, player, scoreboard):

    dt = 0                                                                                  # Inits
    game_over = False
    
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: exit_msg()                                                        # Catch screen close button
            
        update_objects(updatable, dt)                                                                       # Recalculate all objects in updatable group
        game_over, start_new_game = game_mechanics(asteroidfield, asteroids, shots, player, scoreboard)     # Perform actual game mechaniscs
        
        if not game_over:                                                                                   # Game ended, abort loop
            clear_screen()                                                                                  # Drawing section
            draw_objects(drawable)
            refresh_screen(player, scoreboard)
            dt = clock.tick(60) / 1000                                                                      # "Advance time"

    return start_new_game

def init_game():                                                # Initialise base game objects
    asteroidfield = AsteroidField()                                                             
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    scoreboard = ScoreBoard(player.lives, STARTING_LEVEL)
    return asteroidfield, player, scoreboard

def cleanup_game(updatable, scoreboard):
     # Remove all objects
     del scoreboard
     for obj in updatable:
         obj.kill()

def main(): 
    print("Starting asteroids!")

    # Initialisation section
    pygame.init()                                                                               # Pygame
    pygame.mixer.music.play(-1)

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

    # Start menu
    # Have an initial loop here to display starting screen with menu and keybinds

    start_new_game = True
    while start_new_game:                                                                        
        asteroidfield, player, scoreboard = init_game()                                         # crucial variables initialisation
        start_new_game = game_loop(asteroidfield, drawable, updatable, 
                                   asteroids, shots, player, scoreboard)                        # Start game loop
        cleanup_game(updatable, scoreboard)

    exit_msg()                                                                                  # Game over, no restart requested

# Start program
if __name__ == "__main__":
    main()
