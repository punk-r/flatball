import pygame
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

# fonty
TestFont = pygame.font.SysFont("Arial", 5)
MenuFont = pygame.font.SysFont("Arial", 18)
MenuFont_heading = pygame.font.SysFont("Arial", 30)
WelcomeFont = pygame.font.SysFont("Arial", 40)

#--------------------------------------------------------------------------------------------class buttons
# trida pro tlacika
class button():

    def __init__(self):
        self.number = 0         # id tlacitka
        self.x_corner = 0       # souradnice
        self.y_corner = 0
        self.size = [10,10]     # velikost tlacitka: lenght, hight
        self.name ='n'          # popisek (text) tlacitka
        self.graphic = "notset" # zatim nepouzito priprava pro pixel art
        self.frame = False      # pravidla zobrazeni ramecku

    # nastaveni tlacitka
    def set_button_name_number (self,name,number):
        self.name  = name
        self.number = number

    # kontrola kliku na tlacitko
    def is_mouse_over_button (self,mouse_position,screen_ID_lower_screen):
        decision = "nomatch"  # error hodnota
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        screen_ID = screen_ID_lower_screen[0]
        lower_screen_ID = screen_ID_lower_screen[1]

        if mouse_x > self.x_corner   and mouse_x < self.x_corner  + self.size[0]:
            if mouse_y > self.y_corner   and mouse_y  <  self.y_corner  + self.size[1] :
                decision = self.number

                # kontrola pro 2 tlacitka na stejnem miste v ruznych SCREENS
                # > 1 znamena button neni z hlavniho menu
                if  decision > 1:
                    if trunc(decision) == screen_ID:
                        decision == self.number
                    else:
                        if decision == 15.1:
                            decision = 15.1
                        else:
                            if trunc(decision) == 21 and  screen_ID == screens.teammanagement.value:
                                decision == self.number
                            else:
                                decision = "nomatch"


        return decision


# --------------------------MENU-----------------------
# vytvoreni instanci tlacitek
# tlacitka pro ostatni volby
def create_buttons_instances(The_game_window,The_field):

    # popisky(jmena) tlacitek, cesky/anglicky
    if The_game_window.language == "CZ":

        menu_list = ["TRENER","  -Management domaci","  -Trening  ","  -Management hoste","  -Stats", \
                    "ROZHODCI ",  "  -Delka utkani", "  -Potvrdit teamy ", "  -Nastaveni hriste ","  -Zpet na zapas",  \
                    "NASTAVENI ","  -Language / Jazyk", "  -Velikost okna",\
                    "LAB ", "  -zapnout lab mod","  -vypnout grafiku" , \
                    "Napoveda "]

        team_management_buttons = ["Smazat hrace" ,"Kopirovat hrace","vlozit hrace","un/select team","Ulozit team"]
        edit_player = [" CH1 "  ," CH2 "  ," CH3 "  ," CH4 "  ," CH5 "  ," CH6 "   ]
        team_managementaway_buttons = ["un/select team", ]
        trening_buttons = ["potvrdd hrace","MN stat trng h/h" ,"MN dyn trng h/ai ", " AUT starttrenng ai/ai"]
        confirm_teams_for_game = ["H/AI" , "AI/H", "AI/AI","zacithru", "ukoncit rozehranou hru"]
        reff_at_game_buttons = ["pause", "unpause"," 2 "," 3 "," 4 "]
        back_to_menu = ["MENU"]

    else:
        menu_list = ["COACH " ,  "  -Team management"  , "  -Stats"  ,"  -Training  " , \
                    "REFF ",  "  -Match lenght", "  -Teams for game  ", "  -Field settings ","  -back to game",  \
                    "SETTINGS ","  -Jazyk / Language", "  -Resolution",\
                    "LAB ", "  -Lab mode on/off","  -Graphic on/off" , \
                    "HELP "]

        team_management_buttons = ["Smazat hrace" ,"Kopirovat hrace","vlozit hrace","???","Ulozit team"]
        edit_player = [" CH1 "  ," CH2 "  ," CH3 "  ," CH4 "  ," CH5 "  ," CH6 "   ]
        trening_buttons = ["potvrdd hrace","MN stat trng h/h" ,"MN dyn trng h/ai ", " AUT starttrenng ai/ai"]
        confirm_teams_for_game = ["H/AI" , "AI/H", "AI/AI","zacithru", "ukoncit rozehranou hru"]
        reff_at_game_buttons = ["pause", "play"," 2 "," 3 "," 4 "]
        back_to_menu = ["MENU"]

    '''
    SCREENS ENUMS:
        welcome = 0  coach = 1  teammanagement = 2  teammanagementedit = 21  stats = 3  trening = 4  intrening = 41
        reff = 5  matchlenght = 6  teamsconfirmation =7  ingame = 71  fieldsettings = 8  backtogame = 9
        settings = 10  language = 11  vindowsize = 12  lab = 13  labmodswitcher = 14
        help = 15

    index  0 pro menu ktere ma 5 zakladnich kategorii    0.1 trener/ 0.2 rozhotci/ 0.3 nastaveni/ 0.4 lab/ 0.5 napoveda
    ostatni tlacitka maji index dle screen enum kde jsou zobrazeny
    '''
    buttons_ids = [ 0.10, 0.11, 0.12, 0.13, 0.14, 0.20, 0.21, 0.22, 0.23, 0.24, 0.30, 0.31, 0.32, 0.40 , 0.41, 0.42, 0.50, \
                    2.10, 2.20, 2.30, 2.40, 2.50, \
                    21.10, 21.20, 21.30, 21.40, 21.50, 21.60, \
                    22.10, \
                    4.10, 4.20, 4.30 , 4.40, \
                    7.10, 7.20, 7.30, 7.40, 7.50, \
                    71.10, 71.20, 71.30, 71.40, 71.50, \
                    15.10 ]

    # tlacitka krom menu
    other_buttns_list = team_management_buttons + edit_player +team_managementaway_buttons+ trening_buttons + \
                            confirm_teams_for_game + reff_at_game_buttons + back_to_menu
    # vsechny tlacitka
    buttons_names_list = menu_list + other_buttns_list
    lenght_menu = len (menu_list)
    lenght_mngmnt_buttons = len(team_management_buttons)
    lenght_ref_buttons = len(reff_at_game_buttons)
    lenght_confirm_teams_for_game = len(confirm_teams_for_game)

    list = []                       # list vsech instanci tridy button pro hru
    ref_buttons_counter = 0         # pocitadlo tlacitek rozhodtico v prubehu hry
    mngmnt_buttons_counter = 0      # pocitadlo tlacitek team management stranky
    mngmntedit_buttons_counter = 0
    trening_buttons_counter = 0     # pocitadlo tlacitek trenovani teamu
    choose_teams_counter = 0        # pocitadlo tlacitek vyberu teamu do hry
    mngmntaway_buttons_counter = 0

    # generovani tlacitek
    for generating_buttons_loop in range (0,len(buttons_names_list)):
        new_button = button()
        new_button.set_button_name_number (buttons_names_list [generating_buttons_loop] ,buttons_ids[generating_buttons_loop])
        new_button.frame = True
        list.append(new_button)

        ## nastaveni vygenerovaneho tlacitka
        # menu tlacitka
        if trunc(buttons_ids[generating_buttons_loop]) == 0 :
            new_button.frame = False
            new_button.size = [150,18]
            new_button.x_corner = The_game_window.game_menu_x_start
            new_button.y_corner = The_game_window.heading_shift + generating_buttons_loop  * The_game_window.menu_line_spacing

        #  team management tlacitka
        elif trunc(buttons_ids[generating_buttons_loop]) ==  screens.teammanagement.value:
            new_button.size = [100,40]
            new_button.x_corner = The_game_window.game_menu_x_end + The_game_window.mngmt_shift_from_menu +  \
                                     mngmnt_buttons_counter * The_game_window.mngmt_column_width
            new_button.y_corner =  The_game_window.heading_shift +(1+ The_game_window.team_detail_lines ) *  \
                                    The_game_window.mngmt_text_ratio *  The_game_window.menu_line_spacing
            mngmnt_buttons_counter = mngmnt_buttons_counter + 2

        #  team managementaway
        elif trunc(buttons_ids[generating_buttons_loop]) ==  screens.teammanagementaway.value:
            new_button.size = [100,40]
            new_button.x_corner = The_game_window.game_menu_x_end + The_game_window.mngmt_shift_from_menu +  \
                                     mngmntaway_buttons_counter * The_game_window.mngmt_column_width
            new_button.y_corner =  The_game_window.heading_shift +(1+ The_game_window.team_detail_lines ) *  \
                                    The_game_window.mngmt_text_ratio *  The_game_window.menu_line_spacing
            mngmntaway_buttons_counter = mngmntaway_buttons_counter + 2


        #  team managementedit player tlacitka
        elif trunc(buttons_ids[generating_buttons_loop]) ==  screens.teammanagementedit.value:
            new_button.size = [100,40]
            new_button.x_corner = The_game_window.game_menu_x_end + The_game_window.mngmt_shift_from_menu +  \
                                     mngmntedit_buttons_counter * The_game_window.mngmt_column_width
            new_button.y_corner =  The_game_window.game_menu_y_end + The_game_window.heading_shift *2
            mngmntedit_buttons_counter = mngmntedit_buttons_counter + 2

        # reff behem hry
        elif trunc(buttons_ids[generating_buttons_loop]) == screens.ingame.value:
            new_button.size = [60,40]
            new_button.x_corner = The_field.field_bl_corner [0] +  ref_buttons_counter * The_game_window.mngmt_column_width
            new_button.y_corner =  The_field.field_bl_corner[1] + 3*The_game_window.menu_line_spacing
            ref_buttons_counter = ref_buttons_counter + 1

        # vyber teamu do hry
        elif trunc(buttons_ids[generating_buttons_loop]) == screens.teamsconfirmation.value:
            new_button.size = [60,40]
            new_button.x_corner = The_game_window.game_menu_x_end + The_game_window.mngmt_shift_from_menu + \
                                  choose_teams_counter * The_game_window.mngmt_column_width
            new_button.y_corner =  The_game_window.game_menu_y_end + The_game_window.heading_shift *2
            choose_teams_counter = choose_teams_counter + 1



        # trenovani teamu
        elif trunc(buttons_ids[generating_buttons_loop]) == screens.trening.value:
            new_button.size = [100,40]
            new_button.x_corner = The_game_window.game_menu_x_end + The_game_window.mngmt_shift_from_menu + \
                                     trening_buttons_counter * The_game_window.mngmt_column_width
            new_button.y_corner =  The_game_window.heading_shift +(1+ The_game_window.team_detail_lines ) *  \
                                    The_game_window.mngmt_text_ratio *  The_game_window.menu_line_spacing
            trening_buttons_counter = trening_buttons_counter + 2

        # zobrazeni menu
        elif trunc(buttons_ids[generating_buttons_loop]) == screens.help.value:
            new_button.frame = True
            new_button.size = [100,40]
            new_button.x_corner = 0
            new_button.y_corner = 0


    # vraci list vsech tlacitek
    return list

# tisk urciteho n-tlacitka z seznamu tlacitek
def draw_button_No(The_game_window,button_no):
    # pokud tlacitko nema grafiku(obrazek) vykresli se jako text s rameckem
    if The_game_window.buttons[button_no].graphic == "notset":
        button_name = MenuFont.render(The_game_window.buttons[button_no].name, 1, grey)
        The_game_window.surface.blit(button_name,(The_game_window.buttons[button_no].x_corner, The_game_window.buttons[button_no].y_corner))

        # TESTY kontrola vykreslovani
        test_print_x = TestFont.render("x", 1, red)
        The_game_window.surface.blit(test_print_x,(The_game_window.buttons[button_no].x_corner, The_game_window.buttons[button_no].y_corner))

        # ramecek tlacitka
        # pozice_x,pozive_y,delka,vyska
        if The_game_window.buttons[button_no].frame == True :
            '''
            rectangle_details = [The_game_window.buttons[button_no].x_corner, \
                                The_game_window.buttons[button_no].y_corner, \
                                The_game_window.buttons[button_no].size[0], \
                                The_game_window.buttons[button_no].size[1]]

            pygame.draw.rect(The_game_window.surface, grey, rectangle_details  ,  2)
            '''

            # kriz
            cross_height = 10
            cross_lenght = 20

            pygame.draw.lines(The_game_window.surface,  grey, True, ((The_game_window.buttons[button_no].x_corner -2, The_game_window.buttons[button_no].y_corner + 10  ) , \
                                                                     (The_game_window.buttons[button_no].x_corner -2, The_game_window.buttons[button_no].y_corner +25  )), 1)

            pygame.draw.lines(The_game_window.surface,  grey, True, ((The_game_window.buttons[button_no].x_corner -7,The_game_window.buttons[button_no].y_corner + 20) , \
                                                                     (The_game_window.buttons[button_no].x_corner +20,The_game_window.buttons[button_no].y_corner + 20 )), 1)





# vykresli hlavni menu
def draw_main_menu(The_game_window):
    # pocet tlacitek hlavniho menu
    main_menu_buttons = 17

    # menu nadpis
    menu_heading = "GAME MENU"
    menu_menu_heading_pages = MenuFont_heading.render(menu_heading, 1, green_field)
    The_game_window.surface.blit(menu_menu_heading_pages,(The_game_window.game_menu_x_start, 0.25 *The_game_window.menu_line_spacing))

    # Loop pro vypsani celeho menu
    for menu_loop in range(0,main_menu_buttons):
        draw_button_No(The_game_window, menu_loop)

        if menu_loop <10:
            # TESTY kontrola vykreslovani
            test_print_x = TestFont.render("x", 1, red)
            The_game_window.surface.blit(test_print_x,(The_game_window.game_menu_x_start, \
                                                        menu_loop * The_game_window.menu_line_spacing + The_game_window.heading_shift))


'''
PLAN VYPRACOVANI
Rozdeleni okna aplikace 4x ruzne plochy
 ___________________         ___________________
| 1 | 3             |       | 4                 |
|   |               |       |                   |
|___|_______________|   =>  |___________________|
| 2                 |       | 2                 |
|___________________|       |___________________|

'''

# okno rozdeleno na 3 casti
def draw_menu_lines_ID_3(The_game_window):
    #rozdeleni obrazovky aplikace
    pygame.draw.rect(The_game_window.surface, white , (0, 0, The_game_window.window_width, The_game_window.window_height),  1)
    pygame.draw.lines(The_game_window.surface,  grey, True, ((The_game_window.game_menu_x_end,0 ) , \
                                                             ( The_game_window.game_menu_x_end  ,The_game_window.game_menu_y_end )), 1)
    pygame.draw.lines(The_game_window.surface,  grey, True, ((0 ,The_game_window.game_menu_y_end ) ,  \
                                                             (The_game_window.window_width ,The_game_window.game_menu_y_end)), 1)

# zapas => menu je ukryto - okno rozdeleno na 2 casti
def draw_menu_lines_ID_4(The_game_window):
    #rozdeleni obrazovky aplikace
    pygame.draw.rect(The_game_window.surface, white , (0 ,0 ,The_game_window.window_width, The_game_window.window_height ),  1)
    pygame.draw.lines(The_game_window.surface,  grey, True, ((0 ,The_game_window.game_menu_y_end ) ,  \
                                                             (The_game_window.window_width ,The_game_window.game_menu_y_end)), 1)


# volani funkce/metody dle volby z menu(tlacitek)
def f_menu_selected(position_clicked,The_game_window,The_field,The_reff,screen_ID_lower_screen):
    print (position_clicked)
    print ( trunc(position_clicked))
    screen = screen_ID_lower_screen[0]
    lower_screen = 0
    button_selected = position_clicked

    ## tlacitka zacinajici indexem 0 => hlavni menu
    if  trunc(button_selected) == 0 and The_game_window.menu_on_screen == True:

        # trener
        if  button_selected == 0.10:  #testy
            print("gamestatsus"  ,"teamtype"   ,"team"  )
            print(vars(The_reff))
            for no_of_ingamers in range (1,len(The_reff.list_of_ingamers)):#testy
                print(The_reff.list_of_ingamers[no_of_ingamers].game_status, \
                The_reff.list_of_ingamers[no_of_ingamers].team_type , \
                The_reff.list_of_ingamers[no_of_ingamers].team )

        elif  button_selected == 0.11 :
            The_reff.coach_team_A.reset_selected_slot_team_management()
            screen = screens.teammanagement.value
        elif  button_selected == 0.12 :
            The_reff.coach_team_A.reset_selected_slot_team_management()
            screen = screens.trening.value
        elif  button_selected == 0.13 :
            The_reff.coach_team_B.reset_selected_slot_team_management()
            screen = screens.teammanagementaway.value
        elif  button_selected == 0.14 :
            screen = screens.stats.value
        # reff
        elif  button_selected == 0.20 : #testy
            The_reff.teams_for_game  = ["A","B","H","AI"]
            The_reff.start_match (The_game_window,The_field,True)
            The_game_window.menu_on_screen = False
            screen = screens.ingame.value

        elif  button_selected == 0.21 :
            pass
        elif  button_selected == 0.22 :
            The_reff.coach_team_A.loaded_teams_xml[0][0][2] = "selected"
            The_reff.coach_team_A.loaded_teams_xml[1][0][2] = "selected"
            if The_reff.count_selected_teams() != 2:
                screen = screens.error.value                                        #oprav na   draw_teams_selection_error
            else:
                The_reff.load_teams_for_game_to_slot()
                screen = screens.teamsconfirmation.value

        elif  button_selected == 0.23 :
            pass
        elif  button_selected == 0.24 :
            if The_reff.game_type != "none":
                screen = screens.ingame.value # zpet na zapas pokud nebyl ukoncen
                The_game_window.menu_on_screen = False
        # nastaveni
        elif  button_selected == 0.30 :
            pass
        elif  button_selected == 0.31 :
            The_game_window.swap_language()
            The_game_window.buttons = create_buttons_instances(The_game_window,The_field)
        elif  button_selected == 0.32 :
            #The_game_window.set_window_size([800,400])                                # testovaci hodnoty
            #The_field.set_field(The_game_window)
            pass
        # lab mode
        elif  button_selected == 0.40 :
            pass
        elif  button_selected == 0.41 :
            pass
        elif  button_selected == 0.42 :
            pass
        elif  button_selected == 0.5 :#napoveda
            The_game_window.menu_on_screen = False
            screen = screens.help.value

    ## tlacitka  hry pro reff
    if trunc(button_selected) == screens.ingame.value :
        if  button_selected == 71.10 :
            The_reff.pause_game(self,The_game_window,The_field)
            screen = screens.ingame.value
        if  button_selected == 71.20 :
            The_reff.unpause_game(The_game_window,The_field)
        if  button_selected == 71.30 :#testy
            print("gamestatsus"  ,"teamtype"   ,"team"  )
            for no_of_ingamers in range (1,len(The_reff.list_of_ingamers)):#testy
                print(The_reff.list_of_ingamers[no_of_ingamers].game_status, \
                The_reff.list_of_ingamers[no_of_ingamers].team_type , \
                The_reff.list_of_ingamers[no_of_ingamers].team )


    ## tlacitka  team management
    if  trunc(button_selected) == screens.teammanagement.value  and screen == screens.teammanagement.value:
        if  button_selected == 2.10 :
            The_reff.coach_team_A.delete_player_from_slot()
        if  button_selected == 2.20 :
            The_reff.coach_team_A.copy_player_from_slot()
        if  button_selected == 2.30 :
            The_reff.coach_team_A.paste_player_from_other_slot()
        if  button_selected == 2.40 :
            The_reff.coach_team_A.choose_team_from_selection()
        if  button_selected == 2.50 :
            The_reff.coach_team_A.save_team_from_teammngmt_table()

    ## tlacitka  team managementedit
    if  trunc(button_selected) == screens.teammanagementedit.value  and screen == screens.teammanagement.value:
        if  button_selected == 21.10 :
            The_reff.coach_team_A.edit_player_position("ahoj")
        if  button_selected == 21.20 :
            The_reff.coach_team_A.edit_player_position("GK")
        if  button_selected == 21.30 :
            pass
        if  button_selected == 21.40 :
            pass
        if  button_selected == 21.50 :
            pass

    ## tlacitka  team management
    if  trunc(button_selected) == screens.teammanagementaway.value  and screen == screens.teammanagementaway.value:
        if  button_selected == 22.10 :
            The_reff.coach_team_B.choose_team_from_selection()


    ## tlacitka  vyber teamu do hry
    if  trunc(button_selected) == screens.teamsconfirmation.value and screen == screens.teamsconfirmation.value:
        if  button_selected == 7.10 :
            The_reff.set_teams_type_for_game("H/AI")
        if  button_selected == 7.20 :
            #The_reff.set_teams_type_for_game("AI/H")
            pass
        if  button_selected == 7.30 :
            #The_reff.set_teams_type_for_game("AI/AI")
            pass
        if  button_selected == 7.40 :
            #hra lze zacit pouze s 2 teamy
            if  The_reff.count_selected_teams() == 2:
                The_reff.start_match (The_game_window,The_field,True)
                The_game_window.menu_on_screen = False
                screen = screens.ingame.value
        if  button_selected == 7.50 :#reset  pro reff ze muze zacit nova hra

            The_reff.set_game_status_to_self("none")
            print(The_reff.game_type)
            The_reff.set_game_status_to_players()


    ## tlacitka  vyber teamu do treningu
    if  trunc(button_selected) == screens.trening.value  and screen == screens.trening.value:
        start_training_check = [False,"empty"]

        if  button_selected == 4.10 :
            The_reff.coach_team_A.copy_player_from_slot() #ulozi hrace do bufferu

        # trening h/h
        if  button_selected == 4.20 :
            The_reff.set_teams_type_for_game("H/H")
            start_training_check = The_reff.start_training()
            The_reff.set_teams_type_for_game("H/H")
            print("start_training_check", start_training_check)
        # trening h/AI
        if  button_selected == 4.30 :
            #start_training_check =The_reff..start_training()
            #The_reff.set_teams_type_for_game("H/AI")
            pass
        # trening AI/AI
        if  button_selected == 4.40 :
            #start_training_check = The_reff..start_training()
            #The_reff.set_teams_type_for_game("AI/AI")
            pass
        # vyhodnoceni
        if start_training_check[0] == True:
            # prvni team je trenovany
            The_reff.start_match(The_game_window,The_field,True)
            The_reff.set_game_status_to_players()

            for ingamers_loop in range (1,len(The_reff.list_of_ingamers)):
                # nastavi trenovaneho hrace
                if The_reff.list_of_ingamers[ingamers_loop].ID == start_training_check[1]:
                    The_game_window.menu_on_screen = False
                    The_reff.list_of_ingamers[ingamers_loop].set_selected(True)
                    The_reff.list_of_ingamers[ingamers_loop].team_coach.active_trening = True
                    The_reff.list_of_ingamers[ingamers_loop].team_coach.reset_training_arrays()
            screen = screens.intrening.value

    ## zobrazeni schovaneho menu
    if  trunc(button_selected) == screens.help.value :
        if  button_selected == 15.10:
            The_game_window.menu_on_screen = True
            if screen == screens.help.value:
                screen = screens.welcome.value

    # vraci novou obrazovku dle menu nebo tlacitek                                                                                       # spustit hru
    return [screen,lower_screen]
