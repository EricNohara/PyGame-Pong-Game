import pygame as pg
from helper.myconstants import *
from helper.quitcheck import check_exit

###################################################################################################################
# PADDLE OBJECT
###################################################################################################################

class Paddle(object):
    def __init__(self):
        self.height = 120
        self.width = 20
        self.pos_x = WIDTH-40
        self.pos_y = (HEIGHT-self.height)/2
        self.score = 0
        self.scores = [0,0,0,0,0]
        self.color = "white"
        self.is_clicked = False
        self.clicked_loc = 0
        
    def draw(self, surface):
        rect = pg.Rect((self.pos_x, self.pos_y), (self.width, self.height))
        pg.draw.rect(surface, self.color, rect)

    def increase_score(self):
        self.score += 1

    def get_center(self):
        return self.pos_y + (self.height/2)

    def check_valid_pos(self):
        min_height = 0
        max_height = HEIGHT - self.height

        if self.pos_y <= min_height:
            return min_height
        elif self.pos_y >= max_height:
            return max_height
        else:
            return self.pos_y
        
    def mouse_on_paddle(self, m_posx, m_posy):
        if m_posx >= self.pos_x and m_posx <= (self.pos_x + self.width):
            if m_posy >= self.pos_y and m_posy <= (self.pos_y + self.height):
                return True
        return False
        
    def handle_keys(self):
        keys = pg.key.get_pressed()
        mouse_pos = pg.mouse.get_pos()
        adjusted_speed = DEFAULT_SPEED + 10 if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT] else DEFAULT_SPEED

        if keys[pg.K_w] or keys[pg.K_UP]:
            self.pos_y -= adjusted_speed
            self.pos_y = self.check_valid_pos()
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            self.pos_y += adjusted_speed
            self.pos_y = self.check_valid_pos()

        # Handle clicking and dragging as an input for moving the paddle
        for event in pg.event.get():
            check_exit(event)
            if event.type == pg.MOUSEBUTTONDOWN:
                self.is_clicked = self.mouse_on_paddle(mouse_pos[0], mouse_pos[1])
                self.clicked_loc = mouse_pos[1] - self.pos_y
            if event.type == pg.MOUSEBUTTONUP:
                self.is_clicked = False
        if self.is_clicked:
            self.pos_y = mouse_pos[1] - self.clicked_loc
            self.pos_y = self.check_valid_pos()

                

            

           
            

                
                

        
