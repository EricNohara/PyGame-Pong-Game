import pygame as pg, math
from pygame import mixer
from helper.myconstants import *
from helper.quitcheck import check_exit
from helper.ball import *

###################################################################################################################
# PADDLE OBJECT
###################################################################################################################
class Paddle(object):
    """Do define a generic paddle class inherited by PlayerPaddles and OpponentPaddles."""
    def __init__(self):
        """Return instance variables and methods for the paddle class."""
        self.height = 120
        self.width = 20
        self.pos_x = 20
        self.pos_y = (HEIGHT-self.height)/2
        self.color = "white"
        self.score = 0

    def draw(self, surface):
        """Do draw paddle to the given surface."""
        rect = pg.Rect((self.pos_x, self.pos_y), (self.width, self.height))
        pg.draw.rect(surface, self.color, rect)

    def increase_score(self):
        """Do increment the paddle's score."""
        self.score += 1

    def check_valid_pos(self):
        """Do check if the current position of the paddle is valid."""
        min_height = 0
        max_height = HEIGHT - self.height

        if self.pos_y <= min_height:
            return min_height
        elif self.pos_y >= max_height:
            return max_height
        else:
            return self.pos_y
        
    def get_center(self):
        """Returns the calculated center of the paddle."""
        return self.pos_y + (self.height/2)
    
    def add_score(self): 
        """Do add one to the paddle's score."""
        self.score += 1
    
class PlayerPaddle(Paddle):
    """Do define a player paddle class which creates a player paddle."""
    def __init__(self):
        """Do set instance variables defined by parent class."""
        super().__init__()
        self.pos_x = WIDTH-40
        self.scores = [0,0,0,0,0]
        self.is_clicked = False
        self.clicked_loc = 0
        self.hitbox_x = self.pos_x
        
    def mouse_on_paddle(self, m_posx, m_posy):
        """Do return true if the mouse is on the paddle, and false otherwise."""
        if m_posx >= self.pos_x and m_posx <= (self.pos_x + self.width):
            if m_posy >= self.pos_y and m_posy <= (self.pos_y + self.height):
                return True
        return False
        
    def handle_keys(self):
        """Do handle keypresses to move the player up or down
        Do check if pygame is exited.
        Do check if a player position is valid.
        """
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

class OpponentPaddle(Paddle):
    """Do define opponent player paddle class."""
    def __init__ (self):
        """Do define opponent instance variables from parent class."""
        super().__init__()
        self.hitbox_x = self.pos_x + self.width

    def find_projected_y(self, ball):
        """Do calculate the projected number of wall hits using trigonometry.
        Return the project y position of the ball after the player paddle collides with the ball
        """
        angle = ball.bounce_angle
        active_width = WIDTH - 80 - ball.radius
        tan_calc = abs(math.tan(angle) * active_width)
        ball_pos = ball.pos_when_hit
        
        if angle < 0:
            if ball_pos < (HEIGHT - ball.radius) and tan_calc >= ball_pos:
                num_collisions = ((tan_calc - ball_pos)//HEIGHT) + 1
            else:
                num_collisions = tan_calc // HEIGHT

            remainder = (tan_calc + (HEIGHT - ball_pos)) % HEIGHT

            if num_collisions % 2 != 0:
                proj_height = remainder + 1
            elif num_collisions % 2 == 0:
                proj_height = HEIGHT - remainder

        elif angle >= 0:
            if ball_pos > 0 and tan_calc >= (HEIGHT - ball_pos):
                num_collisions = ((tan_calc - (HEIGHT - ball_pos))//HEIGHT) + 1
            else:
                num_collisions = tan_calc // HEIGHT

            remainder = (tan_calc + ball_pos) % HEIGHT
            
            if num_collisions % 2 != 0:
                proj_height = HEIGHT - remainder - 1
            elif num_collisions % 2 == 0:
                proj_height = remainder

        return proj_height - self.height/2

    def find_relative_error(self, projected_y):
        """Return the relative error for the given projected y value."""
        return ((projected_y + OPPONENT_MAX_SPEED) - (projected_y - OPPONENT_MAX_SPEED))/2

    def move_to_projected_y(self, projected_y, error):
        """Do move the opponent to the projected y value of the ball at a fixed speed."""
        if self.pos_y < projected_y and abs(self.pos_y - projected_y) > error:
            self.pos_y += OPPONENT_MAX_SPEED
            self.pos_y = self.check_valid_pos()
        elif self.pos_y > projected_y and abs(self.pos_y - projected_y) > error:
            self.pos_y -= OPPONENT_MAX_SPEED
            self.pos_y = self.check_valid_pos()
