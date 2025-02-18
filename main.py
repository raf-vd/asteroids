import pygame
from constants import *
from resources import (settings,
                       apply_master_volume, apply_music_volume, apply_sounds_volume,
                       asteroid_break_channel, background, boss_image, clock, font20_fsb, font64, game_over_sound, game_won_sound, game_sounds, hitboss_sound, player_explosion_frames, screen, shot_sound, surface)
from functions import exit_msg, render_line
from explosion import Explosion
from asteroid import LumpyAsteroid
from asteroidfield import AsteroidField
from boss import Boss, BossBullet
from health_bar import HealthBar
from menu import Menu
from particle import ExplosionParticleCloud
from player import Player, PowerUp
from scoreboard import ScoreBoard
from slider import Slider
from shot import Shot

def menu_placeholder():
    dt = 0
    while True:                                                                
        
        for event in pygame.event.get():                
            if event.type == pygame.QUIT: exit_msg(settings)                                    # Game killed with x on window
            if event.type == pygame.KEYDOWN:                         
                if event.key == pygame.K_ESCAPE: return True                                    # Return to main menu

        clear_screen()                                                                          # Empty screen

        menu_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)                       # Create a surface for the menu to be drawn upon
        menu_overlay.fill((255, 255, 255, 100))                                                 # Fill surface with transparent white

        render_line(font64, "menu placeholder", menu_overlay, (255, 255, 0), 100)               # Actual data

        render_line(font20_fsb, "Press ESC to continue", menu_overlay, (255, 255, 255), menu_overlay.get_height() - 100)
        screen.blit(menu_overlay, (0,0))

        pygame.display.flip()
        dt += clock.tick(FRAME_RATE_MENU)/1000

def sound_settings():
    global global_music_volume                                                                                          # global keyword needed because the variables (possibly) get changed
    global global_sounds_volume

    # Declare sliders
    master_volume_slider = Slider(SCREEN_WIDTH / 4, 200, SCREEN_WIDTH / 2, "MASTER volume", settings.get("master volume"), MASTER_VOLUME_MAX, base_color=(100,150,100,150))
    music_volume_slider = Slider(SCREEN_WIDTH / 4, 300, SCREEN_WIDTH / 2, "MUSIC volume", settings.get("music volume"), MASTER_VOLUME_MAX, base_color=(100,150,100,150))
    sounds_volume_slider = Slider(SCREEN_WIDTH / 4, 400, SCREEN_WIDTH / 2, "SOUNDS volume", settings.get("sounds volume"), MASTER_VOLUME_MAX, base_color=(100,150,100,150))

    dt = 0
    while True:                                                                
        
        for event in pygame.event.get():                
            if event.type == pygame.QUIT: exit_msg(settings)                                                                    # Game killed with x on window
            if event.type == pygame.KEYDOWN:                         
                if event.key == pygame.K_ESCAPE: return True                                                                    # Return to previous menu on ESC

                # Apply changes on ENTER                                                            
                if (event.key == pygame.K_KP_ENTER) or (event.key == pygame.K_RETURN):
                    settings.set("master volume", apply_master_volume(MASTER_VOLUME_MAX * master_volume_slider.get_value()))    # Adjust all volumes 1st
                    settings.set("music volume", music_volume_slider.get_value())                                               # Store music & sound values BEFORE master volume adjustment
                    settings.set("sounds volume", sounds_volume_slider.get_value())
                    apply_music_volume(settings.get("master volume") * settings.get("music volume"))                            # Adjust music & sounds (based off CURRENT master volume)
                    apply_sounds_volume(settings.get("master volume") * settings.get("sounds volume"))                                   
                    shot_sound.play()                                                                                           # Play a sound for reference

            # Handle events for sliders                   
            master_volume_slider.handle_event(event)                                                                            # Handle master volume slider events
            music_volume_slider.handle_event(event)                                                                             # Handle music volume slider events
            sounds_volume_slider.handle_event(event)                                                                            # Handle sounds volume slider events

        clear_screen()                                                                                                          # Empty screen

        menu_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)                                                       # Create a surface for the menu to be drawn upon
        menu_overlay.fill((255, 255, 255, 100))                                                                                 # Fill surface with transparent white

        vertical_offset = 75
        vertical_offset = render_line(font64, "Sound", menu_overlay, (255, 255, 0), vertical_offset, 2)                         # Title
        master_volume_slider.draw(menu_overlay)                                                                                 # Master Volume slider
        music_volume_slider.draw(menu_overlay)                                                                                  # Music Volume slider
        sounds_volume_slider.draw(menu_overlay)                                                                                 # Sounds Volume slider

        render_line(font20_fsb, "Press ENTER to Save changes, ESC to Cancel", menu_overlay, (255, 255, 255), menu_overlay.get_height() - 100)
        screen.blit(menu_overlay, (0,0))

        pygame.display.flip()
        dt += clock.tick(FRAME_RATE_MENU)/1000

def keybinds_screen():                                                                           # Show information screen with keybinds for the game

    dt = 0
    while True:                                                                
        
        for event in pygame.event.get():                
            if event.type == pygame.QUIT: exit_msg(settings)                                    # Game killed with x on window
            if event.type == pygame.KEYDOWN:                         
                if event.key == pygame.K_ESCAPE: return True                                    # Return to main menu

        clear_screen()                                                                          # Empty screen

        menu_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)                       # Create a surface for the menu to be drawn upon
        menu_overlay.fill((255, 255, 255, 100))                                                 # Fill surface with transparent white
        
        vertical_offset = 75
        vertical_offset = render_line(font64, "Keybinds", menu_overlay, (255, 255, 0), vertical_offset, 2)                        # Actual data
        vertical_offset = render_line(font20_fsb, "Z or ↑ = thrusters", menu_overlay, (0, 0, 0), vertical_offset)
        vertical_offset = render_line(font20_fsb, "S or ↓ = reverse thrusters", menu_overlay, (0, 0, 0), vertical_offset)
        vertical_offset = render_line(font20_fsb, "Q or ← = rotate left", menu_overlay, (0, 0, 0), vertical_offset)
        vertical_offset = render_line(font20_fsb, "D or → = rotate right", menu_overlay, (0, 0, 0), vertical_offset)
        vertical_offset = render_line(font20_fsb, "A = strafe left", menu_overlay, (0, 0, 0), vertical_offset)
        vertical_offset = render_line(font20_fsb, "E = strafe right", menu_overlay, (0, 0, 0), vertical_offset,2 )
        vertical_offset = render_line(font20_fsb, "SPACEBAR = fire main weapon", menu_overlay, (0, 0, 0), vertical_offset)
        vertical_offset = render_line(font20_fsb, "Left SHIFT = BRAKE", menu_overlay, (0, 0, 0), vertical_offset)
        vertical_offset = render_line(font20_fsb, "TAB = Swap rotate & strafe controls (auto used in boss mode)", menu_overlay, (0, 0, 0), vertical_offset)
        vertical_offset = render_line(font20_fsb, "Press ESC to continue", menu_overlay, (255, 255, 255), menu_overlay.get_height() - 75)
        screen.blit(menu_overlay, (0,0))

        pygame.display.flip()
        dt += clock.tick(FRAME_RATE_MENU)/1000

def game_over_screen(scoreboard, player, win=False):                                # End game with a bang & final scores (or victory yell)

    if game_sounds.get_busy(): game_sounds.stop()
    if win:
        game_won_sound.play()                                                       # VICTORY
    else:
        game_over_sound.play()                                                      # BANG
        player_explosion = Explosion(player.position, 1, player_explosion_frames)   # Final player explosion animation

    dt = 0
    while True:                                                                     # Display final score untill player choice
        
        for event in pygame.event.get():                
            if event.type == pygame.QUIT: exit_msg(settings)                        # Game killed with x on window
            if event.type == pygame.KEYDOWN:                         
                if event.key == pygame.K_ESCAPE: return True                        # Return to main menu

        clear_screen()
        if not win:                                                                 # Animate final player explosion (continues version) if lost
            player_explosion.update(dt)
            player_explosion.draw()                                                 
            if player_explosion.current_frame == len(player_explosion.frames) -1:
                player_explosion.current_frame = 0
        
        scoreboard.game_over(win)                                                   # Show final score
        screen.blit(surface, (0, 0))                                                # overlay surface
        pygame.display.flip()
        dt += clock.tick(FRAME_RATE)/1000

def update_objects(updatable, dt, boss, player):
    for obj in updatable: 
        if isinstance(obj, Player):
            obj.update(dt, boss)
        elif isinstance(obj, Boss):
            obj.update(dt, player)
        else:
            obj.update(dt)

def draw_objects(drawable):
    for obj in drawable:                                # Draw anything except player & asteroid explosions first
        if not(isinstance(obj, Explosion) or
               isinstance(obj, Player)):
            obj.draw()                                              

    for play in drawable:                               # Draw player next (and speedometer)
        if isinstance(play, Player):   
            play.draw()
                
    for exp in drawable:                                # Draw asteroid explosions last (to be on to of all)
        if isinstance(exp, Explosion):   
            exp.draw()

def clear_screen():
    surface.fill((0, 0, 0, 0))                          # reset surface
    screen.blit(background, (0,0))                      # show background

def refresh_screen(player, scoreboard):
    scoreboard.update(player)                           # Scoreboard updated (and drawn) on top of all
    screen.blit(surface, (0, 0))                        # overlay surface
    pygame.display.flip()                               # refresh display

def game_mechanics_boss(boss, boss_bullets, dt, player, scoreboard, shots):

    if player.lives < 1: return True                                                    # Return game over when no more lives

    for bb in boss_bullets:                                                             # BOSS BULLET DAMAGE
        if player.collides(bb):                                                         # PLAYER COLLISION DETECTION
            if player.lives < 1: return True                                            # Return game over when no more lives
        
    if boss.ready:
        for bullet in shots:                                                            # PLAYER DAMAGE
            if boss.hp < 1: break                                                       # Stop processing bullets if boss is dead
            
            boss.rect.topleft = (boss.position.x, boss.position.y)                      # Move bounding rect to current boss position
            if bullet.circle_vs_rect(boss.rect):                                        # Bullet in boss rect => closer check through mask
                if bullet.circle_vs_mask(boss.mask, boss.rect):                         # Check actual detailed hit through mask
                    asteroid_break_channel.play(hitboss_sound)                          # Use asteroid break channel since it's free now
                    ExplosionParticleCloud(bullet.position.x, bullet.position.y, 0.5)   # Show sparkles where boss wass hit
                    scoreboard.add(BOSS_BASE_HIT_VALUE)                                 # Increase score
                    boss.reduce_hp(1)                                                   # Reduce boss healht
                    bullet.kill()                                                       # Remove bullet

        if boss.hp < 1:                                                                 # Check if boss is killed
            if not boss.death_animation_active(dt):                                     # BURN & VANISH
                scoreboard.add(BOSS_KILL_VALUE)                                         # Add a fat boss kill valkue
                boss.kill()                                                             # Clear the boss instance variable
                boss.ready = False                                                      
                print("You killed the boss !!!")            
                return True                                                             # Return game over = True

    return False                                                                        # Return False to indicate boss & player are both alive

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
                return True

    return game_over                                                        # Pass on game flow variables

def game_loop(asteroidfield, boss, player, scoreboard, asteroids, boss_bullets, drawable, shots, updatable):
    win = False                                                                                 # Inits
    dt = 0                                                                                      
    clock.tick()                                                                                # Reset the clock's time delta
    while True:
        for event in pygame.event.get():                                                        # Catch screen close button
            if event.type == pygame.QUIT:
                exit_msg(settings)                                                              # Forced quit by x on window
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:                   # Allow menu access in the game loop
                return boss, 'PAUSE'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:   
                    player.toggle_strafe()                                                      # Swap player strafe mode
            
        update_objects(updatable, dt, boss, player)                                             # Recalculate all objects in updatable group
        if not player.boss_active():
            game_over = game_mechanics(asteroidfield, player, scoreboard, asteroids, shots)     # Perform actual game mechaniscs
        else:
            game_over = game_mechanics_boss(boss, boss_bullets, dt, player, scoreboard, shots)  # Perform actual game mechaniscs for boss fight
            if boss.hp == 0: win = True

        if game_over:
            game_over_screen(scoreboard, player, win)                                           # Show endscore, track that game is over
            return boss, 'MENU'                                                                 # Game over => back to menu
            
        if scoreboard.level == BOSS_SPAWN_LEVEL and not player.boss_active():                   # Spawn boss
            asteroidfield.kill()                                                                # Stop spawning asteroids
            for asteroid in asteroids:                                                          
                asteroid.kill()                                                                 # Remove remaining asteroids
            # Spawn boss
            boss = Boss((SCREEN_WIDTH - boss_image.get_width())/ 2, -boss_image.get_height() - 10, boss_image)
            player.shield_regeneration = 0
            player.non_hit_scoring_streak = 0
            player.toggle_boss_mode()                
            if not player.strafe_active(): player.toggle_strafe()                               # Force boss fase start in strafe mode

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
    ExplosionParticleCloud.containers = (drawable, updatable)
    HealthBar.containers = (updatable)
    LumpyAsteroid.containers = (asteroids, drawable, updatable)
    Player.containers = (drawable, updatable)
    Shot.containers = (drawable, shots, updatable)

    settings_menu = Menu("Settings",[("Keybinds", keybinds_screen, True),
                                     ("Sound", sound_settings, True),
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
                boss = None
                player = None
                scoreboard = None

            result_value = current_menu.handle_menu_loop()                                      # Show the current menu, recieve the chosen action
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
            boss, game_state = game_loop(asteroidfield, boss, player, scoreboard, 
                                         asteroids, boss_bullets, drawable, shots, updatable)

    exit_msg(settings)                                                                          # Close the program with a final message

# Start program
if __name__ == "__main__":
    main()
