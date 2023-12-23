import pygame as pg, sys
# from pygame import mixer
from helper.paddle import *
from helper.ball import *
from helper.myconstants import *

pg.init()

###################################################################################################################
# MAIN GAME LOOP
###################################################################################################################

def play():
    pg.display.set_caption("Play Game")
    clock = pg.time.Clock()
    surface = pg.Surface(SCREEN.get_size()).convert()

    paddle = Paddle()
    ball = Ball()

    print(ball.velocity)

    while True:
        surface.fill("black")

        paddle.handle_keys()
        paddle.draw(surface)

        ball.draw(surface)
        ball.move()

        SCREEN.blit(surface, (0,0))
        pg.display.update()
        clock.tick(60)

play()