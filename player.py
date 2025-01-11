import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot


# Class to handle the player
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.spawn_guard = PLAYER_SPAWN_SAFEGUARD
        self.lives = 3
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

        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_z]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

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