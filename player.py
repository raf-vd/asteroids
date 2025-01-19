import pygame
from constants import *
from resources import player_death_sound
from circleshape import CircleShape
from shot import Shot
from functions import point_in_triangle, point_to_line_distance

# Class to handle the player
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.__upgrade_key_cooldown_timer = 0
        self.__upgrade_countdown_piercing = 0
        self.__upgrade_countdown_bulletsize = 0
        self.rotation = 0
        self.shoot_timer = 0
        self.spawn_guard = PLAYER_SPAWN_SAFEGUARD
        self.lives = PLAYER_STARTING_LIVES
        self.colour = "green"
        self.shield_charge = 10             # start with 10 shieldcharge
        self.shield_regeneration = 0
        self.non_hit_scoring_streak = 0

    #  calculate a triangle for player
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius * 1.25 # 25% correction on point a location to appear "better centered"
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    # override draw from CircleShape
    def draw(self, screen, surface):
        self.wrap_screen(screen)
        pygame.draw.polygon(screen, self.colour, self.triangle(), 2)
        if self.shield_charge > 0:
            pygame.draw.circle(surface, (150, 250, 150, 50), self.position, self.radius + 10 + int(self.shield_charge), int(self.shield_charge))

    # rotate the player (left, right)
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    # move the player (forward, back)
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt 

    # process inputs from keys
    def update(self, dt):

        self.shoot_timer -= dt
        if self.spawn_guard < PLAYER_SPAWN_SAFEGUARD * 0.2: # return to fighting color at 80% of spawn_guard has passed so player gets to safety asap
            self.colour = "white"

        if self.spawn_guard > 0:
            self.spawn_guard -= dt

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
            if self.shield_regeneration < 2.5:
                self.shield_regeneration = self.non_hit_scoring_streak / 10000
            self.activate_upgrade("INCREASE_SHIELD", self.shield_regeneration)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:     self.rotate(-dt)
        if keys[pygame.K_d]:     self.rotate(dt)
        if keys[pygame.K_z]:     self.move(dt)
        if keys[pygame.K_s]:     self.move(-dt)
        if keys[pygame.K_SPACE]: self.shoot()

        if self.__upgrade_key_cooldown_timer > 0:
            return False
        
        if keys[pygame.K_DELETE]:
            self.activate_upgrade("PIERCING")
            self.__upgrade_key_cooldown_timer = UPGRADE_KEY_COOLDOWN_TIMER

        if keys[pygame.K_PAGEUP]:
            self.activate_upgrade("BIGGER_SHOT")
            self.__upgrade_key_cooldown_timer = UPGRADE_KEY_COOLDOWN_TIMER
        if keys[pygame.K_PAGEDOWN]:
            self.activate_upgrade("SMALLER_SHOT")
            self.__upgrade_key_cooldown_timer = UPGRADE_KEY_COOLDOWN_TIMER

        if keys[pygame.K_HOME]:
            self.activate_upgrade("INCREASE_SHIELD", 10)
            # self.__upgrade_key_cooldown_timer = UPGRADE_KEY_COOLDOWN_TIMER
        if keys[pygame.K_END]:
            self.activate_upgrade("DECREASE_SHIELD", 10)
            #self.__upgrade_key_cooldown_timer = UPGRADE_KEY_COOLDOWN_TIMER

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
                self.non_hit_scoring_streak = 0                # hits on shield resets scoring streak
                self.shield_regeneration * 0.9                 # hits on shield decrease regeneration rate
                self.activate_upgrade("DECREASE_SHIELD", 1)    # reduce shieldcharge on hit
                return False                                   # return False prevent hits from hitting player while shielded

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
        if self.spawn_guard > 0: 
            return False
        
        if self.check_collision(target):
            player_death_sound.play()
            self.lives -= 1
            if self.lives == 0:
                return True                             # Player died => don't respawn
            self.colour = "green"                       # Change player color to show he is invulnerable for now
            self.spawn_guard = PLAYER_SPAWN_SAFEGUARD
            self.position.x = SCREEN_WIDTH / 2
            self.position.y = SCREEN_HEIGHT / 2
            self.non_hit_scoring_streak = 0             # dying resets scoring streak
            self.shield_regeneration = 0                # dying resets shield regeneration rate
            self.shield_charge = 10                     # shield inits at 10 strength when respawning
            return True
        return False
    
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
