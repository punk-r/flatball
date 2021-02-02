import pygame
import math
import random

# barvy
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
grey = (192,192,192)
grey_lines = (102,102,102)
green_field =(0, 128, 43)
yellow_item_selected = (255, 255, 153)

debug_mode = 0
debug_mode2 = 0

#-----------------------------------------FUNKCE--------------------------------------------------------------

def pythagoras_distance (location_1,location_2):
    ingamer_adjescent =  abs (location_1[0]  -  location_2[0])
    ingamer_opposite =  abs (location_1[1] -  location_2[1])
    ingamer_hypotensue = math.sqrt(ingamer_adjescent **2 + ingamer_opposite **2)

    return ingamer_hypotensue


def f_is_clikced_on_circle(x_limits,y_limits,position_clicked):
    test = False
    if x_limits[0] <  position_clicked[0] and x_limits[1] > position_clicked[0]:
        if  y_limits[0] <  position_clicked[1] and y_limits[1] > position_clicked[1]:
            test = True

    return test


def draw_trening_field (game_window,game_field):                                                                               #POUZIVAT???? bude chybet 'sector' hriste pro hracovu polohu
    field_corners = [0,0,0,0]

    # hriste
    field = pygame.draw.rect(game_window.surface, green_field , (game_field.field_bl_corner[0] ,game_field.field_bl_corner[1] -game_field.field_height ,  \
                                                    game_field.field_width,game_field.field_height  )   ,  1)
    # 2x brany
    pygame.draw.rect(game_window.surface, white , (game_field.field_bl_corner[0] - game_field.goals_width  ,game_field.field_bl_corner[1] - game_field.field_height/2 - game_field.goals_height /2 ,  \
                                                    game_field.goals_width,game_field.goals_height  )   ,  1)


def draw_5aside_field (game_window,game_field):

    field_corners = [0,0,0,0]

    # hriste
    field = pygame.draw.rect(game_window.surface, green_field , (game_field.field_bl_corner[0] ,game_field.field_bl_corner[1] -game_field.field_height ,  \
                                                    game_field.field_width,game_field.field_height  )   ,  2)
    # 2x brany
    pygame.draw.rect(game_window.surface, blue , (game_field.field_bl_corner[0] - game_field.goals_width  ,game_field.field_bl_corner[1] - game_field.field_height/2 - game_field.goals_height /2 ,  \
                                                    game_field.goals_width,game_field.goals_height  )   ,  1)
    pygame.draw.rect(game_window.surface, red , (game_field.field_bl_corner[0] + game_field.field_width  ,game_field.field_bl_corner[1] - game_field.field_height/2 - game_field.goals_height /2 ,  \
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
