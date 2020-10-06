import pygame
import sys
import math
import random
import os.path
from os import path
import f_menu
from f_menu import *
import f_clases
from f_clases import *


#pygame modul
pygame.init()
from pygame.locals import *

clock = pygame.time.Clock()

# testovani
debug_mode = 0

The_game_window = game_window()
pygame.display.set_caption(" Flatball ")

The_field = game_field()
The_field.set_field(The_game_window)


The_reff = reff([ The_field.field_bl_corner[0] + int(The_field.field_width / 2) , The_field.field_bl_corner[1] - int( The_field.field_height * 1.05 ) ])
#The_reff.draw_ingamer(The_game_window)

The_coach_A = class_coach()
The_coach_B = class_coach()
The_reff.coach_team_A = The_coach_A
The_reff.coach_team_B = The_coach_B

The_ball = ball([   The_field.field_bl_corner[0] + int(The_field.field_width / 2) , The_field.field_bl_corner[1] - int( The_field.field_height * 0.5 )   ])
#The_ball.draw_ingamer(The_game_window)
The_ball.path_target = 0
The_ball.team_type = "H"  # zabrani oznaceni balonu po kliknuti                                                           # H pouze pro testy jinak  AI


key_down = 0
was_clicked = 0
position_clicked = [0,0]

game_menu_active = True
game_menu_selcection = 'A'
screen_ID = 3 # welcome screen
screen_lower_ID = 0
list_of_ingamers = [The_reff,The_ball]                                                                          # list by mohl but v windows instanci
selected_player = 'emptynow'           #pro volani vykresleni lower menu
action_for_player = False



# MAIN GAME LOOP
while True:

    for event in pygame.event.get():                                                                              # opravit ball a reff indexy sou hardcoded v loop ne uplne supr reseni
        if event.type == QUIT:
            sys.exit()

        # KLAVESNICE
        if event.type == KEYDOWN:                                                                                 #kontrola events udelat lip loop se opakuje
            key = pygame.key.get_pressed()
            if key[K_SPACE]:    # mozna dodelat 2 klavesy kick/ pass
                for no_of_ingamers in range (2,len(list_of_ingamers)):

                    if list_of_ingamers[no_of_ingamers].selected_b == True and list_of_ingamers[1].owner == list_of_ingamers[no_of_ingamers] :
                        ball_angle = list_of_ingamers[no_of_ingamers].calculate_angle_to_other_object(list_of_ingamers[1].position)
                        vision_angle = list_of_ingamers[no_of_ingamers].path_target
                        diff_ball_to_vision = abs (ball_angle - vision_angle )
                        # pokud se hrac diva jinam nezli kop,mic dostane min energie  70%
                        list_of_ingamers[no_of_ingamers].send_data_to_coach("k",list_of_ingamers)

                        if diff_ball_to_vision > 20:
                            list_of_ingamers[1].speed = int (200 * 0.7)
                        else:
                            list_of_ingamers[1].speed = 200

            if key[K_w]:
                key_down = True


        if event.type == KEYUP:                                                                                  # !!!!!!!!!!kontrola events udelat lip loop se opakuje
            key_down = False


        # MYS
        if event.type == MOUSEBUTTONDOWN:
            was_clicked = 1
            position_clicked = pygame.mouse.get_pos()
            selected_player = "emptynow"
            for no_of_ingamers in range (0,len(list_of_ingamers)):
                if list_of_ingamers[no_of_ingamers].is_selected_by_click (position_clicked) == True:            # pride kontrolu pri hre human/pc musi u teamu human by vzdy jeden hrac oznaceny
                    list_of_ingamers[no_of_ingamers].set_selected(True)
                    selected_player = list_of_ingamers[no_of_ingamers]
                else:
                    list_of_ingamers[no_of_ingamers].set_selected(False)





        if event.type == MOUSEMOTION:
            position_over = pygame.mouse.get_pos()
            over_x = position_over[0]
            over_y = position_over[1]
            # set_path se nenastavuje prvnim dvou clenum reff a ball, reff se nehybe a ball dostava koordinace od metod
            for no_of_ingamers in range (2,len(list_of_ingamers)):
                if list_of_ingamers[no_of_ingamers].selected_b == True :
                    new_angle = list_of_ingamers[no_of_ingamers].calculate_angle_to_other_object(position_over)
                    original_target = list_of_ingamers[no_of_ingamers].path_target
                    if round(-original_target + new_angle ) >= 0:                                                                       #zkontroluj znamenko
                        angle_done = 10
                    else:
                        angle_done = -10
                    list_of_ingamers[no_of_ingamers].set_path_target(new_angle)
                    list_of_ingamers[no_of_ingamers].send_data_to_coach( angle_done,list_of_ingamers  )

                    #zapamatuj kde je vyber menu podle toho volej co se ma stat metoda/funcke



    #------------------konec kontroly eventu--------------------------------------------------------------

    if key_down == True :
        for no_of_ingamers in range (2,len(list_of_ingamers)):
            if list_of_ingamers[no_of_ingamers].selected_b == True :
                list_of_ingamers[no_of_ingamers].move(The_game_window,The_field,list_of_ingamers)


    if was_clicked == 1 and game_menu_active == True:
        if position_clicked[0] < The_game_window.game_menu_x_end:
            screen_ID = f_menu_selected(position_clicked,The_game_window,The_field,list_of_ingamers)
        was_clicked = 0

    #record training data
    if action_for_player == True:
        #record data

        #reset
        action_for_player = False



    #posune mic v pripade ze ma nejakou energii (speed)
    The_ball.moving(The_game_window,The_field,list_of_ingamers)

    The_game_window.surface.fill(black)

    # vykresli game menu, pri zapase je neaktivni
    if game_menu_active == True:
        draw_main_menu(The_game_window)
        draw_menu_lines_ID_3(The_game_window,The_field)
    else:
        draw_menu_lines_ID_4(The_game_window,The_field)

    # vykresli pozadovanou obrazovku
    if screen_ID == 3:                                                                                       # dat do menu knihovny?  opravid indexy a jmena podle wordu
        draw_weclome(The_game_window)
    elif screen_ID == 4 :
        draw_5aside_field (The_game_window,The_field)
        #print("selected_player",selected_player)
        if selected_player != "emptynow" :
            selected_player.draw_data_lower_menu (The_game_window,The_field,list_of_ingamers)


    '''
    if screen_lower_ID  == 1 :
        print_score(The_reff.score,The_game_window,The_field)
    '''


    if screen_ID == 4:
        #The_player_no_B1.move_round(The_game_window,The_field,list_of_ingamers)
        #The_player_no_B2.move_round(The_game_window,The_field,list_of_ingamers)                              #delam 2 x redraw ??? v loop a taky v metode
        for no_of_ingamers in range (0,len(list_of_ingamers)):
            list_of_ingamers[no_of_ingamers].draw_ingamer(The_game_window)


    pygame.display.update()
    clock.tick(60)
