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
import screens
from screens import *
import testing_logs
from testing_logs import *
#-ppppppppppak smazat
import neural_network
from neural_network import *
import reinforsment_learning
from reinforsment_learning import *
#-pppppppppppppp

from random import randint
import tensorflow as tf
from tensorflow import keras
import numpy as np
#import matplotlib.pyplot as plt

#-------------------------------------------------------------------------------class player
class player (ingamer):
    game_status = "notSpecified"             # hra, pausa, ....
    angle = "notSpecified"                   #???ZKONTROLUJ UZ JE V INGAMER TRIDE                                           #neni potreba je uzito path target
    user_driven = "notSpecified"             # kdyz je team_type human , je hrac ovladany uzivatelem Y/N
    team = "notSpecified"                    # jmeno teamu
    speed  = 0                               # osobnost hrace, urcuje rychlost kroku
    kick_power = 0                           # osobnost hrace, urcuje rychlost mice
    balance  = 0                             # osobnost hrace, urcuje zda hrac muze spadnouot  -----ZATIM nepouzito-------
    acuracy = 0                              # osobnost hrace, urcuje presnost kopu            -----ZATIM nepouzito-------
    player_type = "notSpecified"                    # utocnik, obrance, brankar, midfielder
    position_by_strategy = "notSpecified"    # -----ZATIM nepouzito-------
    strategy = 0                             # -----ZATIM nepouzito-------
    tactic= 0                                # -----ZATIM nepouzito-------
    dsetination_kick = "notSpecified"        # -----ZATIM nepouzito-------  asi nebude treba
    vision = 5                            # zatim vyuzitojen pro vykresleni hrace
    ball_owner_b = False                     # pokud je hrac ball owner muze provect kop
    team_coach = "notSpecified"              # trener teamu
    #AI_metrix =0                                                                                                           # -----ZATIM nepouzito------- asi neni treba bo je pouzit skills_level
    model = "empty"                                                                                                        # -----zkontrolovat je treba kdyz je znam ID ??
    ID = "empty"                             # DATE TIME STAMP bude stejne jako nazev .h5 souboru
    name ="empty"
    message = 0                              # -----ZATIM nepouzito-------
    trening_time = 0
    trening_type_player = 0
    model_needs_reload = False
    path_folders = 'none'
    NN_functions_set_defined = []
    skills_level = 0                         # osobnost hrace, urcuje kolik vstupu hrac rozpozna pri treningu
    skills_set = []                           #skill set hrace pri vytoreni
    isREtrainingRawData = False
    TEST_NN_TESTING_VALUE = True


    # vstup metody muze byt i zaporny
    def turn_player_path_by_angle(self,new_angle):
        if (self.path_target + new_angle) >= 360:
            result_angle = (self.path_target + new_angle) - 360
        else:
            result_angle = (self.path_target + new_angle)
        if (self.path_target - new_angle) <= 0:
            result_angle = (self.path_target + new_angle) + 359
        else:
            result_angle = (self.path_target + new_angle)

        self.set_path_target(result_angle)


    def isplayer_closest_to_ball(self,list_of_ingamers):
        lenght = 0
        lenght_buffer = 10000
        angle  = 0
        result = 0
        for player in range (1,len(list_of_ingamers)):
            lenght = pythagoras_distance(list_of_ingamers[0].rect.center, list_of_ingamers[player].rect.center)
            if lenght < lenght_buffer:
                lenght_buffer = lenght
                result_player = list_of_ingamers[player]
        if result_player == self:
            result = 1
        return result


    def find_distance_to_closest_player(self,team_players):
        lenght = 0
        lenght_buffer = 10000
        angle  = 0
        result_player = 'none'
        for player in range (0,len(team_players)):
            if team_players[player] != self:
                lenght = pythagoras_distance(self.rect.center, team_players[player].rect.center)
                if lenght < lenght_buffer:
                    lenght_buffer = lenght
                    result_player = team_players[player]
        return lenght_buffer


    def find_angle_to_closest_player(self,team_players):
        lenght = 0
        lenght_buffer = 10000
        angle  = 0
        result_player = 'none'
        for player in range (0,len(team_players)):
            if team_players[player] != self:
                lenght = pythagoras_distance(self.rect.center, team_players[player].rect.center)
                if lenght < lenght_buffer:
                    lenght_buffer = lenght
                    result_player = team_players[player]

        self.calculate_angle_to_other_object(result_player.rect.center)
        return angle


    def move_on_screen(self,The_game_window):
        self.rect.center =  [self.rect.center[0] + self.velocity[0], self.rect.center[1] + self.velocity[1]]
        if self.rect.center[0] < 10 or self.rect.center[1]< 10 or self.rect.center[0] >  The_game_window.window_width or self.rect.center[1]> The_game_window.window_height:
            self.set_path_target(self.calculate_angle_to_other_object([0,0]))
            self.set_graphic("player_a.png")
            if randint( 0, 1) ==0:
                self.set_graphic("player_b.png")
            self.set_position (randint(0, The_game_window.window_width), \
                                randint( 0, The_game_window.window_height))


    def set_screen_player(self):
        self.field_site = "left"
        self.set_path_target(self.calculate_angle_to_other_object([0,0]))
        self.game_status = "game"
        self.set_graphic("player_a.png")


    def save_trening_time (self,time):
        self.trening_time = int(self.trening_time) + time


    # nastavi trening pro xml
    def save_trening_type(self,new_trening):
        if int(self.trening_type_player) == TreningType.not_trained.value or self.trening_type_player == int(new_trening):
            self.trening_type_player = new_trening
        else:
            self.trening_type_player = TreningType.mixed.value
        return   self.trening_type_player


    # ulozi jmeno trenera pro team
    def set_coach (self,new_coach):
        self.team_coach = new_coach


    # pri pohybu(i jine akci) hrace trener zaznamena data,vyuzito pro trenovani
    def send_data_to_coach(self,action,list_of_ingamers,The_field):
        self.team_coach.process_data(self,action, self.get_NN_data(The_field,list_of_ingamers) )


    def get_NN_data(self,The_field,list_of_ingamers):
        teamBplayers = [ list_of_ingamers[6], list_of_ingamers[7], list_of_ingamers[8], list_of_ingamers[9], list_of_ingamers[10] ]

                            ##                                                                    ##
                                ##                                                            ##
                # # # # # #         ##                    NN                              ##          # # # # # # # #
                                ##                                                            ##
                            ##                                                                    ##

        if self.isREtrainingRawData == False:
            field_ratio_width  = The_field.field_bl_corner[0] + The_field.field_width
            field_ratio_height = The_field.field_bl_corner[1] + The_field.field_height
            inputs = [round(self.path_target/360,5), \
                    self.player_type, \
                    calculate_sector(1,self.field_site,self.rect.center,[ The_field.field_width,The_field.field_height], The_field.field_bl_corner) / 100  , \
                    round( pythagoras_distance(  self.rect.center  , list_of_ingamers[0].rect.center ),5), \
                    round(self.find_angle_to_closest_player( self.team_coach.team_players) / 360,5) , \
                    round(self.find_distance_to_closest_player( self.team_coach.team_players) / 1000,5), \
                    round(self.find_angle_to_closest_player( teamBplayers) / 360 ,5), \
                    round(self.find_distance_to_closest_player( teamBplayers) /1000,5), \
                    self.isplayer_closest_to_ball(list_of_ingamers), \
                    round(self.calculate_angle_to_other_object(list_of_ingamers[0].rect.center)/360,5) ]
            for loop in range (0,len(self.skills_set)):
                if self.skills_set[loop] == False:
                    inputs[loop] = 0

        else:
            field_ratio_width  = The_field.field_bl_corner[0] + The_field.field_width
            field_ratio_height = The_field.field_bl_corner[1] + The_field.field_height
            shift_begining = 2
            shift_pairs = 2
            inputs = 24 * [0]
            # naplni pole o velikosti 24 a jestli patri do vstupu dle kodu skills_set jinak necha 0
            # od indexu 2 jsoiu to pary souradnic pro vsechny ingamers vcertne ball
            inputs[0] = round(self.path_target/360 , 5)
            inputs[1] = self.player_type
            for no_of_ingamers in range (0,len(list_of_ingamers)):
                if self.skills_set[ no_of_ingamers * shift_pairs  + shift_begining] == True:
                    inputs[no_of_ingamers + no_of_ingamers + 2] = round( list_of_ingamers[no_of_ingamers].rect.center[0] / field_ratio_width , 5)
                    inputs[no_of_ingamers + no_of_ingamers + 3] = round( list_of_ingamers[no_of_ingamers].rect.center[1]  / field_ratio_height , 5)

            for loop in range (0,3):# treba kontrolovat prvni 2
                if self.skills_set[loop] == False:
                    inputs[loop] = 0
        return inputs


    # pro hrace ovladaneho PC team ma jedno vlakno
    def move_round_once(self,The_field,list_of_ingamers):
        action = 404 #neutralni hodnota
        no_of_inputs = int(self.skills_level)
        turn_angle = 22 # hrac se muze pootocin jen o 22 stupnu (zaokrouhlovani pro cele pixely)
        inputs = no_of_inputs * [0]
        selection_coding = self.skills_set
        inputs = self.get_NN_data(The_field,list_of_ingamers)

        if self.model_needs_reload == True:
            self.model_needs_reload = False
            full_path = get_path_home_folder()
            self.model= load_model( full_path +  self.ID + ".h5")

        #model=self.model
        prediction =  self.model.predict([[[inputs]]])     # ok s 3[]
        action = np.argmax(prediction[0])
        '''Outputs:
             - otoc +22 stupnu  (kod 0)
             - otoc -22 stupnu  (kod 1)
             - krok             (kod 2)
             - kop do mice      (kod 3)
             - bez akce         (kod 4)
        '''
        #clock.tick(120)   # 5 pro testovani zmen na 60
        '''
        if self.selected_b == False:
            # oprava pro uhly kdyz presahnou 360 / 0
            if action == 0:
                self.turn_player_path_by_angle(turn_angle)
            elif action == 1:
                self.turn_player_path_by_angle(-1 * turn_angle)
            elif action == 2:
                self.move(The_field,list_of_ingamers)
            elif action == 3 and list_of_ingamers[0].owner == self:
                list_of_ingamers[0].speed = 200   #testovaci kop
        '''



        if self.selected_b == False:
            # oprava pro uhly kdyz presahnou 360   /    0                                            KOD 3 x !!!!!!!!!!  opakuje se
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
                self.set_path_target(uhel)
            elif action == 2:
                self.move(The_field,list_of_ingamers)
            elif action == 3 and list_of_ingamers[0].owner == self:
                list_of_ingamers[0].speed = 200   #testovaci kop


    # pro hrace ovladaneho PC kazdy hrac sve vlakkno
    def move_round(self,The_field,list_of_ingamers):
        while self.game_status ==  "game" :
            self.move_round_once(The_field,list_of_ingamers)


    # prdelana metoda pomoci sprites
    def move(self,The_field,list_of_ingamers):                                                          # FUNKCE move POTREBUJE ZPREHLEDNIT
        ball_index = 0

        # hranice hriste
        bottom = The_field.field_bl_corner[1]
        top    = The_field.field_bl_corner[1] - The_field.field_height
        right  = The_field.field_bl_corner[0] + The_field.field_width
        left   = The_field.field_bl_corner[0]

        test_target_on_field = 0
        test_player_free_path = 1
        test_ball_free_path = 1
        ball_is_frozen = False

        # kontrola zda mic neni v radius hrace
        if pythagoras_distance (list_of_ingamers[ball_index].rect.center,  self.rect.center) < list_of_ingamers[ball_index].radius + self.radius:
            ball_is_frozen = True

        #  detekce pohybu na hristi, cast hrace muze prejit pres linii hriste , pro pripad ze se balon zastavil prave na teto linii
        if self.rect.center[0] + self.velocity[0] > left - self.radius/2  and self.rect.center[0] + self.velocity[0] < right + self.radius/2  and \
            self.rect.center[1] + self.velocity[1] < bottom + self.radius/2  and self.rect.center[1] + self.velocity[1] > top - self.radius/2  :

            test_target_on_field = 1

        # kontrola kolize s micem
        if ball_is_frozen == False :

            # pohyb posune mic, hrac udelal pohyb na lokaci mice => mic se posune                           # chyba nekdy mic zamrzne u hrace mozna zaokrouhlovani pri vypoctu souradnic
            if pythagoras_distance (list_of_ingamers[ball_index].rect.center,  self.rect.center) <= (list_of_ingamers[ball_index].radius + self.radius) + 3:
            # if  pygame.sprite.collide_circle(self, list_of_ingamers[ball_index]) :

                list_of_ingamers[0].set_owner(self)

                # novy uhel(posun mice)  je stred hrace a souradnice kontaktu s micem
                ball_new_target = self.calculate_angle_to_other_object(list_of_ingamers[ball_index].rect.center)
                list_of_ingamers[ball_index].set_path_target (ball_new_target)

                test_ball_free_path  = list_of_ingamers[ball_index].is_ball_path_clear(The_field,list_of_ingamers)  #2711

                if test_ball_free_path == 1 :
                    list_of_ingamers[ball_index].speed = 2
                else:
                    list_of_ingamers[ball_index].speed = 0

            # hrac odejde od mice => jiz neni jeho vlastnik
            if pythagoras_distance (list_of_ingamers[ball_index].rect.center,  self.rect.center) > (list_of_ingamers[ball_index].radius + self.radius) + 5:
            #if pygame.sprite.collide_circle(self, list_of_ingamers[ball_index]) == False:
                  list_of_ingamers[ball_index].reset_owner(self)

        # detekce ostatnich hracu # vynecha 'sebe' v kontrolre kolize , vynecha mic index '0' v list_of_ingamers
        for no_of_ingamers in range (1,len(list_of_ingamers)):

            # vynecha 'sebe' v kontrolre kolize , vynecha mic index '0' v list_of_ingamers

            # if pygame.sprite.collide_circle(self, list_of_ingamers[no_of_ingamers]) and \
            #     list_of_ingamers[no_of_ingamers].rect.center != self.rect.center :
            distance = pythagoras_distance (list_of_ingamers[no_of_ingamers].rect.center,  self.rect.center)
            #print ("dstn a no_of_ingamers" , dstnc , no_of_ingamers)
            #if distance <= 2*self.radius:
            #    test_player_free_path = 0


        # pokud jsou  podminky splneny hrac se muze pohnout
        if test_target_on_field == 1 and test_ball_free_path == 1 and test_player_free_path == 1:

            self.rect.center =  [self.rect.center[0] + self.velocity[0], self.rect.center[1] + self.velocity[1]]

    def movexx(self,The_field,list_of_ingamers):
        test_mode = True
        The_ball = list_of_ingamers[0]

        # - 0 - hranice hriste
        if self.is_move_over_field(The_field):
            if test_mode: print('- 0 - ')
            return

        # - 1 -  kontrola zda je hrac ball owner
        # pokud vice hracu v blizkosti tak plati, posledni kdo dojde k mici je vzdy owner
        tolerance_ballowners = 3
        if self.do_ingamer_colide( The_ball , tolerance_ballowners) == True:
            if test_mode: print('- 1 - ')
            if test_mode: print('owner ,rozdil :', self.name, 'diff' , tolerance_ballowners)
            if test_mode: print('mic ',The_ball.rect.center)
            if test_mode: print('plr ', self.rect.center)
            The_ball.set_owner(self)
            ball_new_target = self.calculate_angle_to_other_object(The_ball.rect.center)
            The_ball.set_path_target (ball_new_target)

        # - 1.1 - hrac jde na misto mice posune mic jestli je misto jinak je move neplatny
        tolerance = self.step
        if self.do_ingamer_after_step_colide( The_ball , tolerance) == True:
            if test_mode: print('- 1.1 -     ')
            #is_move_to_ingamer = self.is_move_to_ingamer(The_ball)
            if test_mode: print('    mic vel ',The_ball.velocity)
            if test_mode: print('    plr vel ', self.velocity)
            test_ball_free_path  = The_ball.is_ball_path_clear(The_field,list_of_ingamers, self)
            # hrac se hybe smerek m mici a ten nema misto pro move
            if test_ball_free_path == False :    #  nad is_move_to_ingamer = True :
                if test_mode: print('- 1.2 -     ')
                return

            ball_new_target = self.calculate_angle_to_other_object(The_ball.rect.center)
            The_ball.set_path_target (ball_new_target)
            The_ball.speed = 2

        # - 2 -  hrac odejde od mice => jiz neni jeho vlastnik  OPRAVA
        if pythagoras_distance (The_ball.rect.center,  self.rect.center) > (The_ball.radius + self.radius) + 5:
            if test_mode: print('- 2 - ')
            #if pygame.sprite.collide_circle(self, list_of_ingamers[ball_index]) == False:
            The_ball.reset_owner(self)

        # - 2 -  hrac odejde od mice => jiz neni jeho vlastnik
        #if self.ball_owner_b == True:
        if False:
            if test_mode: print('- 2 - ')
            tolerance_ballNOTowners = 5
            if  self.do_ingamer_after_step_colide( The_ball , tolerance_ballNOTowners):     # + self.step + 2:
                if test_mode: print('  - 2.1 - plr reset owner ')
                if test_mode: print('  mic ',The_ball.rect.center)
                if test_mode: print('  plr ', self.rect.center)
                The_ball.reset_owner(self)

        # MOVE OK
        self.rect.center =  [self.rect.center[0] + self.velocity[0], self.rect.center[1] + self.velocity[1]]


    def draw_data_lower_menu (self,The_game_window,The_field,list_of_ingamers):                                            # opravit nema byt metoda ale funkce v screens, vykreslovani
        f_print_player_details_ingame(The_game_window,The_field,self,list_of_ingamers)

        # zobrazeni hodnot jen pro tesy mozna LAB_mode
        if self.team_type == "AI" and self.selected_b == False:
            live_data = [round(self.path_target), \
                        round(self.calculate_angle_to_other_object(list_of_ingamers[1].rect.center)), \
                        # oprava pro rozdil od hrany hrace ne od stredu kruznic (umozni vypocet nezavisle na velikosti hracu a mice)
                        round(pythagoras_distance (self.rect.center,list_of_ingamers[1].rect.center) - self.radius - list_of_ingamers[1].radius  )]

    '''

    PRIDEJ metodu 'no action' pro automatizovaneho hrace

    '''

#-------------------------------------------------------------------------------class ball
class ball (ingamer):
    radius = 7
    team_type = "AI"    #  mic je neklikatelny
    resistance = 1      # udava jak mic zpomaluje  ---zatim nevyuzito---
    color = WHITE
    owner = False
    speed = 0

    def draw_data_lower_menu(self,The_game_window,The_field,list_of_ingamers):                                         # opravit nema byt metoda ale funkce v screens, vykreslovani
        f_print_ball_details(The_game_window,The_field,self,list_of_ingamers)




    # kontrola pro hrace kdyz nemuze udelat krok, protoze mic nema misto kam se posunout
    # path v instanci je uz novy od metody move od hrace
    #def is_ball_path_clear(self,The_game_window,The_field,list_of_ingamers):                                            #opakujicis se kod pro preponu kolize
    def is_ball_path_clear(self,The_field,list_of_ingamers):
        decision = 1

        bottom = The_field.field_bl_corner[1]
        top    = The_field.field_bl_corner[1] - The_field.field_height
        right  = The_field.field_bl_corner[0] + The_field.field_width
        left   = The_field.field_bl_corner[0]

        #  detekce pohybu na hristi, odraz od sten
        if self.rect.center[0] - self.radius + self.velocity[0]  < left :
            decision =0
        if self.rect.center[0] + self.radius + self.velocity[0]  > right :
            decision =0
        if self.rect.center[1] + self.radius + self.velocity[1]  > bottom :
            decision =0
        if self.rect.center[1]  - self.radius + self.velocity[1]  < top :
            decision =0

        # detekce hracu,mic ma v draze dalsiho hrace
        for no_of_ingamers in range (2,len(list_of_ingamers)):
            other_ingamer_position = list_of_ingamers[no_of_ingamers].rect.center
            ingamer_adjescent =  abs (self.rect.center[0] + self.velocity[0] -  other_ingamer_position[0])
            ingamer_opposite =  abs ( self.rect.center[1]  + self.velocity[1]-  other_ingamer_position[1])
            ingamer_hypotensue = sqrt(ingamer_adjescent **2 + ingamer_opposite **2)

            if ingamer_hypotensue <= self.radius + list_of_ingamers[no_of_ingamers].radius  :                          # zkontrolovat porovnani

                decision =0

        return decision








    def is_ball_path_clearxxx(self,The_field,list_of_ingamers,player):
        print(   'is_ball_path_clear   ' )
        decision = not self.is_move_over_field(The_field)   # over field je false ale znamena ze path volny
        print(   '   is_move_over_field   ',  decision )
        tolerance = 1
        for no_of_ingamers in range (1,len(list_of_ingamers)):
            if  list_of_ingamers[no_of_ingamers] != player:
                decision2 = self.do_ingamer_after_step_colide( list_of_ingamers[no_of_ingamers] , tolerance)

                print(   '       do_ingamer_after_step_colide   ',  decision2 , 'plr ' ,  list_of_ingamers[no_of_ingamers].ID)
                print( '        mic ',self.rect.center)
                print('         plr ', list_of_ingamers[no_of_ingamers].rect.center)
                if self.do_ingamer_after_step_colide( list_of_ingamers[no_of_ingamers] , tolerance) == True:
                    decision = False

        return decision

    def reset_owner(self,player):
        if self.owner == player:
            self.owner = False
            self.color = WHITE
            player.ball_owner_b = False

    def reset_ownerx(self,player):
        if self.owner == player:
            self.owner = False
            self.color = WHITE
            player.ball_owner_b = False

    def set_owner(self,new_owner):
        new_owner.ball_owner_b = True
        self.set_path_target(self.path_target)
        self.owner = new_owner
        self.color = GREEN
        self.field_site = new_owner.field_site

    def set_ownerx(self,new_owner):
        new_owner.ball_owner_b = True
        #self.step = new_owner.kick_power
        self.set_path_target(self.path_target)
        self.owner = new_owner
        self.color = GREEN
        self.field_site = new_owner.field_site

    def calculate_fieldSite_forNN(self):
        calculated_value = 1
        if self.field_site == 'left':
            calculated_value = 0





    # pohyb mice,podobny pohybu hrace, ale mic se muze odrazet od prekazek
    def move(self,The_field,list_of_ingamers):                                                #zkontroluj jaka cast move lze udelat pro ingamer a pak jen zdedit

        if debug_mode == 1:
            print('metodaball')

        # 2 je rychlost pri 'driblingu'
        if self.speed > 2 :
            # kdyz krac mic odkopne ,mic ztraci vlatnika
            self.owner = 0
            self.color = WHITE

        step = self.step
        bottom = The_field.field_bl_corner[1]
        top    = The_field.field_bl_corner[1] - The_field.field_height
        right  = The_field.field_bl_corner[0] + The_field.field_width
        left   = The_field.field_bl_corner[0]

        #-------------DODELAT bounderies / colisions ----------------------

        # detekce hracu
        for no_of_ingamers in range (1,len(list_of_ingamers)):
            other_ingamer_position = list_of_ingamers[no_of_ingamers].rect.center
            ingamer_adjescent =  abs (self.rect.center[0] + self.velocity[0] -  other_ingamer_position[0])
            ingamer_opposite =  abs ( self.rect.center[1]  + self.velocity[1]-  other_ingamer_position[1])
            ingamer_hypotensue = sqrt(ingamer_adjescent **2 + ingamer_opposite **2)

            if ingamer_hypotensue <= self.radius + list_of_ingamers[no_of_ingamers].radius  :
                                                                                                                    # JEN PRO TESTY ,JINAK POTREBA DODELAT VYPOCET UHLU ODRAZu
                self.velocity[0] = self.velocity[0] * -1
                self.velocity[1] = self.velocity[1] * -1

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
        if self.rect.center[0] - self.radius + self.velocity[0]  < left :
            self.velocity[0] = self.velocity[0] * -1
        if self.rect.center[0] + self.radius + self.velocity[0]  > right :
            self.velocity[0] = self.velocity[0] * -1
        if self.rect.center[1] + self.radius + self.velocity[1]  > bottom :
            self.velocity[1] = self.velocity[1] * -1
        if self.rect.center[1]  - self.radius + self.velocity[1]  < top :
            self.velocity[1] = self.velocity[1] * -1

        # potvrzeni nove pozice
        self.rect.center =  [self.rect.center[0] + self.velocity[0]  ,self.rect.center[1]  + self.velocity[1]  ]








    # pohyb mice,podobny pohybu hrace, ale mic se muze odrazet od prekazek
    def movexxx(self,The_field,list_of_ingamers):                                                #zkontroluj jaka cast move lze udelat pro ingamer a pak jen zdedit

        # 2 je rychlost pri 'driblingu'
        if self.owner != False  and self.speed > 3 :
            print('ball reset owner')
            # kdyz krac mic odkopne ,mic ztraci vlatnika
            self.owner = 0
            self.color = WHITE

        step = self.step
        bottom = The_field.field_bl_corner[1]
        top    = The_field.field_bl_corner[1] - The_field.field_height
        right  = The_field.field_bl_corner[0] + The_field.field_width
        left   = The_field.field_bl_corner[0]

        #-------------DODELAT bounderies / colisions ----------------------

        # detekce hracu
        for no_of_ingamers in range (1,len(list_of_ingamers)):
            other_ingamer_position = list_of_ingamers[no_of_ingamers].rect.center
            ingamer_adjescent =  abs (self.rect.center[0] + self.velocity[0] -  other_ingamer_position[0])
            ingamer_opposite =  abs ( self.rect.center[1]  + self.velocity[1]-  other_ingamer_position[1])
            ingamer_hypotensue = sqrt(ingamer_adjescent **2 + ingamer_opposite **2)

            if ingamer_hypotensue <= self.radius + list_of_ingamers[no_of_ingamers].radius + 1 :
                print('no '  ,   no_of_ingamers,'hypoten ' ,  ingamer_hypotensue   ,  'sum ' ,self.radius   + list_of_ingamers[no_of_ingamers].radius +1  )
                print('ball narazi do nekoho')
                index = randint(0,2)
                myarray = [ 0, 1, -1]
                self.velocity[0] = self.velocity[0] * myarray[index]
                if index == 0:
                    myarray = [ 1, 1, -1]

                self.velocity[1] = self.velocity[1] * myarray[index]

                # snizeni energie(speed)
                if self.speed > 100 :
                    self.speed = int( self.speed * 0.8  )
                elif self.speed > 5 and self.speed <= 100  :
                    self.speed = int( self.speed * 0.5  )
                elif self.speed < 5:
                    self.speed = 0

        #  detekce pohybu na hristi, odraz od sten
        if self.rect.center[0] - self.radius + self.velocity[0]  < left :
            self.velocity[0] = self.velocity[0] * -1
        if self.rect.center[0] + self.radius + self.velocity[0]  > right :
            self.velocity[0] = self.velocity[0] * -1
        if self.rect.center[1] + self.radius + self.velocity[1]  > bottom :
            self.velocity[1] = self.velocity[1] * -1
        if self.rect.center[1]  - self.radius + self.velocity[1]  < top :
            self.velocity[1] = self.velocity[1] * -1

        # potvrzeni nove pozice
        self.rect.center =  [self.rect.center[0] + self.velocity[0]  ,self.rect.center[1]  + self.velocity[1]  ]


    # pokud ma mic energii(speed) tak vola metodu move
    def moving(self,The_field,The_reff):
        The_ball = The_reff.list_of_ingamers[0]

        for no_of_ingamers in range (1, len(The_reff.list_of_ingamers)):
            The_reff.list_of_ingamers[no_of_ingamers].ball_owner_b = False

        if self.speed != 0:
            self.speed = self.speed -1
            self.move(The_field,The_reff.list_of_ingamers)
            isGoeal = The_reff.goal_check(The_field,The_ball)
            if isGoeal == True and The_reff.coach_team_A.automated_trening_type != True:
                The_reff.game_reset_after_goal (The_field)







    #   -------------------------- konec   ------------------
