import pygame
from constants import *
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


    #  calculate a triangle for player
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    # override draw from CircleShape
    def draw(self, screen):
        self.wrap_screen(screen)
        pygame.draw.polygon(screen, self.colour, self.triangle(), 2)

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

    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def check_collision(self, other):
        # Broad check (avoid detailed checks when possible)
        if self.position.distance_to(other.position) > self.radius + other.radius:
            return False
        
        # Circle-centre check (avoid detailed checks when possible)
        triangle_points = self.triangle()
        if point_in_triangle(other.position, triangle_points):
            True

        # Check circle-centre distance to all (3) sides of self
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
            self.lives -= 1
            self.colour = "green"                       # Change player color to show he is invulnerable for now
            self.spawn_guard = PLAYER_SPAWN_SAFEGUARD
            self.position.x = SCREEN_WIDTH / 2
            self.position.y = SCREEN_HEIGHT / 2
            return True
        return False
    
    def activate_upgrade(self, upgrade):
        if upgrade == "PIERCING":
            if not Shot.piercing_active:
                Shot.piercing_active = True
                self.__upgrade_countdown_piercing = 5
        elif upgrade == "BIGGER_SHOT":
            if Shot.shot_size_multiplier < 10:
                Shot.shot_size_multiplier += 1
                self.__upgrade_countdown_bulletsize = 3
        elif upgrade == "SMALLER_SHOT":
            if Shot.shot_size_multiplier > 1:
                Shot.shot_size_multiplier -= 1
                if Shot.shot_size_multiplier > 1:
                    self.__upgrade_countdown_bulletsize = 3