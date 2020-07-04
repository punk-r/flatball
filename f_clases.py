import f_menu
from f_menu import *

import math
import random

#pygame modul
import pygame
from pygame.locals import *

# class window
class game_window():
    window_width = 900
    window_height = 500
    surface = pygame.display.set_mode((window_width,window_height),0,32)
    items_on_surface =0



class game_field():
    goals_height = 100
    goals_width = 10
    field_bl_window = [100,500]
    lab_mode_b = 1
    field_width = 1000
    field_height = 500
    field_bl_corner = [200,650]
    #rozdil okna pro hriste a hriste samotneho
    gap = 20

    def set_field (self,game_window):
        self.field_bl_window[0] = 1/6 * game_window.window_width
        self.field_bl_window[1] = 4/5 * game_window.window_height
        self.field_bl_corner[0] = 1/6 * game_window.window_width + self.gap
        self.field_bl_corner[1] = 4/5 * game_window.window_height - self.gap
        self.field_width = 0.75 * game_window.window_width
        self.field_height = 0.7 * game_window.window_height


class ingamer():
    def __init__(self,new_position):
        self.position = new_position
    radius = 15
    destination_move = [0,0]
    lab_mode_b = 1
    velocity = [1,0]
    color = blue
    collision_allowed_b = 0
    selected_b = 0
    path_target =[0,0]

    def set_path_target(self,new_target):
        self.path_target = new_target

    def draw_ingamer (self,game_window):
        if self.selected_b == 1:
            color = yellow_item_selected
        else :
            color = self.color
        ingamer_item = pygame.draw.circle(game_window.surface, color, ( self.position[0] ,self.position[1]) ,self.radius, self.radius)

    def set_position(self,new_x,new_y):
        self.position = [new_x,new_y]

    def move(self,The_game_window,The_field):
        #global The_field
        bottom = The_field.field_bl_corner[1]
        top    = The_field.field_bl_corner[1] + The_field.field_width
        right  = The_field.field_bl_corner[0] + The_field.field_width
        left   = The_field.field_bl_corner[0]

        #-------------DODELAT zadany testovaci hodnoty----------------------
        self.position =  [ self.position[0] + self.velocity[0]  ,self.position[1]  + self.velocity[1]  ]
        if self.position[0] < 10:
            self.velocity[0] = -1 * self.velocity[0]
        if self.position[0] > 600:
            self.velocity[0] = -1 * self.velocity[0]

        self.draw_ingamer(The_game_window)




    def is_selected (self,position_clicked):
        x_limits = [  self.position[0] - self.radius   ,  self.position[0] + self.radius    ]
        y_limits = [  self.position[1] - self.radius   ,  self.position[1] + self.radius    ]

        if f_is_clikced_on_circle(x_limits,y_limits,position_clicked) == 1:
            self.selected_b = 1
        else:
            self.selected_b = 0




    def read_selected_b (self):
        return self.selected_b



def f_is_clikced_on_circle(x_limits,y_limits,position_clicked):
    test = 0
    if x_limits[0] <  position_clicked[0] and x_limits[1] > position_clicked[0]:
        if  y_limits[0] <  position_clicked[1] and y_limits[1] > position_clicked[1]:
            test = 1

    return test



class player (ingamer):
    game_status = 0
    angle = 0
    user_driven = 0
    team = 0
    speed  = 0
    balance  = 0
    acuracy = 0
    team = 0
    player_type = 0
    position_by_strategy = 0
    strategy = 0
    tactic= 0
    dsetination_kick = 0
    vision = 50



    def draw_player(self,game_window):
        self.draw_ingamer(game_window)
        # qvadrant
        under = 1
        left = 1
        if self.path_target[0] < self.position[0]:
            left = -1
        # osa y zacina nulou a roste smerem dolu
        if self.path_target[1] < self.position[1]:
            under = -1

        mouse_adjescent =  abs (self.position[0] -  self.path_target[0])
        mouse_opposite =  abs (  self.position[1] -  self.path_target[1]  )
        mouse_hypotensue = math.sqrt(mouse_opposite**2   +    mouse_adjescent**2)

        ratio_hypotensue =  mouse_hypotensue / self.vision
        # vision ukazuje vzdy stejnou vzdalenost
        if mouse_hypotensue < 1:
            mouse_hypotensue = 1

        vision_opposite = mouse_opposite / ratio_hypotensue
        vision_adjescent = mouse_adjescent / ratio_hypotensue


        if self.lab_mode_b == 1:
            pygame.draw.lines(game_window.surface, grey_lines, True, ((self.position[0] ,self.position[1] ), \
                                                                    ( self.position[0] + vision_adjescent * left ,self.position[1]  )), 1)

            pygame.draw.lines(game_window.surface, grey_lines, True, ((self.position[0] + vision_adjescent * left ,self.position[1] ), \
                                                    ( self.position[0] + vision_adjescent * left ,self.position[1] + vision_opposite * under )), 1)


            # posun 2 pixely aby se neprektyvaly linky
            pygame.draw.lines(game_window.surface, red, True, ((self.position[0] + 2,self.position[1]+ 2 ), \
                                                                    ( self.position[0] + mouse_adjescent * left + 2 ,self.position[1] + 2 )), 1)

            pygame.draw.lines(game_window.surface, red, True, ((self.position[0] + mouse_adjescent * left + 2 ,self.position[1]  + 2), \
                                                    ( self.position[0] + mouse_adjescent * left + 2 ,self.position[1] + mouse_opposite * under + 2 )), 1)

            pygame.draw.lines(game_window.surface, red, True, ((self.position[0] + 2 ,self.position[1] +2 ), \
                                                    ( self.position[0] + mouse_adjescent * left + 2,self.position[1] + mouse_opposite * under + 2 )), 1)




        pygame.draw.lines(game_window.surface, blue, True, ((self.position[0] ,self.position[1] ), \
                                                ( self.position[0] + vision_adjescent * left ,self.position[1] + vision_opposite * under )), 1)





class ball (ingamer):
    resistance = 1
    color = white
    radius = 10



#jak se hybe kontroluje path !!!!!!!





def draw_5aside_field (game_window,game_field):
    field_corners = [0,0,0,0]

    # hriste
    field = pygame.draw.rect(game_window.surface, green_field , (game_field.field_bl_corner[0] ,game_field.field_bl_corner[1] -game_field.field_height ,  \
                                                    game_field.field_width,game_field.field_height  )   ,  1)

    # 2x brany
    pygame.draw.rect(game_window.surface, white , (game_field.field_bl_corner[0] - game_field.goals_width  ,game_field.field_bl_corner[1] - game_field.field_height/2 - game_field.goals_height /2 ,  \
                                                    game_field.goals_width,game_field.goals_height  )   ,  1)

    pygame.draw.rect(game_window.surface, white , (game_field.field_bl_corner[0] + game_field.field_width  ,game_field.field_bl_corner[1] - game_field.field_height/2 - game_field.goals_height /2 ,  \
                                                    game_field.goals_width,game_field.goals_height  )   ,  1)

    # pulici cara hriste
    pygame.draw.lines(game_window.surface, grey_lines, True, ((game_field.field_bl_corner[0] + game_field.field_width /2 ,field.top ) ,  \
                                                        ( game_field.field_bl_corner[0] + game_field.field_width /2,field.bottom )), 1)

    # 2x stred hriste
    pygame.draw.circle(game_window.surface, grey_lines, ( int(game_field.field_bl_corner[0] + game_field.field_width /2) ,int(field.top + game_field.field_height/2)) , 6, 1)
    pygame.draw.circle(game_window.surface, grey_lines, ( int(game_field.field_bl_corner[0] + game_field.field_width /2) ,int(field.top + game_field.field_height/2)) , 50, 1)


    # sektory hriste - orintace hracu v poli
    if game_field.lab_mode_b == 1:
            pygame.draw.rect(game_window.surface, darkBlue , (game_field.field_bl_corner[0] + game_field.field_width /3   ,field.top + 5,  \
                                                            game_field.field_width /3  ,game_field.field_height -10  )   ,  1)

            pygame.draw.rect(game_window.surface, darkBlue , (field.left +5 ,game_field.field_bl_corner[1] - game_field.field_height * 2/3,  \
                                                            game_field.field_width -10 ,game_field.field_height /3  )   ,  1)
