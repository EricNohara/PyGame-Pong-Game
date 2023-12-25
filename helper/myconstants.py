import pygame as pg
import math
from pygame import mixer

pg.init()

# SCREEN SETTINGS
SIZE = (WIDTH, HEIGHT) = (1280, 720)
# SIZE = (WIDTH, HEIGHT) = (640, 360)       # Testing Mode
SCREEN = pg.display.set_mode(SIZE)
CLOCK = pg.time.Clock()     #set the clock to the pygame clock

# FONTS
FONT = pg.font.Font('assets/good-times.otf', 30)
HEADER_FONT = pg.font.Font('assets/good-times.otf', 60)

# AUDIO
SCORE_SOUND = pg.mixer.Sound("assets/score.mp3")
PADDLE_SOUND = pg.mixer.Sound("assets/paddle-hit.mp3")
WALL_SOUND = pg.mixer.Sound("assets/wall-hit.mp3")

# GAME SETTINGS
DEFAULT_SPEED = 20
MAX_BOUNCE_ANGLE = 5 * (math.pi/12)
OPPONENT_MAX_SPEED = DEFAULT_SPEED / 4