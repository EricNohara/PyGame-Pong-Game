import pygame as pg, sys

pg.init()

def check_exit(event):
    if event.type == pg.QUIT:
        pg.quit()
        sys.exit()