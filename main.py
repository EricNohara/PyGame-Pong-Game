import pygame as pg, sys
# from pygame import mixer
from helper.paddle import *
from helper.myconstants import *
from helper.quitcheck import check_exit

pg.init()

###################################################################################################################
# MAIN GAME LOOP
###################################################################################################################

def play():
    pg.display.set_caption("Play Game")
    clock = pg.time.Clock()
    surface = pg.Surface(SCREEN.get_size()).convert()
    surface.fill("black")

    paddle = Paddle()

    while True:
        paddle.handle_keys()
        paddle.draw(surface)
        
        SCREEN.blit(surface, (0,0))
        pg.display.update()
        clock.tick(60)

play()