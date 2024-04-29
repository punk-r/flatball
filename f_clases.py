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
import class_coach
from class_coach import *

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
    window_width = 1280   # pomer 16/9
    window_height = 720
    resolution_ratio = 1
    surface = pygame.display.set_mode((window_width,window_height))
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
    isrender_REtraining = True          # render trening pri re trening
    draw_circles_on_screen = False       # render player

    # new_size msi byt pole dva prvky
    def resize_window(self,new_size,The_field):
        self.resolution_ratio = new_size[0] / 1280
        self.surface = pygame.display.set_mode((self.window_width,self.window_height),pygame.RESIZABLE)
        self.surface = pygame.display.set_mode((new_size[0],new_size[1]))
        self.set_window_size(new_size,The_field)
        self.resize_to_new_values()
        self.buttons = create_buttons_instances(self,The_field)


    def draw_all_ingamers(self,list_of_ingamers):
        for no_of_ingamers in range (0,len(list_of_ingamers)):
            list_of_ingamers[no_of_ingamers].draw_ingamer(self)


    def resize_to_new_values(self):                                                                                 # je metoda treba????????????????????
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

        self.field_width = int (  game_window.window_width  - 2 * field_gap_to_window )
        self.field_height = int ( 0.7 * game_window.window_height )
        self.goals_height = 0.2 * self.field_height
        self.longest_distance = int( pythagoras_distance (self.field_bl_corner,  \
                                                      (self.field_bl_corner[0]+ self.field_width, self.field_bl_corner[1] - self.field_height  )))

'''
# nacte teamy z xml
The_reff.load_data_from_xml()

'''

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
    running_threads = [  0 , 0   ]
    match_start_time = 0
    match_time = 20000#180000  # 3m - 180000 , 5m - 300000   v ms


    # projde vsechny teamy jak najde ty ze zapasu zupdatuje je
    def update_teams_game_stats(self):
        team_details = 0
        team_id = 3
        wins_index = 6
        sumgames_index = 9
        coach_selected =  self.coach_team_A
        isFirstTeam = True

        for coach in range (0,2):
            for team in range (0,10):
                if coach_selected.loaded_teams_xml[team] != SavingType.empty_team_slot.value:
                    if coach_selected.loaded_teams_xml[team][team_details][team_id] == self.teams_for_game[0][team_details][team_id] or \
                        coach_selected.loaded_teams_xml[team][team_details][team_id] == self.teams_for_game[1][team_details][team_id]:

                        team_selected  = coach_selected.loaded_teams_xml[team]
                        # update kazdeh HRACE
                        for player in range (1,6):
                            if isFirstTeam:
                                if self.score[0] > self.score[1]:
                                    team_selected[player][wins_index] =  str ( int(team_selected[player][wins_index]) + 1)
                            if isFirstTeam == False:
                                if self.score[0] < self.score[1]:
                                    team_selected[player][wins_index] =  str ( int(team_selected[player][wins_index]) + 1)

                            team_selected[player][sumgames_index] =  str ( int(team_selected[player][sumgames_index]) + 1)

                        #  ulozeni zmen
                        create_xml_file(team_selected)

                        isFirstTeam = False
            coach_selected =  self.coach_team_B

    def reset_ball(self,The_field):
        bl_corner = The_field.field_bl_corner
        The_ball = self.list_of_ingamers[0]

        The_ball.rect.center = [bl_corner [0] + int(The_field.field_width/2), bl_corner[1] - int(The_field.field_height/2)]


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
        team_index = 0

        # nelze trenovat se sebou
        if trenovany_team_index[0] == druhy_team_index[0] :
            return [start_training_check,player_selected_ID  ]

        if druhy_team_index[0]  == -1  or  trenovany_team_index[0] == -1 :
            return [start_training_check,player_selected_ID  ]

        if  self.coach_team_A.loaded_teams_xml[druhy_team_index[0]] == SavingType.empty_team_slot.value or \
                self.coach_team_A.loaded_teams_xml[trenovany_team_index[0]] == SavingType.empty_team_slot.value  :
            return [start_training_check,player_selected_ID  ]

        #druhy musi byt oznacen team
        if self.coach_team_A.loaded_teams_xml[druhy_team_index[1]] == team_index  :
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


    def game_reset_after_goal (self,The_field):
        self.list_of_ingamers[0].speed = 0
        self.list_of_ingamers[0].color = WHITE
        #self.list_of_ingamers[0].field_site = list_of_ingamers[1].field_site
        self.coach_team_A.move_players_for_new_training_run_startMatch_position(The_field,self.list_of_ingamers)


    def draw_ingamer (self,game_window):
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


    def set_selected (self,new_status):
        if new_status == True :
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


    #def read_selected (self):
        #return self.selected_b


    def start_match (self,The_field,called_at_begining, is_sequence_correct):
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
        shift_x = The_field.field_bl_corner[0] + The_field.field_width*0.2
        shift_y = The_field.field_bl_corner[1] * 0.3
        # set pro hru nastaveni pozice rozhotciho
        self.position = [  int( horizontal_max / 2 + self.radius ) , int(vertical_min  - self.radius )  ]

        self.load_teams_for_game_to_slot()

        # input ma tvar : [team_name,5x [pl_name, pl_ID,pl_position,trening_type,trening_time]]
        # pri treningu vzdy trenovany team prvni, vybere do teams_for_game'selected' teamy z listu vsech teamu
        if is_sequence_correct: all_teams = [self.teams_for_game[0] , self.teams_for_game[1]]
        else: all_teams = [self.teams_for_game[1] , self.teams_for_game[0]]

        # protoze index 0 je mic
        ingamer_saving_loop = 1
        for teams_lops in range (0,2):

            # nacte folder pro teamy
            if self.coach_types_check[teams_lops] == 'Home' :
                full_path = get_path_home_folder()
            else:
                full_path = get_path_away_folder()

            # index 0 je nazev teamu
            for players_loop in range (1,6):

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
                new_player.step = 2# randint(1,3)
                new_player.kick_power = 2#randint(1,3)

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

                new_player.model= load_model( full_path +  new_player_ID + ".h5")
                self.list_of_ingamers[ingamer_saving_loop] = new_player

                shift_y = shift_y + The_field.field_height * 0.1
                ingamer_saving_loop = ingamer_saving_loop + 1

            shift_x = The_field.field_bl_corner[0] + The_field.field_width*0.8

        if called_at_begining:
            self.coach_team_A.move_players_for_new_training_run_startMatch_position(The_field,self.list_of_ingamers)

        if thread_team_A:
            thread_A_team =  Thread (target = self.coach_team_A.move_around_team   ,args =  (The_field,self.list_of_ingamers))
            self.running_threads[0] = thread_A_team
            thread_A_team.start()

        if thread_team_B:
            thread_B_team =  Thread (target = self.coach_team_B.move_around_team   ,args =  (The_field,self.list_of_ingamers))
            self.running_threads[1] = thread_B_team
            thread_B_team.start()

        if False:#a player
            player11 =  Thread (target = self.list_of_ingamers[1].move_round   ,args =  (The_field,self.list_of_ingamers))
            player11.start()
        if False:#a player
            player11 =  Thread (target = self.list_of_ingamers[6].move_round   ,args =  (The_field,self.list_of_ingamers))
            player11.start()


    # nastavi novy game_status sobe
    def set_game_status_to_self(self,new_status):
        self.game_type = new_status


    # nastavi  game_status  vsem hracum
    def set_game_status_to_players(self):
        if self.list_of_ingamers[1] == 0 :
            return
        for no_of_ingamers in range (1,len(self.list_of_ingamers)):
            self.list_of_ingamers[no_of_ingamers].game_status = self.game_type


    def pause_game(self):
        self.set_game_status_to_self("pause")
        self.set_game_status_to_players()
        self.running_threads = [0,0]


    def unpause_game(self,The_game_window,The_field):
        #treba reload model kvuli threads
        for no_of_ingamers in range (1,len(self.list_of_ingamers)):
            self.list_of_ingamers[no_of_ingamers].model_needs_reload = True

        self.set_game_status_to_self("game")
        self.set_game_status_to_players()

        thread_team_A = thread_team_B = True

        # pri treningu jdou threads vypnout ale pri zapase sou vzdy zaply
        if self.coach_types_check[0] == 'Home' and self.coach_types_check[1] == 'Home':
            if self.coach_team_A.arethreads_on[0] != True:
                thread_team_A = False
            if self.coach_team_A.arethreads_on[1] != True:
                thread_team_B = False

        if thread_team_A:
            thread_A_team =  Thread (target = self.coach_team_A.move_around_team   ,args =  (The_field,self.list_of_ingamers))
            self.running_threads[0] = thread_A_team
            thread_A_team.start()

        if thread_team_B:
            thread_B_team =  Thread (target = self.coach_team_B.move_around_team   ,args =  (The_field,self.list_of_ingamers))
            self.running_threads[1] = thread_B_team
            thread_B_team.start()


    def draw_data_lower_menu (self,The_game_window,The_field):                           # zkontroluj proc je metoda dyz se muze vykreslovat jak ostatni   vseci ingamer maji jak metodu zkontroluj
        f_print_reff_ingame_lower_menu(self.score,The_game_window,The_field)
