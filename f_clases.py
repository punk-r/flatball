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

'''
Tridy :

        game_window - okno hry , surafec pro kresleni grafiky
        game_field  - hodnoty pro vykreslenu hraciho hriste
        class_coach - trener, vyhodnocuje trening, urcuje strategii hry
        reff        - rozhotci, potvrzuje hrace do hry ,kterou pote kontroluje

'''

#--------------------------------------------------------------------------------------------class game_window
# trida pro okno aplikace
class game_window():
    window_width = 1280
    window_height = 720
    surface = pygame.display.set_mode((window_width,window_height), pygame.RESIZABLE)
    screen_size_type = "none"                                                                            # uzite?
    items_on_surface = 0                                                                                 #   MOZNA NEBUDE POUZITE???
    game_menu_x_start = 5                       # hranice pro hlavni menu
    game_menu_x_end = int (window_width / 6)
    game_menu_y_end = int (window_height * 4/ 5 )
    menu_line_spacing = int( window_height / 34.2 )   # nastaveni pro hlavni menu
    heading_shift = 2 * menu_line_spacing
    menu_on_screen = False
    language = "CZ"
    #lab_mode_b = 0
    # nastavni okna, tabulky, team manegmentu, vyberu hracudo hry
    team_detail_lines = 6                       # 1 x nazev + 5 hracu teamu
    mngmt_column_width = int(0.48 *  game_menu_x_end  )                                                           #udelat pomerem z ruznych velikosti okna
    mngmt_teams_on_page = 10
    mngmt_text_ratio = 3                        # zvetseni pisma ku menu fontu
    selection_game_text_ratio = 2               # zvetseni pisma ku menu fontu
    mngmt_shift_from_menu = int( 1.1 *  menu_line_spacing)
    buttons = []
    number_buttons_main_menu = 13  # o jeden min zacina od 0
    isrender_REtraining = True


    def draw_all_ingamers(self,list_of_ingamers):
        for no_of_ingamers in range (0,len(list_of_ingamers)):
            list_of_ingamers[no_of_ingamers].draw_ingamer(self)


    def resize_values(self):                                                                                 # je metoda treba????????????????????
        self.game_menu_x_end = int (self.window_width / 6)
        self.game_menu_y_end = int (self.window_height * 4/ 5)
        self.menu_line_spacing = int(self.window_height / 34.2)
        self.heading_shift = 2 *self.menu_line_spacing
        self.mngmt_column_width = int(0.48 *  self.game_menu_x_end  )
        self.mngmt_shift_from_menu = int( 1.1 * self.menu_line_spacing)

    def swap_language(self):
        if self.language == "CZ" :
            self.language = "NOTCZ"
        else:
            self.language = "CZ"

    def set_window_size(self,new_size,The_field):

        self.window_width = new_size[0]
        self.window_height = new_size[1]
        self.surface = pygame.display.set_mode((self.window_width,self.window_height),pygame.RESIZABLE)
        The_field.set_field(self)
    '''
    def draw_text(self, font , text, size, color, x, y ):
            font = pygame.font.Font(self.font_name,size)
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.center = (x,y)
            .display.blit(text_surface,text_rect)
    '''

#--------------------------------------------------------------------------------------------class game_field
# trida pro hraci pole
class game_field():
    type ="notSpecified"       # pro ruzna vykreslovani hriste,zatim NEVYUZITO
    goals_height = 100         # velikosti branek
    goals_width = 10            # velikosti branek
    #field_bl_window = [0,0]    # ram pro hraci hriste,hotnoty sou nastaveny pri set field
    #lab_mode_b = 1             # zobrazeni pomocnych vypoctu
    field_width = 0            # hotnoty sou nastaveny pri set field
    field_height = 0           # hotnoty sou nastaveny pri set field
    field_bl_corner = [0,0]    # hranice hracih o hriste,hotnoty sou nastaveny pri set field
    gap = 15
    longest_distance = 0

    # nastaveni dle hodnot aplikace
    def set_field (self,game_window):
        field_gap_to_window = 20
        #self.field_bl_window[0] = int ( 1/6 * game_window.window_width  )
        #self.field_bl_window[1] = int ( 4/5 * game_window.window_height  )

        #self.field_bl_corner[0] = int ( 1/6 * game_window.window_width + self.gap )
        self.field_bl_corner[0] = int (field_gap_to_window)
        self.field_bl_corner[1] = int ( 4/5 * game_window.window_height - self.gap/2 )

        self.field_width = int ( 0.95 * game_window.window_width )
        self.field_height = int ( 0.7 * game_window.window_height )
        self.goals_height = 0.2 * self.field_height
        self.longest_distance = int( pythagoras_distance (self.field_bl_corner,  \
                                                      (self.field_bl_corner[0]+ self.field_width, self.field_bl_corner[1] - self.field_height  )))

'''
# nacte teamy z xml
The_reff.load_data_from_xml()

'''

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
    trening_sesion_total_runs = 5000    # 5000  celkovy pocet uceni pro spusteny trening
    RE_trening_sesion_runs = 4000
    trening_repetition_sequence = 0
    trening_repetition_total = 10
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

        # po dosazeni max runs se data vyhodnoti
        if len(self.data_trening) < self.trening_sesion_total_runs:

            self.data_trening.append([run_to_save])
            # labels
            self.data_labels.append(action)

        else:
            # manual training (supervised)
            if self.automated_trening_type != True:

                self.set_game_status_to_all("pause")

                #print ("The self.data_trening eight",self.data_trening)
                #print ("The self.data_labelsht",self.data_labels)

                train_model([self.data_trening], [self.data_labels], player.ID )
                #train_model_tensorflowboard([self.data_trening], [self.data_labels], player.ID )
                #print ("The self.data_trening eight",self.data_trening)
                #self.save_training()   #testy

                '''
                player.save_trening_time (self.RE_trening_sesion_runs)
                for save_loop  in range (0,len(self.loaded_teams_xml)):
                    if self.loaded_teams_xml[save_loop][0][1] == "original":
                        create_xml_file ( self.loaded_teams_xml[save_loop] )
                '''

                self.set_game_status_to_all("game")

            else:
                self.set_game_status_to_all("pause")
                proces_reinforsment_data(player.ID,self.data_trening,self.data_labels)
                processed_training = self.data_trening
                processed_labels =self.data_labels
                #train_model(processed_training, processed_labels, processed_training, processed_labels, player.ID)

            self.reset_training_arrays()
            self.update_trening_player(player.ID, 1,TreningType.manual_static.value,player)                                                      # dodelat davam vzdy jen manual-static
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

                    list_of_ingamers[no_of_ingamers].set_position (randint( player_field_area[0], player_field_area[0] + player_field_area[2]), \
                                                                   randint( player_field_area[1], player_field_area[1] + player_field_area[3]))
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
        list_of_ingamers[ball_index].set_position ( horizontal_min + int (The_field.field_width / 3) ,  vertical_max - The_field.field_height /2  )
        print(  'set_position' ,list_of_ingamers[ball_index].rect.center   )
        if (list_of_ingamers[ball_index].rect.center[1] < vertical_max  - The_field.field_height / 2):
            list_of_ingamers[ball_index].set_path_target( randint( 0 , 10  ))
        else:
            list_of_ingamers[ball_index].set_path_target( randint( 350 , 360  ))
        list_of_ingamers[ball_index].speed = 200




        list_of_ingamers[ball_index].field_site = "neutral"


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



    def get_selected_createNos(self):

        selected_trening_code = self.trainig_code
        if self.new_player_isREtrainingRawData == True:
            selected_trening_code = self.trainig_code2

        counter = 0
        for loop in range (0,len(selected_trening_code)):
            if selected_trening_code[loop] == True:
                counter = counter + 1

        return counter

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
            errorCode = 'not a player slot'
            return errorCode

        if self.loaded_teams_xml [index_teamu] != SavingType.empty_team_slot.value:
            if self.loaded_teams_xml [index_teamu][index_hrace] != SavingType.empty_player_slot.value:
                errorCode = 'slot not empty'
                return errorCode

        #pokud neexistujici team vytvori novy
        if self.loaded_teams_xml [index_teamu] == SavingType.empty_team_slot.value:
            # pro prazny slot teamu se vytvori sablona , A = asci 65
            self.loaded_teams_xml [index_teamu] = [[chr(65 + index_teamu ),"updated","notselected"]]                    #dodelat random nazev  teamu

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
        #print('skills created player ' , self.loaded_teams_xml [index_teamu] [index_hrace][3]    )
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
            errorCode = 'wrong slot'
            return errorCode

        if self.loaded_teams_xml [team_slot] != SavingType.empty_team_slot.value and \
            self.loaded_teams_xml [team_slot][player_slot] != SavingType.empty_player_slot.value:

            position_copy = copy.deepcopy(self.selected_slot_team_management)
            self.selected_slot_team_management_buffer =  copy.deepcopy(position_copy)
        else:
            errorCode = 'empty slot'

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
            errorCode = 'no need save'
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











#--------------------------------------------------------------------------------------------class reff
# trida rozhodciho
class reff ():
    def __init__(self):
            self.coach_team_A = class_coach("Home")                # rozhodci ma prehled o cele hre i o trenerech
            self.coach_team_B = class_coach("Away")

    position = [0,0]
    coach_types_check = ["Home","Home"]
    teams_for_game  = [" "," ","H","H"]        # oznacene 2 teamy pro hru a jejich nastaveni
    radius = 15                                 # velikost
    #lab_mode_b = 1                              # laboratory mode, odemkne nektera nastaveni
    game_type = "none"                          # typ hry: pause/match/none
    selected_b = False                          # ukazatel zda je ingamer oznaceny                      zkontroluj ,mely by byt uz z ingamer tridy!!
    score  = [0,0]                              # pocitadlo golu
    time  = 0                                   # odpocet casu
    color_check  = 0                            # hodnoty pro nastaveni hry zatim epouzito
    set_color  = 0
    was_clicked  = 0                            # reff byl oznacen pri hre
    #stop_game  = 0                                                                                            # ? uzito ??
    #pause_game   = 0                           # puse pro zapocatou hru
    team_type = "neutral"                       # ???  zkontroluj
    H_teams_available_list = []                 # home teams   ASI NENI treba pouzit list vsech teamu co sou k dispozici (loaded_teams_xml)
    A_teams_available_list = []                 # away teams  ASI NENI TREBA
    list_of_ingamers = [ ball([10,10]),0,0,0,0,0,0,0,0,0,0 ]    # ball+ players


    def load_teams_for_game_to_slot(self):
        save_index = 0
        all_teams = self.coach_team_A.loaded_teams_xml + self.coach_team_B.loaded_teams_xml
        for team_no in range (0,len(all_teams)):
            if all_teams[team_no] != SavingType.empty_team_slot.value:
                if all_teams[team_no][0][2] == "selected":
                    if save_index == 0:
                        self.teams_for_game[0] = all_teams[team_no]
                        save_index = 1
                    else:
                        self.teams_for_game[1] = all_teams[team_no]
                        break


        #print('load_teams_for_game_to_slot' ,  print_all_indexes_from_menu_TESTING( self.teams_for_game ,1))


        '''
        print(self.teams_for_game[0])
        print(self.teams_for_game[1])
        print(self.teams_for_game[2])
        print(self.teams_for_game[3])
        '''

    def set_teams_type_for_game(self,type):
        self.teams_for_game[2] = "AI"
        self.teams_for_game[3] = "AI"

        if type == "H/AI":
            self.teams_for_game[2] ="H"
        elif type == "AI/H":
            self.teams_for_game[3] ="H"
        elif type == "H/H":                    # pouze pro manualni staticky trening
            self.teams_for_game[2] = "H"
            self.teams_for_game[3] = "H"

    def reset_teams_buffer_for_game(self):
        self.teams_for_game  = [" "," ","H","H"]
        #print_all_indexes_from_menu_TESTING(  self.coach_team_A.loaded_teams_xml  , 1)
        for teams_reset_loop  in range (0,len(self.coach_team_A.loaded_teams_xml )):
            if self.coach_team_A.loaded_teams_xml [teams_reset_loop] != SavingType.empty_team_slot.value:
                if self.coach_team_A.loaded_teams_xml[teams_reset_loop][0][2] == "selected" :
                    self.coach_team_A.loaded_teams_xml[teams_reset_loop][0][2] = "notselected"
        for teams_reset_loop  in range (0,len(self.coach_team_B.loaded_teams_xml )):
            if self.coach_team_B.loaded_teams_xml [teams_reset_loop] != SavingType.empty_team_slot.value:
                if self.coach_team_B.loaded_teams_xml[teams_reset_loop][0][2] == "selected" :
                    self.coach_team_B.loaded_teams_xml[teams_reset_loop][0][2] = "notselected"


    # povrzeni teamu do treningu
    def start_training(self):                                                                                               # POJMENOVANI SPATNE ma byt check trening , start trening mate s start game
        # trening lze zacit pokud jso oznaceny sloty s existujicimi teamy
        # teamy maji status original->zkontrolovany
        # vybran team a hrac (hracuv team je automaticky vybran jako (!) PRVNI (!) pro trening)
        # prvni index je team , druhy je hrac
        # priklad  index_team_a =[0,0]  je oznacen team 0 ,  [1,2]  znamena team na indexu 1 a jeho hrac na indexu 2
        druhy_team_index = self.coach_team_A.selected_slot_team_management
        trenovany_team_index = self.coach_team_A.selected_slot_team_management_buffer  #buffer je A team !!
        print( 'trenovany_team_index   druhy_team_index   ',trenovany_team_index ,druhy_team_index)

        player_selected_ID = "none"
        start_training_check = False

        # nelze trenovat se sebou
        if trenovany_team_index == druhy_team_index :
            return [start_training_check,player_selected_ID  ]

        if druhy_team_index[0]  == -1  or  trenovany_team_index[0] == -1 :
            return [start_training_check,player_selected_ID  ]

        if  self.coach_team_A.loaded_teams_xml[druhy_team_index[0]] == SavingType.empty_team_slot.value or \
                self.coach_team_A.loaded_teams_xml[trenovany_team_index[0]] == SavingType.empty_team_slot.value  :
            return [start_training_check,player_selected_ID  ]


        #print(self.teams_for_game )
        if  self.coach_team_A.loaded_teams_xml[druhy_team_index[0]][0][1] == "original" and \
                self.coach_team_A.loaded_teams_xml[trenovany_team_index[0]][0][1] == "original"  :                               #zkontroluj podmnku

                player_selected_ID = self.coach_team_A.loaded_teams_xml[trenovany_team_index[0]][trenovany_team_index[1]][1]

                self.coach_team_A.loaded_teams_xml[druhy_team_index[0]][0][2] = "selected"
                self.coach_team_A.loaded_teams_xml[trenovany_team_index[0]][0][2] = "selected"

                self.teams_for_game[0] = self.coach_team_A.loaded_teams_xml[trenovany_team_index[0]]
                self.teams_for_game[1] = self.coach_team_A.loaded_teams_xml[druhy_team_index[0]]

                self.set_game_status_to_self("none")
                start_training_check = True
                self.coach_types_check = ["Home","Home"]

        print( 'self.teams_   for_game  1      2hy ',self.teams_for_game[0][0] , self.teams_for_game[1][0] )
        return [start_training_check,player_selected_ID  ]

    # spocte vsechny selected teams
    def count_selected_teams(self):
        master_list = self.coach_team_A.loaded_teams_xml + self.coach_team_B.loaded_teams_xml
        teams_selected = 0

        # kontrola ze 2 teamy jsou oznaceny
        for check_loop in range (0,len(master_list)):
            # team slot neni prazdny len("none") = 4
            if master_list[check_loop] != SavingType.empty_team_slot.value :
                if master_list[check_loop][0][2] == "selected":
                    teams_selected = teams_selected + 1
                    if teams_selected ==0 and check_loop > 9 :
                        self.coach_types_check[0] = "Away"
                    if teams_selected ==1 and check_loop > 9 :
                        self.coach_types_check[1] = "Away"

        return  teams_selected

    # zkontroluje zda jsou oznaceny pouze dva teamy
    def check_selected_teams(self):
        teams_selected = self.count_selected_teams()

        # ulozi 2x jmeno vybranych teamu
        if  teams_selected == 2 or teams_selected == 1:
            self.teams_for_game[0] = " "
            self.teams_for_game[1] = " "
            saving_index = 0
            for save_loop in range (0,len(self.loaded_teams_xml)):
                if self.loaded_teams_xml[save_loop] != SavingType.empty_team_slot.value:
                    if self.loaded_teams_xml[save_loop][0][2] == "selected":
                        self.teams_for_game[saving_index] = self.loaded_teams_xml[save_loop][0][0]
                        saving_index = saving_index + 1

        elif teams_selected > 2:
            self.teams_for_game[0] = "2!"
            self.teams_for_game[1] = "1!"

        elif  teams_selected == 0:
            self.teams_for_game[0] = " "
            self.teams_for_game[1] = " "


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
            print ('ball',The_ball.rect.center)
            print("game_fieldwth"  ,The_field.field_width )
            print("game_fieldhght"  ,The_field.field_height )

        # kontrola pozice mice ku branam
        if The_ball.rect.center[1] - The_ball.radius < goal_bottom  and The_ball.rect.center[1]  + The_ball.radius > goal_top:

            # rozdil 1 - mic se zastavi pixel pred carou
            if The_ball.rect.center[0] - The_ball.radius - 1  <= field_left  :
                self.score [1] = self.score [1]  + 1
                #self.game_reset (The_field,The_ball)
                return True

            if The_ball.rect.center[0] + The_ball.radius + 1  >= field_right :
                self.score [0] = self.score [0]  + 1
                #self.game_reset (The_field,The_ball)
                return True

        return False


    # resetovani mice
    def game_reset (self,game_field,The_ball):
        The_ball.speed = 0
        The_ball.color = WHITE
        The_ball.set_position    (randint( 400,800 ), randint(100 ,500 ) )


    def draw_ingamer (self,game_window):                                                                      #zmen na draw ref??
        if self.selected_b == True:
            color = YELLOW_SELECTED_ITEMS
        else :
            color = WHITE

        # Rozhodci se vykresluje jako bilo-cerny kruh
        # pomocny vypocet
        rectangle_for_drawing = [ self.position[0] - self.radius , self.position[1] - self.radius ,2 * self.radius , 2* self.radius ]
        # arc(surface, color, rect, start_angle, stop_anglenline)
        pygame.draw.arc(game_window.surface, color, rectangle_for_drawing, radians (90) ,  radians (180), self.radius)
        pygame.draw.arc(game_window.surface, color, rectangle_for_drawing, radians (270) ,  radians (360), self.radius)
        pygame.draw.circle(game_window.surface, color, ( self.position[0] ,self.position[1]) ,self.radius, 1)


    def set_selected (self,new_status):                                                                              #reff potomek ingamer??? opakuje se dost metod pri reff jako nezdedena trida
        # hrac muze byt oznaceny pouze pokud je v team_type "human"
        if new_status == True :
            if self.team_type != "AI":
                self.selected_b = True
        else:
            self.selected_b = False

    # jestli je item oznacen mysi nastavi se na selected , dle podminek set_selected
    def is_selected_by_click (self,position_clicked):
        x_limits = [  self.position[0] - self.radius   ,  self.position[0] + self.radius    ]
        y_limits = [  self.position[1] - self.radius   ,  self.position[1] + self.radius    ]

        if is_clikced_on_circle(x_limits,y_limits,position_clicked) == True:
            return True
        else:
            return False


    def read_selected (self):
        return self.selected_b


    def start_match (self,The_field,called_at_begining, is_sequence_correct):                           # potreba?called_at_begining ?
        thread_team_A = self.coach_team_A.arethreads_on[0]
        thread_team_B = self.coach_team_A.arethreads_on[1]
        ball_index = 0
        self.score  = [0,0] #reset z pedesle hry

        # nelze spustit vice her
        if self.game_type != "none" :
            return

        self.game_type = "game"

        # pro trening
        vertical_max    = The_field.field_bl_corner [1]
        vertical_min    = The_field.field_bl_corner [1] - The_field.field_height
        horizontal_min  = The_field.field_bl_corner [0]
        horizontal_max  = The_field.field_bl_corner [0] + The_field.field_width
        #team_A_slot = self.teams_for_game [0] # ulozi jmeno teamu
        #team_B_slot = self.teams_for_game [1] # ulozi jmeno teamu

        # set pro hru nastaveni pozice rozhotciho  a mice pro zacatek hry
        self.position = [  int( horizontal_max / 2 + self.radius ) , int(vertical_min  - self.radius )  ]
        self.list_of_ingamers[ball_index].radius = 7
        self.list_of_ingamers[ball_index].rect.center = [int( horizontal_max / 2 + self.radius ), int(vertical_max / 2)   ]
        self.list_of_ingamers[ball_index].set_path_target(180)

        self.load_teams_for_game_to_slot()

        if is_sequence_correct:
            all_teams = [self.teams_for_game[0] , self.teams_for_game[1]]
        else:
            all_teams = [self.teams_for_game[1] , self.teams_for_game[0]]

        print(" start match -all_teams" )
        print(" start match -all_teams" ,  print_all_indexes_from_menu_TESTING(all_teams,1)   )
        print(" start match -all_teams" )
                                                                                                            # pridat kontrolu teamu,
        # input ma tvar : [team_name,5x [pl_name, pl_ID,pl_position,trening_type,trening_time]]
        shift_x = The_field.field_bl_corner[0] + The_field.field_width*0.2

        ingamer_saving_loop = 1 # 2 protoze index 0 je eff index 1 je ball
        for teams_lops in range (0,2):    # vybere 'selected' teamy z listu vsech teamu

            if True : # puvodni kontrola neni treba , start_match se vola uz s kontrolovanyma hodnotama

                shift_y = The_field.field_bl_corner[1] * 0.3
                for players_loop in range (1,6):   # index 0 je nazev teamu
                    # vypsani teamu a hracu,prvni column je pro popisky
                    #print("team/players_loop" , teams_lops," "    ,players_loop)
                    #print(       "numbr"    , int( all_teams[teams_lops][players_loop][3]) )
                    if self.coach_types_check[teams_lops] == 'Home' :
                        full_path = get_path_home_folder()
                    else:
                        full_path = get_path_away_folder()

                    new_player_ID = all_teams[teams_lops][players_loop][1]
                    new_player = player ([int(shift_x),int(shift_y)])
                    new_player.path_target = 180
                    new_player.game_status = "game"
                    new_player.set_path_target(180)
                    new_player.ID = new_player_ID
                    new_player.name = all_teams[teams_lops][players_loop][0]
                    new_player.player_type = float(all_teams[teams_lops][players_loop][2])
                    new_player.skills_level = int(all_teams[teams_lops][players_loop][3])
                    new_player.trening_time = all_teams[teams_lops][players_loop][4]
                    new_player.skills_set =   all_teams[teams_lops][players_loop][5]
                    new_player.trening_type_player =   all_teams[teams_lops][players_loop][6]
                    new_player.model_needs_reload = True
                    new_player.path_folders = full_path
                    new_player.isREtrainingRawData = all_teams[teams_lops][players_loop][8]
                    #print (new_player.skills_set)

                    # nastaveni v zavislosti na teamu
                    if teams_lops == 0:
                        new_player.team_type = self.teams_for_game[2]
                        new_player.team = all_teams[teams_lops][0][0]
                        new_player.field_site = "left"
                        new_player.set_coach(self.coach_team_A)
                        new_player.set_graphic("player_a.png")
                        self.coach_team_A.team_players[players_loop -1] = new_player
                    else:
                        new_player.team_type = self.teams_for_game[3]
                        new_player.team = all_teams[teams_lops][0][0]
                        new_player.color = RED
                        new_player.field_site = "right"
                        new_player.set_coach(self.coach_team_B)
                        new_player.set_graphic("player_b.png")
                        self.coach_team_B.team_players[players_loop -1] = new_player

                    print(  ' new_player.ID  ', new_player.ID  ,   '  new_player.field_site '  ,   new_player.field_site     )

                    new_player.model= load_model( full_path +  new_player_ID + ".h5")   # zmenin na file dle ID hrace

                    if new_player.skills_level == 4:
                        pass
                        #print(new_player.model.summary())
                    '''
                    x = 1 #pro testy
                    if x == 1:
                        thread_new_player =  Thread (target = new_player.move_round   ,args =  (The_game_window,The_field,list_of_ingamers))
                        thread_new_player.start()
                    '''
                    shift_y = shift_y + The_field.field_height * 0.1

                    self.list_of_ingamers[ingamer_saving_loop] = new_player
                    ingamer_saving_loop = ingamer_saving_loop + 1


                shift_x = The_field.field_bl_corner[0] + The_field.field_width*0.8

        #reset na dalsi hru
        self.reset_teams_buffer_for_game()

        if thread_team_A:
            thread_A_team =  Thread (target = self.coach_team_A.move_around_team   ,args =  (The_field,self.list_of_ingamers))
            thread_A_team.start()

        if thread_team_B:
            thread_B_team =  Thread (target = self.coach_team_B.move_around_team   ,args =  (The_field,self.list_of_ingamers))
            thread_B_team.start()

        if True:#a player
            player11 =  Thread (target = self.list_of_ingamers[1].move_round   ,args =  (The_field,self.list_of_ingamers))
            player11.start()
        if True:#a player
            player11 =  Thread (target = self.list_of_ingamers[6].move_round   ,args =  (The_field,self.list_of_ingamers))
            player11.start()

    '''    # vygenerovani zapasu / treningu
    def start_matchx (self,The_field,called_at_begining,teams_threds):                           # potreba?called_at_begining ?
        if self.game_type != "none" :
            return

        thread_team_A = teams_threds[0]
        thread_team_B = teams_threds[1]
        team_A_type = self.teams_for_game[2]
        team_B_type = self.teams_for_game[3]
        ball_index = 0

        # pro trening
        vertical_max    = The_field.field_bl_corner [1]
        vertical_min    = The_field.field_bl_corner [1] - The_field.field_height
        horizontal_min  = The_field.field_bl_corner [0]
        horizontal_max  = The_field.field_bl_corner [0] + The_field.field_width


        # set pro hru nastaveni pozice rozhotciho  a mice pro zacatek hry
        self.position = [  int( horizontal_max / 2 + self.radius ) , int(vertical_min  - self.radius )  ]
        self.list_of_ingamers[ball_index].radius = 7
        self.list_of_ingamers[ball_index].rect.center = [int( horizontal_max / 2 + self.radius ), int(vertical_max / 2)   ]
        self.list_of_ingamers[ball_index].set_path_target(180)
        start_game_coordinates = [int( horizontal_max / 2 + self.radius ), int(vertical_max / 2)   ]
        self.load_teams_for_game_to_slot()
        team_A_name = self.teams_for_game [0][0][0]
        team_B_name = self.teams_for_game [1][0][0]
        print ( 'self.teams_for_game'  ,    self.teams_for_game [0][0][0]   )



        self.game_type = "game"

        field_site =  "left"
        print ( 'self.field_site'  ,    field_site  )
        self.coach_team_A.generate_players_instance(team_A_name , field_site, team_A_type , start_game_coordinates)

        field_site =  "right"
        print ( 'self.field_site'  ,    field_site )
        self.coach_team_B.generate_players_instance(team_B_name , field_site, team_B_type, start_game_coordinates)


        #   index 0 je ball
        for teams_lops in range (1,11):
            if teams_lops < 6:
                self.list_of_ingamers.append(self.coach_team_A.team_players[teams_lops - 1])
            else:
                self.list_of_ingamers.append(self.coach_team_B.team_players[teams_lops - 6])



        #if thread_team_A:#testy
        if False:#testy
            print ("   start treads       ")
            thread_A_team =  Thread (target = self.coach_team_A.move_around_team   ,args =  (The_field,self.list_of_ingamers))
            thread_A_team.start()
        if False:
            thread_B_team =  Thread (target = self.coach_team_B.move_around_team   ,args =  (The_field,self.list_of_ingamers))
            thread_B_team.start()
        if False:#a player
            thread_A_team_player6 =  Thread (target = self.list_of_ingamers[6].move_round   ,args =  (The_field,self.list_of_ingamers))
            thread_A_team_player6.start()
            thread_A_team_player3 =  Thread (target = self.list_of_ingamers[3].move_round   ,args =  (The_field,self.list_of_ingamers))
            thread_A_team_player3.start()
            thread_A_team_player7 =  Thread (target = self.list_of_ingamers[7].move_round   ,args =  (The_field,self.list_of_ingamers))
            thread_A_team_player7.start()
            thread_A_team_player2 =  Thread (target = self.list_of_ingamers[2].move_round   ,args =  (The_field,self.list_of_ingamers))
            thread_A_team_player2.start()
    '''

    # nastavi novy game_status sobe
    def set_game_status_to_self(self,new_status):
        self.game_type = new_status

    # nastavi  game_status  vsem hracum
    def set_game_status_to_players(self):
        if self.list_of_ingamers[1] == 0 :
            return
        for no_of_ingamers in range (1,len(self.list_of_ingamers)):
            self.list_of_ingamers[no_of_ingamers].game_status = self.game_type

    def pause_game(self):#,The_game_window,The_field):                                                    #   potrebuje vsechny vstupy??
        self.set_game_status_to_self("pause")
        self.set_game_status_to_players()


    def unpause_game(self,The_game_window,The_field):
        #treba reload model kvuli threads
        for no_of_ingamers in range (1,len(self.list_of_ingamers)):
            self.list_of_ingamers[no_of_ingamers].model_needs_reload = True

        self.set_game_status_to_self("game")
        self.set_game_status_to_players()
        #treba reload model kvuli threads
        thread_A_team =  Thread (target = self.coach_team_A.move_around_team   ,args =  (The_field,self.list_of_ingamers))
        thread_A_team.start()
        thread_B_team =  Thread (target = self.coach_team_B.move_around_team   ,args =  (The_field,self.list_of_ingamers))
        thread_B_team.start()




    '''
    def restart_players(self,The_game_window,The_field,list_of_ingamers):                   #zkontroluj je pouzito
        self.start_match (The_game_window,The_field,list_of_ingamers,False)
    '''

    def draw_data_lower_menu (self,The_game_window,The_field):                           # zkontroluj pro je metoda dyz se muze vykreslovat jak ostatni
        f_print_score(self.score,The_game_window,The_field)
