import pygame as pg, sys
from helper.myconstants import *

pg.init()

class Ball(object):
    def __init__(self):
        self.radius = 10
        self.pos_x = WIDTH/2 - self.radius
        self.pos_y = HEIGHT/2 - self.radius
        self.color = "white"

    def draw(self, surface):
        pg.draw.circle(surface, self.color, (self.pos_x, self.pos_y), self.radius)
        