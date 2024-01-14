import pygame as pg, sys

pg.init()

def check_exit(event):
    """Do check if pygame is exited."""
    if event.type == pg.QUIT:
        pg.quit()
        sys.exit()