import pygame
import sys
import math
import random
import os.path
from os import path
import neural_network
from neural_network import *
import support_functions
from support_functions import *


import xml_f
from xml_f import *

#pygame modul
pygame.init()
from pygame.locals import *

MenuFont = pygame.font.SysFont("Arial", 18)
MenuFont_heading = pygame.font.SysFont("Arial", 30)
WelcomeFont = pygame.font.SysFont("Arial", 40)

#--------------------------------------------------------------------------------------------class buttons
# trida pro tlacika
class button():

    def __init__(self):
        self.number = 0
        self.x_corner = 0
        self.y_corner = 0
        self.size = [10,10] # lenght, hight
        self.name ='n'
        self.graphic = "notset"

    def set_button_name_number (self,name,number):
        self.name  = name
        self.number = number

    def is_mouse_over_item (self,mouse_position):
        decision = "nomatch"  #error hodnota
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]


        if mouse_x > self.x_corner   and mouse_x < self.x_corner  + self.size[0]:
            if mouse_y < self.y_corner   and mouse_y  >  self.y_corner  - self.size[1] :
                decision = self.number

        #print ("decision",decision)
        #print ("mouse_position",mouse_position)
        #print ("x,y",self.x_corner,self.y_corner )

        return decision

# --------------------------MENU-----------------------
# vytvoreni instanci tlacitek
# tlacitka pro ostatni volby ,3 x team management , volby trenera
def create_buttons_instances(The_game_window,The_field):
    if The_game_window.language == "CZ":
        menu_list = ["TRENER", "  -Team management"  , "  -Stats"  ,"  -Trening  " , \
                    "ROZHODCI ",  "  -Delka utkani", "  -Potvrdit teamy ", "  -Nastaveni hriste ","  -Novy zapas",  \
                    "NASTAVENI ","  -Jazyk / Language", "  -Velikost okna",\
                    "LAB ", "  -zapnout lab mod","  -vypnout grafiku" , \
                    "NAPOVEDA "]

        other_buttns_list = ["Smazat hrace" ,"Kopirovat hrace","Ulozit team","pause tr", "k1tr","2ktr","22ktr","3ktr"]

    else:
        menu_list = ["TRENER " ,  "  -Team management"  , "  -Stats"  ,"  -Trening  " , \
                    "REFF ",  "  -Delka utkani", "  -Potvrdit teamy ", "  -Nastaveni hriste ","  -Novy zapas",  \
                    "SETTINGS ", "  -Velikost okna",\
                    "LAB ", "  -zapnout lab mod","  -vypnout grafiku" , \
                    "HELP "]

        other_buttns_list = ["delete " ," copy"  , "save","pause", "k1","2k","22k","3k"]

    buttons_names_list = menu_list + other_buttns_list
    # menu tlacitek 15 , mngmn tlacitek 3 , reff tlacitek ?
    lenght_menu = len (menu_list)
    lenght_mngmnt_buttons = 3
    lenght_ref_buttons = 3


    list = []
    ref_buttons_counter = 0
    mngmnt_buttons_counter = 0
    for generating_buttons_loop in range (0,len(buttons_names_list)):
        new_button = button()
        new_button.set_button_name_number (buttons_names_list [generating_buttons_loop] ,generating_buttons_loop)
        list.append(new_button)
        #JEDNOTNY VELIKOSTI BUTTONS!!! MENU VSECHNY STEJNY PAK OSTATNI VSECHNY STEJNY

        # menu tlacitka
        if generating_buttons_loop < lenght_menu :
            new_button.size = [100,18]
            new_button.x_corner = The_game_window.game_menu_x_start
            new_button.y_corner = The_game_window.heading_shift + (1+generating_buttons_loop)  * The_game_window.menu_line_spacing

        #  team management tlacitka
        elif generating_buttons_loop >= lenght_menu and generating_buttons_loop < lenght_menu + lenght_mngmnt_buttons:
            new_button.size = [40,40]
            new_button.x_corner = The_game_window.mngmt_shift_from_menu + The_field.field_bl_window[0] + \
                                     ref_buttons_counter * The_game_window.mngmt_column_width
            new_button.y_corner =  The_game_window.heading_shift +(1+ The_game_window.team_detail_lines ) *  \
                                    The_game_window.mngmt_text_ratio *  The_game_window.menu_line_spacing

            ref_buttons_counter = ref_buttons_counter + 2

        # reff behem hry
        elif generating_buttons_loop >= lenght_menu + lenght_mngmnt_buttons:
            new_button.size = [40,40]
            new_button.x_corner = The_game_window.mngmt_shift_from_menu +  mngmnt_buttons_counter * The_game_window.mngmt_column_width
            new_button.y_corner =  The_field.field_bl_window[1]
            mngmnt_buttons_counter = mngmnt_buttons_counter + 1



    return list

def draw_other_buttons(The_game_window,button_no):

    button_name = MenuFont.render(The_game_window.buttons[button_no].name, 1, grey)
    The_game_window.surface.blit(button_name,(The_game_window.buttons[button_no].x_corner, The_game_window.buttons[button_no].y_corner))




def draw_main_menu(The_game_window):
    main_menu_buttons = 16

    # menu nadpis
    menu_heading = "GAME MENU"
    menu_menu_heading_pages = MenuFont_heading.render(menu_heading, 1, green_field)
    The_game_window.surface.blit(menu_menu_heading_pages,(The_game_window.game_menu_x_start, 0.25 *The_game_window.menu_line_spacing))

    # Loop pro vypsani celeho menu
    for menu_loop in range(0,main_menu_buttons):
        menu_moves_pages = MenuFont.render(The_game_window.buttons[menu_loop].name, 1, grey)
        The_game_window.surface.blit(menu_moves_pages,(The_game_window.game_menu_x_start, menu_loop *  The_game_window.menu_line_spacing + The_game_window.heading_shift))

    # ?? buttons maji v instanci ulozenou pozici !!!! opravit funkci vyse prosouradnice na  render

'''
Rozdeleni okna aplikace 4x ruzne plochy
 ___________________         ___________________
| 1 | 3             |       | 4                 |
|   |               |    => |                   |
|___|_______________|       |___________________|
| 2                 |       | 2                 |
|___________________|       |___________________|

'''

# okno rozdeleno na 3 casti
def draw_menu_lines_ID_3(The_game_window,The_field):
    #rozdeleni obrazovky aplikace
    pygame.draw.rect(The_game_window.surface, white , (0 ,0 ,The_game_window.window_width, The_game_window.window_height  )   ,  1)
    pygame.draw.lines(The_game_window.surface,  grey, True, ((The_field.field_bl_window[0],0 ) , \
                                                             ( The_field.field_bl_window[0] , The_field.field_bl_window[1] )), 1)
    pygame.draw.lines(The_game_window.surface,  grey, True, ((0 ,The_field.field_bl_window[1] ) ,  \
                                                             ( The_game_window.window_width ,The_field.field_bl_window[1] )), 1)

# zapas => menu je ukryto - okno rozdeleno na 2 casti
def draw_menu_lines_ID_4(The_game_window,The_field):
    #rozdeleni obrazovky aplikace
    pygame.draw.rect(The_game_window.surface, white , (0 ,0 ,The_game_window.window_width, The_game_window.window_height  )   ,  1)
    pygame.draw.lines(The_game_window.surface,  grey, True, ((0 ,The_field.field_bl_window[1] ) ,  \
                                                             ( The_game_window.window_width ,The_field.field_bl_window[1] )), 1)


# volani funkce/metody dle volby z menu                                                                                                 # Zjednodusene vypracovani pro testy,predelat na class_buttons
def f_menu_selected(position_clicked,The_game_window,The_field,list_of_ingamers):                                                       # vyber indexu z listu funkci ,cela funkce jde napsat prehledneji
    screen = 0
    # The_game_window.heading_shift posun na zacatku menu
    line_selected = position_clicked  # line_selected je cislo tlacitka
    if  line_selected == 8:
        #ref
        list_of_ingamers[0].start_test_match (The_game_window,The_field,list_of_ingamers,True)
        screen = 4
    elif  line_selected == 100000:
        for no_of_ingamers in range (2 , len(list_of_ingamers)):
            list_of_ingamers[no_of_ingamers].game_status = "pause"
        screen = 4
    elif  line_selected == 1000000:
        for no_of_ingamers in range (2 , len(list_of_ingamers)):
            list_of_ingamers[no_of_ingamers].game_status = "pause"
        list_of_ingamers[0].restart_players(The_game_window,The_field,list_of_ingamers)
        screen = 4
    elif  line_selected == 200000:
        #print (list_of_ingamers[3].team_coach.data)
        list_of_ingamers[3].team_coach.save_training()
        train_model(list_of_ingamers[3].team_coach.data_trening, list_of_ingamers[3].team_coach.data_labels , \
                    list_of_ingamers[3].team_coach.data_trening, list_of_ingamers[3].team_coach.data_labels )   #testu trening data sou stejny jak test data
        list_of_ingamers[3].team_coach.data_trening = []
        list_of_ingamers[3].team_coach.data_labels = []
        print_model_values("model.h5")
                                                                                #TESTY
        screen = 4

    elif  line_selected == 1:
        screen = 5


    elif  line_selected == 6:
        screen = 6


    #DODELAT MENU
    # vrati jaky screen se ma zobrazit
    return screen




# -------------------------------------------SCREENS---------------------------------------------------

# teams selection pro hru
def draw_teams_for_game(The_game_window,The_field,The_reff,list_of_ingamers):
    # hodnoty musi by ulozeny v 'window' aby slo vypocitat polohu mysi => spustit metodu/funkci
    lines = 13
    column_width = 1.5 * The_game_window.mngmt_column_width
    teams_on_page = The_game_window.mngmt_teams_on_page + 2   # +2 hostujici teamy
    columns = 7
    text_ratio = The_game_window.selection_game_text_ratio
    shift_from_menu = The_game_window.mngmt_shift_from_menu

    # hranice tabulky teamu
    table_top = The_game_window.heading_shift
    table_left = shift_from_menu + The_game_window.game_menu_x_end
    table_bottom = table_top + text_ratio * lines * The_game_window.menu_line_spacing
    table_right = table_left + columns * column_width

    if The_game_window.language == "CZ":
        page_heading = WelcomeFont.render('vyberteam vitejte', 1, grey)
        note_1 = WelcomeFont.render('vybrane teamy', 1, grey)
        table_headngs = ["team","trenovano" ,"trening" ,"prum skills" , "zapasu", "vyher", "vybrano",]
    else:
        page_heading = WelcomeFont.render('chooseteam welcome', 1, grey)
        note_1 = WelcomeFont.render('envybrane teamy', 1, grey)
        table_headngs = ["ukteams","a" ,"b" ,"c" , "d", "e", "selected"]

    teams_chosen = WelcomeFont.render( The_reff.teams_for_game[0]  + ' X ' + The_reff.teams_for_game[1]  , 1, grey)

    The_game_window.surface.blit(page_heading,( table_left  ,  0.1 * The_game_window.menu_line_spacing ))
    The_game_window.surface.blit(note_1,( table_left  , The_field.field_bl_window[1] +   The_game_window.menu_line_spacing ))
    The_game_window.surface.blit(teams_chosen,( table_left  , The_field.field_bl_window[1] + 4 * The_game_window.menu_line_spacing )) # 4 radku odsazeni


    ## Vykresleni tabulky
    # Rect(left, top, width, height)
    pygame.draw.rect(The_game_window.surface, red, ( table_left, table_top, \
                                                    columns * column_width, \
                                                    text_ratio * lines * The_game_window.menu_line_spacing),1)

    # line  radky sloupce(surface, color, start_pos, end_pos, width)
    shift = 0
    for row_loop in range (0,lines):
        shift = shift + text_ratio * The_game_window.menu_line_spacing
        pygame.draw.lines(The_game_window.surface, grey_lines, True,((table_left, table_top + shift), \
                                                                        (table_right, table_top + shift)), 1)

    shift = 0
    for row_loop in range (0,columns):
        table_headngs_rendered = MenuFont.render(table_headngs[row_loop], 1, grey)
        The_game_window.surface.blit(table_headngs_rendered,( table_left + shift  + column_width/4  , table_top    )) # posun 1/4 sirka boxu
        shift = shift + column_width
        pygame.draw.lines(The_game_window.surface, grey_lines, True,((table_left + shift, table_top), \
                                                                     (table_left + shift, table_bottom )), 1)

    column_teams_shift =  text_ratio * The_game_window.menu_line_spacing
    player_line_shift = 0
    leter_shift_from_boarder = 5 #odsazeni od hran tabulky
    font_diference = 1   #rozdil mezi fontem a linkou

    # domaci teamy 10 slotu , + 2 sloty hoste   => 12
    for teams_loop in range (0,12):
        team_name = The_reff.loaded_teams_xml[teams_loop][0][0]
        if team_name != "n":  # n prvni char z "none"

            test = MenuFont.render( team_name, 1, grey)
            The_game_window.surface.blit(test,( table_left  + leter_shift_from_boarder , \
                                                table_top +  player_line_shift + column_teams_shift ))

            player_line_shift = player_line_shift +  2*The_game_window.menu_line_spacing   # *3 team ma jen jmeno a musi se posunout 3 linie dolus

        column_teams_shift = column_teams_shift + text_ratio * The_game_window.menu_line_spacing
        player_line_shift = 0




def draw_team_managemet(The_game_window,The_field,The_reff,list_of_ingamers):
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

    if The_game_window.language == "CZ":
        test = WelcomeFont.render('mnngmmgmmgt vitejte', 1, grey)
    else:
        test = WelcomeFont.render('mnngmmgmmgt welcome', 1, grey)

    The_game_window.surface.blit(test,( table_left  ,  0.1 * The_game_window.menu_line_spacing ))


    ## Vykresleni tabulky
    # Rect(left, top, width, height)
    pygame.draw.rect(The_game_window.surface, red, ( table_left, table_top, teams_on_page * column_width,text_ratio * lines * The_game_window.menu_line_spacing)    ,  1)

    # line(surface, color, start_pos, end_pos, width)
    shift = 0
    for row_loop in range (0,lines):
        shift = shift + text_ratio * The_game_window.menu_line_spacing
        pygame.draw.lines(The_game_window.surface, grey_lines, True,( ( table_left ,table_top + shift ),(table_right ,table_top + shift  ) )    , 1)

    shift = 0
    for row_loop in range (0,teams_on_page):
        shift = shift + column_width
        pygame.draw.lines(The_game_window.surface, grey_lines, True,( ( table_left + shift ,table_top  ),(table_left + shift  , table_bottom ) )    , 1)


    column_teams_shift = 0
    player_line_shift = 0
    leter_shift_from_boarder = 5 #odsazeni od hran tabulky
    font_diference = 1   #rozdil mezi fontem a linkou
    for teams_loop in range (0,10):
        players_data =  The_reff.loaded_teams_xml[teams_loop]
        #print ("11",players_data)
        for players_loop in range (0,6):  # 1 nazev teamu +  5 hracu  => 6 radku
            if players_data[0] != "n":  # n prvni char z "none"
                # >1 players
                if players_loop >= 1:
                    for player_details in range (0,3 ):                                                                  #DODELAT OPODLE POCTU DETAILS NA HRACE
                        # ID se nezobrazuje
                        if player_details !=1:
                            test = MenuFont.render( players_data[players_loop][player_details]   , 1, grey)
                            The_game_window.surface.blit(test,( table_left + column_teams_shift + leter_shift_from_boarder, table_top +  player_line_shift  ))

                            player_line_shift = player_line_shift + The_game_window.menu_line_spacing
                    #vynecha radek
                    player_line_shift = player_line_shift + The_game_window.menu_line_spacing                                                           # zkontroluj lines
                # < 1 team
                else:
                    test = MenuFont.render( The_reff.loaded_teams_xml[teams_loop][0][0], 1, grey)
                    The_game_window.surface.blit(test,( table_left + column_teams_shift + leter_shift_from_boarder , table_top +  player_line_shift  ))

                    player_line_shift = player_line_shift +3* The_game_window.menu_line_spacing   # *3 team ma jen jmeno a musi se posunout 3 linie dolu

        column_teams_shift = column_teams_shift + column_width
        player_line_shift = 0


# print team management buttons
def f_print_teammngmt_buttons(The_game_window):
    for loop in range (0,4):
        button_shift = 15
        draw_other_buttons(The_game_window,button_shift + loop)

# tisk score
def f_print_score(score,The_game_window,The_field):
    show_score = WelcomeFont.render(str(score), 1, grey)
    The_game_window.surface.blit(show_score,(The_field.field_bl_window [0], The_field.field_bl_window[1] + The_game_window.menu_line_spacing ))
    for loop in range (0,3):
        button_shift = 19
        draw_other_buttons(The_game_window,button_shift + loop)


# tisk hrace pri hre
def f_print_player_details(The_game_window,The_field,player,list_of_ingamers):
    shift_vertikal = 0
    list_of_tags = ["angle: ","ball angle: ","ball distance(cntr-cntr)","velocity: ","site: "]
    list_of_data =[str(round(player.path_target)), \
                   str(round(player.calculate_angle_to_other_object(list_of_ingamers[1].position))), \
                   str(round(pythagoras_distance (player.position,list_of_ingamers[1].position))), \
                   str(player.velocity), \
                   player.field_site ]

    for data_index in range (0,len(list_of_data)):
        data = MenuFont.render(  list_of_tags[data_index] + list_of_data[data_index]   , 1, grey)
        The_game_window.surface.blit(data,(The_field.field_bl_window [0], The_field.field_bl_window[1] + The_game_window.menu_line_spacing + shift_vertikal ))
        shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing


#test prints                                                                                            #testy souradnic
def print_test_x(The_game_window):
    xx = MenuFont.render( "XX"  , 1, red)
    The_game_window.surface.blit(xx,(300, 650 ))
    #print("xx")

# vizualizace keras.modelu
def f_print_model_live(The_game_window,The_field,player,list_of_ingamers,live_data,model_values):
    data = [0,0,0,0]
    data = calculate_live_model(live_data,model_values)
    data.append([ "otoc","-otoc","krok","kop" ,"nic" ])
    x_shift = 300
    shift_vertikal = 0

    for list_index in range (0,len(data)):
        for inner_list_index in range (0,len(data[list_index])):
            if list_index < len(data)-1:
                data_print = MenuFont.render(  str(round(data[list_index][inner_list_index],4)  ) , 1, grey)
            else:
                data_print = MenuFont.render(  data[list_index][inner_list_index] , 1, grey)
            The_game_window.surface.blit(data_print,(The_field.field_bl_window [0] + x_shift, The_field.field_bl_window[1] + The_game_window.menu_line_spacing + shift_vertikal ))
            shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing

        x_shift = x_shift + 100
        shift_vertikal = 0







# tisk nastaveni /hodnot balonu (uzito pro kontrolu funkci)
def f_print_ball_details(The_game_window,The_field,ball,list_of_ingamers):
    shift_vertikal = 0
    list_of_tags = ["angle: ","owner: ","velocty: ","site: "]
    list_of_data =[str(round(ball.path_target)), \
                   str(ball.owner), \
                   str(ball.velocity), \
                   str(ball.field_site) ]


    for data_index in range (0,len(list_of_data)):
        data = MenuFont.render(  list_of_tags[data_index] + list_of_data[data_index]   , 1, grey)
        The_game_window.surface.blit(data,(The_field.field_bl_window [0], The_field.field_bl_window[1] + The_game_window.menu_line_spacing + shift_vertikal ))
        shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing



# tisk uvitaci plochy
def draw_weclome(The_game_window):
    if The_game_window.language == "CZ":
        test = WelcomeFont.render('Flatball vitejte', 1, grey)
    else:
        test = WelcomeFont.render('Flatball welcome', 1, grey)

    The_game_window.surface.blit(test,(The_game_window.window_width * 0.4 , The_game_window.window_height * 0.3))





# pomocna funkce, pythagorovo pravidlo
def pythagoras_distance (location_1,location_2):                                                                            #stejna funkce v 2 modulech Zkontroluj
    ingamer_adjescent =  abs (location_1[0]  -  location_2[0])
    ingamer_opposite =  abs (location_1[1] -  location_2[1])
    ingamer_hypotensue = math.sqrt(ingamer_adjescent **2 + ingamer_opposite **2)

    return ingamer_hypotensue
