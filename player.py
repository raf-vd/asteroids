import pygame
import random
import math
from constants import *
from resources import alarm_sound, player_death_sound, player_explosion_frames, player_image, screen, shield_hit_sound, surface
from circleshape import CircleShape
from shot import Shot
from explosion import Explosion
from functions import point_in_triangle, point_to_line_distance

# Class to handle the player
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.__upgrade_key_cooldown_timer = 0
        self.__upgrade_countdown_piercing = 0
        self.__upgrade_countdown_bulletsize = 0
        self.__respawn_countdown = 0
        self.rotation = 0
        self.shoot_timer = 0
        self.spawn_guard = PLAYER_SPAWN_SAFEGUARD
        self.lives = PLAYER_STARTING_LIVES
        # self.colour = "green"
        self.shield_charge = 10             
        self.shield_regeneration = 0
        self.non_hit_scoring_streak = 0
        self.alpha = 255
 
    def triangle(self):                     # calculate a triangle for player
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius * 1.25 # 25% correction on point a location to appear "better centered"
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self):                                                         # override draw from CircleShape
        if self.__respawn_countdown > 0:                                    # Don't show player while respawn cooldown is active
            return False                
        self.wrap_screen()
        #pygame.draw.polygon(screen, self.colour, self.triangle(), 2)       # Original version drew a triangle
        r_img = pygame.transform.rotate(player_image, -self.rotation)       # Make sure image rotates with player
        r_img.set_alpha(self.alpha)                                         # Handle 'invulnerable oscilation'
        rect = r_img.get_rect()
        rect.center = self.position  
        screen.blit(r_img, rect)                                            # Draw the actual image

        if int(self.shield_charge) > 0:
            # Fluctuate shield transparancy for nice visual effect
            pygame.draw.circle(surface, (150, 250, 150, random.randint(20, 80)), self.position, self.radius + 10 + int(self.shield_charge), int(self.shield_charge))
    
    def rotate(self, dt):                   # rotate the player (left, right)
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def move(self, dt):                     # move the player (forward, back)
        # Limit maximum speed
        if self.velocity.magnitude() < PLAYER_MAXIMUM_SPEED:
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            # self.position += forward * PLAYER_SPEED * dt 
            self.velocity += forward * PLAYER_ACCELERATION * dt

    def slow_down(self, dt, slow_factor):
        # If velocity is very small, just stop completely
        if self.velocity.magnitude() < 0.1:
            self.velocity = pygame.Vector2(0, 0)
        else:
            # Reduce velocity more aggressively than natural drag
            slowing_force = self.velocity.normalize() * slow_factor
            self.velocity -= slowing_force * dt        

    def update(self, dt):                   # process inputs from keys and do all sorts of changes to player

        if self.__respawn_countdown > 0:
            self.__respawn_countdown -= dt
            return False                # Don't do anything while respawn cooldown is active

        self.shoot_timer -= dt
        
        # if self.spawn_guard < PLAYER_SPAWN_SAFEGUARD * 0.15: # return to fighting color at 85% of spawn_guard has passed so player gets to safety asap
        #     self.colour = "white"

        if self.spawn_guard > 0:
            self.alpha = 75 + int(125 * (math.sin(pygame.time.get_ticks() / 200) + 1) / 2)
            self.spawn_guard -= dt
        else:
            self.alpha = 255

        if self.__upgrade_key_cooldown_timer > 0:
            self.__upgrade_key_cooldown_timer -= dt

        if self.__upgrade_countdown_piercing > 0:
            self.__upgrade_countdown_piercing -= dt
        else:
            if Shot.piercing_active:
                Shot.piercing_active = False

        if self.__upgrade_countdown_bulletsize > 0:
            self.__upgrade_countdown_bulletsize-= dt
        else:
            self.activate_upgrade("SMALLER_SHOT")

        if self.non_hit_scoring_streak > PLAYER_MIN_SCORE_STREAK:  # you need to have a minimal scoring streak to have any shield regeneration
            if self.shield_regeneration < 2.0:                                                                  # Hardcap shieldregen
                self.shield_regeneration = (self.non_hit_scoring_streak / 100) * (1 / (self.shield_charge*3 +1)) # Shield regen lowers when more shield is active
            self.activate_upgrade("INCREASE_SHIELD", self.shield_regeneration)

        # Process input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:     self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:    self.rotate(dt)
        if keys[pygame.K_z] or keys[pygame.K_UP]:       self.move(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:     self.move(-dt)
        if keys[pygame.K_SPACE]:                        self.shoot()
        if keys[pygame.K_LSHIFT]:                       self.slow_down(dt, PLAYER_BRAKE_FORE)

        # Move player according to current speed
        self.position += self.velocity          

        # Create some drag to stop player even without braking
        if self.velocity.magnitude() > 0:
            self.slow_down(dt, PLAYER_DRAG)

        # if self.__upgrade_key_cooldown_timer > 0:
        #     return False
        
        # if keys[pygame.K_DELETE]:
        #     self.activate_upgrade("PIERCING")
        #     self.__upgrade_key_cooldown_timer = UPGRADE_KEY_COOLDOWN_TIMER

        # if keys[pygame.K_PAGEUP]:
        #     self.activate_upgrade("BIGGER_SHOT")
        #     self.__upgrade_key_cooldown_timer = UPGRADE_KEY_COOLDOWN_TIMER
        # if keys[pygame.K_PAGEDOWN]:
        #     self.activate_upgrade("SMALLER_SHOT")
        #     self.__upgrade_key_cooldown_timer = UPGRADE_KEY_COOLDOWN_TIMER

        # if keys[pygame.K_HOME]:
        #     self.activate_upgrade("INCREASE_SHIELD", 10)
        #     # self.__upgrade_key_cooldown_timer = UPGRADE_KEY_COOLDOWN_TIMER
        # if keys[pygame.K_END]:
        #     self.activate_upgrade("DECREASE_SHIELD", 10)
        #     #self.__upgrade_key_cooldown_timer = UPGRADE_KEY_COOLDOWN_TIMER

    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def check_collision(self, other):

        # Check for shield collision first (if shield is active)
        if self.shield_charge > 0:
            if self.shield_collides(other):
                rc = other.check_collision(self)                # Check returns -2 for miss,-1 for body hit, index of lump for lump hit                
                if rc >= -1: alarm_sound.play()                 # Alarm sound: ship body in contact with asteroid while shielded
                if rc > -1:  del other.lumps[rc]                # Shield destroys lumps when they hit player ship while shielded

                shield_hit_sound.play()                         # warning buzz     
                self.non_hit_scoring_streak = 0                 # hits on shield resets scoring streak
                self.shield_regeneration * 0.9                  # hits on shield decrease regeneration rate
                self.activate_upgrade("DECREASE_SHIELD", 1)     # reduce shieldcharge on hit
                return False                                    # return False prevent hits from hitting player while shielded

        # Broad check: circular player outside mainradius + lumpradius
        if self.position.distance_to(other.position) > self.radius + other.radius * (1 + ASTEROID_MAX_LUMP_SIZE):
            return False
        
        # Check player collides with main body
        if self.triangle_circle_collide(other):
            return True

        # Check player collides with any lump
        for lump in other.lumps:
            if self.triangle_circle_collide(lump):
                return True

        return False

    def shield_collides(self, other):

        # Broad check: shield outside mainradius + lumpradius
        if self.position.distance_to(other.position) > self.radius + 10 + self.shield_charge + other.radius * (1 + ASTEROID_MAX_LUMP_SIZE):
            return False

        # Check player collides with any lump
        for lump in other.lumps:
            if lump.position.distance_to(self.position) <= self.radius + 10 + self.shield_charge + lump.radius:
                return True

        # Check player collides with asteroid main body
        if other.position.distance_to(self.position) <= self.radius + 10 + self.shield_charge + other.radius:
            return True

        return False
    
    def triangle_circle_collide(self, other):

        # Circle-centre check (avoid detailed checks when possible)
        triangle_points = self.triangle()
        if point_in_triangle(other.position, triangle_points):
            True

        # Check if circle collised with any side
        for i in range(3):
            start = triangle_points[i]           # 1 -> 2 -> 3
            end = triangle_points[ (i + 1) % 3]  # 2 -> 3 -> 1
            if point_to_line_distance(other.position, start, end) <= other.radius:
                return True
            
        return False

    def collides(self, target):
        # disable collision for PLAYER_SPAWN_SAFEGUARD seconds after spawning
        # (this will also safeguard player during respawn cooldown)
        if self.spawn_guard > 0:                                                                # Prevent colision while recently reswpawned
            return False                       
        
        if self.check_collision(target): 
            player_death_sound.play()                                                           # Play sound
            self.lives -= 1                                                                     # Player collided, take a life awat
            if self.lives == 0:                                                                 # Out of lives => game ends
                return True                             
            Explosion(self.position, 1, player_explosion_frames)                                # Go BOOM
            self.__respawn(pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), self.lives)     # Respawn player in centre of screen          
            return True
        
        return False                                                                            # No collision
    
    def activate_upgrade(self, upgrade, value=1):
        if upgrade == "PIERCING":
            if not Shot.piercing_active:
                Shot.piercing_active = True
                self.__upgrade_countdown_piercing = 5
        
        elif upgrade == "BIGGER_SHOT":
            if Shot.shot_size_multiplier < 10:
                Shot.shot_size_multiplier += 1
                self.__upgrade_countdown_bulletsize = 1
        elif upgrade == "SMALLER_SHOT":
            if Shot.shot_size_multiplier > 1:
                Shot.shot_size_multiplier -= 1
                if Shot.shot_size_multiplier > 1:
                    self.__upgrade_countdown_bulletsize = 1
        
        elif upgrade == "INCREASE_SHIELD":
            if self.shield_charge + value < 100:
                self.shield_charge += value
            else:
                self.shield_charge = 100    # force down to max if somehow surpasses max
        elif upgrade == "DECREASE_SHIELD":
            if self.shield_charge - value> 0:
                self.shield_charge -= value
            else:
                self.shield_charge = 0      # force up to 0 if somehow goes negative

    def __respawn(self, position, remaining_lives):         # Reset player & bufs
        self.init_player(position, remaining_lives)         # player
        self.__respawn_countdown = 2                        # Set timer to track respawn delay (invisible for duration)
        Shot.reset_class_variables()                        # bufs

    def init_player(self, position, remaining_lives):       
        self.spawn_guard = PLAYER_SPAWN_SAFEGUARD           # Set timer to track respawn invincable duration (but visable)
        self.__respawn_countdown = 0                        
        self.rotation = 0
        self.position = position
        self.velocity = pygame.Vector2(0, 0)
        # self.colour = "green"                               # Change player color to show he is invulnerable for now
        self.lives = remaining_lives                    
        self.non_hit_scoring_streak = 0                     # dying resets scoring streak
        self.shield_regeneration = 0                        # dying resets shield regeneration rate
        self.shield_charge = 10                             # shield inits at 10 strength when respawning
        self.shoot_timer = 0
