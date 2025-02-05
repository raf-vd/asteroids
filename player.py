import math, pygame, random
from constants import *
from functions import point_in_triangle, point_to_line_distance
from resources import alert_channel, alert_sound, player_death_sound, player_explosion_frames, player_image, shield_channel, shield_hit_sound, surface
from circleshape import CircleShape
from enum import Enum
from explosion import Explosion
from particle import ParticleSystem, ThrusterPosition
from shot import Shot
from speedometer import Speedometer

# Possible powerups in an enum
PowerUp = Enum("PowerUp", ["PIERCING", "BIGGER_SHOT", "SMALLER_SHOT", "INCREASE_SHIELD", "DECREASE_SHIELD"])

# Class to handle the player
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.__piercing_active = False
        self.__shot_size_multiplier = 1
        self.__upgrade_countdown_piercing = 0
        self.__upgrade_countdown_bulletsize = 0
        self.__respawn_countdown = 0
        self.__strafe_active = False
        self.__boss_active = False
        self.angle = 0
        self.last_rotation = 0
        self.shoot_timer = 0
        self.spawn_guard = PLAYER_SPAWN_SAFEGUARD
        self.lives = PLAYER_STARTING_LIVES
        self.shield_charge = PLAYER_STARTING_SHIELD
        self.shield_regeneration = 0
        self.non_hit_scoring_streak = 0
        self.alpha = 255
        self.speedometer = Speedometer()
        self.front_thrusterL = ParticleSystem(self, ThrusterPosition.LEFT_FRONT)
        self.front_thrusterR = ParticleSystem(self, ThrusterPosition.RIGHT_FRONT)
        self.rear_thrusterL = ParticleSystem(self, ThrusterPosition.LEFT_BACK)
        self.rear_thruster = ParticleSystem(self, ThrusterPosition.BACK)
        self.rear_thrusterR = ParticleSystem(self, ThrusterPosition.RIGHT_BACK)
 
    def toggle_strafe(self):
        self.__strafe_active = not self.__strafe_active

    def strafe_active(self):
        return self.__strafe_active

    def toggle_boss_mode(self):
        self.__boss_active = not self.__boss_active

    def boss_active(self):
        return self.__boss_active

    def piercing_active(self):
        return self.__piercing_active

    def shot_size_multiplier(self):
        return self.__shot_size_multiplier

    def triangle(self):                     # calculate a triangle for player
        forward = pygame.Vector2(0, 1).rotate(self.angle)
        right = pygame.Vector2(0, 1).rotate(self.angle + 90) * self.radius / 1.5
        a = self.position + forward * self.radius * 1.25 # 25% correction on point a location to appear "better centered"
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self):                                                         # override draw from CircleShape
        if self.__respawn_countdown > 0:                                    # Don't show player while respawn cooldown is active
            self.speedometer.draw(True)                                     # If player is waiting for respawn: Draw broken speedometer
            return False  
                      
        self.wrap_screen()                                                  # Handle screen_wrapping (inherited method)

        #pygame.draw.polygon(screen, self.colour, self.triangle(), 2)       # Original version drew a triangle, replaced by same shape & size image
        r_img = pygame.transform.rotate(player_image, -self.angle)          # Make sure image rotates with player
        r_img.set_alpha(self.alpha)                                         # Handle 'invulnerable oscilation'
        rect = r_img.get_rect()
        rect.center = self.position  
        surface.blit(r_img, rect)                                           # Draw the actual image

        if int(self.shield_charge) > 0:                                     # Draw some fancy shields
            base_radius = self.radius + 10                                  # Base size of shield from player
            
            # Create multiple circles with varying radii and alpha
            for i in range(3):                                              # Number of ripple layers
                wave_speed = 0.003                                          # Lower = slower waves
                wave_amplitude = 8                                          # Higher = bigger waves (higer values cause collision detection to trigger seemingly too late)
                # Constrain the wave effect to stay to circle that is the actual shield
                raw_wave = math.sin(pygame.time.get_ticks() * wave_speed + i * 2) * wave_amplitude
                wave_offset = max(-self.shield_charge/2, min(self.shield_charge/2, raw_wave))                

                alpha_start = 100                                           # Starting alpha value
                alpha_decrease = 30                                         # How much alpha decreases per layer
                alpha = max(20, alpha_start - i * alpha_decrease)
                color = (100, 200, 250, alpha)                              # # Shield color and drawing, RGB + alpha
                shield_thickness = max(2, int(self.shield_charge/2))        # Thickness of shield line
                
                pygame.draw.circle(surface, color, self.position, base_radius + wave_offset + int(self.shield_charge), shield_thickness)

        # Show thrusters & speedometer
        self.front_thrusterL.draw()
        self.front_thrusterR.draw()
        self.rear_thrusterL.draw()
        self.rear_thruster.draw()
        self.rear_thrusterR.draw()
        self.speedometer.draw()
    
    def rotate(self, dt):                   # rotate the player (left, right)
        self.last_rotation = PLAYER_TURN_SPEED * dt  # Add this line
        self.angle += PLAYER_TURN_SPEED * dt    
        if self.last_rotation > 0:
            self.rear_thrusterR.create_particles(4)
        else:
            self.rear_thrusterL.create_particles(4)

    def strafe_or_rotate(self, keys, dt):
        if self.strafe_active():                                                  # swap controls
            if keys[pygame.K_q] or keys[pygame.K_LEFT]:     self.strafe(dt)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:    self.strafe(-dt)
            if keys[pygame.K_a]:                            self.rotate(-dt)
            if keys[pygame.K_e]:                            self.rotate(dt)
        else:                                                                   # original controls
            if keys[pygame.K_q] or keys[pygame.K_LEFT]:     self.rotate(-dt)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:    self.rotate(dt)
            if keys[pygame.K_a]:                            self.strafe(dt)
            if keys[pygame.K_e]:                            self.strafe(-dt)
            
    def move(self, dt):                     # move the player (forward, back)
        if self.velocity.magnitude() < PLAYER_MAXIMUM_SPEED:            # Limit maximum speed
            forward = pygame.Vector2(0, 1).rotate(self.angle)
            self.velocity += forward * PLAYER_ACCELERATION * dt
        if dt > 0: self.rear_thruster.create_particles(4)              # If moving forward (dt > 0), create thruster particles

    def strafe(self, dt):
        if self.velocity.magnitude() < PLAYER_MAXIMUM_SPEED:            # Limit maximum speed
            side = pygame.Vector2(1, 0).rotate(self.angle)
            self.velocity += side * PLAYER_ACCELERATION * dt
        if dt < 0: 
            self.front_thrusterL.create_particles(4)              # If strafing right (dt < 0), create thruster particles
            self.rear_thrusterL.create_particles(4)              
        if dt > 0:
            self.front_thrusterR.create_particles(4)              # If strafinf left (dt > 0), create thruster particles
            self.rear_thrusterR.create_particles(4)

    def slow_down(self, dt, slow_factor):
        if self.velocity.magnitude() < 0.01:                             # If velocity is very small, just stop completely
            self.velocity = pygame.Vector2(0, 0)
        else:
            slowing_force = self.velocity.normalize() * slow_factor     
            self.velocity -= slowing_force * dt                         # Reduce velocity natural drag or braking force in slow_factor

    def update(self, dt):                   # process inputs from keys and do all sorts of changes to player

        self.last_rotation = 0                              # Init rotation to keep track how much rotation there was in a frame

        if self.__respawn_countdown > 0:                    # Delay player respawn after death a short while (feels better)
            self.__respawn_countdown -= dt
            return False                                    # Don't do anything while respawn cooldown is active

        self.shoot_timer -= dt                              # Reduce the cooldown on the player's ability to shoor
        
        if self.spawn_guard > 0:                            # Change player transparancy when he respanws (fluctuating formula)
            self.alpha = 75 + int(125 * (math.sin(pygame.time.get_ticks() / 200) + 1) / 2)
            self.spawn_guard -= dt
        else:
            self.alpha = 255                                # Solid state again

        if self.__upgrade_countdown_piercing > 0:           # Limit buf duration
            self.__upgrade_countdown_piercing -= dt
        else:
            self.__piercing_active = False

        if self.__upgrade_countdown_bulletsize > 0:         # Limit buf duration
            self.__upgrade_countdown_bulletsize-= dt
        else:
            self.activate_upgrade(PowerUp.SMALLER_SHOT)

        if self.non_hit_scoring_streak > PLAYER_MIN_SCORE_STREAK:  # you need to have a minimal scoring streak to have any shield regeneration
            if self.shield_regeneration < 2.0:                                                                  # Hardcap shieldregen
                self.shield_regeneration = (self.non_hit_scoring_streak / 100) * (1 / (self.shield_charge*3 +1)) # Shield regen lowers when more shield is active
            self.activate_upgrade(PowerUp.INCREASE_SHIELD, self.shield_regeneration)

        # Process input
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_q] or keys[pygame.K_LEFT]:     self.rotate(-dt)
        # if keys[pygame.K_d] or keys[pygame.K_RIGHT]:    self.rotate(dt)
        # if keys[pygame.K_a]:                            self.strafe(dt)
        # if keys[pygame.K_e]:                            self.strafe(-dt)
        if keys[pygame.K_z] or keys[pygame.K_UP]:       self.move(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:     self.move(-dt)
        self.strafe_or_rotate(keys, dt)
        if keys[pygame.K_SPACE]:                        self.shoot()
        if keys[pygame.K_LSHIFT]:                       self.slow_down(dt, PLAYER_BRAKE_FORE)

        # Clamp vector components to restrict player to a certain area (when in boss mode)
        next_position = self.position + self.velocity          
        if self.boss_active():
            next_position.x = max(min(next_position.x, SCREEN_WIDTH - self.radius), self.radius)
            next_position.y = max(min(next_position.y, SCREEN_HEIGHT - self.radius), SCREEN_HEIGHT * 0.6)
            self.velocity = next_position - self.position

        # Move player according to current speed
        # self.position += self.velocity        
        self.position = next_position  

        # Create some drag to stop player even without braking
        if self.velocity.magnitude() > 0:
            self.slow_down(dt, PLAYER_DRAG)

        # Update thrusters & speedometer
        self.front_thrusterL.update()
        self.front_thrusterR.update()
        self.rear_thrusterL.update()
        self.rear_thruster.update()
        self.rear_thrusterR.update()
        self.speedometer.update(self.velocity)

    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS * self.__shot_size_multiplier, self.__piercing_active)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.angle) * PLAYER_SHOOT_SPEED

    def check_collision(self, other):

        # Check for shield collision first (if shield is active)
        if self.shield_charge > 0:
            if self.shield_collides(other):

                rc = other.check_collision(self)                            # Check returns -2 for miss,-1 for body hit, index of lump for lump hit                
                if rc >= -1: 
                    if shield_channel.get_busy(): shield_channel.stop()     # Quiet shield on emminent danger
                    if not alert_channel.get_busy():                        # Prevent sound overlap
                        alert_channel.play(alert_sound)                     # Alarm sound: ship body in contact with asteroid while shielded

                if rc > -1:  del other.lumps[rc]                            # Shield destroys lumps when they hit player ship while shielded

                if not alert_channel.get_busy():                            # Don't play shield buzz when alert is playing
                    if not shield_channel.get_busy():                       # Avoid overlapping same sound multiple times
                        shield_channel.play(shield_hit_sound)               # warning buzz

                self.non_hit_scoring_streak = 0                             # hits on shield resets scoring streak
                self.shield_regeneration * 0.9                              # hits on shield decrease regeneration rate
                self.activate_upgrade(PowerUp.DECREASE_SHIELD, 1)                 # reduce shieldcharge on hit
                return False                                                # return False prevent hits from hitting player while shielded

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
            if alert_channel.get_busy(): alert_channel.stop()                                   # Stop whatever the channel is playing
            alert_channel.play(player_death_sound)                                              # Play crash sound
            self.lives -= 1                                                                     # Player collided, take a life awat
            if self.lives == 0:                                                                 # Out of lives => game ends
                return True                             
            Explosion(self.position, 1, player_explosion_frames)                                # Go BOOM
            self.__respawn(pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), self.lives)     # Respawn player in centre of screen          
            return True
        
        return False                                                                            # No collision
    
    def activate_upgrade(self, upgrade, value=1):

        match upgrade:
        
            case PowerUp.PIERCING:
                if not self.__piercing_active:
                    self.__piercing_active = True
                    self.__upgrade_countdown_piercing = 5

            case PowerUp.BIGGER_SHOT:        
                if self.__shot_size_multiplier < 10: 
                    self.__shot_size_multiplier += 1
                    self.__upgrade_countdown_bulletsize = 1
                # if Shot.shot_size_multiplier < 10:
                #     Shot.shot_size_multiplier += 1
                #     self.__upgrade_countdown_bulletsize = 1

            case PowerUp.SMALLER_SHOT:
                if self.__shot_size_multiplier > 1:
                    self.__shot_size_multiplier -= 1
                    if self.__shot_size_multiplier > 1:
                        self.__upgrade_countdown_bulletsize = 1
                # if Shot.shot_size_multiplier > 1:
                #     Shot.shot_size_multiplier -= 1
                #     if Shot.shot_size_multiplier > 1:
                #         self.__upgrade_countdown_bulletsize = 1

            case PowerUp.INCREASE_SHIELD:
                if self.shield_charge + value < 100:
                    self.shield_charge += value
                else:
                    self.shield_charge = 100    # force down to max if somehow surpasses max

            case PowerUp.DECREASE_SHIELD:
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
        self.__strafe_active = False
        self.angle = 0
        self.last_rotation = 0
        self.position = position
        self.velocity = pygame.Vector2(0, 0)
        self.lives = remaining_lives                    
        self.non_hit_scoring_streak = 0                     # dying resets scoring streak
        self.shield_regeneration = 0                        # dying resets shield regeneration rate
        self.shield_charge = PLAYER_STARTING_SHIELD         # shield inits at 10 strength when respawning
        self.shoot_timer = 0
