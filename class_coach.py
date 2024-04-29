from random import randint
import pygame
from pygame.locals import *
from threading import  Thread
import time
import copy

import xml_f
from xml_f import *
import f_menu                                                                          # ne vsechny metody potrebujou okno jako parametr zkontroluj
from f_menu import *
import neural_network
from neural_network import *
import class_ingamer
from class_ingamer import *
import class_player_ball
from class_player_ball import *
import support_functions
from support_functions import *
import screens
from screens import *
import Re_reward_rules
from Re_reward_rules import *

import testing_logs
from testing_logs import *

clock = pygame.time.Clock()




#--------------------------------------------------------------------------------------------class coach
# trida trenera
class class_coach ():
    def __init__(self,team):
        self.team_play_at = team              # urcuje zda je tym domaci nebo ne ,pro nedomaci team se nezobrazuji detaily
        self.loaded_teams_xml = []
        for loop in range (0,10):
            self.loaded_teams_xml.append(SavingType.empty_team_slot.value)
        self.load_data_from_xml()
        self.load_trening_areas()
        self.training_areas_players_updated = True

    # buffers pro vyber teamu v 'team management'
    selected_slot_team_management = [-1,-1]
    selected_slot_team_management_buffer = [-1,-1]
    data_trening = []                   # hrac zasle svoje data, ktere trener vyhodnocuje. vse se uklada do data trening a data labels
    data_labels = []
    active_trening = False              # ukazatel treningu nebo zapasu
    trening_sesion_total_runs = 20 # 5000    # 5000  celkovy pocet uceni pro spusteny trening
    RE_trening_sesion_runs = 500
    trening_repetition_sequence = 0
    trening_repetition_total = 1
    automated_trening_type = False      # true jestli je spusten zautomatizovy trening
    training_areas_ball = [[False,True,False],[False,True,False]]     # hriste rozdeleno na 9 sektoru
    training_areas_players = []
    training_areas_players_updated = True
    trainig_code = 10 * [  True ]
    trainig_code2 = 24 * [ True ]
    team_players = [0,0,0,0,0]
    testdata1 = [0,0,2,2 ]
    testdata2 = [0,0,2,2 ]
    exit_RE_trening = False
    arethreads_on = [False,False]
    new_player_isREtrainingRawData = True



    def isSlotPlayer(self):
        if self.loaded_teams_xml[self.selected_slot_team_management[0]] == SavingType.empty_team_slot.value:
            return False
        if   self.loaded_teams_xml[self.selected_slot_team_management[0]][self.selected_slot_team_management[1]] == SavingType.empty_player_slot.value:
            return False

        return True


    '''
    def generate_players_instance(self,team_name , field_side,team_type,start_game_coordinates):
        shift_x =  start_game_coordinates[0] - 20
        shift_y =  start_game_coordinates[1]
        all_teams = self.loaded_teams_xml
        load_check_ok = False

        teamindex =  self.get_teamindex_from_teamname(team_name)
        if teamindex == 'none' :
            full_path = get_path_away_folder()
            self.load_data_from_xml()
            teamindex =  self.get_teamindex_from_teamname(team_name)
        else:
            full_path = get_path_home_folder()

        if teamindex == 'none' :
            self.team_play_at = "Home"   #oprava pro trening
            full_path = get_path_home_folder()
            self.load_data_from_xml()
            teamindex =  self.get_teamindex_from_teamname(team_name)

        print ('teamindex' , teamindex)

        # input ma tvar : [team_name,5x [pl_name, pl_ID,pl_position,trening_type,trening_time]]
        for players_loop in range (1,6):  # 0 je info o teamu
            shift_y = shift_y + 20
            new_player_ID = all_teams[teamindex][players_loop][1]
            new_player = player ([0,0])
            new_player.path_target = 180
            new_player.game_status = "game"
            new_player.set_path_target(180)
            new_player.ID = new_player_ID
            new_player.name = all_teams[teamindex][players_loop][0]
            new_player.player_type =  float(all_teams[teamindex][players_loop][2])
            new_player.skills_level = int(all_teams[teamindex][players_loop][3])
            new_player.trening_time = all_teams[teamindex][players_loop][4]
            new_player.skills_set =   all_teams[teamindex][players_loop][5]
            new_player.trening_type_player =   all_teams[teamindex][players_loop][6]
            new_player.model_needs_reload = True
            new_player.set_coach(self)
            self.team_players[players_loop -1] = new_player  # 0 je info o teamu
            new_player.team_type = team_type
            new_player.team = all_teams[teamindex][0][0]
            #print (new_player.skills_set)

            # nastaveni v zavislosti na teamu/strane hriste pri obou domacich teamech
            if field_side == "left":
                new_player.set_position (int (shift_x - 40) ,int(shift_y))
                new_player.field_site = "left"
                new_player.set_graphic("player_a.png")
            else:
                new_player.set_position (int (shift_x + 40) ,int(shift_y))
                new_player.color = RED
                new_player.field_site = "right"
                new_player.set_graphic("player_b.png")

            new_player.model= load_model( full_path +  new_player_ID + ".h5")   # zmenin na file dle ID hrace
            print ("  new_player_ID  "    ,   new_player_ID)

    '''

    def get_teamindex_from_teamname(self,teamname):
        teamindex = 'none'
        #print (  'loaded_teams_xml' , self.loaded_teams_xml)
        #print (  'teamname' , teamname)
        for teams_loop in range (0,10):  # 10 - pocet teamu
            if self.loaded_teams_xml[teams_loop] != 0 :

                if self.loaded_teams_xml[teams_loop][0][0] == teamname:
                    teamindex = teams_loop
                    #print (  'teamindex' , teamindex)
                    return teamindex
        #print (  'teamindex' , teamindex)
        return teamindex


        if self.loaded_teams_xml [index_team_a[0]] != SavingType.empty_team_slot.value:
            if index_team_a[1] != 0 and index_team_a[1] != -1:
                # status teamu je original
                if  self.loaded_teams_xml[index_team_a[0]][0][1] == "original" :                               #zkontroluj podmnku
                        player_selected_ID = self.loaded_teams_xml[index_team_a[0]][index_team_a[1]][1]
                        player_selected_ID = str(player_selected_ID)
        if self.training_areas_players_updated  == True:
            pass
            #print('get_playerID' ,player_selected_ID)


        return player_selected_ID # playerid
    def get_playerID_from_slot(self):
        index_team_a = self.selected_slot_team_management
        player_selected_ID ='none'
        if self.loaded_teams_xml [index_team_a[0]] != SavingType.empty_team_slot.value:
            # oznacen hrac
            if index_team_a[1] != 0 and index_team_a[1] != -1:
                # status teamu je original
                if  self.loaded_teams_xml[index_team_a[0]][0][1] == "original" :                               #zkontroluj podmnku
                        player_selected_ID = self.loaded_teams_xml[index_team_a[0]][index_team_a[1]][1]
                        player_selected_ID = str(player_selected_ID)
        if self.training_areas_players_updated  == True:
            #print('get_playerID' ,player_selected_ID)
            pass


        return player_selected_ID # playerid

    def load_trening_areas(self):
        print ('load_trening_areas')
        for teams_loop in range (0,10):  # 10 - pocet teamu
            if self.loaded_teams_xml[teams_loop] !=0:
                for player_loop in range (1,6):
                    playerid = self.loaded_teams_xml[teams_loop][player_loop][1]
                    self.training_areas_players.append([playerid,[[False,True,False],[False,True,False]]])

    def set_trening_areas_for_player(self,player_id,new_training_area):
        for players_loop in range (0,len(self.training_areas_players)):
            if  player_id == self.training_areas_players[players_loop][0]:
                self.training_areas_players[players_loop][1] = new_training_area
                #print('settrening_areas' ,player_id,'new_training_area',new_training_area)

    def get_trening_areas_for_player(self,player_id):
        trening_area ='none'
        #print('p   rint    data)', self.training_areas_players)
        for players_loop in range (0,len(self.training_areas_players)):
            #print('print    data)')
            #print('player_id ' , player_id)
            if  str(player_id) == self.training_areas_players[players_loop][0]:
                trening_area =  self.training_areas_players[players_loop][1]
                #print (   'data',  data)
        if self.training_areas_players_updated  == True:
            print('trening_area' ,trening_area)
        return trening_area

    def get_trainingareaplayers_index_for_player(self,player_id):
        index ='none'
        for players_loop in range (0,len(self.training_areas_players)):
            if  str(player_id) == self.training_areas_players[players_loop][0]:
                index =  players_loop
        if self.training_areas_players_updated  == True:
            print('indexplayer' ,index)
        return index

    def set_training_areas_player(self,change_input_index):  # change_input_index cislo 0 do 5
        playerid = self.get_playerID_from_slot()
        buffer = copy.deepcopy(self.get_trening_areas_for_player(playerid))
        player_index = self.get_trainingareaplayers_index_for_player(playerid)
        index = int(change_input_index)

        if playerid != 'none':
            if change_input_index <3:
                self.training_areas_players[player_index][1][0][index] = not self.training_areas_players[player_index][1][0][index]
            else:
                self.training_areas_players[player_index][1][1][index - 3] = not self.training_areas_players[player_index][1][1][index - 3]

            # area je vzdy jeden celek ,nelze oznacit dve oddelene casti
            if  self.training_areas_players[player_index][1][0] == [True,False,True]  or \
                  self.training_areas_players[player_index][1][1] == [True,False,True]:
                self.training_areas_players[player_index][1] = buffer

        #playerid = self.get_playerID_from_slot()
        #self.set_trening_areas_for_player(playerid,buffer)



    def set_training_areas_ball(self,change_input_index):  # change_input_index cislo 0 do 5
        buffer = copy.deepcopy(self.training_areas_ball)
        index = int(change_input_index)
        if change_input_index <3:
            self.training_areas_ball[0][index] = not self.training_areas_ball[0][index]
        else:
            self.training_areas_ball[1][index - 3] = not self.training_areas_ball[1][index - 3]

        # area je vzdy jeden celek ,nelze oznacit dve oddelene casti
        if  self.training_areas_ball[0] == [True,False,True]  or \
              self.training_areas_ball[1] == [True,False,True]:
            self.training_areas_ball = buffer



    def set_trening_number_of_runs(self,run_type,value):
        if  run_type == 'trening_sesion_total_runs':
            self.trening_sesion_total_runs = value
        if  run_type == 'RE_trening_sesion_runs':
            self.RE_trening_sesion_runs = value
        if  run_type == 'trening_repetition_total':
            self.trening_repetition_total = value

    def team_reset_graphic(self):
        for players_loop in range (0,5):
            self.team_players[players_loop].reset_graphic()

    # nacte data pro teamu a hrace z xml
    def load_data_from_xml(self):

        # nacteni teamu do seznamu
        list_of_teams = []

        if self.team_play_at == "Home":
            for filename in os.listdir( get_path_home_folder() ):
                if not filename.endswith('.xml'): continue
                list_of_teams.append(filename)
        else:
            for filename in os.listdir( get_path_away_folder() ):
                if not filename.endswith('.xml'): continue
                list_of_teams.append(filename)

        # !!zatim se ukazuje jen 10teamu
        if len(list_of_teams) > 10:
            show_teams = 10
        else :
            show_teams =  len(list_of_teams)

        if self.team_play_at == "Home":
        # domaci teamy
            for teams_loop in range (0,show_teams):
                team_name = list_of_teams[teams_loop]
                self.loaded_teams_xml[teams_loop] =  f_read_from_xml (get_path_home_folder() + team_name )
        else:
            # hoste
            for teams_loop in range (0,show_teams):
                team_name = list_of_teams[teams_loop]
                self.loaded_teams_xml[teams_loop] =  f_read_from_xml (get_path_away_folder() + team_name )

    def set_game_status_to_all(self,new_status):
        for teams_loop in range (0,5):
            self.team_players[teams_loop].game_status = new_status


    # ulozi data z treningu
    def process_data(self,player,action,run_to_save):
        reset_loop = 0

        if len(self.data_trening) < self.trening_sesion_total_runs:

            self.data_trening.append([run_to_save])
            self.data_labels.append(action)

        else:
            # manual training (supervised)
            if self.automated_trening_type != True:

                self.set_game_status_to_all("pause")

                train_model([self.data_trening], [self.data_labels], player.ID )

                self.set_game_status_to_all("game")

            self.reset_training_arrays()
            trening_type = TreningType.manual_static.value
            if self.arethreads_on[0] or self.arethreads_on[1] : TreningType.manual_dynamic.value 
            self.update_trening_player(player.ID, 1,trening_type,player)                                                      # dodelat davam vzdy jen manual-static
            #start trainkeras model

            #print(  "po",player.model  )


    def check_team_training_type(self,list_of_teams,team_index):
        for players_loop in range (1,6):
            if players_loop == 1:
                type_previouse = list_of_teams[team_index][players_loop][7]
            else:
                type = list_of_teams[team_index][players_loop][7]

                if  type_previouse == type:
                    team_training_type = type
                    type_previouse = type
                else:
                    team_training_type = TreningType.mixed.value
                    return team_training_type

        return team_training_type

    def team_trenings_summary(self,list_of_teams,team_index):
        summary = 0
        for players_loop in range (1,6):

            summary = summary + int(list_of_teams[team_index][players_loop][4])
        return summary


    def team_skills_averadge(self,list_of_teams,team_index):
        summary = 0
        for players_loop in range (1,6):

            summary = summary +  int(list_of_teams[team_index][players_loop][3])

        summary =  round  ( summary  / 5 ,  2)
        return summary


    def  update_trening_player(self,player_ID,new_time,trening_type,player):
        #print ("player_ID",self.team_play_at)
        #print ("player_ID",player_ID)
        for team_loop in range (0,10):
            for loop_pl in range (1,6):
                if self.loaded_teams_xml[team_loop] != SavingType.empty_team_slot.value and \
                   self.loaded_teams_xml[team_loop][loop_pl] != SavingType.empty_player_slot.value:
                    if self.loaded_teams_xml[team_loop][loop_pl][1] == player_ID:
                        # index 4 = trening_time
                        self.loaded_teams_xml[team_loop][loop_pl][4] = str( int( self.loaded_teams_xml[team_loop][loop_pl][4]) + new_time)
                        self.loaded_teams_xml[team_loop][loop_pl][7] = str( player.save_trening_type(trening_type))
                        create_xml_file(self.loaded_teams_xml[team_loop])


    # zmena souradnic pro hrace v prubehu treningu
    def move_players_for_new_training_run_startMatch_position (self,The_field,list_of_ingamers):

        ball_index = 0
        list_of_ingamers[ball_index].field_site = list_of_ingamers[1].field_site
        list_of_ingamers[ball_index].set_position ( The_field.field_bl_corner[0] + int(The_field.field_width/2) , The_field.field_bl_corner[1] - int(The_field.field_height/2) )
        list_of_ingamers[ball_index].set_path_target(180)

        shift_y  =  The_field.field_bl_corner[1] * 0.3
        for no_of_ingamers in range (1,6): #mic a hraci jsou posunuti na novou pozici
                list_of_ingamers[no_of_ingamers].set_position (   The_field.field_bl_corner[0] + The_field.field_width*0.2    ,   shift_y )

                list_of_ingamers[no_of_ingamers+5].set_position ( The_field.field_bl_corner[0] + The_field.field_width*0.8    ,    shift_y  )

                shift_y = shift_y + The_field.field_height * 0.1


    # zmena souradnic pro hrace v prubehu treningu
    def move_players_for_new_training_run (self,The_field,list_of_ingamers):

        vertical_max    = The_field.field_bl_corner [1]
        vertical_min    = The_field.field_bl_corner [1] - The_field.field_height
        horizontal_min  = The_field.field_bl_corner [0]
        horizontal_max  = The_field.field_bl_corner [0] + The_field.field_width
        The_field_rect_format = [horizontal_min, vertical_min, \
                                 The_field.field_width, \
                                 The_field.field_height]

        ball_index = 0
        list_of_ingamers[ball_index].speed = 0
        ball_field_ratio = calculate_trening_area_ratio (self.training_areas_ball)
        ball_field_area = calculate_trening_area_coordinates (ball_field_ratio,The_field_rect_format,"horisontal")

        # testy
        #self.testdata1 = player_field_area
        #self.testdata2 = ball_field_area

        list_of_ingamers[ball_index].field_site = list_of_ingamers[1].field_site

        list_of_ingamers[ball_index].set_position (randint( ball_field_area[0], ball_field_area[0] + ball_field_area[2]), \
                                                   randint( ball_field_area[1], ball_field_area[1] + ball_field_area[3]))


        for no_of_ingamers in range (1,len(list_of_ingamers)): #mic a hraci jsou posunuti na novou pozici
            #player
            playerid =  list_of_ingamers[no_of_ingamers].ID
            playerid =str(playerid)
            #print(  'list_of_ingamers[no_of_ingamers].player_type' ,list_of_ingamers[no_of_ingamers].player_type    )
            # GK se nehybe na novou pozici
            if (list_of_ingamers[no_of_ingamers].player_type != PlayerType.GK.value):
                player_trening_data = self.get_trening_areas_for_player(playerid)

                player_field_ratio =  calculate_trening_area_ratio(player_trening_data)
                player_field_area = calculate_trening_area_coordinates (player_field_ratio,The_field_rect_format,"horisontal")

                list_of_ingamers[no_of_ingamers].set_position (randint( player_field_area[0], player_field_area[0] + player_field_area[2]), \
                                                               randint( player_field_area[1], player_field_area[1] + player_field_area[3]))
            else:
                list_of_ingamers[no_of_ingamers].set_position (randint( horizontal_min, horizontal_min + 10 ), \
                                                               randint( int(vertical_min + The_field.field_height / 4) ,int(vertical_max  - The_field.field_height / 4)  ))



        list_of_ingamers[ball_index].field_site = "neutral"

        '''
            if list_of_ingamers[no_of_ingamers].selected_b == False and  \
                list_of_ingamers[no_of_ingamers].reinforsment == False   :

                list_of_ingamers[no_of_ingamers].set_position (randint(horizontal_min, horizontal_max), \
                                                               randint(vertical_min, vertical_max))

            else:
                list_of_ingamers[no_of_ingamers].set_position (randint( player_field_area[0], player_field_area[0] + player_field_area[2]), \
                                                               randint( player_field_area[1], player_field_area[1] + player_field_area[3]))
        '''


    def move_players_for_TEST (self,The_field,list_of_ingamers):
        vertical_max    = The_field.field_bl_corner [1]
        vertical_min    = The_field.field_bl_corner [1] - The_field.field_height
        horizontal_min  = The_field.field_bl_corner [0]
        horizontal_max  = The_field.field_bl_corner [0] + The_field.field_width
        The_field_rect_format = [horizontal_min, vertical_min, \
                                 The_field.field_width, \
                                 The_field.field_height]


        list_of_ingamers[0].set_position (horizontal_min  + 100 , int(vertical_max  - The_field.field_height / 4)  )
        list_of_ingamers[4].set_position (horizontal_min  + 150 , int(vertical_max  - The_field.field_height / 4)  )
        list_of_ingamers[2].set_position (horizontal_min  + 50 , int(vertical_max  - The_field.field_height / 4)  )
        list_of_ingamers[3].set_position (horizontal_min  + 100 , int(vertical_max  - The_field.field_height / 4) + 40 )



    # special pro trening GK
    def move_players_for_new_training_run_GK (self,The_field,list_of_ingamers,trening_type):

        vertical_max    = The_field.field_bl_corner [1]
        vertical_min    = The_field.field_bl_corner [1] - The_field.field_height
        horizontal_min  = The_field.field_bl_corner [0]
        horizontal_max  = The_field.field_bl_corner [0] + The_field.field_width
        The_field_rect_format = [horizontal_min, vertical_min, \
                                 The_field.field_width, \
                                 The_field.field_height]

        ball_index = 0

        #ball_field_ratio = calculate_trening_area_ratio (self.training_areas_ball)
        #ball_field_area = calculate_trening_area_coordinates (ball_field_ratio,The_field_rect_format,"horisontal")

        list_of_ingamers[ball_index].field_site = list_of_ingamers[1].field_site

        #list_of_ingamers[ball_index].set_position (randint( ball_field_area[0], ball_field_area[0] + ball_field_area[2]), \
        #                                           randint( ball_field_area[1], ball_field_area[1] + ball_field_area[3]))


        for no_of_ingamers in range (1,len(list_of_ingamers)): #mic a hraci jsou posunuti na novou pozici
            #player
            playerid =  list_of_ingamers[no_of_ingamers].ID
            playerid =str(playerid)
            #print(  'list_of_ingamers[no_of_ingamers].player_type' ,list_of_ingamers[no_of_ingamers].player_type    )
            # GK se nehybe na novou pozici
            if (list_of_ingamers[no_of_ingamers].player_type != PlayerType.GK.value):
                if (trening_type == 'team'):
                    player_trening_data = self.get_trening_areas_for_player(playerid)

                    player_field_ratio =  calculate_trening_area_ratio(player_trening_data)
                    player_field_area = calculate_trening_area_coordinates (player_field_ratio,The_field_rect_format,"horisontal")

                    #list_of_ingamers[no_of_ingamers].set_position (randint( player_field_area[0], player_field_area[0] + player_field_area[2]), \
                    #                                               randint( player_field_area[1], player_field_area[1] + player_field_area[3]))
                    list_of_ingamers[no_of_ingamers].set_position (randint( horizontal_min , horizontal_max), \
                                                                  randint( vertical_min, vertical_max ))


                else:
                    #hraci sou bokem
                    list_of_ingamers[no_of_ingamers].set_position (horizontal_min + 20 , vertical_min + 20 )

            else:
                #vztahuje se jen na GK trenovaneho teamu
                if (no_of_ingamers < 6):
                    list_of_ingamers[no_of_ingamers].set_position (randint( horizontal_min, horizontal_min + 10 ), \
                                                               randint( int(vertical_min + The_field.field_height / 4) ,int(vertical_max  - The_field.field_height / 4)  ))


        #ball dostane  specila move
        #list_of_ingamers[ball_index].set_position (randint( horizontal_min, horizontal_min + 200 ), randint( vertical_min , vertical_max) )
        list_of_ingamers[ball_index].set_position (    horizontal_min + int (The_field.field_width /4) ,  randint( vertical_min +20  ,  vertical_max - 20 ) )
        #print(  'set_position' ,list_of_ingamers[ball_index].rect.center   )

        list_of_ingamers[ball_index].field_site = "left"

        if (list_of_ingamers[ball_index].rect.center[1] > vertical_max  - The_field.field_height / 2):
            list_of_ingamers[ball_index].set_path_target( randint( 1 , 25  ))
        else:
            list_of_ingamers[ball_index].set_path_target( randint( 335, 359  ))
        list_of_ingamers[ball_index].speed = 200







    def set_managementcreateNo(self,index):
        if self. new_player_isREtrainingRawData == False:
            # oprava pro kratsi ckills nez puvodne 13
            print(  'in  dex' ,len(self.trainig_code)  )
            print(  'index' ,index )
            if index  >   len(self.trainig_code) - 1: # tlacitka sou od 1ku ale pole od 0
                return
            self.trainig_code[index] = not self.trainig_code[index]
        else:
            #vzdy sou dvojce pozic  krom index 0,1 to je uhel,type
            if index > 1 :
                shift = index -2
                self.trainig_code2[index + shift ] = not self.trainig_code2[index + shift]
                self.trainig_code2[index + shift + 1] = not self.trainig_code2[index + shift + 1]
            else:
                self.trainig_code2[index] = not self.trainig_code2[index]


    def get_selected_truecount_Nos(self):
        selected_trening_code = self.trainig_code
        if self.new_player_isREtrainingRawData == True:
            selected_trening_code = self.trainig_code2

        counter = 0
        for loop in range (0,len(selected_trening_code)):
            if selected_trening_code[loop] == True:
                counter = counter + 1
        return counter


    def get_selected_createNos(self):

        selected_trening_code = self.trainig_code
        if self.new_player_isREtrainingRawData == True:
            selected_trening_code = self.trainig_code2

        counter = 0
        for loop in range (0,len(selected_trening_code)):
            if selected_trening_code[loop] == True:
                counter = counter + 1
        #return counter
        return len(selected_trening_code)


    def reset_training_arrays (self):
        self.data_trening = []
        self.data_labels = []

    def Xsave_training(self):                                                                                        # pro testy, aplikace neuklada data do txt
        #time = datetime.now()
         # dd/mm/YY H:M:S
        #dt_string = time.strftime("%d-%m-%Y_%H-%M-%S")
        #file_name = 'SaveGeme_' + dt_string + '.txt'
        file_name_testing = 'training.txt'
        with open(file_name_testing, 'w') as f:
            for write_loop in range (0,len(self.data_trening[0][0])):
                f.write( str(self.data_trening[write_loop][0]))
                f.write( '\n')

        file_name_testing = 'traininglabels.txt'
        with open(file_name_testing, 'w') as f:
            for write_loop in range (0,len(self.data_labels)):
                f.write( str(self.data_labels[write_loop]))
                f.write(",")

    def save_training(self):                                                                                        # pro testy, aplikace neuklada data do txt
        file_name_testing = 'training.txt'
        #xx =[  [[0,1,2,5,4,5,6,7,8,9,1,1,11]],[[0,1,2,5,4,5,6,7,8,9,1,1,11]]  ]
        #x = [1,0]
        with open(file_name_testing, 'w') as f:
            for write_loop in range (0,len(self.data_trening)):
                for write_inner_loop in range (0,13):
                    f.write( str(self.data_trening[write_loop][0][write_inner_loop]))
                    if write_inner_loop != 12:
                        f.write( ",")
                f.write( '\n')

        file_name_testing = 'traininglabels.txt'
        with open(file_name_testing, 'w') as f:
            for write_loop in range (0,len(self.data_labels)):
                f.write( str(self.data_labels[write_loop]))
                if write_loop != (len(self.data_labels)-1):
                    f.write( ",")

    def move_around_team (self,The_field,list_of_ingamers):
        while list_of_ingamers[1].game_status ==  "game" and list_of_ingamers[6].game_status == "game" :
            for move_around_loop in range (1,len(list_of_ingamers)):
                if list_of_ingamers[move_around_loop].team_coach == self and list_of_ingamers[move_around_loop].reinforsment == False:
                    list_of_ingamers[move_around_loop].move_round_once(The_field,list_of_ingamers)
    '''
     >>>>>>>>>>>> RE TESTING    vypnute move around   <<<<<<<<<<<<<

    def move_around_team (self,The_field,list_of_ingamers):
        pass


    '''

    '''

    PRIDAT METODY PRO KONTROLU TEAMU ,na misto po jednom hraci
        - zmena   strategy ....

    '''


    def create_new_player(self):
        errorCode = ErrorCodes.OK.value
        # 0 index je cislo teamu z seznamu celkem misto 10 teamu
        # 1 index je poradi hrace v teamu                                                                                         #pridej kontrolu pro zakaz kopirovani prazdneho slotu
        index_teamu = self.selected_slot_team_management[0]
        index_hrace = self.selected_slot_team_management[1]
        index_team_settings = 0   # cely team se sklada z pole v nem je vlastnost teamu a pak 5 jednotlivich hracu
        print('index_teamu ' ,index_teamu)
        print('index_hrace' ,index_hrace)

        # slot hracu, zaporne hodnoty error stavy, nelze prepsat existujiciho hrace
        if  index_hrace < 1 :
            errorCode =  [ 'vyber musi byt hrac', 'not a player slot']
            return errorCode

        if self.loaded_teams_xml [index_teamu] != SavingType.empty_team_slot.value:
            if self.loaded_teams_xml [index_teamu][index_hrace] != SavingType.empty_player_slot.value:
                errorCode = ['slot musi byt prazdny','slot not empty']
                return errorCode

        #pokud neexistujici team vytvori novy
        if self.loaded_teams_xml [index_teamu] == SavingType.empty_team_slot.value:
            # pro prazny slot teamu se vytvori sablona , A = asci 65
            self.loaded_teams_xml [index_teamu] = [[chr(65 + index_teamu ),"updated","notselected",time.strftime("%d%m%H%M%S")]]                    #dodelat random nazev  teamu

            # vytvori se prazdny team kde se pak dolni nas vytvoreny hrac
            for loop_pl in range (1,6):
                self.loaded_teams_xml[index_teamu].append(SavingType.empty_player_slot.value)
            #print('TESTY ' , print_all_indexes_from_menu_TESTING (self.loaded_teams_xml , 0)  )
        # nastavi team na status updated => hrac neni ulozeny do xml file
        #self.loaded_teams_xml [index_teamu][0][1] = "updated"


        selected_trening_code = copy.deepcopy(self.trainig_code)
        if self.new_player_isREtrainingRawData == True:
            selected_trening_code = copy.deepcopy(self.trainig_code2)

        #
        #  player : name, ID, position, skills level, trening time, treningcode, pocet vyher ,jak trenovan
        new_player_data = create_new_random_player_data (selected_trening_code , str(self.get_selected_createNos()), self.new_player_isREtrainingRawData )

        self.loaded_teams_xml [index_teamu] [index_hrace] = new_player_data
        #print('loaded_teams_xml ' , self.loaded_teams_xml    )
        # vytvoreni modelu dle 'skills' hrace, pocet vstupu neural network
        model = create_model_tf2( self.get_selected_createNos()  )
        print('skills created player ' , self.get_selected_createNos()    )
        print('skills created player ' , self.loaded_teams_xml [index_teamu] [index_hrace] [1]    )
        # ulozeni dle hracova ID, date stampt ktery zaruci ze model se neulozi duplikovany                                                                    # nebude konstanta
        model.save( get_path_home_folder() + self.loaded_teams_xml [index_teamu] [index_hrace] [1]  + ".h5")

        self.selected_slot_team_management = [-1,-1] # reset bufferu

        return errorCode


    ## 3 metody pro team managemet hraci jdou mazat a kopirovat
    # smazat hrace v team management
    def delete_player_from_slot(self):
        team_index = self.selected_slot_team_management[0]
        player_index = self.selected_slot_team_management[1]
        # kontrola  slot neni prazdny a je pro hrace
        if player_index > 0:
            # team slot neni prazdny len("none") = 4
            if self.loaded_teams_xml[team_index] != SavingType.empty_team_slot.value : # slot ma ulozeny team
                self.loaded_teams_xml [team_index][player_index] = SavingType.empty_player_slot.value                                                           #pridej team neni original
                # nastavi team na status updated => hodnoty nactene ve hre se lisi od hodnot ulozenych v xml souboru
                self.loaded_teams_xml [team_index][0][1] = "updated"
                self.loaded_teams_xml [team_index][0][2] = "unselected"


    def copy_player_from_slot(self):
        errorCode = ErrorCodes.OK.value
        team_slot = self.selected_slot_team_management[0]
        player_slot = self.selected_slot_team_management[1]

        if player_slot == 0 : #nelze oznacit team
            errorCode = ['spatny vyber', 'wrong slot']
            return errorCode

        if self.loaded_teams_xml [team_slot] != SavingType.empty_team_slot.value and \
            self.loaded_teams_xml [team_slot][player_slot] != SavingType.empty_player_slot.value:

            position_copy = copy.deepcopy(self.selected_slot_team_management)
            self.selected_slot_team_management_buffer =  copy.deepcopy(position_copy)
            errorCode = ErrorCodes.plselectedfromslot.value
        else:
            errorCode =  ['spatny vyber', 'empty slot']

        return errorCode


    def is_sequence_correct(self):
        check = False
        if self.selected_slot_team_management_buffer[0] <  self.selected_slot_team_management[0]:
            check = True
            print (  'buff norml'   , self.selected_slot_team_management_buffer[0]    ,    self.selected_slot_team_management[0]     )
            return check



    def paste_player_from_other_slot(self):
        # slot jsou souradnice
        # 0 index je cislo teamu z seznamu celkem misto 10 teamu
        # 1 index je poradi hrace v teamu                                                                                         #pridej kontrolu pro zakaz kopirovani prazdneho slotu
        from_slot = self.selected_slot_team_management_buffer
        to_slot   = self.selected_slot_team_management

        # slot hracu, zaporne hodnoty error stavy  , nelze kopirovat prazdny slot
        if to_slot[1] >0 and from_slot[1] >0 and \
            self.loaded_teams_xml [from_slot[0]] != SavingType.empty_team_slot.value and \
            self.loaded_teams_xml [from_slot[0]][from_slot[1]] != SavingType.empty_player_slot.value :

            if self.loaded_teams_xml [to_slot[0]] == SavingType.empty_team_slot.value:  # 4 = len(none)
                # pro prazny slot teamu se vytvori sablona
                # A = asci 65
                self.loaded_teams_xml [to_slot[0]] = [[chr(65 + to_slot[0] ),"updated","notselected"]]                    #dodelat random nazev  teamu

                for loop_pl in range (1,6):
                    self.loaded_teams_xml[to_slot[0]].append(SavingType.empty_player_slot.value)


            # nastavi team na status updated => hodnoty nactene ve hre se lisi od hodnot ulozenych v xml souboru
            self.loaded_teams_xml [to_slot[0]][0][1] = "updated"

            self.loaded_teams_xml [to_slot[0]] [to_slot[1]] = copy.deepcopy(self.loaded_teams_xml [from_slot[0]] [from_slot[1]])

            # player id dle datetime stamp
            self.loaded_teams_xml [to_slot[0]] [to_slot[1]] [1] = time.strftime("%d%m%H%M%S")
            self.loaded_teams_xml [to_slot[0]] [to_slot[1]] [0] = players_names (randint( 0,94 ))


            # vytvoreni modelu dle 'skills' hrace, pocet vstupu neural network
            # model = create_model(   self.loaded_teams_xml [to_slot[0]] [to_slot[1]][3]   )
            model = create_model_tf2(  int( self.loaded_teams_xml [to_slot[0]] [to_slot[1]][3] )  )
            print('skills created player ' , self.loaded_teams_xml [to_slot[0]] [to_slot[1]][3]    )
            # ulozeni dle hracova ID, date stampt ktery zaruci ze model se neulozi duplikovany                                                                    # nebude konstanta
            model.save( get_path_home_folder() + self.loaded_teams_xml [to_slot[0]] [to_slot[1]] [1]  + ".h5")

        self.selected_slot_team_management_buffer = [-1,-1] # reset bufferu
        self.selected_slot_team_management = [-1,-1] # reset bufferu

    def can_edit_player(self):
        player_selected = False
        team_index = self.selected_slot_team_management[0]
        player_index = self.selected_slot_team_management[1]
        if  player_index > 0 and self.loaded_teams_xml[team_index] != SavingType.empty_team_slot.value : # slot ma ulozeny team, je vybran hrac
            if self.loaded_teams_xml [team_index][player_index] != SavingType.empty_player_slot.value : # slot hrace neni prazdny
                player_selected = True
        return player_selected                                  # rename player selected no sence

    def edit_player_position(self,new_position):
        team_index = self.selected_slot_team_management[0]
        player_index = self.selected_slot_team_management[1]
        if self.can_edit_player() == True :
            self.loaded_teams_xml [team_index][0][1] = "updated"
            self.loaded_teams_xml [team_index][player_index][2] = str(new_position)


    def reset_selected_slot_team_management(self):
        self.selected_slot_team_management = [-1,-1]
        self.selected_slot_team_management_buffer = [-1,-1]

    # ulozi team do xml
    def save_team_from_teammngmt_table(self):
        team_index = self.selected_slot_team_management[0]
        player_index = self.selected_slot_team_management[1] # index 0 je team pak 5x hrac
        checked_team = self.loaded_teams_xml[team_index]
        errorCode = ErrorCodes.OK.value

        #pokud prazdny slot metoda nic nevykona ,#oznacen je team ne hrac
        if checked_team == SavingType.empty_team_slot.value or player_index != 0:
            errorCode = ErrorCodes.cantSaveTeam.value
            return errorCode

        for check_team_loop in range (1,5):
            if checked_team [check_team_loop] == SavingType.empty_player_slot.value:                                       # 4 = len(none)   opakovani kodu zlepsit
                errorCode = ErrorCodes.cantSaveTeam.value
                return errorCode

        #netreba ukladat neni zmenen
        if self.loaded_teams_xml[team_index][0][1] == "original":
            errorCode = ['netreba ukladat' , 'no need save']
            return errorCode

        # potvrdi ulozeni teamu
        self.loaded_teams_xml[team_index][0][1] = "original"
        create_xml_file(  checked_team)
        #nastaveni pro novy team a naceni
        self.training_areas_players = []  #reset
        self.load_trening_areas()

        return errorCode


    # vypocita slot z team management tabulky z souradnic mysi
    def calculate_slot_index(self,position_clicked,The_game_window):

        # hodnoty musi by ulozeny v 'window' aby slo vypocitat polohu mysi => spustit metodu/funkci
        lines = The_game_window.team_detail_lines
        column_width = The_game_window.mngmt_column_width
        teams_on_page = The_game_window.mngmt_teams_on_page
        text_ratio = The_game_window.mngmt_text_ratio
        shift_from_menu = The_game_window.mngmt_shift_from_menu

        # hranice tabulky teamu
        table_top = The_game_window.heading_shift
        table_left = shift_from_menu + The_game_window.game_menu_x_end
        table_bottom = table_top + text_ratio * lines * The_game_window.menu_line_spacing
        table_right = table_left + teams_on_page * column_width

        if position_clicked[0] > table_left and position_clicked[0] < table_right:
            if position_clicked[1] > table_top and position_clicked[1] < table_bottom:
                self.selected_slot_team_management[0] =  int( (position_clicked[0] - table_left ) // column_width )
                self.selected_slot_team_management[1] =  int ( (position_clicked[1] - table_top ) // (text_ratio * The_game_window.menu_line_spacing ) )
                self.training_areas_players_updated = True
    '''
    # nacte teamy z slozky z predchozich her
    def save_H_team_available_to_list (self,new_teams):
        self.H_teams_available_list = new_teams
                                                                                                #metody smazat nepouzite
    def save_A_team_available_to_list (self,new_teams):
        self.A_teams_available_list = new_teams
    '''

    # zmeni team na selected ,pro vyber teamu pro hru
    def choose_team_from_selection(self):
        team = self.selected_slot_team_management[0]

        # dvakrat vybrany team
        if self.loaded_teams_xml[team] != SavingType.empty_team_slot.value:
            #team neni vybran
            if self.loaded_teams_xml[team][0][2] == "notselected" and self.loaded_teams_xml[team][0][1] == "original":
                self.loaded_teams_xml[team][0][2] = "selected"
            else:
                self.loaded_teams_xml[team][0][2] = "notselected"


    #NEPOUZIVASE
    def define_NN_data_for_player(self,The_field,list_of_ingamers):
        The_ball = list_of_ingamers[0]


                            ##                                                                    ##
                                ##                                                            ##
                # # # # # #         ##      potreba elegantnejsi a rychlejsi reseni       ##          # # # # # # # #
                                ##                                                            ##
                            ##                                                                    ##


        '''                                                                         #!!!! 2x v player +1 v kodu opravit!!!!   classes 165 radky
        Inputs:
              Hrac
            xhrace[0] - angle to own goal   /kam se diva/
            yhrace[1] - angle to ball
            xmice[2] - distance to ball
            ymice[3] - player type (GK,striker,defender,etc)
                self.path_target[4] - qvadrant (zatim zakladni 3 & 3) 9 moznosti 12.12 prvni v prostred v nem prvni v prostred
            [4] - MISTOKVADRANTU ROVNOU SOURADNICE x - y  napr 5   x=20 - y =15    deleno1000 aby byly menci cisla
             Team
            [5] - je z teamu nejblize mici   1 je 0 neni
            [6] - tactic
            [7] - strategy
            [8] - message
            [9] - team je u balonu ball
            [10] - je v view nejaky hrac ?nastav vzdalenost?
             Hra
            [11] - game status
            [12] - game type
        Outputs:
             - otoc +22 stupnu  (kod 0)
             - otoc -22 stupnu  (kod 1)
             - krok             (kod 2)
             - kop do mice      (kod 3)
             - bez akce         (kod 4)

        '''
        inputs = [self.rect.center[0]/1000, \
            self.rect.center[1]/100, \
            The_ball.rect.center[0]/1000, \
            The_ball.rect.center[1]/100, \
            self.path_target/100 ]

        for inputs_loop in range (0,len(inputs)):
            if self.skills_set[inputs_loop] == False:
                inputs[inputs_loop] = 0

        return inputs
