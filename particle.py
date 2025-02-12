import math, pygame, random
from constants import PLAYER_TURN_SPEED, FRAME_RATE, PARTICLE_CLOUD_DENSITY
from resources import surface
from enum import Enum

ThrusterPosition = Enum("ThrusterPosition", ["BACK", "LEFT_FRONT", "LEFT_BACK", "RIGHT_FRONT", "RIGHT_BACK"])


class ExplosionParticle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.size = 1
        self.time_to_live = 0.2
        self.updatefrequency = 3
        self.grow_factor = 3
        self.color = color

    def update(self, dt):
        if self.time_to_live > 0:                                           # Decrease time particle still has to live
            self.time_to_live -= dt
        if self.updatefrequency > 0:                                        # Decrease updatefrequency (tweak 'FLICKER & grow' effect here)
            self.updatefrequency -= 1
            return
        self.size = self.size * (1 + self.grow_factor * self.time_to_live)  # Increase size (tweak 'flicker & GROW' effect here)

    def draw(self):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

    def is_alive(self):
        return self.time_to_live > 0
    

class ExplosionParticleCloud:
    def __init__(self, x, y, duration=5.0, size=15):
        self.x = x
        self.y = y
        self.size = size
        self.time_to_live = duration
        self.create_frequency = 0
        self.particles = []

    def update(self, dt):
        self.generate_particles(dt)                                         # generate new particles to keep explosion going
        self.particles = [p for p in self.particles if p.is_alive()]        # Remove dead particles from list
        for particle in self.particles:                                    
            particle.update(dt)                                             # Update the living particles

    def draw(self):
        for particle in self.particles:
            particle.draw()

    def generate_particles(self, dt):
        if self.time_to_live > 0:                                           # Decrease time the cloud will stay generating particles
            self.time_to_live -= dt
        else:
            return                                                          # Abort creation when no longer active
        if self.create_frequency > 0:                                       # Control how fast particles are added to a cloud
            self.create_frequency -= 1
            return                                                          # Only create every so aften
        else:
            self.create_frequency = int(FRAME_RATE / 
                                        PARTICLE_CLOUD_DENSITY)             # Circle calue (60/30=every2 frames a particle is added)
        self.particles.append(                                                 
                ExplosionParticle(random.randint(-self.size,self.size) + self.x, 
                                  random.randint(-self.size,self.size) + self.y - 15, 
                                  (230 + random.randint(0,25), 150 + random.randint(0, 100), random.randint(0,50), 175)))    # 'Yellow/Orange/Red-ish', trying to look like explosion colors

    def is_active(self):
        return self.time_to_live > 0

class ThrusterParticle:
    def __init__(self, ship, thruster_position=ThrusterPosition.BACK, color=(255, 200, 0)):        
        self.ship = ship
        self.x, self.y = self.__get_coordinates(thruster_position)
        self.lifetime = 8                               # how many frames it lives
        self.current_life = self.lifetime
        self.size = 3
        self.color = color                              # orange-yellow by def
        self.speed = random.uniform(1.0, 2.0)
        self.angle = self.__get_angle(thruster_position)

    def __get_angle(self, thruster_position):
        match thruster_position:
            case ThrusterPosition.BACK:
                return self.ship.angle - 90 + random.uniform(-20, 20)
            case ThrusterPosition.LEFT_BACK:
                return self.ship.angle - 55 + random.uniform(-20, 20)
            case ThrusterPosition.RIGHT_BACK:
                return self.ship.angle - 125 + random.uniform(-20, 20)
            case ThrusterPosition.LEFT_FRONT:
                return self.ship.angle + 55 + random.uniform(-20, 20)
            case ThrusterPosition.RIGHT_FRONT:
                return self.ship.angle + 125 + random.uniform(-20, 20)
            case _:                                                         # Default position = BACK
                return self.ship.angle - 90 + random.uniform(-20, 20)

    def __get_coordinates(self, thruster_position):
        match thruster_position:

            case ThrusterPosition.BACK:
                points = self.ship.triangle()
                back_point = (points[1] + points[2]) / 2                    # BACK = centre of base triangle

            case ThrusterPosition.LEFT_FRONT:
                points = self.ship.triangle()
                side_vector = points[0] - points[1]                         # Vector along left side
                side_direction = side_vector.normalize()                    # Normalize it
                back_point = points[1] + (side_direction * side_vector.length() * 0.7)  # 70% up the side

            case ThrusterPosition.RIGHT_FRONT:
                points = self.ship.triangle()
                side_vector = points[0] - points[2]                         # Vector along right side
                side_direction = side_vector.normalize()                    # Normalize it
                back_point = points[2] + (side_direction * side_vector.length() * 0.7)  # 70% up the side

            case ThrusterPosition.LEFT_BACK:
                points = self.ship.triangle()
                base_vector = points[2] - points[1]                         # Get direction vector along the base
                base_direction = base_vector.normalize()                    # Normalize it
                back_point = points[1] - (base_direction * 4)               # Move slightly left from points[1] (negative direction)                

            case ThrusterPosition.RIGHT_BACK:                                                       
                points = self.ship.triangle()
                base_vector = points[2] - points[1]                         # Get direction vector along the base
                base_direction = base_vector.normalize()                    # Normalize it
                back_point = points[2] + (base_direction * 4)               # Move slightly left from points[1] (negative direction)                
                
            case _:                                                         # Default position = BACK
                points = self.ship.triangle()
                back_point = (points[1] + points[2]) / 2

        return back_point.x, back_point.y

    def update(self):
        # Original movement code
        self.x += math.cos(math.radians(self.angle)) * self.speed + self.ship.velocity.x
        self.y += math.sin(math.radians(self.angle)) * self.speed + self.ship.velocity.y
        
        # Base life reduction
        life_reduction = 1
        
        # Increase life reduction when rotating
        if hasattr(self.ship, 'last_rotation') and self.ship.last_rotation != 0:
            # Scale life reduction based on rotation speed
            rotation_factor = 50 * abs(self.ship.last_rotation) / PLAYER_TURN_SPEED
            life_reduction = 1 + rotation_factor
        
        self.current_life -= life_reduction
        # self.current_life -= 1

    def is_alive(self):
        return self.current_life > 0

    def draw(self):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)


class ParticleSystem:
    def __init__(self, ship, thruster_position=ThrusterPosition.BACK):
        self.ship = ship
        self.thruster_position = thruster_position
        self.particles = []
    
    def create_particle(self, color=(255, 200, 0)):
        particle = ThrusterParticle(self.ship, self.thruster_position, color)
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
    
    def draw(self):
        for particle in self.particles:
            particle.draw()
