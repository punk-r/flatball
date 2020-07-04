import pygame
import sys
import math
import random

import os.path
from os import path

#pygame modul
pygame.init()
from pygame.locals import *

MenuFont = pygame.font.SysFont("Arial", 18)
WelcomeFont = pygame.font.SysFont("Arial", 40)

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

menu_line_spacing = 20
heading_shift = 30


def choose_menu_from_selection(The_game_window,The_field,selection):

    draw_menu_lines(The_game_window,The_field)

    if selection == 'A':
         draw_main_menu(The_game_window,menu_line_spacing,heading_shift)
    elif selection == 'AA':
        draw_AA_menu(The_game_window,menu_line_spacing,heading_shift)
    elif selection == 'AB':
        draw_AB_menu(The_game_window,menu_line_spacing,heading_shift)
    elif selection == 'AC':
        draw_AC_menu(The_game_window,menu_line_spacing,heading_shift)
    elif selection == 'AD':
        draw_AD_menu(The_game_window,menu_line_spacing,heading_shift)
    elif selection == 'AE':
        draw_AE_menu(The_game_window,menu_line_spacing,heading_shift)
    else:
        pass

def f_choose_scree_from_selection(game_menu_selcection):
    screen = 1
    if game_menu_selcection == 'AA' :
        screen = 2
    return screen    

def draw_weclome(The_game_window):
    test = WelcomeFont.render('Flatball vitejte', 1, grey)
    The_game_window.surface.blit(test,(The_game_window.window_width * 0.4 , The_game_window.window_height * 0.3))


def draw_main_menu(The_game_window,menu_line_spacing,heading_shift):
    menu = [ 'nova hra', 'trener','reff','nastaveni','napoveda','Lab','1','2','3' ]
    for menu_loop in range(0,len(menu)):
        menu_moves_pages = MenuFont.render(menu[menu_loop], 1, grey)
        The_game_window.surface.blit(menu_moves_pages,(50, menu_loop *  menu_line_spacing + heading_shift))


def draw_AA_menu(The_game_window,menu_line_spacing,heading_shift):
    menu = [ '<-nova hra zahajena', 'statss','menu zamkly','1','2','3','1','2','3' ]
    for menu_loop in range(0,len(menu)):
        menu_moves_pages = MenuFont.render(menu[menu_loop], 1, grey)
        The_game_window.surface.blit(menu_moves_pages,(50, menu_loop *  menu_line_spacing + heading_shift))

def draw_AB_menu(The_game_window,menu_line_spacing,heading_shift):
    menu = [ '<-trener', 'b','c','1','2','3','1','2','3' ]
    for menu_loop in range(0,len(menu)):
        menu_moves_pages = MenuFont.render(menu[menu_loop], 1, grey)
        The_game_window.surface.blit(menu_moves_pages,(50, menu_loop *  menu_line_spacing + heading_shift))

def draw_AC_menu(The_game_window,menu_line_spacing,heading_shift):
    menu = [ '<-reff', 'b','c','1', ]
    for menu_loop in range(0,len(menu)):
        menu_moves_pages = MenuFont.render(menu[menu_loop], 1, grey)
        The_game_window.surface.blit(menu_moves_pages,(50, menu_loop *  menu_line_spacing + heading_shift))

def draw_AD_menu(The_game_window,menu_line_spacing,heading_shift):
    menu = [ '<-nastaveni', 'b','c','1','2','3' ]
    for menu_loop in range(0,len(menu)):
        menu_moves_pages = MenuFont.render(menu[menu_loop], 1, grey)
        The_game_window.surface.blit(menu_moves_pages,(50, menu_loop *  menu_line_spacing + heading_shift))

def draw_AE_menu(The_game_window,menu_line_spacing,heading_shift):
    menu = [ '<-napoveda', 'b','c','1','2', ]
    for menu_loop in range(0,len(menu)):
        menu_moves_pages = MenuFont.render(menu[menu_loop], 1, grey)
        The_game_window.surface.blit(menu_moves_pages,(50, menu_loop *  menu_line_spacing + heading_shift))

def draw_menu_lines(The_game_window,The_field):

    pygame.draw.rect(The_game_window.surface, white , (0 ,0 ,The_game_window.window_width, The_game_window.window_height  )   ,  1)

    pygame.draw.lines(The_game_window.surface,  grey, True, ((The_field.field_bl_window[0],0 ) , \
                                                        ( The_field.field_bl_window[0] , The_field.field_bl_window[1] )), 1)

    pygame.draw.lines(The_game_window.surface,  grey, True, ((The_field.field_bl_window[0] ,The_field.field_bl_window[1] ) ,  \
                                                        ( The_game_window.window_width ,The_field.field_bl_window[1] )), 1)
