import pygame as pg, sys
from helper.myconstants import *
import random
import numpy as np

pg.init()

class Ball(object):
    def __init__(self):
        self.radius = 10
        self.pos_x = WIDTH/2 - self.radius
        self.pos_y = HEIGHT/2 - self.radius
        self.color = "white"
        self.velocity = self.set_init_velocity()

    def set_init_velocity(self):
        rand_x = random.random()
        return [rand_x, 1-rand_x]       #return a normalized vector

    def draw(self, surface):
        pg.draw.circle(surface, self.color, (self.pos_x, self.pos_y), self.radius)

    def move(self):
        self.pos_x += self.velocity[0] * DEFAULT_SPEED
        self.pos_y += self.velocity[1] * DEFAULT_SPEED
        if self.pos_x <= self.radius or self.pos_x >= (WIDTH - self.radius):
            self.velocity[0] *= -1
        if self.pos_y <= self.radius or self.pos_y >= (HEIGHT - self.radius):
            self.velocity[1] *= -1
        