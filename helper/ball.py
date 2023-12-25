import pygame as pg, math
import random
from helper.myconstants import *
from helper.paddle import *

pg.init()

class Ball(object):
    def __init__(self):
        self.radius = 10
        self.diameter = 2 * self.radius
        self.pos_x = WIDTH/2 - self.radius
        self.pos_y = HEIGHT/2 - self.radius
        self.color = "white"
        self.velocity = self.set_init_velocity()
        self.bounce_angle = MAX_BOUNCE_ANGLE
        self.hit_by_player = False
        self.pos_when_hit = 0

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
    
    def reset_ball(self):
        self.velocity = self.set_init_velocity()
        self.hit_by_player = False
        self.pos_when_hit = 0
        self.bounce_angle = MAX_BOUNCE_ANGLE
        self.pos_x = WIDTH/2 - self.radius
        self.pos_y = HEIGHT/2 - self.radius

    def move(self, player, opponent):
        self.pos_x += self.velocity[0] * DEFAULT_SPEED
        self.pos_y += self.velocity[1] * DEFAULT_SPEED
        if self.pos_x <= self.radius or self.pos_x >= (WIDTH - self.radius):
            won_point = player if self.pos_x <= self.radius else opponent
            won_point.add_score()
            self.reset_ball()
        if self.pos_y <= self.radius or self.pos_y >= (HEIGHT - self.radius):
            self.reflect_velocity(1)

    def test(self):
        if self.pos_x <= 45 and self.pos_x >= 30:
            print(self.pos_y + self.radius)

    def collide(self, player, opponent):
        ball_center_y = self.get_center()
        ball_center_x = self.pos_x + self.radius
        if (ball_center_x + self.radius) >= player.hitbox_x:
            if (ball_center_y + self.radius) >= player.pos_y and (ball_center_y - self.radius) <= (player.pos_y + player.height):
                self.hit_by_player = True
                self.pos_when_hit = self.get_center()
                intersect = ball_center_y - player.get_center()
                normalized_intersect = intersect/(player.height/2)
                self.bounce_angle = normalized_intersect * MAX_BOUNCE_ANGLE
                self.velocity[0] = math.cos(self.bounce_angle) * -1
                self.velocity[1] = math.sin(self.bounce_angle)
        elif (ball_center_x - self.radius) <= opponent.hitbox_x:
            if (ball_center_y + self.radius) >= opponent.pos_y and (ball_center_y - self.radius) <= (opponent.pos_y + opponent.height):
                self.hit_by_player = False
                intersect = ball_center_y - opponent.get_center()
                normalized_intersect = intersect/(opponent.height/2)
                self.bounce_angle = normalized_intersect * MAX_BOUNCE_ANGLE
                self.velocity[0] = math.cos(self.bounce_angle) 
                self.velocity[1] = math.sin(self.bounce_angle)
