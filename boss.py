import pygame
import random
from constants import *
from functions import point_to_line_distance, scale_to_circle
from resources import boss_bullet_sound, boss_laser_channel, boss_laser_sound, boss_bullet_frames, shot_channel, surface
from circleshape import CircleShape
from particle import ExplosionParticleCloud
from health_bar import HealthBar

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__(self.containers)                   # Call the base class constructor to pass on the containers
        self.position = pygame.Vector2(x, y)
        self.framecount = 0                                 # Use to manipulate speed related actions
        self.vertical = 1                                   # Moving Up or Downn
        self.horizontal = 1                                 # Moving Left or Right
        self.target_x1 = self.position.x - 150              # Boss most left point
        self.target_x2 = self.position.x + 150              # Boss most right point
        self.target_y1 = 125                                # Boss low point
        self.target_y2 = self.target_y1 - 50                # Boss high point
        self.image = image  
        self.image.set_alpha(225)                           # Set transparency, values range from 0 (completely transparent) to 255 (completely solid)
        self.mask = pygame.mask.from_surface(self.image)    # Create a mask from the non-transparent pixel
        self.rect = self.image.get_rect()
        self.spawn_wait = 2
        self.max_hp = 25
        self.hp = 25
        self.death_animation_duration = 5.0
        self.health_bar = None
        self.ready = False
        self.alive = True
        self.bullets = []
        self.boss_bullet_cooldown = 2                       # Time between boss bullets
        self.laser_cooldown = BOSS_LASER_COOLDOWN           # Time between boss laser activations
        self.laser_radius = 1                               # Init laser spawning point radius
        self.laser_x = SCREEN_WIDTH                         # Init lasertarget x coordinate
        self.laser_color = (150,255,255,128)

    def update(self, dt, player):

        if self.hp == 0: return                                                                                                 # Stop calculating anything when dead      

        self.basic_movement(dt)                                                                                                 # Move around a bit
        if not self.ready: return                                                                                               # Fully spawn/descend first

        if self.laser_cooldown > 0:                                                                                             # Control laser frequency
            self.laser_cooldown -= dt
        else:
            self.laser_cooldown = BOSS_LASER_COOLDOWN                                                                           # Reset cooldown
        
        if self.laser_cooldown < 1:                                                                                             # Charge and Fire laser in 3 steps
            dx = random.randint(0, 100)
            if self.position.x + (self.image.get_width() / 2) > (SCREEN_WIDTH / 2): dx = -dx                                    # Aim a bit left/right from center when boss is right/left
            self.laser_x = self.position.x + (self.image.get_width()/2) + dx                                                    # Store aim (for collision & drawing)
            self.laser_radius = 6                                                                                               # Store laser spawn spot size in attribute for reference while firing
            if self.laser_hits_target(player): player.take_laser_hit()                                                          # Check & handle if/when lear hit the player
        elif self.laser_cooldown < 1.1:
            if not boss_laser_channel.get_busy(): boss_laser_sound.play()                                                       # Has it's own channel to force 1x play and not each beam
            self.laser_radius *= 1.2                                                                                            # Increase radius for burst-out effect right before firing
        elif self.laser_cooldown < 2:
            self.laser_radius += 0.175                                                                                          # Build up radius to indicate charging laser a bit before firing
        else:
            self.laser_radius = 1                                                                                               # Reset laser radius

        if self.boss_bullet_cooldown > 0:                                                                                       # Control boss bulllet frequency
            self.boss_bullet_cooldown -= dt
        else:
            self.boss_bullet_cooldown = 2                                   
            dx = random.choice([int(self.position.x) - 185, int(self.position.x) + 175])                                        # Randomly pick Left or Right side to fire from
            bb_size = BOSS_BULLET_SIZE
            if self.hp / self.max_hp < 0.25:                                                                                    # Increase size of boss bullets depending on his damaged %
                bb_size *= 1.75                                                                                 
            elif self.hp / self.max_hp < 0.50:          
                bb_size *= 1.50
            elif self.hp / self.max_hp < 0.75:          
                bb_size *= 1.25
            self.bullets.append(BossBullet(self.image.get_width() / 2 + dx, 
                                           self.position.y + self.image.get_height() - 10, 
                                           bb_size))                                                                            # Spawn a bullet when timer reaches 0

    def draw(self):
        surface.blit(self.image, self.position)                             # Draw boss
        if self.health_bar: 
            self.health_bar.draw(self.position)                             # Draw healthbar (only active after fully spawning in)
        self.draw_laser((150,255,255,128), self.laser_x, SCREEN_HEIGHT)     # Draw laser

        # Draw some sparkles to indicate boss is on fire
        if self.hp / self.max_hp < 0.25:
            size = 50
            ExplosionParticleCloud(self.position.x + 1/6 * self.image.get_width(), self.position.y + 2/3 * self.image.get_height(), 0.1, size)   # Show sparkles where boss wass hit
            ExplosionParticleCloud(self.position.x + 5/6 * self.image.get_width(), self.position.y + 2/3 * self.image.get_height(), 0.1, size)   # Show sparkles where boss wass hit
            ExplosionParticleCloud(self.position.x + 2/6 * self.image.get_width(), self.position.y + 1/5 * self.image.get_height(), 0.1, size)   # Show sparkles where boss wass hit
            ExplosionParticleCloud(self.position.x + 4/6 * self.image.get_width(), self.position.y + 4/5 * self.image.get_height(), 0.1, size)   # Show sparkles where boss wass hit
        elif self.hp / self.max_hp < 0.50:
            size = 35
            ExplosionParticleCloud(self.position.x + 1/6 * self.image.get_width(), self.position.y + 2/3 * self.image.get_height(), 0.1, size)   # Show sparkles where boss wass hit
            ExplosionParticleCloud(self.position.x + 5/6 * self.image.get_width(), self.position.y + 2/3 * self.image.get_height(), 0.1, size)   # Show sparkles where boss wass hit
        elif self.hp / self.max_hp < 0.75:
            size = 10
            ExplosionParticleCloud(self.position.x + 1/6 * self.image.get_width(), self.position.y + 2/3 * self.image.get_height(), 0.05, size)   # Show sparkles where boss wass hit
            ExplosionParticleCloud(self.position.x + 5/6 * self.image.get_width(), self.position.y + 2/3 * self.image.get_height(), 0.05, size)   # Show sparkles where boss wass hit

    def death_animation_active(self, dt):
        if self.death_animation_duration > 0:
            self.death_animation_duration -= dt
            alpha = self.image.get_alpha() - 0.50
            self.image.set_alpha(max(alpha,0))
        else:
            return False
        if self.image.get_alpha() < 10:
            size = 10
            duration = 0.4
        elif self.image.get_alpha() < 50:
            size = 25
            duration = 0.3
        elif self.image.get_alpha() < 100:
            size = 50
            duration = 0.2
        else:
            size = 75
            duration = 0.1
        ExplosionParticleCloud(self.position.x + 1/6 * self.image.get_width(), self.position.y + 2/3 * self.image.get_height(), duration, size)   # Show sparkles where boss wass hit
        ExplosionParticleCloud(self.position.x + 5/6 * self.image.get_width(), self.position.y + 2/3 * self.image.get_height(), duration, size)   # Show sparkles where boss wass hit
        ExplosionParticleCloud(self.position.x + 2/6 * self.image.get_width(), self.position.y + 1/5 * self.image.get_height(), duration, size)   # Show sparkles where boss wass hit
        ExplosionParticleCloud(self.position.x + 4/6 * self.image.get_width(), self.position.y + 4/5 * self.image.get_height(), duration, size)   # Show sparkles where boss wass hit
        ExplosionParticleCloud(self.position.x + 1/2 * self.image.get_width(), self.position.y + 1/2 * self.image.get_height(), duration, size)   # Show sparkles where boss wass hit
        ExplosionParticleCloud(self.position.x + 5/6 * self.image.get_width(), self.position.y + 1/4 * self.image.get_height(), duration, size)   # Show sparkles where boss wass hit
        ExplosionParticleCloud(self.position.x + 4/7 * self.image.get_width(), self.position.y + 3/5 * self.image.get_height(), duration, size)   # Show sparkles where boss wass hit
        return True

    def draw_laser(self, color, x2, y2):
        x_start = self.position.x + (self.image.get_width() / 2)                            # Laser starting point coordinates
        y_start = self.position.y + 50 + (self.image.get_height() / 2)
        if self.hp == 0: return                                                             # Stop drawing lasers when dead
        if self.laser_cooldown  < 1:
            pygame.draw.line(surface, color, (x_start, y_start), (x2, y2), 5)               # Draw laser in final second of timer
        if self.laser_cooldown < 2:
            pygame.draw.circle(surface, color, (x_start, y_start), self.laser_radius, 0)    # Draw laser spawning spot in last 2 seconds of timer

    def basic_movement(self, dt):
        self.framecount += 1                                        # Speed controlled by framerate

        if not self.ready:                                          # Initial descent/entry
            if self.framecount % 2 == 0: return                     # Reduce descendin speed (1x every 2 frames)
            self.framecount = 0                                     # Reset framecount
            self.position.y += 1                                    # Move down
            if self.position.y == self.target_y1: 
                self.ready =True                                    # Reached descent/entry => create healthbar
                self.health_bar = HealthBar(self.image.get_width(), 15, self.max_hp)
            return 
        
        if self.spawn_wait > 0:                                     # Hold still for 2s after arriving at low point
            self.spawn_wait -= dt
            return
        else:
            self.spawn_wait = 0                                     # make sure spawn_wait is at exactly 0, so not negative

        if self.framecount % 300 == 0:                              # Every 300 frames => randomlt change directions (or not)
            self.horizontal = random.choice([1, -1])
            self.vertical = random.choice([1, -1])
            self.framecount = 0

        if self.framecount % 2 == 0: return                    # Reduce descendin speed (1x every 2 frames)
        if self.position.y == self.target_y1: self.vertical = -1    # Control up/down
        if self.position.y == self.target_y2: self.vertical = 1 
        self.position.y += 1 * self.vertical                        # Move vertically

        if self.position.x == self.target_x1: self.horizontal = 1   # Control left/right
        if self.position.x == self.target_x2: self.horizontal = -1 
        self.position.x += 1 * self.horizontal                      # Move horizontally

    def reduce_hp(self, damage):
        self.hp -= damage
        self.health_bar.decrease(damage)
        if self.hp <= 0:
            self.alive = False

    def laser_hits_target(self, player):
        # Get laser start/end in vectors
        laser_start = pygame.Vector2(self.position.x + (self.image.get_width() / 2), self.position.y + 50 + (self.image.get_height() / 2))  
        laser_end = pygame.Vector2(self.laser_x, SCREEN_HEIGHT)                                                                                 
        distance = point_to_line_distance(player.position, laser_start, laser_end)              # Get distance from player centre to line
        if player.shield_charge > 0:
            # print(f"dis: {distance:<20}shr: 12.5+{player.radius}+{player.shield_charge}= {player.radius + 10 + player.shield_charge + 2.5}" )
            return distance <= (player.radius + 10 + player.shield_charge + 2.5)                # If shield is active, check against shield radius + half line width
        else:
            return distance <= (player.radius + 2.5)                                            # For non-shielded player, check against player radius + half line width

    def BOOTS__init__(self, image, x, y, width, height, hp):
        self.image = image
        self.x = x
        self.y = y
        # self.target_y = 100  # Where the boss will stop moving
        # self.width = width
        # self.height = height
        # self.hp = hp
        # self.alive = True
        # self.parts = {
        #     "core": {"rect": pygame.Rect(x + 50, y + 50, 100, 100), "hp": 100},
        #     "left_wing": {"rect": pygame.Rect(x, y + 50, 50, 100), "hp": 50},
        #     "right_wing": {"rect": pygame.Rect(x + 150, y + 50, 50, 100), "hp": 50}
        # }
        # self.bullets = []
        # self.last_shot_time = 0
        # self.shield_active = True
        # self.shield_hp = 200  # Shield health
        # self.max_shield_hp = 200  # For visual purposes        

    def BOOTS_draw(self, surface):
        """Draw the boss and its parts."""
        if self.alive:
            # Draw the main body
            surface.blit(self.image, (self.x, self.y))
            
            # Draw parts if still functional
            if self.parts["left_wing"]["hp"] > 0:
                surface.blit(self.left_wing_image, (self.x, self.y + 50))
            if self.parts["right_wing"]["hp"] > 0:
                surface.blit(self.right_wing_image, (self.x + 150, self.y + 50))
            
            self.draw_shield(surface)
            self.draw_bullets(surface)

    def BOOTS_take_damage(self, part_name, damage):
        """Handle damage dealt to the boss or its shield."""
        if self.shield_active:  # Damage the shield first
            self.shield_hp -= damage
            if self.shield_hp <= 0:
                self.shield_active = False  # Deactivate shield
                print("Shield destroyed!")
        else:
            # Normal per-part damage
            """Deal damage to a specific part."""
            if self.parts[part_name]["hp"] > 0:
                self.parts[part_name]["hp"] -= damage
                if self.parts[part_name]["hp"] <= 0:
                    print(f"{part_name} destroyed!")
                    # Optional: Hide the destroyed part or spawn debris            

    def BOOTS_fire_straight_bullets(self):
        """Fire bullets downward at regular intervals."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > 1000:  # Fire every 1000ms
            self.bullets.append(BossBullet(self.x + 75, self.y + 100, 5))  # Adjust positions
            self.bullets.append(BossBullet(self.x + 125, self.y + 100, 5))
            self.last_shot_time = current_time

    def BOOTS_fire_tracking_bullet(self, player_x, player_y):
        """Fire a slow tracking bullet at the player."""
        self.bullets.append(TrackingBullet(self.x + 100, self.y + 100, player_x, player_y, 2))  # Moderate speed

    def BOOTS_draw_shield(self, surface):
        """Visual representation of the shield as a circle or glow."""
        if self.shield_active:
            # Draw the shield as a translucent circle around the boss
            shield_color = (0, 128, 255)  # Blue-ish hue
            pygame.draw.ellipse(surface, shield_color, 
                                 (self.x - 20, self.y - 20, self.width + 40, self.height + 40), 3)
        
        # Handle turret mechanics
        if self.parts["left_wing"]["hp"] > 0:
            self.fire_left_turret()
        if self.parts["right_wing"]["hp"] > 0:
            self.fire_right_turret()

        # Remove any destroyed parts visually or mechanically
        for part_name, part in self.parts.items():
            if part["hp"] <= 0:
                print(f"{part_name} is no longer functioning!")


class BossBullet(CircleShape):
    def __init__(self, x, y, radius=BOSS_BULLET_SIZE, speed=2):
        super().__init__(x, y, radius)
        shot_channel.play(boss_bullet_sound)
        self.frames =  boss_bullet_frames
        self.normalize_frames()                                 # 1x untill I have decent frame images
        self.current_frame = 0
        self.image = pygame.transform.scale(self.frames[self.current_frame], (radius * 3.75, radius * 3.75))
        self.rect = self.image.get_rect(center=self.position)
        self.speed = speed
        self.animation_speed = 0.025
        self.timer = 0        

    def normalize_frames(self):
        for i in range(len(self.frames)):
            self.frames[i] = scale_to_circle(self.frames[i], self.radius)

    def update(self, dt):
        self.position.y += self.speed                           # Move bullet downwards
        self.timer += dt
        if self.timer >= self.animation_speed:
            self.timer = 0
            self.current_frame += 1
            if self.current_frame == len(self.frames):
                self.current_frame = 0
            self.image = self.frames[self.current_frame]

    def draw(self):
        if self.is_off_screen():
            self.kill()
        else:
            # keeping this commented out to verify collision with actual radius vs image size
            rect = self.image.get_rect()
            rect.center = self.position
            surface.blit(self.image, rect)
            # pygame.draw.circle(surface, "white", self.position, self.radius , 1)

class TrackingBullet: # BOOTS
    def __init__(self, x, y, target_x, target_y, speed):
        self.x, self.y = x, y
        # Calculate direction
        dx, dy = target_x - x, target_y - y
        distance = (dx**2 + dy**2)**0.5
        self.dx, self.dy = (dx / distance) * speed, (dy / distance) * speed
        self.rect = pygame.Rect(x, y, 15, 15)  # Slightly larger than regular bullets

    def update(self):
        """Move the bullet towards the target."""
        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 128, 0), self.rect.center, 8)  # Orange bullet