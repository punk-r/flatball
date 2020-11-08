import math
import random
import pygame
from pygame.locals import *
import threading
import time
import copy

import f_menu                                                                           # ne vsechny metody potrebujou okno jako parametr zkontroluj
from f_menu import *
import neural_network
from neural_network import *
import class_ingamer
from class_ingamer import *
import class_player_ball
from class_player_ball import *
import support_functions
from support_functions import *

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
#import matplotlib.pyplot as plt

clock = pygame.time.Clock()


#--------------------------------------------------------------------------------------------class game_window
# trida window
class game_window():
    window_width = 1200
    window_height = 700
    surface = pygame.display.set_mode((window_width,window_height),0,32)
    items_on_surface = 0                                                                                             #   MOZNA NEBUDE POUZITE???
    game_menu_x_start = 5
    game_menu_x_end = 200
    menu_line_spacing = 20
    heading_shift = 2 * menu_line_spacing
    menu_selection = 0
    language = "CZ"



#--------------------------------------------------------------------------------------------class game_field
# trida pro hraci pole
class game_field():
    type ="notSpecified"       # pro ruzna vykraslovani hriste,zatim NEVYUZITO
    goals_height = 100         # velikosti branek
    goals_width = 10           # velikosti branek
    field_bl_window = [0,0]    # ram pro hraci hriste,hotnoty sou nastaveny pri set field
    lab_mode_b = 1             # zobrazeni pomocnych vypoctu
    field_width = 0            # hotnoty sou nastaveny pri set field
    field_height = 0           # hotnoty sou nastaveny pri set field
    field_bl_corner = [0,0]    # hranice hracih o hriste,hotnoty sou nastaveny pri set field
    gap = 0                    # hotnoty sou nastaveny pri set field, rozdil okna(area) pro hriste a hriste samotneho



    def set_field (self,game_window):
        print ("set field")
        self.gap = int (self.goals_width * 1.5) # mezera je sirka  brany a pul
        self.field_bl_window[0] = int ( 1/6 * game_window.window_width )
        self.field_bl_window[1] = int ( 4/5 * game_window.window_height )
        self.field_bl_corner[0] = int ( 1/6 * game_window.window_width + self.gap )
        self.field_bl_corner[1] = int ( 4/5 * game_window.window_height - self.gap/2 )
        self.field_width = int ( 0.7 * game_window.window_width - self.gap)
        self.field_height = int ( 0.7 * game_window.window_height - self.gap)



#--------------------------------------------------------------------------------------------class coach
# trida trenera
class class_coach ():
    data_trening = []   # TRENER UKLADA DATA PRO trening ??!! bude zmeneno ,kazdy hrac si bude data vyhodnocovat sam =>bude jednodussi
    data_labels = []

    def process_data(self,player,action,list_of_ingamers):
        if len(self.data_trening) <5000:

            # ukladani dat: uhel k sve brane,uhel k mici,vzdalenost k mici, provedena akce hracem
            self.data_trening.append([round(player.path_target), \
                             round(player.calculate_angle_to_other_object(list_of_ingamers[1].position)), \
                             # oprava pro rozdil od hrany hrace ne od stredu kruznic (umozni vypocet nezavisle na velikosti hracu a mice)
                             round(pythagoras_distance (player.position,list_of_ingamers[1].position) - player.radius - list_of_ingamers[1].radius  ) ])

            # labels
            self.data_labels.append( action)
        else:
            list_of_ingamers[1].color = black


                                                                                                # pro testy pote predelat
    def save_training(self):                                                                     #zkontroluj zavreni souboru
        #time = datetime.now()
         # dd/mm/YY H:M:S
        #dt_string = time.strftime("%d-%m-%Y_%H-%M-%S")
        #file_name = 'SaveGeme_' + dt_string + '.txt'
        file_name_testing = 'training.txt'
        with open(file_name_testing, 'w') as f:
            for write_loop in range (0,len(self.data_trening)):
                f.write( str(self.data_trening[write_loop]))
                f.write( '\n')

        file_name_testing = 'traininglabels.txt'
        with open(file_name_testing, 'w') as f:
            for write_loop in range (0,len(self.data_labels)):
                f.write( str(self.data_labels[write_loop]))
                f.write( '\n')


    '''

    PRIDAT METODY PRO KONTROLU TEAMU ,na misto po jednom hraci

    '''



#--------------------------------------------------------------------------------------------class reff
# trida rozhodciho
class reff ():
    def __init__(self,new_position):
        self.position = new_position
    radius = 15             # velikost
    lab_mode_b = 1          # laboratory mode, odemkne nektera nastaveni
    game_type = "none"      # typ hrany                                                                      zkontroluj UZITO????
    selected_b = False      # ukazatel zda je ingamer oznaceny                                               zkontroluj ,mely by byt uz z ingamer tridy!!
    score  = [0,0]          # pocitadlo golu
    time  = 0               # odpocet casu
    #mtds
    color_check  = 0        #  hodnoty pro nastaveni hry zatim epouzito
    set_color  = 0
    teams_for_game  = 0
    was_clicked  = 0
    stop_game  = 0
    pause_game   = 0
    team_type = "neutral"  # ???  zkontroluj
    coach_team_A = "none"  # rozhodci ma prehled o cele hre i o trenerech
    coach_team_B = "none"

    # kontrola pro vstreleny gol
    def goal_check(self,The_field,The_ball):
        decision_goal = 0

        goal_top    = The_field.field_bl_corner[1] - The_field.field_height/2 - The_field.goals_height/2
        goal_bottom = The_field.field_bl_corner[1] - The_field.field_height/2 + The_field.goals_height/2

        field_right  = The_field.field_bl_corner[0] + The_field.field_width
        field_left   = The_field.field_bl_corner[0]

        if False:
            print (' .goal_top',goal_top)
            print ('goal_bottom',goal_bottom)
            print ('field_rightt',field_right)
            print ('field_left',field_left)
            print ('ball',The_ball.position)
            print("game_fieldwth"  ,The_field.field_width )
            print("game_fieldhght"  ,The_field.field_height )

        # kontrola pozice mice ku branam
        if The_ball.position[1] - The_ball.radius < goal_bottom  and The_ball.position[1]  + The_ball.radius > goal_top:

            # rozdil 1 - mic se zastavi pixel pred carou
            if The_ball.position[0] - The_ball.radius - 1  <= field_left  :
                self.score [0] = self.score [0]  + 1
                self.game_reset (The_field,The_ball)

            elif The_ball.position[0] + The_ball.radius + 1  >= field_right :
                self.score [1] = self.score [1]  + 1
                self.game_reset (The_field,The_ball)

    # resetovani mice
    def game_reset (self,game_field,The_ball):
        The_ball.speed = 0
        The_ball.color = white
        The_ball.set_position    (random.randint( 400,800 ), random.randint(100 ,500 ) )


    def draw_ingamer (self,game_window):                                            #zmen na draw ref??
        if self.selected_b == True:
            color = yellow_item_selected
        else :
            color = white

        # Rozhodci se vykresluje jako bilo-cerny kruh
        # pomocny vypocet
        rectangle_for_drawing = [ self.position[0] - self.radius , self.position[1] - self.radius ,2 * self.radius , 2* self.radius ]
        # arc(surface, color, rect, start_angle, stop_anglenline)
        pygame.draw.arc(game_window.surface, color, rectangle_for_drawing, math.radians (90) ,  math.radians (180), self.radius)
        pygame.draw.arc(game_window.surface, color, rectangle_for_drawing, math.radians (270) ,  math.radians (360), self.radius)
        pygame.draw.circle(game_window.surface, color, ( self.position[0] ,self.position[1]) ,self.radius, 1)
    '''
    def is_selected_by_click (self,position_clicked):
        x_limits = [  self.position[0] - self.radius   ,  self.position[0] + self.radius    ]
        y_limits = [  self.position[1] - self.radius   ,  self.position[1] + self.radius    ]

        if f_is_clikced_on_circle(x_limits,y_limits,position_clicked) == True:
            self.selected_b = True
        else:
            self.selected_b = False
    '''

    def set_selected (self,new_status):                                                                                         #reff potomek ingamer??? opakuje se dost metod pri reff jako nezdedena trida
        #hrac muze byt oznaceny pouze pokud je v teamu uzivatele
        if new_status == True :
            if self.team_type != "AI":
                self.selected_b = True
        else:
            self.selected_b = False

    # jestli je item oznacen mysi nastavi se na selected , dle podminek set_selected
    def is_selected_by_click (self,position_clicked):
        x_limits = [  self.position[0] - self.radius   ,  self.position[0] + self.radius    ]
        y_limits = [  self.position[1] - self.radius   ,  self.position[1] + self.radius    ]

        if f_is_clikced_on_circle(x_limits,y_limits,position_clicked) == True:
            return True
        else:
            return False



    def read_selected (self):
        return self.selected_b


    def start_test_match (self,The_game_window,The_field,list_of_ingamers,called_at_begining):
        vertical_max   =       The_field.field_bl_corner [1]
        vertical_min  =       The_field.field_bl_corner [1] - The_field.field_height
        horizontal_min  =      The_field.field_bl_corner [0]
        horizontal_max  =     The_field.field_bl_corner [0] + The_field.field_width

        The_player_no_A1 = player ([random.randint(horizontal_min, horizontal_max),random.randint( vertical_min, vertical_max)])
        The_player_no_A2 = player ([random.randint(horizontal_min, horizontal_max),random.randint( vertical_min, vertical_max)])
        The_player_no_A1.path_target = 180
        The_player_no_A2.path_target = 180
        The_player_no_A1.team_type = "H"
        The_player_no_A2.team_type = "H"
        if os.path.isfile("model.h5"):
            The_player_no_A1.model= load_model("model.h5")
            The_player_no_A2.model= load_model("model.h5")
        The_player_no_A1.team = "A"
        The_player_no_A2.team = "A"
        The_player_no_A1.game_status = "game"
        The_player_no_A2.game_status = "game"
        The_player_no_A1.field_site = "left"
        The_player_no_A2.field_site = "left"
        The_player_no_A1.set_coach(self.coach_team_A)
        The_player_no_A2.set_coach(self.coach_team_A)

        if called_at_begining == True:
            list_of_ingamers.append(The_player_no_A1)
            list_of_ingamers.append(The_player_no_A2)
        else:
            list_of_ingamers[2] = The_player_no_A1
            list_of_ingamers[3] = The_player_no_A2


        #print("pth targgget",The_player_no_A2.path_target)

        The_player_no_B1 = player ([random.randint(horizontal_min, horizontal_max),random.randint( vertical_min, vertical_max)])
        The_player_no_B2 = player ([random.randint(horizontal_min, horizontal_max),random.randint( vertical_min, vertical_max)])
        The_player_no_B1.path_target = 180
        The_player_no_B2.path_target = 180
        The_player_no_B2.team_type = "H" #"AI"
        The_player_no_B1.team_type = "H" #"AI"
        if os.path.isfile("model.h5"):
            The_player_no_B1.model= load_model("model.h5")
            The_player_no_B2.model= load_model("model.h5")

        The_player_no_B2.team = "B"
        The_player_no_B1.team = "B"
        The_player_no_B1.game_status = "game"
        The_player_no_B2.game_status = "game"
        The_player_no_B1.color = red
        The_player_no_B2.color = red
        The_player_no_B1.field_site = "right"
        The_player_no_B2.field_site = "right"
        The_player_no_B1.set_coach(self.coach_team_A)   # pro testy keras.modelu je stejny coach !!!!!!!
        The_player_no_B2.set_coach(self.coach_team_A)

        if called_at_begining == True:
            list_of_ingamers.append(The_player_no_B1)
            list_of_ingamers.append(The_player_no_B2)
        else:
            list_of_ingamers[4] = The_player_no_B1
            list_of_ingamers[5] = The_player_no_B2



        #testovani
        '''
        thread_a1 =  threading.Thread (target = The_player_no_A1.move_round   ,args =  (The_game_window,The_field,list_of_ingamers))
        thread_a1.start()
        '''


        x = 1
        if x == 1:
            The_player_no_B1.team_type = "AI"
            thread_b1 =  threading.Thread (target = The_player_no_B1.move_round   ,args =  (The_game_window,The_field,list_of_ingamers))
            thread_b1.start()

            The_player_no_B2.team_type = "AI"
            thread_b2 =  threading.Thread (target = The_player_no_B2.move_round   ,args =  (The_game_window,The_field,list_of_ingamers))
            thread_b2.start()

            #The_player_no_A1.team_type = "AI"
            #thread_a1 =  threading.Thread (target = The_player_no_A1.move_round   ,args =  (The_game_window,The_field,list_of_ingamers))
            #thread_a1.start()

            #The_player_no_A2.team_type = "AI"
            #thread_a2 =  threading.Thread (target = The_player_no_A2.move_round   ,args =  (The_game_window,The_field,list_of_ingamers))
            #thread_a2.start()


        #print ("threads active",threading.active_count)



    def restart_players(self,The_game_window,The_field,list_of_ingamers):
        self.start_test_match (The_game_window,The_field,list_of_ingamers,False)


    def draw_data_lower_menu (self,The_game_window,The_field,list_of_ingamers):
        f_print_score(self.score,The_game_window,The_field)
