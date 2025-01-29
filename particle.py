import math, pygame, random
from resources import screen

class Particle:
    def __init__(self, x, y, color = (255, 200, 0 )):
        self.x = x
        self.y = y
        self.lifetime = 8                               # how many frames it lives
        self.current_life = self.lifetime
        self.size = 3
        self.color = color                              # orange-yellow by def
        self.speed = random.uniform(1.5, 3)
        self.angle = 180 + random.uniform(-15, 15)

    def update(self):                                   # Particles now move "forward" in the cone
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        self.current_life -= 1

    def is_alive(self):
        return self.current_life > 0

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def create_particle(self, x, y, color=(255, 200, 0)):
        particle = Particle(x, y, color)
        self.particles.append(particle)

    def create_particles(self, x, y, count=1):
        for i in range(count):
            if i % 2:
                self.create_particle(x, y)                                                                    # alternate base orange-yellow 
            else:
                self.create_particle(x, y, (225 + random.randint(-60,30), 170 + random.randint(-30, 60), 0))  # alternate with some random built-in

    def update(self): # Update all particles and remove dead ones
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update()
    
    def draw(self, ):
        for particle in self.particles:
            particle.draw()
