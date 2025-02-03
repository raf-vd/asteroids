import pygame
from constants import *

class Boss:
    def __init__(self, image, x, y, width, height, hp):
        self.image = image
        self.x = x
        self.y = y
        self.target_y = 100  # Where the boss will stop moving
        self.width = width
        self.height = height
        self.hp = hp
        self.alive = True
        self.parts = {
            "core": {"rect": pygame.Rect(x + 50, y + 50, 100, 100), "hp": 100},
            "left_wing": {"rect": pygame.Rect(x, y + 50, 50, 100), "hp": 50},
            "right_wing": {"rect": pygame.Rect(x + 150, y + 50, 50, 100), "hp": 50}
        }
        self.bullets = []
        self.last_shot_time = 0
        self.shield_active = True
        self.shield_hp = 200  # Shield health
        self.max_shield_hp = 200  # For visual purposes        

    def enter_field(self):
        """Move the boss down until it reaches its target position."""
        if self.y < self.target_y:
            self.y += 2  # Adjust speed as desired

    def draw(self, surface):
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
            
    def reduce_hp(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False

    def take_damage(self, part_name, damage):
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

    def fire_straight_bullets(self):
        """Fire bullets downward at regular intervals."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > 1000:  # Fire every 1000ms
            self.bullets.append(BossBullet(self.x + 75, self.y + 100, 5))  # Adjust positions
            self.bullets.append(BossBullet(self.x + 125, self.y + 100, 5))
            self.last_shot_time = current_time

    def update_bullets(self):
        """Update and remove off-screen bullets."""
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.rect.y > SCREEN_HEIGHT:  # Remove off-screen bullets
                self.bullets.remove(bullet)

    def draw_bullets(self, surface):
        for bullet in self.bullets:
            bullet.draw(surface)

    def fire_tracking_bullet(self, player_x, player_y):
        """Fire a slow tracking bullet at the player."""
        self.bullets.append(TrackingBullet(self.x + 100, self.y + 100, player_x, player_y, 2))  # Moderate speed

    def draw_shield(self, surface):
        """Visual representation of the shield as a circle or glow."""
        if self.shield_active:
            # Draw the shield as a translucent circle around the boss
            shield_color = (0, 128, 255)  # Blue-ish hue
            pygame.draw.ellipse(surface, shield_color, 
                                 (self.x - 20, self.y - 20, self.width + 40, self.height + 40), 3)

    def update(self):
        """Update the boss behavior and remove destroyed parts."""
        self.enter_field()
        
        # Handle turret mechanics
        if self.parts["left_wing"]["hp"] > 0:
            self.fire_left_turret()
        if self.parts["right_wing"]["hp"] > 0:
            self.fire_right_turret()

        # Remove any destroyed parts visually or mechanically
        for part_name, part in self.parts.items():
            if part["hp"] <= 0:
                print(f"{part_name} is no longer functioning!")

        self.update_bullets()

class BossBullet:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 10, 20)  # Adjust size as needed
        self.speed = speed

    def update(self):
        """Move the bullet downward."""
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)  # Red bullets


class TrackingBullet:
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