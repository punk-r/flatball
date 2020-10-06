
                                                                                                                # ne vsechny metody potrebujou okno jako parametr


import f_menu
from f_menu import *

import math
import random

#pygame modul
import pygame
from pygame.locals import *
import threading
import time
import copy

clock = pygame.time.Clock()

debug_mode = 0
debug_mode2 = 0

# class window
class game_window():
    window_width = 1200
    window_height = 700
    surface = pygame.display.set_mode((window_width,window_height),0,32)
    items_on_surface = 0   #   MOZNA NEBUDE POUZITE???
    game_menu_x_start = 5
    game_menu_x_end = 200
    menu_line_spacing = 20
    heading_shift = 2 * menu_line_spacing
    menu_selection = 0
    language = "CZ"



class game_field():
    type ='a'                       #pro ruzna vykraslovani hriste,zatim nepouzito
    goals_height = 100
    goals_width = 10
    field_bl_window = [100,500]     #hotnoty sou prepsany pri set field
    lab_mode_b = 1
    field_width = 500               #hotnoty sou prepsany pri set field
    field_height = 200              #hotnoty sou prepsany pri set field
    field_bl_corner = [200,650]     #hotnoty sou prepsany pri set field
    gap = 20                        #rozdil okna pro hriste a hriste samotneho

    def set_field (self,game_window):
        self.field_bl_window[0] = int ( 1/6 * game_window.window_width )
        self.field_bl_window[1] = int ( 4/5 * game_window.window_height )
        self.field_bl_corner[0] = int ( 1/6 * game_window.window_width + self.gap )
        self.field_bl_corner[1] = int ( 4/5 * game_window.window_height - self.gap/2 )
        self.field_width = int ( 0.7 * game_window.window_width - self.gap)
        self.field_height = int ( 0.7 * game_window.window_height - self.gap)
        self.gap = self.goals_width * 1.5 #meera je sirka  brany a pul


#--------------------------------------------------------------------------------------------class ingamer
# parent class pro pohybujici se objekty v hre
class ingamer():
    def __init__(self,new_position):
        self.position = new_position
        self.path_target = 0
        self.velocity = [1,0]

    #path_target = 0
    #velocity = [0,0]
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
    2.hrac se muze nastavit pouze jednim smerem to znamena kdyz chsi nastavit -20 supnu musim uzit 340   (360 -20)
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



    def calculate_angle_to_other_object(self,new_target):
        # pozice newtarget ku 'self'
        below = True
        left = True
        new_angle = 180
        # error hodnota pro pripad ze ew target je uvnit radiusu hrace => hrac bude natocen k souperove brane
        # nelze nastavit target blizez k hraci nez radius

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

        return new_angle


    def set_path_target(self,new_angle):
        below = -1
        left = -1

        # krok je 2 pixely => mene trhane pohyby , lze nastavit
        step = 2

                                                                                                                        # !! kvadranty sou na opak ZKONTROLUJ JEDE ale NEMElOBY!!!!!!

        #  cislo kvadrantu se vypocita jinak nezli klasicke oznaceni, zalezi na pootoceni od brany
        qvadrant =  math.floor (new_angle / 90)  # pro mic je cislo 0,1,2,3

        if self.field_site == "right":
            qvadrant =  math.floor (new_angle / 90)  # je cislo 0,1,2,3
            qvadrants_list = [[1 ,-1 ],[1 ,-1 ],[1 ,-1 ],[1 , -1]]                                                       #zkontrolovat!!!

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



    def draw_ingamer (self,game_window):
        if self.selected_b == True:
            color = yellow_item_selected
        else :
            color = self.color
        #ingamer_item = pygame.draw.circle(game_window.surface, color, ( self.position[0] ,self.position[1]) ,self.radius, self.radius)
        pygame.draw.circle(game_window.surface, color, ( self.position[0] ,self.position[1]) ,self.radius, self.radius)



    def set_position(self,new_x,new_y):
        self.position = [new_x,new_y]

    def set_selected (self,new_status):
        #hrac muze byt oznaceny pouze pokud je v teamu uzivatele
        if new_status == True :
            if self.team_type != "AI" :
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



#--------------------------------------------------------------------------------------------class player

class player (ingamer):
    game_status = 0         # hra, pausa, ....
    angle = 0                                                                                                               #neni potreba je uzito path target
    user_driven = 0          # kdyz je team_type human , je hrac ovladany uzivatelem Y/N
    team = 0                 # jmeno teamu
    speed  = 0
    balance  = 0
    acuracy = 0
    player_type = "notSpecified"          # utocnik obrance brankar midfielder
    position_by_strategy = 0
    strategy = 0
    tactic= 0
    dsetination_kick = 0
    vision = 50
    ball_owner_b = False
    team_coach = "notSpecified"


    # loc_home_goal = [0,0]
    # angle_to_home_goal = 180   #zacina otoceny


    #def automated_move():


    def set_coach (self,new_coach):
        self.team_coach = new_coach

    def send_data_to_coach(self,action,list_of_ingamers):
        self.team_coach.process_data(self,action,list_of_ingamers)


    # pro testy
    def move_round(self,The_game_window,The_field,list_of_ingamers):

        while self.game_status ==  "game" :
            clock.tick(5)
            if self.selected_b == False:
                #print("aroundmetoda")
                self.set_path_target( self.path_target + 10 )
                if  self.path_target == 360:
                    self.set_path_target( 0 )
                self.move (The_game_window,The_field,list_of_ingamers)


    def move(self,The_game_window,The_field,list_of_ingamers):
        if debug_mode == 1:
            print('metodaplayer')

        bottom = The_field.field_bl_corner[1]
        top    = The_field.field_bl_corner[1] - The_field.field_height
        right  = The_field.field_bl_corner[0] + The_field.field_width
        left   = The_field.field_bl_corner[0]

        #-------------DODELAT bounderies / colisions ----------------------
        test_target_on_filed = 0
        test_target_too_close = 1
        path_for_ball_check = 1
        ball_is_frozen = 0

        #  1.detekce pohybu na hristi, cast hrace muze prejit pres linii hriste , pro pripad ze se balon zastavil prave na teto linii
        if self.position[0] + self.velocity[0] > left - self.radius/2  and self.position[0] + self.velocity[0] < right + self.radius/2  and \
            self.position[1] + self.velocity[1] < bottom + self.radius/2  and self.position[1] + self.velocity[1] > top - self.radius/2  :

            test_target_on_filed = 1

        # 3. detekce hracu / mice
        for no_of_ingamers in range (1,len(list_of_ingamers)):
                other_ingamer_position = list_of_ingamers[no_of_ingamers].position
                ingamer_adjescent =  abs (self.position[0] + self.velocity[0] -  other_ingamer_position[0])
                ingamer_opposite =  abs (  self.position[1]  + self.velocity[1]-  other_ingamer_position[1])
                ingamer_hypotensue = math.sqrt(ingamer_adjescent **2 + ingamer_opposite **2)

                ingamer_adjescent_before_step =  abs (self.position[0]  -  other_ingamer_position[0])
                ingamer_opposite_before_step =  abs (  self.position[1] -  other_ingamer_position[1])
                ingamer_hypotensue_before_step = math.sqrt(ingamer_adjescent_before_step **2 + ingamer_opposite_before_step **2)



                # specialni pripad kdy je mic 'pod' hracem => phyb jen hrace , 2 je krok hrace , mic a hrac maji stejnou polohy pred krokem hrcace
                # podminka opravuje chybu kde hrac pri pohybu pro blokovany mic udela krok,to vedlo k zamrznuti mice k hracovu radiusu
                # velikost je mensi nez pred kroke a to presne o jeden pixel
                if ingamer_hypotensue_before_step < list_of_ingamers[no_of_ingamers].radius + self.radius:
                    ball_is_frozen = 1


                # kontrola kolize s micem
                if no_of_ingamers == 1 and ball_is_frozen == 0 :


                    distance_to_owned_ball = 3
                    # 1. pohyb neposune mic, hrac je v blizkosti mice => je vlastnik
                    if ingamer_hypotensue < list_of_ingamers[no_of_ingamers].radius + self.radius + distance_to_owned_ball and \
                        ingamer_hypotensue > list_of_ingamers[no_of_ingamers].radius + self.radius:

                        list_of_ingamers[no_of_ingamers].set_owner(self)

                        ball_new_target = self.calculate_angle_to_other_object(list_of_ingamers[no_of_ingamers].position)
                        list_of_ingamers[no_of_ingamers].set_path_target (ball_new_target)


                                                                                                                                        # chyba nekdy mic zamrzne u hrace mozna zaokrouhlovani pri vypoctu souradnic
                    # 2. pohyb posune mic, hrac udelal pohyb na lokaci mice => mic se o kousek posune
                    if ingamer_hypotensue < list_of_ingamers[no_of_ingamers].radius + self.radius  :


                        list_of_ingamers[no_of_ingamers].set_owner(self)
                        # novy uhel(posun mice)  je stred hrace a souradnice kontaktu s micem
                        ball_new_target = self.calculate_angle_to_other_object(list_of_ingamers[no_of_ingamers].position)
                        list_of_ingamers[no_of_ingamers].set_path_target (ball_new_target)

                        path_for_ball_check  = list_of_ingamers[no_of_ingamers].is_ball_path_clear(The_game_window,The_field,list_of_ingamers)

                        if path_for_ball_check == 1:
                            list_of_ingamers[no_of_ingamers].speed = 2
                        else:
                            list_of_ingamers[no_of_ingamers].speed = 0


                    if ingamer_hypotensue > list_of_ingamers[no_of_ingamers].radius + self.radius + 2 and \
                            list_of_ingamers[no_of_ingamers].owner == self :
                              list_of_ingamers[no_of_ingamers].reset_owner(self)


                # vynecha 'sebe' v kontrolre kolize , vynecha mic index '1' v list_of_ingamers
                if ingamer_hypotensue < 2 * self.radius and other_ingamer_position != self.position and no_of_ingamers > 1 :
                    test_target_too_close = 0


        if test_target_on_filed == 1 and test_target_too_close ==1 and path_for_ball_check == 1:
            self.position =  [ self.position[0] + self.velocity[0]  ,self.position[1]  + self.velocity[1]  ]

            #data tracking
            if self.selected_b == True:
                self.send_data_to_coach("m",list_of_ingamers)



        if debug_mode == 1:
            print('plr---------- ')
            print (list_of_ingamers[1])
            print(vars(list_of_ingamers[1]))
            print (list_of_ingamers[2])
            print(vars(list_of_ingamers[2]))
            print (list_of_ingamers[3])
            print(vars(list_of_ingamers[3]))
            print('---------- ')



            # DRAW je pro testovani skoro stejny pro mic i hrace

    def draw_ingamer(self,game_window):
        #self.draw_ingamer(game_window)
        ingamer.draw_ingamer(self,game_window)

        # kresli vision hrace - kam se diva
        # kresleno z velocity jelikoz to je uhel kam hrac smeruje

        viev = 10 # zobrazeni pohledu je 10 pixelu , velocity je |2| * 5 = 10

        vision_adjescent = viev * self.velocity[0]
        vision_opposite = viev * self.velocity[1]


        if self.ball_owner_b == True :
            viev_color = green
        else:
            viev_color = self.color

        '''
        if self.selected == 1:                                                                                                #s[patne reseni potrebuje opravit]
            pygame.draw.lines(game_window.surface, viev_color, True, ((self.position[0] ,self.position[1] ), \
                                ( self.position[0] + vision_adjescent ,self.position[1] + vision_opposite  )), 1)

        '''


        pygame.draw.lines(game_window.surface, viev_color, True, ((self.position[0] ,self.position[1] ), \
                                ( self.position[0] + vision_adjescent ,self.position[1] + vision_opposite  )), 1)



    def draw_data_lower_menu (self,The_game_window,The_field,list_of_ingamers):
        f_print_player_details(The_game_window,The_field,self,list_of_ingamers)




#--------------------------------------------------------------------------------------------class ball


class ball (ingamer):
    resistance = 1
    color = white
    radius = 10
    owner = 'nooneyet'
    speed = 0


    def draw_data_lower_menu (self,The_game_window,The_field,list_of_ingamers):
        f_print_ball_details(The_game_window,The_field,self,list_of_ingamers)





    # kontrola pro: hrac nemuze udelat krok kdyz je pred nim mic , a mic nema misto kam se posunout
    # path v instanci je uz novy od metody move od hrace
    def is_ball_path_clear(self,The_game_window,The_field,list_of_ingamers):                                                           #opakujicis se kod pro preponu kolize
        decision = 1

        bottom = The_field.field_bl_corner[1]
        top    = The_field.field_bl_corner[1] - The_field.field_height
        right  = The_field.field_bl_corner[0] + The_field.field_width
        left   = The_field.field_bl_corner[0]

        #  detekce pohybu na hristi, odraz od sten
        if self.position[0] - self.radius + self.velocity[0]  < left :
            decision =0
        if self.position[0] + self.radius + self.velocity[0]  > right :
            decision =0
        if self.position[1] + self.radius + self.velocity[1]  > bottom :
            decision =0
        if self.position[1]  - self.radius + self.velocity[1]  < top :
            decision =0


        # detekce hracu
        for no_of_ingamers in range (2,len(list_of_ingamers)):
            other_ingamer_position = list_of_ingamers[no_of_ingamers].position
            ingamer_adjescent =  abs (self.position[0] + self.velocity[0] -  other_ingamer_position[0])
            ingamer_opposite =  abs (  self.position[1]  + self.velocity[1]-  other_ingamer_position[1])
            ingamer_hypotensue = math.sqrt(ingamer_adjescent **2 + ingamer_opposite **2)

            if ingamer_hypotensue <= self.radius + list_of_ingamers[no_of_ingamers].radius  :                                    # zkontrolovat porovnani

                decision =0

        return decision

    def reset_owner(self,player):
        if self.owner == player:
            self.owner = 0
            self.color = white
            player.ball_owner_b = False


    def set_owner(self,new_owner):
                                                                                                                                #nejelo by spravne bo by neslo sebrat teamu mic
        '''
        # nelze nastavit 2 hrace jako owners ve stejny cas
        if self.owner == 0:
            new_owner.ball_owner_b = True
            self.owner = new_owner
            self.color = green
        '''
        new_owner.ball_owner_b = True
        self.owner = new_owner
        self.color = green
        self.field_site = new_owner.field_site




    def move(self,The_game_window,The_field,list_of_ingamers):                                                                  #zkontroluj jaka cast move lze udelat pro ingamer a pak jen zdedit
        if debug_mode == 1:
            print('metodaball')

        # 2 je rychlost pri 'driblingu'
        if self.speed > 2 :
            # kdyz krac mic odkopne ,mic ztraci vlatnika
            self.owner = 0
            self.color = white

        step = 2
        bottom = The_field.field_bl_corner[1]
        top    = The_field.field_bl_corner[1] - The_field.field_height
        right  = The_field.field_bl_corner[0] + The_field.field_width
        left   = The_field.field_bl_corner[0]

        #-------------DODELAT bounderies / colisions ----------------------

        # detekce hracu
        for no_of_ingamers in range (2,len(list_of_ingamers)):
            other_ingamer_position = list_of_ingamers[no_of_ingamers].position
            ingamer_adjescent =  abs (self.position[0] + self.velocity[0] -  other_ingamer_position[0])
            ingamer_opposite =  abs (  self.position[1]  + self.velocity[1]-  other_ingamer_position[1])
            ingamer_hypotensue = math.sqrt(ingamer_adjescent **2 + ingamer_opposite **2)


            if ingamer_hypotensue <= self.radius + list_of_ingamers[no_of_ingamers].radius  :



                # JEN PRO TESTY ,JINAK POTREBA DODELAT VYPOCET UHLU ODRAZu
                self.velocity[0] = self.velocity[0] * -1
                self.velocity[1] = self.velocity[1] * -1


                '''
                                                            #pri pohybu race kdyz posune mic se vola 'move'                     !!!!!!
                                                            # mice ale v tu chvili mic muze byt v radiusu hrace                 !!!!
                                                            # a mic se zacykli a zamrzne u hrace                                !!!!


                #vypocet odrazu balonu od hrace, pomoci uhlu kde je hrac a uhlu kontaktu mice s hracem
                angle_to_player = self.calculate_angle_to_other_object(list_of_ingamers[no_of_ingamers].position)
                angle_of_balls_target = self.path_target
                touch_point_difference = angle_to_player - angle_of_balls_target
                angle_of_reflected_ball = angle_of_balls_target + touch_point_difference
                self.set_path_target(angle_of_reflected_ball)
                '''


                # snizeni energie(speed)
                # hodnoty treba otestovat pri hre, zpomaleni obdobne jako pri skutecne hre
                # zpomaleni s projevi jen pri kontaktu mice a hrace, pri kontaktu mice konce pole se energie nemeni
                if self.speed > 100 :
                    self.speed = int( self.speed * 0.8  )
                elif self.speed > 5 and self.speed <= 100  :
                    self.speed = int( self.speed * 0.5  )
                elif self.speed < 5:
                    self.speed = 0




        #  detekce pohybu na hristi, odraz od sten
        if self.position[0] - self.radius + self.velocity[0]  < left :
            self.velocity[0] = self.velocity[0] * -1
        if self.position[0] + self.radius + self.velocity[0]  > right :
            self.velocity[0] = self.velocity[0] * -1
        if self.position[1] + self.radius + self.velocity[1]  > bottom :
            self.velocity[1] = self.velocity[1] * -1
        if self.position[1]  - self.radius + self.velocity[1]  < top :
            self.velocity[1] = self.velocity[1] * -1


        # potvrzeni nove pozice
        self.position =  [ self.position[0] + self.velocity[0]  ,self.position[1]  + self.velocity[1]  ]


        if debug_mode == 1:
            print('ball---------- ')
            print (list_of_ingamers[1])
            print(vars(list_of_ingamers[1]))
            print (list_of_ingamers[2])
            print(vars(list_of_ingamers[2]))
            print (list_of_ingamers[3])
            print(vars(list_of_ingamers[3]))
            print('---------- ')




    def moving(self,The_game_window,The_field,list_of_ingamers):
        for no_of_ingamers in range (2 , len(list_of_ingamers)):
            list_of_ingamers[no_of_ingamers].ball_owner_b = False
        if self.speed != 0:
            self.speed = self.speed -1
            self.move(The_game_window,The_field,list_of_ingamers)
            list_of_ingamers[0].goal_check(The_field,list_of_ingamers[1])




    #jak se hybe kontroluje path !!!!!!!


    def draw_ingamer(self,game_window):                                                                                   # pouze pro testovani  pak ccela metoda do komentu, a draw dela metoda od ingamer tridyingamer
        #self.draw_ingamer(game_window)
        ingamer.draw_ingamer(self,game_window)

        # kresli vision hrace - kam se diva
        # kresleno z velocity jelikoz to je uhel kam hrac smeruje

        viev = 10 # zobrazeni pohledu je 10 pixelu , velocity je |2| * 5 = 10

        vision_adjescent = viev * self.velocity[0]
        vision_opposite = viev * self.velocity[1]

        '''
        if self.ball_owner_b == True :
            viev_color = green
        else:
            viev_color = self.color


        if self.selected == 1:                                                                                                #s[patne reseni potrebuje opravit]
            pygame.draw.lines(game_window.surface, viev_color, True, ((self.position[0] ,self.position[1] ), \
                                ( self.position[0] + vision_adjescent ,self.position[1] + vision_opposite  )), 1)

        '''


        pygame.draw.lines(game_window.surface, green, True, ((self.position[0] ,self.position[1] ), \
                                ( self.position[0] + vision_adjescent ,self.position[1] + vision_opposite  )), 1)







#--------------------------------------------------------------------------------------------class coach

class class_coach ():
    data = []

    def process_data(self,player,action,list_of_ingamers):
        if len(self.data) <100:

            self.data.append([round(player.path_target), \
                             round(player.calculate_angle_to_other_object(list_of_ingamers[1].position)), \
                             round(pythagoras_distance (player.position,list_of_ingamers[1].position)) , \
                             action])



    def save_training(self):                                                                     #zkontroluj zavreni souboru
        #time = datetime.now()
         # dd/mm/YY H:M:S
        #dt_string = time.strftime("%d-%m-%Y_%H-%M-%S")
        #file_name = 'SaveGeme_' + dt_string + '.txt'
        file_name_testing = 'training.txt'
        with open(file_name_testing, 'w') as f:
            for write_loop in range (0,len(self.data)):
                f.write( str(self.data[write_loop]))
                f.write( '\n')









#--------------------------------------------------------------------------------------------class reff

class reff ():
    def __init__(self,new_position):
        self.position = new_position
    radius = 15
    lab_mode_b = 1
    game_type = 0
    selected_b = False
    score  = [0,0]
    time  = 0
    #mtds
    color_check  = 0
    set_color  = 0
    teams_for_game  = 0
    was_clicked  = 0
    stop_game  = 0
    pause_game   = 0
    team_type = "neutral"
    coach_team_A = "notSpecified"
    coach_team_B = "notSpecified"


    def goal_check(self,The_field,The_ball):

        decision_goal = 0


        goal_top    = The_field.field_bl_corner[1] - The_field.field_height/2 - The_field.goals_height/2
        goal_bottom = The_field.field_bl_corner[1] - The_field.field_height/2 + The_field.goals_height/2

        field_right  = The_field.field_bl_corner[0] + The_field.field_width
        field_left   = The_field.field_bl_corner[0]


        if debug_mode == 1:
            print (' .goal_top',goal_top)
            print ('goal_bottom',goal_bottom)
            print ('field_rightt',field_right)
            print ('field_left',field_left)
            print ('ball',The_ball.position)



        if The_ball.position[1] - The_ball.radius < goal_bottom  and The_ball.position[1]  + The_ball.radius > goal_top:

            # rozdil 1 - mic se zastavi pixel pred carou
            if The_ball.position[0] - The_ball.radius - 1  <= field_left  :
                self.score [0] = self.score [0]  + 1
                self.game_reset (game_field,The_ball)

            elif The_ball.position[0] + The_ball.radius + 1  >= field_right :
                self.score [1] = self.score [1]  + 1
                self.game_reset (game_field,The_ball)







    def game_reset (self,game_field,The_ball):
        The_ball.speed = 0
        The_ball.set_position(int(game_field.field_bl_corner[0]  + game_field.field_width / 2 ), \
                                        int(game_field.field_bl_corner[1]  - game_field.field_height / 2 )  )



    def draw_ingamer (self,game_window):                                            #zmen na draw ref??
        if self.selected_b == True:
            color = yellow_item_selected
        else :
            color = white


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
        The_player_no_B2.team = "B"
        The_player_no_B1.team = "B"
        The_player_no_B1.game_status = "game"
        The_player_no_B2.game_status = "game"
        The_player_no_B1.color = red
        The_player_no_B2.color = red
        The_player_no_B1.field_site = "right"
        The_player_no_B2.field_site = "right"
        The_player_no_B1.set_coach(self.coach_team_B)
        The_player_no_B2.set_coach(self.coach_team_B)

        if called_at_begining == True:
            list_of_ingamers.append(The_player_no_B1)
            list_of_ingamers.append(The_player_no_B2)
        else:
            list_of_ingamers[4] = The_player_no_B1
            list_of_ingamers[5] = The_player_no_B2


        '''
        #testovani
        thread_a1 =  threading.Thread (target = The_player_no_A1.move_round   ,args =  (The_game_window,The_field,list_of_ingamers))
        thread_a1.start()
        thread_b1 =  threading.Thread (target = The_player_no_B1.move_round   ,args =  (The_game_window,The_field,list_of_ingamers))
        thread_b1.start()
        '''

    def restart_players(self,The_game_window,The_field,list_of_ingamers):
        self.start_test_match (The_game_window,The_field,list_of_ingamers,False)


    def draw_data_lower_menu (self,The_game_window,The_field,list_of_ingamers):
        f_print_score(self.score,The_game_window,The_field)





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
