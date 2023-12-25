import pygame as pg, math
from helper.myconstants import *
from helper.quitcheck import check_exit
from helper.ball import *

###################################################################################################################
# PADDLE OBJECT
###################################################################################################################
class Paddle(object):
    def __init__(self):
        self.height = 120
        self.width = 20
        self.pos_x = 20
        self.pos_y = (HEIGHT-self.height)/2
        self.color = "white"

    def draw(self, surface):
        rect = pg.Rect((self.pos_x, self.pos_y), (self.width, self.height))
        pg.draw.rect(surface, self.color, rect)

    def increase_score(self):
        self.score += 1

    def check_valid_pos(self):
        min_height = 0
        max_height = HEIGHT - self.height

        if self.pos_y <= min_height:
            return min_height
        elif self.pos_y >= max_height:
            return max_height
        else:
            return self.pos_y
        
    def get_center(self):
        return self.pos_y + (self.height/2)
    
class PlayerPaddle(Paddle):
    def __init__(self):
        super().__init__()
        self.pos_x = WIDTH-40
        self.score = 0
        self.scores = [0,0,0,0,0]
        self.is_clicked = False
        self.clicked_loc = 0
        self.hitbox_x = self.pos_x
        
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

class OpponentPaddle(Paddle):
    def __init__ (self):
        super().__init__()
        self.hitbox_x = self.pos_x + (2 * self.width)


    def move_to_ball(self, ball):
        if ball.hit_by_player:
            # ball_center = ball.get_center()
            # projected_height = abs(math.tan(ball.bounce_angle) * (WIDTH - 80 - 2*ball.radius) + (HEIGHT - ball.pos_when_hit))

            # num_wall_hits = int(projected_height // HEIGHT)
            # print("wall hits:", num_wall_hits)

            # if ball.bounce_angle <= 0:
            #     true_projected_height = projected_height - (HEIGHT * num_wall_hits)
            #     print(num_wall_hits % 2)
            #     if num_wall_hits % 2 == 0:
            #         true_projected_height = HEIGHT - true_projected_height
            # if ball.bounce_angle > 0:
            #     true_projected_height = projected_height - (HEIGHT * num_wall_hits)
            #     print(num_wall_hits % 2)
            #     if num_wall_hits % 2 != 0:
            #         true_projected_height = HEIGHT - true_projected_height
            # # print("projected_height:", true_projected_height)


            # # projected_ball_y = abs((WIDTH - 80) * ball.velocity[1]) - projected_neg_y
                
            # # print("num walls hit: ", num_ceiling_bounce)
            # # print("projected y: ", projected_height)
            # self.pos_y = self.check_valid_pos()
    
            angle = ball.bounce_angle
            active_width = WIDTH - 80 - ball.radius
            tan_calc = abs(math.tan(angle) * active_width)
            ball_pos = ball.pos_when_hit
            
            if angle < 0:
                if ball_pos < (HEIGHT + ball.radius) and tan_calc >= ball_pos:
                    num_collisions = ((tan_calc - ball_pos)//HEIGHT) + 1
                    projected_y = tan_calc - ball_pos - ((num_collisions-1)*HEIGHT)
                    if num_collisions % 2 == 0:
                        projected_y = HEIGHT - projected_y
                else:
                    num_collisions = tan_calc // HEIGHT
                
            

            elif angle >= 0:
                if ball_pos > 0 and tan_calc >= (HEIGHT - ball_pos):
                    num_collisions = ((tan_calc - (HEIGHT - ball_pos))//HEIGHT) + 1
                else:
                    num_collisions = tan_calc // HEIGHT

                projected_y = tan_calc - (num_collisions * HEIGHT)
                if num_collisions % 2 != 0:
                    projected_y = HEIGHT - projected_y

            print(num_collisions)
            # print("projection:", projected_y)


    




                

            

           
            

                
                

        
