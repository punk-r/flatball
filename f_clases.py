import math
import random
import pygame
from pygame.locals import *
import threading
import time
import copy

import xml_f
from xml_f import *
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
    # nastavni okna/tabulky team manegmentu /vyberu hracu
    team_detail_lines = 6   # 1 x nazev + 5 hracu teamu
    mngmt_column_width = 80                                                                                        #udelat pomerem z ruznych velikosti okna
    mngmt_teams_on_page = 10
    mngmt_text_ratio = 3 # zvetseni pisma ku menu fontu
    selection_game_text_ratio = 2 # zvetseni pisma ku menu fontu
    mngmt_shift_from_menu = 50
    buttons = []


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
        #print ("set field")
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
    data_trening = []                  # TRENER UKLADA DATA PRO trening ??!! bude zmeneno ,kazdy hrac si bude data vyhodnocovat sam =>bude jednodussi
    data_labels = []
    active_trening = False           # ukazatel treningu nebo zapasu
    team_play_at = "Home"            # urcuje zda je tym domaci nebo ne , pro nedomaci team se nezobrazuji detaily
    trening_sesion_total_runs = 5000  #5000  celkovy pocet uceni pro spusteny trening
    trening_runs_counter = 0         # po dosazeni reset_runs se zmeni pozice pro trening
    trening_runs_lenght = 100         # pocet uceni pro stejne rozestaveni hracu
    automated_trening_type = False   # true jestli je zautomatizovy trening

    # ulozi data z treningu
    def process_data(self,player,action,list_of_ingamers,The_field):
        #print ("processss data ")
        reset_loop = 0
        if len(self.data_trening) < self.trening_sesion_total_runs:

            # ukladani dat: uhel k sve brane,uhel k mici,vzdalenost k mici, provedena akce hracem
            self.data_trening.append([round(player.path_target), \
                             round(player.calculate_angle_to_other_object(list_of_ingamers[1].position)), \
                             # oprava pro rozdil od hrany hrace ne od stredu kruznic (umozni vypocet nezavisle na velikosti hracu a mice)
                             round(pythagoras_distance (player.position,list_of_ingamers[1].position) - player.radius - list_of_ingamers[1].radius  ) ])

            # labels
            self.data_labels.append( action)

            '''
            if self.automated_trening_type == False:
                if self.trening_runs_counter == self.trening_runs_lenght :
                    self.trening_runs_counter = 0
                    # zmen pozici hracu
                    self.move_players_for_new_training_run (The_field,list_of_ingamers)

                    #print("self.trening_runs_counter"  , self.trening_runs_counter)

                else:
                    self.trening_runs_counter = self.trening_runs_counter + 1
            '''

        else:
            self.active_trening = False
            # self.save_training()
            train_model(self.data_trening, self.data_labels , self.data_trening, self.data_labels, player.ID)   #testu trening data sou stejny jak test data
            self.reset_training_arrays()
            #start trainkeras model



    def move_players_for_new_training_run (self,The_field,list_of_ingamers):
        vertical_max    = The_field.field_bl_corner [1]
        vertical_min    = The_field.field_bl_corner [1] - The_field.field_height
        horizontal_min  = The_field.field_bl_corner [0]
        horizontal_max  = The_field.field_bl_corner [0] + The_field.field_width

        for no_of_ingamers in range (1,len(list_of_ingamers)): #mic a hraci jsou posunuti na novou pozici
            list_of_ingamers[no_of_ingamers].set_position (random.randint(horizontal_min, horizontal_max), \
                                                           random.randint(vertical_min, vertical_max))






    def reset_training_arrays (self):
        self.data_trening = []
        self.data_labels = []



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
    # buffers pro vyber teamu v 'team management'
    selected_slot_team_management = [-1,-1]
    selected_slot_team_management_buffer = [-1,-1]
    teams_for_game  = [" "," ","AI","human"]   # oznacene 2 teamy pro hru a jejich nastaveni
    radius = 15             # velikost
    lab_mode_b = 1          # laboratory mode, odemkne nektera nastaveni
    game_type = "none"      # typ hry                                                                       zkontroluj UZITO????
    selected_b = False      # ukazatel zda je ingamer oznaceny                                               zkontroluj ,mely by byt uz z ingamer tridy!!
    score  = [0,0]          # pocitadlo golu
    time  = 0               # odpocet casu
    color_check  = 0        # hodnoty pro nastaveni hry zatim epouzito
    set_color  = 0
    was_clicked  = 0        # reff byl oznacen pri hre
    stop_game  = 0                                                                                            # ? uzito ??
    pause_game   = 0        # puse pro zapocatou hru
    team_type = "neutral"  # ???  zkontroluj
    coach_team_A = "none"  # rozhodci ma prehled o cele hre i o trenerech
    coach_team_B = "none"
    H_teams_available_list = [] # home teams   ASI NENI treba pouzit list vsech teamu co sou k dispozici (loaded_teams_xml)
    A_teams_available_list = [] # away teams  ASI NENI TREBA
    # list teamu & dat ctenych z xml souboru
    loaded_teams_xml = ["none","none","none","none","none","none", \
                        "none","none","none","none","none","none"]

    ## 3 metody pro team managemet hraci jdou mazat a kopirovat
    # smazat hrace v team management
    def delete_player_from_slot(self):
        team_index = self.selected_slot_team_management[0]
        player_index = self.selected_slot_team_management[1]
        # kontrola  slot neni prazdny a je pro hrace
        if player_index > 0:
            # team slot neni prazdny len("none") = 4
            if len(self.loaded_teams_xml[team_index]) == 6:
                self.loaded_teams_xml [team_index][player_index] = "    "                                                     #pridej team neni original

    def copy_player_from_slot(self):
        position_copy = copy.deepcopy(self.selected_slot_team_management)
        self.selected_slot_team_management_buffer =  copy.deepcopy(position_copy)

    def paste_player_from_other_slot(self):                                                                                         #pridej kontrolu pro zakaz kopirovani prazdneho slotu
        from_slot = self.selected_slot_team_management_buffer
        to_slot   = self.selected_slot_team_management
        #print ("from_slotto_slot" ,from_slot,to_slot)
        #print ("self.loaded_teams_xml [to_slot[0]]" ,self.loaded_teams_xml [to_slot[0]])
        if to_slot[1] >0 and from_slot[1] >0 : # slot hracu

            if len(self.loaded_teams_xml [to_slot[0]] ) == 4:  # 4 = len(none)
                # pro prazny slot teamu se vytvori sablona
                # A = asci 65
                self.loaded_teams_xml [to_slot[0]] = [[ chr(65 + to_slot[0] )    ,"original","notselected"],"    ","    ","    ","    ","    "]                    #dodelat random nazev  teamu

                #TESTY
                for llloop in range (0,12):
                    print (self.loaded_teams_xml[llloop])

            self.loaded_teams_xml [to_slot[0]] [to_slot[1]] = copy.deepcopy(self.loaded_teams_xml [from_slot[0]] [from_slot[1]])

            # player id dle datetime stamp
            self.loaded_teams_xml [to_slot[0]] [to_slot[1]] [1] = time.strftime("%d%m%H%M%S")

            # create model
            main_path = os.path.abspath(os.getcwd())

            os.chdir("Teams")
            os.chdir("Home")
            # vytvoreni modelu dle 'skills' hrace, pocet vstupu neural network
            #print ("TTTETETETETESTETTE", self.loaded_teams_xml [to_slot[0]] [to_slot[1]][3] )
            model = create_model(   self.loaded_teams_xml [to_slot[0]] [to_slot[1]][3]   )
            #ulozeni dle hracova ID, date stampt ktery zaruci ze model se neulozi duplikovany                                                                    # nebude konstanta
            model.save( self.loaded_teams_xml [to_slot[0]] [to_slot[1]] [1]  + ".h5")

            os.chdir(main_path)

        self.selected_slot_team_management_buffer = [-1,-1] # reset bufferu

        #print("paste")

    def reset_selected_slot_team_management(self):
        self.selected_slot_team_management = [-1,-1]
        self.selected_slot_team_management_buffer = [-1,-1]


    def reset_teams_for_game(self):
        self.teams_for_game  = [" "," ","AI","human"]

    def save_team_from_teammngmt_table(self):
        all_players_check = 1 # kontrola hrac x5 v teamu jinak se team neulozi
        team_index = self.selected_slot_team_management[0]
        player_index = self.selected_slot_team_management[1]
        checked_team = self.loaded_teams_xml[team_index]

        if checked_team != "none": #pokud prazdny slot metoda nic nevykona
            for check_team_loop in range (1,5):
                if len(checked_team [check_team_loop] ) == 4:                                       # 4 = len(none)   opakovani kodu zlepsit
                    all_players_check = 0

            if all_players_check == 1 and player_index == 0: #oznacen je team ne hrac
                main_path = os.path.abspath(os.getcwd())

                os.chdir("Teams")
                os.chdir("Home")

                new_path = os.path.abspath(os.getcwd())
                print ("pppath ", new_path)
                print ("pppath ", checked_team)
                create_xml_file(  checked_team      ,new_path)
                os.chdir(main_path)



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

        # Error hodnoty
        #self.selected_slot_team_management = [-1,-1]

        if position_clicked[0] > table_left and position_clicked[0] < table_right:
            if position_clicked[1] > table_top and position_clicked[1] < table_bottom:
                self.selected_slot_team_management[0] = (position_clicked[0] - table_left ) // column_width
                self.selected_slot_team_management[1] = (position_clicked[1] - table_top ) // (text_ratio * The_game_window.menu_line_spacing )

        #print("clickkked",self.selected_slot_team_management )

    # nacte teamy z slozky z predchozich her
    def save_H_team_available_to_list (self,new_teams):
        self.H_teams_available_list = new_teams
                                                                                                #metody smazat nepouzite
    def save_A_team_available_to_list (self,new_teams):
        self.A_teams_available_list = new_teams

    # zmeni team na selected ,pro vyber teamu pro hru
    def choose_team_from_selection(self,line_in):
        # line 1 (index 0 ) jsou popisky tabulky
        line = line_in - 1
        #print("llline",line)
        # dvakrat vybrany team
        # team slot neni prazdny len("none") = 4
        if len(self.loaded_teams_xml[line]) == 6:
            #team neni vybran
            if self.loaded_teams_xml[line][0][2] == "notselected":
                self.loaded_teams_xml[line][0][2] = "selected"
            else:
                self.loaded_teams_xml[line][0][2] = "notselected"

        # projde seznam teamu a zkontroluje ktere jsou oznaceny
        self.check_selected_teams()


    # povrzeni teamu do treningu
    def start_training(self):
        # trening lze zacit pokud jso oznaceny sloty s existujicimi teamy (lze vybrat trening i teamu sama k sobe)
        #    => slot nesmi byt prazdny nebo mis staus jiny nez original
        # teamy maji status original => nemaji zmenu ktera neni ulozena, maji 5 ulozenych hracu
        # vybran team a hrac (hracuv team je automaticky vybran jako druhy pro trening)


        # prvni index je team , druhy je hrac
        # prilad index_team_a =[0,0]  je oznacen team 0 ,  [1,2]  znamena team na indexu 1 a jeho hrac na indexu 2
        index_team_a = self.selected_slot_team_management
        index_team_b = self.selected_slot_team_management_buffer

        player_selected_ID = "none"
        start_training_check = False

        print ("test   start_training")
        print (self.selected_slot_team_management)
        print (self.selected_slot_team_management_buffer)

        # oba teamy existuji
        if len(self.loaded_teams_xml [index_team_a[0]]) != 4  and  len(self.loaded_teams_xml [index_team_b[0]] ) != 4:  # 4 = len("none")

            # oznacen hrac a team
            if  (index_team_a[1] == 0 or index_team_b[1] == 0)  and \
                (index_team_a[1] != 0 or index_team_b[1] != 0):

                # status teamu je original
                if  self.loaded_teams_xml[index_team_a[0]][0][1] == "original" and \
                    self.loaded_teams_xml[index_team_b[0]][0][1] == "original"  :                               #zkontroluj podmnku

                    #player # ID
                    if index_team_a[1] != 0:
                        player_selected_ID = self.loaded_teams_xml[index_team_a[0]][index_team_a[1]][1]
                    else:
                        player_selected_ID = self.loaded_teams_xml[index_team_b[0]][index_team_b[1]][1]

                    print ("test ok  start_training")
                    print ("player_selected_ID", player_selected_ID)
                    start_training_check = True

                    self.teams_for_game[0] = self.loaded_teams_xml[index_team_a[0]][0][0]
                    self.teams_for_game[1] = self.loaded_teams_xml[index_team_b[0]][0][0]

        # vyuzit self.teams_for_game[0] = "Ooo,Error :("      pro informaci hraci o spatnem vstupu  , udelat print funkci pro error

        return [start_training_check,player_selected_ID  ]


    # zkontroluje zda jsou oznaceny pouze dva teamy
    def check_selected_teams(self):
        teams_selected = 0

        # kontrola ze 2 teamy jsou oznaceny
        for check_loop in range (0,len(self.loaded_teams_xml)):
            # team slot neni prazdny len("none") = 4
            if len(self.loaded_teams_xml[check_loop]) == 6:
                if self.loaded_teams_xml[check_loop][0][2] == "selected":
                    teams_selected = teams_selected + 1

        # ulozi 2x jmeno vybranych teamu
        if  teams_selected == 2 or teams_selected == 1:
            self.teams_for_game[0] = "  "
            self.teams_for_game[1] = "  "
            saving_index = 0
            for save_loop in range (0,len(self.loaded_teams_xml)):
                if len(self.loaded_teams_xml[save_loop]) == 6:
                    if self.loaded_teams_xml[save_loop][0][2] == "selected":
                        self.teams_for_game[saving_index] = self.loaded_teams_xml[save_loop][0][0]
                        saving_index = saving_index + 1

        elif teams_selected > 2:
            self.teams_for_game[0] = "Ooo,Error :("
            self.teams_for_game[1] = " >2! "

    # nacte data pro teamu a hrace z xml
    def load_data_from_xml(self):

        # vypsani teamu a hracu,prvni column je pro popisky
        Teams_path = os.path.abspath(os.getcwd())

        # nacteni teamu do seznamu u rozhotciho
        list_home_teams = []
        list_away_teams = []

        for filename in os.listdir(Teams_path + "\Teams\Home"):
            if not filename.endswith('.xml'): continue
            list_home_teams.append(filename)

        for filename in os.listdir(Teams_path + "\Teams\Away"):
            if not filename.endswith('.xml'): continue
            list_away_teams.append(filename)

        # !!zatim se ukazuje jen 10teamu
        if len(list_home_teams) > 10:
            show_teams = 10
        else :
            show_teams =  len(list_home_teams)

        if len(list_away_teams) > 2:
            show_teams_away = 2
        else :
            show_teams_away =  len(list_away_teams)

        # domaci teamy
        for teams_loop in range (0,show_teams):
            team_name = list_home_teams[teams_loop]
            self.loaded_teams_xml[teams_loop] =  f_read_from_xml (Teams_path + "\Teams\Home\\" + team_name )

        # hoste
        for teams_loop in range (0,show_teams_away):
            team_name = list_away_teams[teams_loop]
            # + 10 ,prvnich 10 slotu je pro domaci team
            self.loaded_teams_xml[teams_loop + 10 ] =  f_read_from_xml (Teams_path + "\Teams\Away\\" + team_name )


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


    def start_match (self,The_game_window,The_field,list_of_ingamers,called_at_begining):                           # potreba?called_at_begining ?
        # pro trening
        vertical_max    = The_field.field_bl_corner [1]
        vertical_min    = The_field.field_bl_corner [1] - The_field.field_height
        horizontal_min  = The_field.field_bl_corner [0]
        horizontal_max  = The_field.field_bl_corner [0] + The_field.field_width
        team_A_slot = self.teams_for_game [0] # ulozi jmeno teamu
        team_B_slot = self.teams_for_game [1] # ulozi jmeno teamu
        #print (  "team_A_slot  team_B_slot"  ,team_A_slot     ,team_B_slot  )

                                                                                                            # pridat kontrolu teamu,

        # input ma tvar : [team_name,5x [pl_name, pl_ID,pl_position,trening_type,trening_time]]
        shift_x = The_field.field_bl_window[0] + The_field.field_width*0.2
        team_switch = 0
        for teams_lops in range (0,12):
            #print (  "self.loaded_teams_xml [teams_lops][0][0]"  ,self.loaded_teams_xml [teams_lops][0][0]  )
            if self.loaded_teams_xml [teams_lops][0][0] == team_A_slot or self.loaded_teams_xml [teams_lops][0][0] == team_B_slot:
                shift_y = The_field.field_bl_window[1] * 0.3
                for players_loop in range (1,6):   # index 0 je nazev teamu
                    # vypsani teamu a hracu,prvni column je pro popisky
                    Teams_path = os.path.abspath(os.getcwd())

                    if teams_lops < 10 :
                        full_path = Teams_path + "\Teams\Home\\"
                    else:
                        full_path = Teams_path + "\Teams\Away\\"

                    new_player_ID = self.loaded_teams_xml[teams_lops][players_loop][1]
                    new_player = player ([int(shift_x),int(shift_y)])

                    if team_switch == 0:
                        new_player.path_target = 180
                        new_player.team_type = "H"
                        new_player.team = "A"
                        new_player.game_status = "game"
                        new_player.field_site = "left"
                        new_player.set_coach(self.coach_team_A)
                        new_player.set_path_target(180)
                        new_player.ID = new_player_ID
                    else:
                        new_player.path_target = 180
                        new_player.team_type = "H"
                        new_player.team = "B"
                        new_player.color = red
                        new_player.game_status = "game"
                        new_player.field_site = "right"
                        new_player.set_coach(self.coach_team_B)
                        new_player.set_path_target(180)
                        new_player.ID = new_player_ID

                    new_player.model= load_model( full_path + new_player_ID + ".h5")   # zmenin na file dle ID hrace

                    x = 2
                    if x == 1:
                        new_player.team_type = "AI"
                        thread_new_player =  threading.Thread (target = new_player.move_round   ,args =  (The_game_window,The_field,list_of_ingamers))
                        thread_new_player.start()




                    #print("team_switch",team_switch)

                    shift_y = shift_y + The_field.field_height * 0.1
                    list_of_ingamers.append(new_player)

                team_switch = 1
                shift_x = The_field.field_bl_window[0] + The_field.field_width*0.8


        #print (  "slist_of_ingamers0]"  ,list_of_ingamers  )


        '''

        if os.path.isfile("model.h5"):
            The_player_no_A1.model= load_model("model.h5")
            The_player_no_A2.model= load_model("model.h5")


        '''
        #testovani
        '''
        thread_a1 =  threading.Thread (target = The_player_no_A1.move_round   ,args =  (The_game_window,The_field,list_of_ingamers))
        thread_a1.start()
        '''

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
        '''


    def restart_players(self,The_game_window,The_field,list_of_ingamers):
        self.start_match (The_game_window,The_field,list_of_ingamers,False)


    def draw_data_lower_menu (self,The_game_window,The_field,list_of_ingamers):
        f_print_score(self.score,The_game_window,The_field)
