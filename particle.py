import math, pygame, random
from resources import screen

class Particle:
    # def __init__(self, x, y, orientation, ship_velocity=pygame.Vector2(0,0), color=(255, 200, 0)):
    def __init__(self, ship, color=(255, 200, 0)):        
        self.ship = ship
        self.x, self.y = self.__get_coordinates()
        self.lifetime = 8                               # how many frames it lives
        self.current_life = self.lifetime
        self.size = 3
        self.color = color                              # orange-yellow by def
        self.speed = random.uniform(1.5, 3)
        self.angle = self.ship.rotation - 90 + random.uniform(-15, 15)

    def __get_coordinates(self):
        points = self.ship.triangle()
        back_point = (points[1] + points[2]) / 2
        return back_point.x, back_point.y

    def update(self):                                   # Particles now move "forward" in the cone
        self.x += math.cos(math.radians(self.angle)) * self.speed + self.ship.velocity.x
        self.y += math.sin(math.radians(self.angle)) * self.speed + self.ship.velocity.y
        self.current_life -= 1

    def is_alive(self):
        return self.current_life > 0

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class ParticleSystem:
    def __init__(self, ship):
        self.ship = ship
        self.particles = []
    
    def create_particle(self, color=(255, 200, 0)):
        particle = Particle(self.ship, color)
        self.particles.append(particle)

    def create_particles(self, count=1):
        for i in range(count):
            if i % 2:
                self.create_particle()                                                                     # alternate base orange-yellow 
            else:
                self.create_particle((225 + random.randint(-60,30), 170 + random.randint(-30, 60), 0))   # alternate with some random built-in

    def update(self): # Update all particles and remove dead ones
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update()
    
    def draw(self, ):
        for particle in self.particles:
            particle.draw()
