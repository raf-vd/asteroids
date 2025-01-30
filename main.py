import pygame
from constants import *
from resources import background, clock, font32, font64, game_over_sound, game_sounds, player_explosion_frames, screen, surface
from functions import exit_msg, render_line
from explosion import Explosion
from scoreboard import ScoreBoard
from player import Player, PowerUp
from asteroid import LumpyAsteroid
from asteroidfield import AsteroidField
from shot import Shot
from menu import Menu

def menu_placeholder():
    dt = 0
    while True:                                                                
        
        for event in pygame.event.get():                
            if event.type == pygame.QUIT: exit_msg()                                            # Game killed with x on window
            if event.type == pygame.KEYDOWN:                         
                if event.key == pygame.K_ESCAPE: return True                                    # Return to main menu

        clear_screen()                                                                          # Empty screen

        bar_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)                        # Create a surface for the menu to be drawn upon
        bar_surface.fill((255, 255, 255, 100))                                                  # Fill surface with transparent white

        render_line(font64, "menu placeholder", bar_surface, (255, 255, 0), 100)                # Actual data

        render_line(font32, "Press ESC to continue", bar_surface, (255, 255, 255), bar_surface.get_height() - 100)
        screen.blit(bar_surface, (0,0))

        pygame.display.flip()
        dt += clock.tick(FRAME_RATE_MENU)/1000

def keybinds_screen():                                                                           # Show information screen with keybinds for the game

    dt = 0
    while True:                                                                
        
        for event in pygame.event.get():                
            if event.type == pygame.QUIT: exit_msg()                                            # Game killed with x on window
            if event.type == pygame.KEYDOWN:                         
                if event.key == pygame.K_ESCAPE: return True                                    # Return to main menu

        clear_screen()                                                                          # Empty screen

        bar_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)                        # Create a surface for the menu to be drawn upon
        bar_surface.fill((255, 255, 255, 100))                                                  # Fill surface with transparent white
        
        render_line(font64, "Keybinds", bar_surface, (255, 255, 0), 100)                        # Actual data
        render_line(font32, "Z or UP-arrow = thrusters", bar_surface, (0, 0, 0), 250)
        render_line(font32, "S or DOWN-arrow = reverse thrusters", bar_surface, (0, 0, 0), 300)
        render_line(font32, "Q or LEFT-arrow = rotate left", bar_surface, (0, 0, 0), 350)
        render_line(font32, "D or RIGHT-arrow = rotate right", bar_surface, (0, 0, 0), 400)
        render_line(font32, "SPACEBAR = fire main weapon", bar_surface, (0, 0, 0), 450)
        render_line(font32, "Left SHIFT = BRAKE", bar_surface, (0, 0, 0), 500)
        render_line(font32, "Press ESC to continue", bar_surface, (255, 255, 255), bar_surface.get_height() - 100)
        screen.blit(bar_surface, (0,0))

        pygame.display.flip()
        dt += clock.tick(FRAME_RATE_MENU)/1000

def game_over_screen(scoreboard, player):                                       # End game with a bang & final scores

    if game_sounds.get_busy(): game_sounds.stop()
    game_over_sound.play()                                                      # BANG
    player_explosion = Explosion(player.position, 1, player_explosion_frames)

    dt = 0
    while True:                                                                 # Display final score untill player choice
        
        for event in pygame.event.get():                
            if event.type == pygame.QUIT: exit_msg()                            # Game killed with x on window
            if event.type == pygame.KEYDOWN:                         
                if event.key == pygame.K_ESCAPE: return True                    # Return to main menu

        clear_screen()             
        player_explosion.update(dt)
        player_explosion.draw()                                                 # Animate final player explosion (continues version)
        if player_explosion.current_frame == len(player_explosion.frames) -1:
            player_explosion.current_frame = 0
        
        scoreboard.game_over()                                                  # Show final score
        pygame.display.flip()
        dt += clock.tick(FRAME_RATE)/1000

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
    surface.fill((0, 0, 0, 0))                          # reset surface
    screen.blit(background, (0,0))                      # show background

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
                        player.activate_upgrade(PowerUp.PIERCING)           # Centre of asteroid hit => enable piercing shots
                    else:
                        player.activate_upgrade(PowerUp.BIGGER_SHOT)        # Smallest size asteroid centre hit => enable larger shots
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
    dt = 0                                                                                      # Init
    clock.tick()                                                                                # Reset the clock's time delta
    while True:
        for event in pygame.event.get():                                                        # Catch screen close button
            if event.type == pygame.QUIT:
                exit_msg()                                                                      # Forced quit by x on window
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:                   # Allow menu access in the game loop
                return 'PAUSE'
            
        update_objects(updatable, dt)                                                           # Recalculate all objects in updatable group
        game_over = game_mechanics(asteroidfield, asteroids, shots, player, scoreboard)         # Perform actual game mechaniscs
        if game_over: return 'MENU'                                                             # Game over => back to menu
            
        clear_screen()                                                                          # Drawing section
        draw_objects(drawable)
        refresh_screen(player, scoreboard)
        dt = clock.tick(FRAME_RATE) / 1000                                                      # Game speed control

def init_game():                                                # Initialise base game objects
    asteroidfield = AsteroidField()                                                             
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    scoreboard = ScoreBoard(player.lives, STARTING_LEVEL)
    return asteroidfield, player, scoreboard

def cleanup_game(updatable, scoreboard):
    # Remove all objects
    clear_screen()
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

    settings_menu = Menu("Settings",[("Keybinds", keybinds_screen, True),
                                     ("Sound", menu_placeholder, True),
                                     ("Back", "back", True)])                                           
    main_menu = Menu("Asteroids",[("New Game", "start", True),
                                  ("Resume", "resume", False),
                                  ("Settings", settings_menu, True),
                                  ("Abort Game", "end", False),
                                  ("Exit", "quit", True)])                                           
    current_menu = main_menu                                                                    # Track current menu

    game_state = "MENU"                                                                         # Init variables
    game_paused = False
    asteroidfield = None
    player = None
    scoreboard = None
    
    while True:        

        if game_state =="PAUSE":                                                                # Handle paused state before anything
            game_paused = True                                                                  # Set pause tracker
            current_menu.update_visibility(game_paused)                                         # During pause Change regular menu flow => force update visibility
            game_state = "MENU"                                                                 # Continue with menu now that pause is tracked

        if game_state == "MENU":
            if not game_paused:                                                                 # If we're coming from a game that ended, clean up
                cleanup_game(updatable, scoreboard)
                asteroidfield = None                                                            # Set everything to None to ensure we are ready for a new game
                player = None
                scoreboard = None

            result_value = current_menu.handle_menu_loop()                                      # Shop the current menu, recieve the chosen action
            if result_value == "start":                                                         # Start a new game
                asteroidfield, player, scoreboard = init_game()
                game_state = "GAME"
                game_paused = False
            elif result_value == "resume":                                                      # Resume current  game
                game_paused = False
                game_state = "GAME"
            elif result_value == "end":                                                         # Stop the current game
                cleanup_game(updatable, scoreboard)                                             # Cleanup variables
                game_paused = False
                game_state = "MENU"                                                             # Update game/menuflow variables
            elif result_value == "quit":
                cleanup_game(updatable, scoreboard)                                             # Cleanup vars before quitting
                break                                                                           # Exit loop when quit was chosen

            current_menu.update_visibility(game_paused)                                         # Regular menu flow: update visibility by default

        elif game_state == "GAME":                                                              # Run the actual gameloop
            game_state = game_loop(asteroidfield, drawable, updatable, asteroids, shots, player, scoreboard)

    exit_msg()                                                                                  # Close the program with a final message

# Start program
if __name__ == "__main__":
    main()
