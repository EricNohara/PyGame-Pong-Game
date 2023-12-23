import pygame as pg
import math

pg.init()

# SCREEN SETTINGS
SIZE = (WIDTH, HEIGHT) = (1280, 720)
SCREEN = pg.display.set_mode(SIZE)
CLOCK = pg.time.Clock()     #set the clock to the pygame clock

# FONTS
FONT = pg.font.Font('freesansbold.ttf', 30)
HEADER_FONT = pg.font.Font('freesansbold.ttf', 60)

# GAME SETTINGS
DEFAULT_SPEED = 15
MAX_BOUNCE_ANGLE = 5 * (math.pi/12)
