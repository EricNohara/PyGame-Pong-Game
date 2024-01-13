import pygame as pg, math
from pygame import mixer
import random
from helper.myconstants import *
from helper.paddle import *

pg.init()

class Ball(object):
    def __init__(self):
        """Return initial instance variables and methods for the ball class."""
        self.radius = 10
        self.diameter = 2 * self.radius
        self.pos_x = WIDTH/2 - self.radius
        self.pos_y = HEIGHT/2 - self.radius
        self.color = "white"
        self.velocity = self.set_init_velocity()
        self.bounce_angle = MAX_BOUNCE_ANGLE
        self.hit_by_player = False
        self.hit_paddle = 0
        self.pos_when_hit = 0
        self.num_hits_by_paddle = 0
        self.current_speed = DEFAULT_SPEED

    def get_center(self):
        return self.pos_y + self.radius

    def set_init_velocity(self):
        rand_x = random.uniform(0.2, 0.8)
        return [rand_x, 1-rand_x]       #return a normalized vector

    def draw(self, surface):
        pg.draw.circle(surface, self.color, (self.pos_x, self.pos_y), self.radius)

    def reflect_velocity(self, axis):
        if axis == 0 or axis == 1:
            WALL_SOUND.play()
            self.velocity[axis] *= -1
    
    def reset_ball(self):
        self.velocity = self.set_init_velocity()
        self.hit_by_player = False
        self.pos_when_hit = 0
        self.bounce_angle = MAX_BOUNCE_ANGLE
        self.pos_x = WIDTH/2 - self.radius
        self.pos_y = HEIGHT/2 - self.radius
        self.num_hits_by_paddle = 0

    def move(self, player, opponent):
        self.current_speed = DEFAULT_SPEED + ((self.num_hits_by_paddle // 2) * 0.5)
        self.pos_x += self.velocity[0] * self.current_speed
        self.pos_y += self.velocity[1] * self.current_speed
        if self.pos_x <= self.radius or self.pos_x >= (WIDTH - self.radius):
            SCORE_SOUND.play()
            won_point = player if self.pos_x <= self.radius else opponent
            won_point.add_score()
            self.reset_ball()
        if self.pos_y <= self.radius or self.pos_y >= (HEIGHT - self.radius):
            self.reflect_velocity(1)
            self.pos_y = self.radius + 1 if self.pos_y <= self.radius else HEIGHT - self.radius + 1

    def test(self):
        if self.pos_x <= 45 and self.pos_x >= 30:
            print(self.pos_y + self.radius)

    def return_valid_angle(self, angle):
        if angle <= MAX_BOUNCE_ANGLE and angle >= (MAX_BOUNCE_ANGLE * -1):
            return angle
        else:
            fixed_angle = MAX_BOUNCE_ANGLE if angle > MAX_BOUNCE_ANGLE else (MAX_BOUNCE_ANGLE * -1)
            return fixed_angle
        
    def increment_num_hit_by_paddle(self):
        if self.hit_paddle == 1:
            self.num_hits_by_paddle += 1

    def collide(self, player, opponent):
        ball_center_y = self.get_center()
        ball_center_x = self.pos_x + self.radius
        if ball_center_x >= player.hitbox_x:
            if (ball_center_y + self.radius) >= player.pos_y and (ball_center_y - self.radius) <= (player.pos_y + player.height):
                PADDLE_SOUND.play()
                self.hit_by_player = True
                self.hit_paddle += 1
                self.pos_when_hit = self.get_center()
                intersect = ball_center_y - player.get_center()
                normalized_intersect = intersect/(player.height/2)
                self.bounce_angle = self.return_valid_angle(normalized_intersect * MAX_BOUNCE_ANGLE)
                self.velocity[0] = math.cos(self.bounce_angle) * -1
                self.velocity[1] = math.sin(self.bounce_angle)
        elif self.pos_x - self.radius <= opponent.hitbox_x:
            if (ball_center_y + self.radius) >= opponent.pos_y and (ball_center_y - self.radius) <= (opponent.pos_y + opponent.height):
                PADDLE_SOUND.play()
                self.hit_by_player = False
                self.hit_paddle += 1
                intersect = ball_center_y - opponent.get_center()
                normalized_intersect = intersect/(opponent.height/2)
                self.bounce_angle = self.return_valid_angle(normalized_intersect * MAX_BOUNCE_ANGLE)
                self.velocity[0] = math.cos(self.bounce_angle) 
                self.velocity[1] = math.sin(self.bounce_angle)
        else:
            self.hit_paddle = 0