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
        ball.move(player, opponent)

        if ball.hit_by_player:
            projected_y = opponent.find_projected_y(ball)
            relative_error = opponent.find_relative_error(projected_y)
            opponent.move_to_projected_y(projected_y, relative_error)

        ball.collide(player, opponent)
     
        # print(ball.velocity)

        SCREEN.blit(surface, (0,0))
        pg.display.update()
        clock.tick(60)

play()