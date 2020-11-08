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

#pygame modul
pygame.init()
from pygame.locals import *

MenuFont = pygame.font.SysFont("Arial", 18)
MenuFont_heading = pygame.font.SysFont("Arial", 30)
WelcomeFont = pygame.font.SysFont("Arial", 40)



# --------------------------MENU-----------------------
def draw_main_menu(The_game_window):

    # vyber jazyka cz/en
    if The_game_window.language == "CZ":
        menu_list = ["START TEST GAME " ,"PAUSE TEST GAME","RESET TEST GAME","ULOZ input DATA","----------------------","TRENER", "  -Team management"  , "  -Stats"  ,"  -Trening  " , \
                    "ROZHODCI ",  "  -Delka utkani", "  -Potvrdit teamy ", "  -Nastaveni hriste ","  -Novy zapas", "  -pcXpc","  -pcXuzivatel" , \
                    "NASTAVENI ","  -Jazyk / Language", "  -Velikost okna",\
                    "LAB ", "  -zapnout lab mod","  -vypnout grafiku" , \
                    "NAPOVEDA "]
    else:
        menu_list = ["TRENER " ,  "  -Team management"  , "  -Stats"  ,"  -Trening  " , \
                    "REFF ",  "  -Delka utkani", "  -Potvrdit teamy ", "  -Nastaveni hriste ","  -Novy zapas", "  -pcXpc","  -pcXuzivatel" , \
                    "SETTINGS ", "  -Velikost okna",\
                    "LAB ", "  -zapnout lab mod","  -vypnout grafiku" , \
                    "HELP "]

    # menu nadpis
    menu_heading = "GAME MENU"
    menu_menu_heading_pages = MenuFont_heading.render(menu_heading, 1, green_field)
    The_game_window.surface.blit(menu_menu_heading_pages,(The_game_window.game_menu_x_start, 0.25 *The_game_window.menu_line_spacing))

    # Loop pro vypsani celeho menu
    for menu_loop in range(0,len(menu_list)):
        menu_moves_pages = MenuFont.render(menu_list[menu_loop], 1, grey)
        The_game_window.surface.blit(menu_moves_pages,(The_game_window.game_menu_x_start, menu_loop *  The_game_window.menu_line_spacing + The_game_window.heading_shift))



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
    line_selected = math.ceil ((position_clicked[1]- The_game_window.heading_shift) / The_game_window.menu_line_spacing   )
    if  line_selected == 1:
        #ref
        list_of_ingamers[0].start_test_match (The_game_window,The_field,list_of_ingamers,True)
        screen = 4
    elif  line_selected == 2:
        for no_of_ingamers in range (2 , len(list_of_ingamers)):
            list_of_ingamers[no_of_ingamers].game_status = "pause"
        screen = 4
    elif  line_selected == 3:
        for no_of_ingamers in range (2 , len(list_of_ingamers)):
            list_of_ingamers[no_of_ingamers].game_status = "pause"
        list_of_ingamers[0].restart_players(The_game_window,The_field,list_of_ingamers)
        screen = 4
    elif  line_selected == 4:
        #print (list_of_ingamers[3].team_coach.data)
        list_of_ingamers[3].team_coach.save_training()
        train_model(list_of_ingamers[3].team_coach.data_trening, list_of_ingamers[3].team_coach.data_labels , \
                    list_of_ingamers[3].team_coach.data_trening, list_of_ingamers[3].team_coach.data_labels )   #testu trening data sou stejny jak test data
        list_of_ingamers[3].team_coach.data_trening = []
        list_of_ingamers[3].team_coach.data_labels = []
        print_model_values("model.h5")
                                                                                #TESTY
        screen = 4


    #DODELAT MENU
    # vrati jaky screen se ma zobrazit
    return screen




# -------------------------------------------SCREENS---------------------------------------------------

# tisk score
def f_print_score(score,The_game_window,The_field):
    show_score = WelcomeFont.render(str(score), 1, grey)
    The_game_window.surface.blit(show_score,(The_field.field_bl_window [0], The_field.field_bl_window[1] + The_game_window.menu_line_spacing ))

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


#test prints
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
