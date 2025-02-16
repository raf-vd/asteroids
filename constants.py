SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FRAME_RATE = 60
FRAME_RATE_MENU = 10
MASTER_VOLUME_MAX = 1.0


ASTEROID_BASE_VALUE = 1800
ASTEROID_KINDS = 3
ASTEROID_MAX_LUMP_SIZE = 0.9        # relative to ASTEROID_MIN_RADIUS
ASTEROID_MIN_RADIUS = 20
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ASTEROID_SPAWN_RATE = 3.0           # seconds
ASTEROID_VELOCITY_MULTIPLIER = 0.1

PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 250
PLAYER_ACCELERATION = 4.0
PLAYER_MAXIMUM_SPEED = 7.5
PLAYER_BRAKE_FORE = 15
PLAYER_DRAG = 1.25
PLAYER_SPAWN_SAFEGUARD = 5          # seconds (2s is used to safeguard player while on respawn cooldown, 3 for immunity while recently respawned)

PLAYER_STARTING_SHIELD = 10
PLAYER_STARTING_LIVES = 2
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN = 0.4
PLAYER_MIN_SCORE_STREAK = 50

UPGRADE_KEY_COOLDOWN_TIMER = 1 # seconds

PARTICLE_CLOUD_DENSITY = 20
SHOT_RADIUS = 4

LASER_HIT_REGISTRATION_COOLDOWN = 0.1
LASER_HIT_DAMAGE = 5

STARTING_LEVEL = 1
LEVEL_UP_VALUE = 250    

BOSS_SPAWN_LEVEL = 2
BOSS_BASE_HIT_VALUE = 10
BOSS_KILL_VALUE = 1500
BOSS_BULLET_SIZE = 25
BOSS_LASER_COOLDOWN = 10