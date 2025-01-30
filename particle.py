import math, pygame, random
from resources import screen
from enum import Enum

ThrusterPosition = Enum("ThrusterPosition", ["BACK","LEFT_BACK", "RIGHT_BACK"])


class Particle:
    # def __init__(self, x, y, orientation, ship_velocity=pygame.Vector2(0,0), color=(255, 200, 0)):
    def __init__(self, ship, thruster_position=ThrusterPosition.BACK, color=(255, 200, 0)):        
        self.ship = ship
        self.x, self.y = self.__get_coordinates(thruster_position)
        self.lifetime = 8                               # how many frames it lives
        self.current_life = self.lifetime
        self.size = 3
        self.color = color                              # orange-yellow by def
        self.speed = random.uniform(1.5, 3)
        self.angle = self.__get_angle(thruster_position)

    def __get_angle(self, thruster_position):
        match thruster_position:
            case ThrusterPosition.BACK:
                return self.ship.rotation - 90 + random.uniform(-15, 15)
            case ThrusterPosition.LEFT_BACK:
                return self.ship.rotation - 55 + random.uniform(-15, 15)
            case ThrusterPosition.RIGHT_BACK:
                return self.ship.rotation - 125 + random.uniform(-15, 15)
            case _:                                                         # Default position = BACK
                return self.ship.rotation - 90 + random.uniform(-15, 15)

    def __get_coordinates(self, thruster_position):
        match thruster_position:

            case ThrusterPosition.BACK:
                points = self.ship.triangle()
                back_point = (points[1] + points[2]) / 2                    # BACK = centre of base triangle

            case ThrusterPosition.LEFT_BACK:
                points = self.ship.triangle()
                # back_point = points[1] + (points[2] - points[1]) * (1/8)
                base_vector = points[2] - points[1]                         # Get direction vector along the base
                base_direction = base_vector.normalize()                    # Normalize it
                back_point = points[1] - (base_direction * 4)               # Move slightly left from points[1] (negative direction)                

            case ThrusterPosition.RIGHT_BACK:                                                       # Default position = BACK
                points = self.ship.triangle()
                # back_point = points[1] + (points[2] - points[1]) * (7/8)
                base_vector = points[2] - points[1]                         # Get direction vector along the base
                base_direction = base_vector.normalize()                    # Normalize it
                back_point = points[2] + (base_direction * 4)               # Move slightly left from points[1] (negative direction)                
                
            case _:                                                         # Default position = BACK
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
    def __init__(self, ship, thruster_position=ThrusterPosition.BACK):
        self.ship = ship
        self.thruster_position = thruster_position
        self.particles = []
    
    def create_particle(self, color=(255, 200, 0)):
        particle = Particle(self.ship, self.thruster_position, color)
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
