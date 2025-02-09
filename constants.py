SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FRAME_RATE = 60
FRAME_RATE_MENU = 10

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_MAX_LUMP_SIZE = 0.9 # relative to ASTEROID_MIN_RADIUS
#ASTEROID_SPAWN_RATE = 0.8  # seconds
ASTEROID_SPAWN_RATE = 3.0  # seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ASTEROID_VELOCITY_MULTIPLIER = 0.1

PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 250
PLAYER_ACCELERATION = 4.0
PLAYER_MAXIMUM_SPEED = 7.5
PLAYER_BRAKE_FORE = 15
PLAYER_DRAG = 1.25
PLAYER_SPAWN_SAFEGUARD = 5 # seconds (2s is used to safeguard player while on respawn cooldown, 3 for immunity while recently respawned)

PLAYER_STARTING_SHIELD = 10
PLAYER_STARTING_LIVES = 3
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN = 0.4
PLAYER_MIN_SCORE_STREAK = 50

UPGRADE_KEY_COOLDOWN_TIMER = 1 # seconds

SHOT_RADIUS = 4
# SHOT_VALUE = 1

STARTING_LEVEL = 1
LEVEL_UP_VALUE = 1000
BOSS_SPAWN_LEVEL = 2