
import pygame
clock = pygame.time.Clock()
import sys
import math
import random
import os.path
from os import path
import support_functions
from support_functions import *

#--------------------------------------------------------------------------------------------class ingamer
# parent class pro pohybujici se objekty v hre                                                                   !!!!??ROZHODCI A TRENERI BUDOU MIT TAKY PREDKA INGAMER I KDYZ SE NEHYBAJI                                                              # ingamer predek i pro reff a coach?? zjednodusil by se kod
class ingamer():
    def __init__(self,new_position):
        self.position = new_position
        self.path_target = 0
        self.velocity = [1,0]

    radius = 15
    destination_move = [0,0]
    lab_mode_b = 1
    color = blue
    collision_allowed_b = False
    selected_b = False
    team_type = "Neutral"          # H - human ,  AI , Neutral for ball and reff
    field_site = "neutral"         # L team ma vlastni branu na levo, R team ma vlastni branu na pravo



    '''
    1.uhel pocitame od brany sveho teamu , kdyz hrac stoji v uhlu 180 ,znamena ze je 'zady' k brane
    2.hrac se muze nastavit pouze jednim smerem to znamena kdyz chci nastavit -20 supnu musim uzit 340   (360 -20)
    pokud je brana v pravo uhly se zrcadli aby platilo pravidlo 1



    field_site = L
                             90
    b                  0.     |     1.
    r                         |
    a               0 ------------------ 180
    n                         |
    a                   3.    |     2.
                             270

    field_site = R
                             90
                       1.     |     0.                b
                              |                       r
                 180 ------------------ 0             a
                              |                       n
                        2.    |     3.                a
                             270


    '''

    # vypocte uhel k druhemu objektu(nebo novy smer) , a to v zavislosti na field_site
    def calculate_angle_to_other_object(self,new_target):
        # pozice newtarget k 'sobe'

        # urceni qvadrantu
        below = True
        left = True

        # error hodnota pro pripad ze ew target je uvnit radiusu hrace => hrac bude natocen k souperove brane
        # nelze nastavit target blizez k hraci nez radius
        new_angle = 180

        # vypocet vzdalenosti
        target_adjescent =  abs (self.position[0] -  new_target[0])
        target_opposite =  abs (  self.position[1] -  new_target[1])
        target_hypotensue = math.sqrt(target_opposite**2   +    target_adjescent**2)                                # pouzij udelanou funkco pythagoras_disnace

        if  target_hypotensue > self.radius and target_adjescent != 0 :
            new_angle = math.degrees (math.atan ( target_opposite / target_adjescent ))

            if self.position[1] < new_target[1] :
                below = False

            if self.field_site == "left"or self.field_site == "neutral":
                if self.position[0] >= new_target[0] :
                    left = False

                # uhel se meri od vodorovne x osy
                # dopocet dle kvadranntu
                if  below == False and left == False :
                    new_angle = 360 - new_angle
                elif  below == True and left == True :
                    new_angle = 90 + ( 90 - new_angle)
                elif  below == False and left == True :
                    new_angle = 180 + new_angle


            if self.field_site == "right":              # orava pro oponenta
                #Print("ooopravaoponent")
                new_angle = math.degrees (math.atan ( target_opposite / target_adjescent ))

                if self.position[0] >= new_target[0]:
                    left = False

                # uhel se meri od vodorovne x osy
                # dopocet dle kvadranntu
                if  below == True and left == False :
                    new_angle = 180 - new_angle
                elif  below == True and left == True :
                    new_angle =  new_angle
                elif  below == False and left == True :
                    new_angle = 360 - new_angle
                elif  below == False and left == False :
                    new_angle =  180 + new_angle

            # prepocet pro mezni hodnotu ,kdy je uhel 90 stupnu => osa Y , vypocet atan vyse
            if self.position[0] == new_target[0]:
                if self.position[1] > new_target[1]:
                    new_angle = 90
                else:
                    new_angle = 270

        # vraci vypocitany uhel k objektu nebo novy 'cil' pohybu
        return new_angle


    # dle uhlu se nastavi vektor pohybu tj. zmena na ose x a y pro pohyb objektu ve hre
    def set_path_target(self,new_angle):
        # qvadrant
        below = -1
        left = -1

        # krok je 2 pixely => mene trhane pohyby , lze nastavit
        step = 2
                                                                                                                # !! kvadranty sou naopak ZKONTROLUJ JEDE ale NEMElOBY!!!!!!

        #  cislo kvadrantu se vypocita jinak nezli klasicke oznaceni, zalezi na pootoceni od brany
        qvadrant =  math.floor (new_angle / 90)  # pro mic je cislo 0,1,2,3

        if self.field_site == "right":
            qvadrant =  math.floor (new_angle / 90)  # je cislo 0,1,2,3
            qvadrants_list = [[1 ,-1 ],[1 ,-1 ],[1 ,-1 ],[1 , -1]]                                               #zkontrolovat!!!

        if self.field_site == "left" or self.field_site == "neutral":
            qvadrant =  math.floor (new_angle / 90)  # je cislo 0,1,2,3
            qvadrants_list = [[-1 ,-1 ],[-1 ,-1 ],[-1 ,-1 ],[-1 , -1]]                                                      #jede ale nemeloby!!!!!!!

        left =  qvadrants_list [qvadrant] [0]
        below = qvadrants_list [qvadrant] [1]


        shift_hypotensue = step
        shift_adjescent = left * math.cos(math.radians(new_angle)) *  shift_hypotensue
        shift_opposite = below * math.sin(math.radians(new_angle)) *  shift_hypotensue

        self.velocity[0] =  round (shift_adjescent)
        self.velocity[1] =  round (shift_opposite)
        self.path_target = new_angle

        if self.field_site == "left"or self.field_site == "neutral":
            # hranicni hodnoty
            if new_angle == 0:
                self.velocity[0] = -1 * step
                self.velocity[1] = 0
            if new_angle == 90:
                self.velocity[0] =  0
                self.velocity[1] = -1 * step
            if new_angle == 180:
                self.velocity[0] = step
                self.velocity[1] =  0
            if new_angle == 270:
                self.velocity[0] =  0
                self.velocity[1] =  step

        if self.field_site == "right":
            # hranicni hodnoty
            if new_angle == 0:
                self.velocity[0] =  step
                self.velocity[1] = 0
            if new_angle == 90:
                self.velocity[0] =  0
                self.velocity[1] = -1 * step
            if new_angle == 180:
                self.velocity[0] = -1 *step
                self.velocity[1] =  0
            if new_angle == 270:
                self.velocity[0] =  0
                self.velocity[1] =  step



    # vykresli objekt hry
    def draw_ingamer (self,game_window):
        if self.selected_b == True:
            color = yellow_item_selected
        else :
            color = self.color
        #ingamer_item = pygame.draw.circle(game_window.surface, color, ( self.position[0] ,self.position[1]) ,self.radius, self.radius)
        pygame.draw.circle(game_window.surface, color, ( self.position[0] ,self.position[1]) ,self.radius, self.radius)

    # nastaveni nove pozice
    def set_position(self,new_x,new_y):
        self.position = [new_x,new_y]

    # nastavi zda je objekt oznacen
    def set_selected (self,new_status):
        #hrac muze byt oznaceny pouze pokud je v teamu uzivatele
        if new_status == True :
            if self.team_type != 1: # "AI" :
                self.selected_b = True
        else:
            self.selected_b = False

    # zkontroluje zda bylo kliknuto na objekt
    def is_selected_by_click (self,position_clicked):
        x_limits = [  self.position[0] - self.radius   ,  self.position[0] + self.radius    ]
        y_limits = [  self.position[1] - self.radius   ,  self.position[1] + self.radius    ]

        if f_is_clikced_on_circle(x_limits,y_limits,position_clicked) == True:
            return True
        else:
            return False

    # vrati hodnotu z slotu
    def read_selected (self):
        return self.selected_b
