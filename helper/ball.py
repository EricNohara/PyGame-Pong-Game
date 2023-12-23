import pygame as pg, math
import random
from helper.myconstants import *
from helper.paddle import *

pg.init()

class Ball(object):
    def __init__(self):
        self.radius = 10
        self.pos_x = WIDTH/2 - self.radius
        self.pos_y = HEIGHT/2 - self.radius
        self.color = "white"
        self.velocity = self.set_init_velocity()

    def get_center(self):
        return self.pos_y + self.radius

    def set_init_velocity(self):
        rand_x = random.uniform(0.2, 0.8)
        return [rand_x, 1-rand_x]       #return a normalized vector

    def draw(self, surface):
        pg.draw.circle(surface, self.color, (self.pos_x, self.pos_y), self.radius)

    def reflect_velocity(self, axis):
        if axis == 0 or axis == 1:
            self.velocity[axis] *= -1

    def move(self):
        self.pos_x += self.velocity[0] * DEFAULT_SPEED
        self.pos_y += self.velocity[1] * DEFAULT_SPEED
        if self.pos_x <= self.radius or self.pos_x >= (WIDTH - self.radius):
            self.reflect_velocity(0)
        if self.pos_y <= self.radius or self.pos_y >= (HEIGHT - self.radius):
            self.reflect_velocity(1)

    def collide(self, paddle):
        ball_center = self.get_center()
        if (self.pos_x + self.radius) >= paddle.pos_x:
            if (ball_center + self.radius) >= paddle.pos_y and (ball_center + self.radius) <= (paddle.pos_y + paddle.height):
                intersect = ball_center - paddle.get_center()
                normalized_intersect = intersect/(paddle.height/2)
                bounce_angle = normalized_intersect * MAX_BOUNCE_ANGLE
                self.velocity[0] = math.cos(bounce_angle) * -1
                self.velocity[1] = math.sin(bounce_angle)
