import pygame
import sys
from constants import *
from resources import clock, background, game_over_sound, player_explosion_frames, screen, surface
from functions import exit_msg
from explosion import Explosion
from scoreboard import ScoreBoard
from player import Player
from asteroid import LumpyAsteroid
from asteroidfield import AsteroidField
from shot import Shot
from menu import Menu

def game_over_screen(scoreboard, player):                                       # End game with a bang & final scores

    game_over_sound.play()                                                   # BANG
    player_explosion = Explosion(player.position, 1, player_explosion_frames)

    dt = 0
    while True:                                                                 # Display final score untill player choice
        
        for event in pygame.event.get():                
            if event.type == pygame.QUIT: exit_msg()                            # Game killed with x on window
            if event.type == pygame.KEYDOWN: return True                        # Return to main menu

        clear_screen()             
        player_explosion.update(dt)
        player_explosion.draw()                                                 # Animate final player explosion (continues version)
        if player_explosion.current_frame == len(player_explosion.frames) -1:
            player_explosion.current_frame = 0
        scoreboard.game_over()                                                  # Show final score
        pygame.display.flip()
        dt += clock.tick(30)/1000

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

    game_over =  False                                                      # Init game flow variables

    for obj in asteroids:

        if game_over: return game_over                                     # Abort loop when game has ended

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
                game_over = game_over_screen(scoreboard, player)            # Show endscore, track that game is over

    return game_over                                                        # Pass on game flow variables

def game_loop(asteroidfield, drawable, updatable, asteroids, shots, player, scoreboard):
    dt = 0                                                                                      # Inits
    game_running = True         
    
    while game_running:
        for event in pygame.event.get():                                                        # Catch screen close button
            if event.type == pygame.QUIT:
                exit_msg()                                                                      # Forced quit by x on window
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:                   # Allow menu access in the game loop
                return 'PAUSE'
            
        update_objects(updatable, dt)                                                           # Recalculate all objects in updatable group
        game_over = game_mechanics(asteroidfield, asteroids, shots, player, scoreboard)         # Perform actual game mechaniscs
        
        if game_over:                                                                           # Game over => back to menu
            return 'MENU'
            
        clear_screen()                                                                          # Drawing section
        draw_objects(drawable)
        refresh_screen(player, scoreboard)
        dt = clock.tick(60) / 1000                                                              # Game speed control

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

    main_menu = Menu.create_main_menu()                                                         # Create menu
    controls_menu = Menu.create_controls_menu()                                                 # Create submenu
    
    game_state = "MENU"                                                                         # Init variables
    asteroidfield = None
    player = None
    scoreboard = None
    
    while True:        
        
        if game_state == "PAUSE":
            pause = True
            game_state = "MENU"
        else:
            pause = False

        if game_state == "MENU":
            if not pause:                                                                       # If we're coming from a game that ended, clean up
                cleanup_game(updatable, scoreboard)
                asteroidfield = None                                                            # Set everything to None to ensure we are ready for a new game
                player = None
                scoreboard = None

            main_menu = Menu.create_main_menu(pause)                                            # Show 'resume' in menu if paused, else show 'new game'
            action = main_menu.handle_menu_loop(screen)
            
            if action == "start":                                                               # Evaluate action chosen in menu
                asteroidfield, player, scoreboard = init_game()
                game_state = "GAME"
            elif action == "resume":
                game_state = "GAME"
            elif action == "controls":
                game_state = "CONTROLS"
            elif action == "quit":
                if player is not None:                                                          # Clean up if quitting during a game
                    cleanup_game(updatable, scoreboard)
                break                                                                           # Exit loop when quit was chosen

        elif game_state == "CONTROLS":                                                          # Submenu handling
            action = controls_menu.handle_menu_loop(screen)
            if action == "back":
                if pause:
                    game_state = "PAUSE"
                else:
                    game_state = "MENU"
                
        elif game_state == "GAME":                                                              # Run the actual gameloop
            game_state = game_loop(asteroidfield, drawable, updatable, asteroids, shots, player, scoreboard)

    exit_msg()                                                                                  # Close the program with a final message

# Start program
if __name__ == "__main__":
    main()
