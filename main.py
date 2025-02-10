import pygame
from constants import *
from resources import asteroid_break_channel, background, boss_image, clock, crack_lump_sound, font20_fsb, font64, game_over_sound, game_sounds, player_explosion_frames, screen, surface
from functions import exit_msg, render_line
from explosion import Explosion
from asteroid import LumpyAsteroid
from asteroidfield import AsteroidField
from boss import Boss, BossBullet
from menu import Menu
from player import Player, PowerUp
from scoreboard import ScoreBoard
from shot import Shot

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

        render_line(font20_fsb, "Press ESC to continue", bar_surface, (255, 255, 255), bar_surface.get_height() - 100)
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
        
        vertical_offset = 75
        vertical_offset = render_line(font64, "Keybinds", bar_surface, (255, 255, 0), vertical_offset, 2)                        # Actual data
        vertical_offset = render_line(font20_fsb, "Z or ↑ = thrusters", bar_surface, (0, 0, 0), vertical_offset)
        vertical_offset = render_line(font20_fsb, "S or ↓ = reverse thrusters", bar_surface, (0, 0, 0), vertical_offset)
        vertical_offset = render_line(font20_fsb, "Q or ← = rotate left", bar_surface, (0, 0, 0), vertical_offset)
        vertical_offset = render_line(font20_fsb, "D or → = rotate right", bar_surface, (0, 0, 0), vertical_offset)
        vertical_offset = render_line(font20_fsb, "A = strafe left", bar_surface, (0, 0, 0), vertical_offset)
        vertical_offset = render_line(font20_fsb, "E = strafe right", bar_surface, (0, 0, 0), vertical_offset,2 )
        vertical_offset = render_line(font20_fsb, "SPACEBAR = fire main weapon", bar_surface, (0, 0, 0), vertical_offset)
        vertical_offset = render_line(font20_fsb, "Left SHIFT = BRAKE", bar_surface, (0, 0, 0), vertical_offset)
        vertical_offset = render_line(font20_fsb, "TAB = Swap rotate & strafe controls (auto used in boss mode)", bar_surface, (0, 0, 0), vertical_offset)
        vertical_offset = render_line(font20_fsb, "Press ESC to continue", bar_surface, (255, 255, 255), bar_surface.get_height() - 75)
        screen.blit(bar_surface, (0,0))
        # text = "Use the arrow keys: ↑ ↓ ← →"
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

def update_objects(updatable, dt, boss):
    for obj in updatable: 
        if isinstance(obj, Player):
            obj.update(dt, boss)
        else:
            obj.update(dt)

def draw_objects(drawable):
    for obj in drawable:                                # Draw Shots & Asteroids first
        if (isinstance(obj, Boss) or                          
            isinstance(obj, BossBullet) or 
            isinstance(obj, LumpyAsteroid) or
            isinstance(obj, Shot)):
            obj.draw()                                              

    for play in drawable:                             # Draw player next (and speedometer)
        if isinstance(play, Player):   
            play.draw()
                
    for exp in drawable:                                # draw explosions last (to be on to of all)
        if isinstance(exp, Explosion):   
            exp.draw()

def clear_screen():
    surface.fill((0, 0, 0, 0))                          # reset surface
    screen.blit(background, (0,0))                      # show background

def refresh_screen(player, scoreboard):
    scoreboard.update(player)                           # Scoreboard updated (and drawn) on top of all
    screen.blit(surface, (0, 0))                        # overlay surface
    pygame.display.flip()                               # refresh display

def game_mechanics_boss(boss, player, scoreboard, boss_bullets, shots):

    game_over =  False                                                      # Init game flow variables

    for bb in boss_bullets:                                                 # BOSS DAMAGE

        if game_over: return game_over                                      # Abort loop when game has ended

        if player.collides(bb):                                             # PLAYER COLLISION DETECTION
            if player.lives < 1:                                            
                game_over = game_over_screen(scoreboard, player)            # Show endscore, track that game is over
        
    for bullet in shots:                                                    # PLAYER DAMAGE
        boss.rect.topleft = (boss.position.x, boss.position.y)              # Move bounding rect to current boss position
        if bullet.circle_vs_rect(boss.rect):                                # Bullet in boss rect => closer check through mask
            if bullet.circle_vs_mask(boss.mask, boss.rect):                 # Check actual detailed hit through mask
                asteroid_break_channel.play(crack_lump_sound)               # Play sound on hit

    return game_over                                                        # Pass on game flow variables

def game_mechanics(asteroidfield, player, scoreboard, asteroids, shots):

    game_over =  False                                                      # Init game flow variables

    for obj in asteroids:                                                   # Loop used in asteroids fase

        if game_over: return game_over                                      # Abort loop when game has ended

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
                        asteroidfield.super_spawn(scoreboard.level) 

        if player.collides(obj):                                            # PLAYER COLLISION DETECTION
            if player.lives < 1:                                            
                game_over = game_over_screen(scoreboard, player)            # Show endscore, track that game is over

    return game_over                                                        # Pass on game flow variables

def game_loop(asteroidfield, boss, player, scoreboard, asteroids, boss_bullets, drawable, shots, updatable):
    dt = 0                                                                                      # Init
    clock.tick()                                                                                # Reset the clock's time delta
    while True:
        for event in pygame.event.get():                                                        # Catch screen close button
            if event.type == pygame.QUIT:
                exit_msg()                                                                      # Forced quit by x on window
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:                   # Allow menu access in the game loop
                return 'PAUSE'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:   
                    player.toggle_strafe()                                                      # Swap player strafe mode
            
        update_objects(updatable, dt, boss)                                                     # Recalculate all objects in updatable group
        if not player.boss_active():
            game_over = game_mechanics(asteroidfield, player, scoreboard, asteroids, shots)     # Perform actual game mechaniscs
        else:
            game_over = game_mechanics_boss(boss, player, scoreboard, boss_bullets, shots)      # Perform actual game mechaniscs for boss fight

        if game_over: return 'MENU'                                                             # Game over => back to menu
            
        if scoreboard.level == BOSS_SPAWN_LEVEL and not player.boss_active():                   # Spawn boss
            asteroidfield.kill()                                                                # Stop spawning asteroids
            for asteroid in asteroids:                                                          
                asteroid.kill()                                                                 # Remove remaining asteroids
            # Spawn boss
            boss = Boss((SCREEN_WIDTH - boss_image.get_width())/ 2, -boss_image.get_height() - 10, boss_image)
            player.toggle_boss_mode()                
            if not player.strafe_active(): player.toggle_strafe()                                 # Force boss fase start in strafe mode

        clear_screen()                                                                          # Drawing section
        draw_objects(drawable)
        refresh_screen(player, scoreboard)
        dt = clock.tick(FRAME_RATE) / 1000                                                      # Game speed control

def init_game():                                                # Initialise base game objects
    asteroidfield = AsteroidField()         
    LumpyAsteroid.velocity_multiplier = 1                                                    
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

    asteroids = pygame.sprite.Group()                                                           # groups
    boss_bullets = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    updatable = pygame.sprite.Group()                                                           

    AsteroidField.containers = updatable                                                        # containers
    Boss.containers = (drawable, updatable)
    BossBullet.containers = (boss_bullets, drawable, updatable)
    Explosion.containers = (drawable, updatable)
    LumpyAsteroid.containers = (asteroids, drawable, updatable)
    Player.containers = (drawable, updatable)
    Shot.containers = (drawable, shots, updatable)

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
    boss = None
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
            game_state = game_loop(asteroidfield, boss, player, scoreboard, 
                                   asteroids, boss_bullets, drawable, shots, updatable)

    exit_msg()                                                                                  # Close the program with a final message

# Start program
if __name__ == "__main__":
    main()
