
# moje knihovny
import f_menu
from f_menu import *
import f_clases
from f_clases import *
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


#--------------------------------------------------------------------------------------------class player

class player (ingamer):
    game_status = "notSpecified"             # hra, pausa, ....
    angle = "notSpecified"                   #???ZKONTROLUJ UZ JE V INGAMER TRIDE                                                                                           #neni potreba je uzito path target
    user_driven = "notSpecified"             # kdyz je team_type human , je hrac ovladany uzivatelem Y/N
    team = "notSpecified"                    # jmeno teamu
    speed  = 0                               # osobnost hrace, urcuje rychlost kroku           -----ZATIM nepouzito-------
    balance  = 0                             # osobnost hrace, urcuje zda hrac muze spadnouot  -----ZATIM nepouzito-------
    acuracy = 0                              # osobnost hrace, urcuje presnost kopu            -----ZATIM nepouzito-------
    skills_level = 3                         # osobnost hrace, urcuje kolik vstupu hrac rozpozna pri treningu
    player_type = "notSpecified"             # utocnik, obrance, brankar, midfielder
    position_by_strategy = "notSpecified"    #
    strategy = "notSpecified"
    tactic= "notSpecified"
    dsetination_kick = "notSpecified"
    vision = 50                             # zatim vyuzitojen pro vykresleni hrace
    ball_owner_b = False
    team_coach = "notSpecified"
    AI_metrix =0
    model = "empty"


    # ulozi jmeno trenera pro team
    def set_coach (self,new_coach):
        self.team_coach = new_coach

    # pri pohybu(i jine akci) hrace trener zaznamena data,vyuzito pro trenovani
    def send_data_to_coach(self,action,list_of_ingamers):
        self.team_coach.process_data(self,action,list_of_ingamers)


    # pro testy,pohyb v kruhu
    def move_round(self,The_game_window,The_field,list_of_ingamers):
        action = 1000 #neutralni hodnota
        model = self.model
        '''
        0: otoc + 10 stupnu
        1: otoc - 10 stupnu
        2: krok
        3: kop do mice
        (4: bez akce)
        '''

        while self.game_status ==  "game" :
            action = 1000 # reset
            turn_angle = 22 # hrac se muze pootocin jen o 22 stupnu (zaokrouhlovani pro cele pixely)
            prediction = model.predict([[round(self.path_target), \
                                        round(self.calculate_angle_to_other_object(list_of_ingamers[1].position)), \
                                        # oprava pro rozdil od hrany hrace ne od stredu kruznic (umozni vypocet nezavisle na velikosti hracu a mice)
                                        round(pythagoras_distance (self.position,list_of_ingamers[1].position) - self.radius - list_of_ingamers[1].radius  ) ]])
            #print (prediction)
            action = np.argmax(prediction[0])

            if action == 3:
                print ("ttttririririririri",prediction)


            #action = 1000 #TESTTTTTSTSTSTSTSTSTYYY
            clock.tick(60)                                       # 5 pro testovani zmen na 60

            #print ("acttion", action)
            if self.selected_b == False:
                # oprava pro uhly kdyz presahnou 360   /    0
                if action == 0:
                    if (self.path_target + turn_angle) >= 360:
                        uhel = (self.path_target + turn_angle) - 360
                    else:
                        uhel =   (self.path_target + turn_angle)
                    self.set_path_target(uhel)
                elif action == 1:
                    if (self.path_target - turn_angle) <= 0:
                        uhel = (self.path_target - turn_angle) + 359
                    else:
                        uhel = (self.path_target - turn_angle)

                    #print ("path player :",self.path_target)
                    #print ("path player :",self.path_target)
                    self.set_path_target(uhel)
                elif action == 2:
                    self.move(The_game_window,The_field,list_of_ingamers)
                elif action == 3 and list_of_ingamers[1].owner == self:
                    list_of_ingamers[1].speed = 200   #testovaci kop




    # KOMPLEXNI metoda pro pohyb. podle uhlu se nastavi vektor pohybu pote se kontroluje zda je volo pred hracem
    # pokud je v draze jiny hrac nepohne se, pokud je v draze mic,vypocita se novy pohyb mice
    def move(self,The_game_window,The_field,list_of_ingamers):                                                          # FUNKCE move POTREBUJE ZPREHLEDNIT

        if debug_mode == 1:
            print('metodaplayer')

        # hranice hriste
        bottom = The_field.field_bl_corner[1]
        top    = The_field.field_bl_corner[1] - The_field.field_height
        right  = The_field.field_bl_corner[0] + The_field.field_width
        left   = The_field.field_bl_corner[0]

        #-------------DODELAT bounderies / colisions ----------------------                                     #jede zkontroluj
        test_target_on_filed = 0
        test_target_too_close = 1
        path_for_ball_check = 1
        ball_is_frozen = 0

        #  detekce pohybu na hristi, cast hrace muze prejit pres linii hriste , pro pripad ze se balon zastavil prave na teto linii
        if self.position[0] + self.velocity[0] > left - self.radius/2  and self.position[0] + self.velocity[0] < right + self.radius/2  and \
            self.position[1] + self.velocity[1] < bottom + self.radius/2  and self.position[1] + self.velocity[1] > top - self.radius/2  :

            test_target_on_filed = 1

        # detekce ostatnich hracu / mice
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
                # velikost je mensi nez pred krok a to presne o jeden pixel
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

                    # 2. pohyb posune mic, hrac udelal pohyb na lokaci mice => mic se posune                           # chyba nekdy mic zamrzne u hrace mozna zaokrouhlovani pri vypoctu souradnic
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

                    # hrac odejde od mice => jiz neni jeho vlastnik
                    if ingamer_hypotensue > list_of_ingamers[no_of_ingamers].radius + self.radius + 2 and \
                            list_of_ingamers[no_of_ingamers].owner == self :
                              list_of_ingamers[no_of_ingamers].reset_owner(self)


                # vynecha 'sebe' v kontrolre kolize , vynecha mic index '1' v list_of_ingamers
                if ingamer_hypotensue < 2 * self.radius and other_ingamer_position != self.position and no_of_ingamers > 1 :
                    test_target_too_close = 0

        # pokud jsou vsechny podminky splneny hrac se muze pohnout
        if test_target_on_filed == 1 and test_target_too_close ==1 and path_for_ball_check == 1:
            self.position =  [ self.position[0] + self.velocity[0]  ,self.position[1]  + self.velocity[1]  ]

            #data tracking
            if self.selected_b == True:
                '''
                0: otoc +10 stupnu,1: otoc -10stupnu,
                2: krok,3: kop do mice,4: bez akce
                '''
                self.send_data_to_coach(2,list_of_ingamers)  # 3 - krok

        if debug_mode == 1:
            print('plr---------- ')
            print (list_of_ingamers[1])
            print(vars(list_of_ingamers[1]))
            print (list_of_ingamers[2])
            print(vars(list_of_ingamers[2]))
            print (list_of_ingamers[3])
            print(vars(list_of_ingamers[3]))
            print('---------- ')


    # DRAW je pro testovani skoro stejny pro mic i hrace                                                #slo by udelat animace mice
    def draw_ingamer(self,game_window):
        #self.draw_ingamer(game_window)
        ingamer.draw_ingamer(self,game_window)

        # kresli vision hrace - kam se diva
        # kresleno z velocity jelikoz to je uhel kam hrac smeruje

        view = 10 # zobrazeni pohledu je 10 pixelu , velocity je |2| * 5 = 10

        vision_adjescent = view * self.velocity[0]
        vision_opposite = view * self.velocity[1]

        if self.ball_owner_b == True :
            view_color = green
        else:
            view_color = self.color

        '''
        if self.selected == 1:                                                                                                #s[patne reseni potrebuje opravit]
            pygame.draw.lines(game_window.surface, view_color, True, ((self.position[0] ,self.position[1] ), \
                                ( self.position[0] + vision_adjescent ,self.position[1] + vision_opposite  )), 1)

        '''


        pygame.draw.lines(game_window.surface, view_color, True, ((self.position[0] ,self.position[1] ), \
                                ( self.position[0] + vision_adjescent ,self.position[1] + vision_opposite  )), 1)



    def draw_data_lower_menu (self,The_game_window,The_field,list_of_ingamers):
        f_print_player_details(The_game_window,The_field,self,list_of_ingamers)

        # zobrazeni hodnot jen pro tesy mozna LAB_mode
        if self.team_type == "AI" and self.selected_b == False:
            live_data = [round(self.path_target), \
                        round(self.calculate_angle_to_other_object(list_of_ingamers[1].position)), \
                        # oprava pro rozdil od hrany hrace ne od stredu kruznic (umozni vypocet nezavisle na velikosti hracu a mice)
                        round(pythagoras_distance (self.position,list_of_ingamers[1].position) - self.radius - list_of_ingamers[1].radius  )]


            f_print_model_live (The_game_window,The_field,self,list_of_ingamers,live_data,read_model_values ("model.h5"))

        #print_test_x(The_game_window)   # jen pro testy

    '''

    PRIDEJ metodu 'no action' pro automatizovaneho hrace

    '''

#--------------------------------------------------------------------------------------------class ball
# trida pro Mic
class ball (ingamer):
    resistance = 1
    color = white
    radius = 10
    owner = 'nooneyet'
    speed = 0

    def draw_data_lower_menu (self,The_game_window,The_field,list_of_ingamers):
        f_print_ball_details(The_game_window,The_field,self,list_of_ingamers)

    # kontrola pro hrace kdyz nemuze udelat krok, protoze mic nema misto kam se posunout
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

        # detekce hracu,mic ma v draze dalsiho hrace
        for no_of_ingamers in range (2,len(list_of_ingamers)):
            other_ingamer_position = list_of_ingamers[no_of_ingamers].position
            ingamer_adjescent =  abs (self.position[0] + self.velocity[0] -  other_ingamer_position[0])
            ingamer_opposite =  abs (  self.position[1]  + self.velocity[1]-  other_ingamer_position[1])
            ingamer_hypotensue = math.sqrt(ingamer_adjescent **2 + ingamer_opposite **2)

            if ingamer_hypotensue <= self.radius + list_of_ingamers[no_of_ingamers].radius  :                                    # zkontrolovat porovnani

                decision =0

        return decision

    # vynulovani vlastnika mice
    def reset_owner(self,player):
        if self.owner == player:
            self.owner = 0
            self.color = white
            player.ball_owner_b = False

    # nastaveni vlatnika mice
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

    # pohyb mice,podobny pohybu hrace, ale mic se muze odrazet od prekazek
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

    # pokud ma mic energii(speed) tak vola metodu move
    def moving(self,The_game_window,The_field,list_of_ingamers):

        for no_of_ingamers in range (2 , len(list_of_ingamers)):
            list_of_ingamers[no_of_ingamers].ball_owner_b = False

        if self.speed != 0:
            self.speed = self.speed -1
            self.move(The_game_window,The_field,list_of_ingamers)
            list_of_ingamers[0].goal_check(The_field,list_of_ingamers[1])

    #jak se hybe kontroluje path !!!!!!!

    def draw_ingamer(self,game_window):                                                                      # pouze pro testovani  pak ccela metoda do komentu, a draw dela metoda od ingamer tridyingamer
        #self.draw_ingamer(game_window)
        ingamer.draw_ingamer(self,game_window)

        # kresli vision hrace - kam se diva
        # kresleno z velocity jelikoz to je uhel kam hrac smeruje

        view = 10 # zobrazeni pohledu je 10 pixelu , velocity je |2| * 5 = 10

        vision_adjescent = view * self.velocity[0]
        vision_opposite = view * self.velocity[1]

        '''
        if self.ball_owner_b == True :
            view_color = green
        else:
            view_color = self.color


        if self.selected == 1:                                                                                                #s[patne reseni potrebuje opravit]
            pygame.draw.lines(game_window.surface, view_color, True, ((self.position[0] ,self.position[1] ), \
                                ( self.position[0] + vision_adjescent ,self.position[1] + vision_opposite  )), 1)

        '''


        pygame.draw.lines(game_window.surface, green, True, ((self.position[0] ,self.position[1] ), \
                                ( self.position[0] + vision_adjescent ,self.position[1] + vision_opposite  )), 1)
