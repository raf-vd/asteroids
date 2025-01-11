import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def check_collision(self, other):
        distance = self.position.distance_to(other.position)
        return distance <= self.radius + other.radius

    def is_off_screen(self, screen):
        return (self.position.x < 0 or self.position.x > screen.get_width() or
                self.position.y < 0 or self.position.y > screen.get_height()) 
    
    def wrap_screen(self, screen):
        if self.position.x < 0 - self.radius:
            self.position.x = screen.get_width()
        elif self.position.x > screen.get_width() + self.radius:
            self.position.x = 0
        
        if self.position.y < 0 - self.radius:
            self.position.y = screen.get_height()
        elif self.position.y > screen.get_height() + self.radius:
            self.position.y = 0
