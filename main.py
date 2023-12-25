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

    player = PlayerPaddle()
    opponent = OpponentPaddle()
    ball = Ball()

    while True:
        surface.fill("black")

        player.handle_keys()
        player.draw(surface)
        opponent.draw(surface)

        ball.draw(surface)
        ball.move()

        if ball.hit_by_player:
            projected_y = opponent.find_projected_y(ball)

        ball.collide(player, opponent)
        # ball.test()
      
        SCREEN.blit(surface, (0,0))
        pg.display.update()
        clock.tick(60)

play()