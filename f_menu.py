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
    def is_mouse_over_button (self,mouse_position,screen_ID):
        decision = "nomatch"  # error hodnota
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]

        if mouse_x > self.x_corner   and mouse_x < self.x_corner  + self.size[0]:
            if mouse_y > self.y_corner   and mouse_y  <  self.y_corner  + self.size[1] :
                decision = self.number

                # kontrola pro 2 tlacitka na stejnem miste v ruznych SCREENS
                # > 1 znamena button neni z hlavniho menu
                if  decision > 1:
                    if trunc(decision) == screen_ID:
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

        menu_list = ["TRENER", "  -Team management"  , "  -Stats"  ,"  -Trening  " , \
                    "ROZHODCI ",  "  -Delka utkani", "  -Potvrdit teamy ", "  -Nastaveni hriste ","  -Zpet na zapas",  \
                    "NASTAVENI ","  -Language / Jazyk", "  -Velikost okna",\
                    "LAB ", "  -zapnout lab mod","  -vypnout grafiku" , \
                    "Napoveda "]

        team_management_buttons = ["Smazat hrace" ,"Kopirovat hrace","vlozit hrace","Edit player","Ulozit team"]
        reff_at_game_buttons = ["pause tr", " 1 "," 2 "," 3 "," 4 "]
        confirm_teams_for_game = ["H/AI" , "AI/H", "AI/AI","zacithru", "ukoncit rozehranou hru"]
        trening_buttons = ["potvrdd hrace","MN stat trng h/h" ,"MN dyn trng h/ai ", " AUT starttrenng ai/ai"]
        back_to_menu = [" "]

    else:
        menu_list = ["COACH " ,  "  -Team management"  , "  -Stats"  ,"  -Training  " , \
                    "REFF ",  "  -Match lenght", "  -Teams for game  ", "  -Field settings ","  -back to game",  \
                    "SETTINGS ","  -Jazyk / Language", "  -Resolution",\
                    "LAB ", "  -Lab mode on/off","  -Graphic on/off" , \
                    "HELP "]

        team_management_buttons = ["Delete player" ,"Copy player","Paste player","Edit player","Save team"]
        reff_at_game_buttons = ["Un/Pause game", " 1 "," 2 "," 3 "," 4 "]
        confirm_teams_for_game = [ "H / AI" , "AI / H", "AI / AI","Start game", "end started game"]
        trening_buttons = ["Confirm player","Game H x H" ,"Game H x AI ", " Game AI x AI "]
        back_to_menu = [" "]


    # index  0 pro menu ktere ma 5 zakladnich rozdeleni trener/rozhotci/nastaveni/lab/napoveda
    # ostatni index je dle screen_ID: 4 je hra, 5 je team management, 6 vyber teamu do hry
    buttons_ids = [ 0.10, 0.11, 0.12, 0.13, 0.20, 0.21, 0.22, 0.23, 0.24, 0.30, 0.31, 0.32, 0.40 , 0.41, 0.42, 0.50, \
                    5.10, 5.20, 5.30, 5.40, 5.50, 4.10, 4.20, 4.30, 4.40, 4.50, 6.10, 6.20, 6.30 , 6.40, 6.50, 7.10, 7.20, 7.30, 7.40, 9.10]

    # tlacitka krom menu
    other_buttns_list = team_management_buttons + reff_at_game_buttons + confirm_teams_for_game + trening_buttons + back_to_menu
    # vsechny tlacitka
    buttons_names_list = menu_list + other_buttns_list
    lenght_menu = len (menu_list)
    lenght_mngmnt_buttons = len(team_management_buttons)
    lenght_ref_buttons = len(reff_at_game_buttons)
    lenght_confirm_teams_for_game = len(confirm_teams_for_game)

    list = []                       # list vsech instanci tridy button pro hru
    ref_buttons_counter = 0         # pocitadlo tlacitek rozhodtico v prubehu hry
    mngmnt_buttons_counter = 0      # pocitadlo tlacitek team management stranky
    trening_buttons_counter = 0     # pocitadlo tlacitek trenovani teamu
    choose_teams_counter = 0        # pocitadlo tlacitek vyberu teamu do hry
    buttons_vertical_counter = 0    # tlacitka pro vyber pro hru

    # generovani tlacitek
    for generating_buttons_loop in range (0,len(buttons_names_list)):
        new_button = button()
        new_button.set_button_name_number (buttons_names_list [generating_buttons_loop] ,buttons_ids[generating_buttons_loop])
        new_button.frame = True
        list.append(new_button)

        ## nastaveni vygenerovaneho tlacitka
        # menu tlacitka
        if buttons_ids[generating_buttons_loop] < 1 :
            new_button.frame = False
            new_button.size = [150,18]
            new_button.x_corner = The_game_window.game_menu_x_start
            new_button.y_corner = The_game_window.heading_shift + generating_buttons_loop  * The_game_window.menu_line_spacing

        #  team management tlacitka
        elif buttons_ids[generating_buttons_loop] < 6 and buttons_ids[generating_buttons_loop] > 5:
            new_button.size = [100,40]
            new_button.x_corner = The_game_window.mngmt_shift_from_menu + The_field.field_bl_window[0] + \
                                     ref_buttons_counter * The_game_window.mngmt_column_width
            new_button.y_corner =  The_game_window.heading_shift +(1+ The_game_window.team_detail_lines ) *  \
                                    The_game_window.mngmt_text_ratio *  The_game_window.menu_line_spacing
            ref_buttons_counter = ref_buttons_counter + 2

        # reff behem hry
        elif buttons_ids[generating_buttons_loop] < 5 and buttons_ids[generating_buttons_loop] > 4:
            new_button.size = [60,40]
            new_button.x_corner = The_game_window.mngmt_shift_from_menu +  mngmnt_buttons_counter * The_game_window.mngmt_column_width
            new_button.y_corner =  The_field.field_bl_window[1] + The_game_window.menu_line_spacing
            mngmnt_buttons_counter = mngmnt_buttons_counter + 1

        # vyber teamu do hry
        elif buttons_ids[generating_buttons_loop] < 7 and buttons_ids[generating_buttons_loop] > 6:
            new_button.size = [60,40]
            if buttons_vertical_counter < 3:
                new_button.x_corner = The_field.field_bl_window[0] + The_game_window.mngmt_shift_from_menu + \
                                      choose_teams_counter * The_game_window.mngmt_column_width/2
                new_button.y_corner =  The_field.field_bl_window[1] + The_game_window.heading_shift *2
                buttons_vertical_counter = buttons_vertical_counter + 1
                choose_teams_counter = choose_teams_counter + 1

            else:
                # spust hru
                new_button.x_corner = The_field.field_bl_window[0] + (choose_teams_counter + 3 )* The_game_window.mngmt_column_width
                new_button.y_corner =  The_field.field_bl_window[1] + The_game_window.heading_shift *2
                choose_teams_counter = choose_teams_counter + 2 #utvori vetsi mezeru


        # trenovani teamu
        elif buttons_ids[generating_buttons_loop] < 8 and buttons_ids[generating_buttons_loop] > 7:
            new_button.size = [100,40]
            new_button.x_corner = The_field.field_bl_window[0] + The_game_window.mngmt_shift_from_menu + \
                                     trening_buttons_counter * The_game_window.mngmt_column_width
            new_button.y_corner =  The_game_window.heading_shift +(1+ The_game_window.team_detail_lines ) *  \
                                    The_game_window.mngmt_text_ratio *  The_game_window.menu_line_spacing
            trening_buttons_counter = trening_buttons_counter + 2

        elif buttons_ids[generating_buttons_loop] < 10 and buttons_ids[generating_buttons_loop] > 9:
            new_button.frame = True
            new_button.size = [200,200]
            new_button.x_corner = 0
            new_button.y_corner = 0


    # vraci list vsech tlacitek
    return list

# tisk urciteho n-tlacitka z seznamu tlacitek
def draw_other_buttons(The_game_window,button_no):
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
    main_menu_buttons = 16

    # menu nadpis
    menu_heading = "GAME MENU"
    menu_menu_heading_pages = MenuFont_heading.render(menu_heading, 1, green_field)
    The_game_window.surface.blit(menu_menu_heading_pages,(The_game_window.game_menu_x_start, 0.25 *The_game_window.menu_line_spacing))

    # Loop pro vypsani celeho menu
    for menu_loop in range(0,main_menu_buttons):
        draw_other_buttons(The_game_window, menu_loop)

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
def draw_menu_lines_ID_3(The_game_window,The_field):
    #rozdeleni obrazovky aplikace
    pygame.draw.rect(The_game_window.surface, white , (0, 0, The_game_window.window_width, The_game_window.window_height),  1)
    pygame.draw.lines(The_game_window.surface,  grey, True, ((The_field.field_bl_window[0],0 ) , \
                                                             (The_field.field_bl_window[0] , The_field.field_bl_window[1])), 1)
    pygame.draw.lines(The_game_window.surface,  grey, True, ((0 ,The_field.field_bl_window[1] ) ,  \
                                                             (The_game_window.window_width ,The_field.field_bl_window[1])), 1)

# zapas => menu je ukryto - okno rozdeleno na 2 casti
def draw_menu_lines_ID_4(The_game_window,The_field):
    #rozdeleni obrazovky aplikace
    pygame.draw.rect(The_game_window.surface, white , (0 ,0 ,The_game_window.window_width, The_game_window.window_height ),  1)
    pygame.draw.lines(The_game_window.surface,  grey, True, ((0 ,The_field.field_bl_window[1] ) ,  \
                                                             (The_game_window.window_width ,The_field.field_bl_window[1])), 1)


# volani funkce/metody dle volby z menu(tlacitek)
def f_menu_selected(position_clicked,The_game_window,The_field,list_of_ingamers,screen_ID):
    print (position_clicked)
    screen = screen_ID
    button_selected = position_clicked
    The_reff = list_of_ingamers[0]

    ## tlacitka zacinajici indexem 0 => hlavni menu
    if  button_selected > 0 and  button_selected < 1 and screen != 9:

        # trener
        if  button_selected == 0.10:
            print(vars(The_reff)) #testy
        elif  button_selected == 0.11 :
            The_reff.reset_selected_slot_team_management()
            screen = 5
        elif  button_selected == 0.12 :
            pass
        elif  button_selected == 0.13 :
            The_reff.reset_selected_slot_team_management()
            screen = 7
        # reff
        elif  button_selected == 0.20 :
            pass
        elif  button_selected == 0.21 :
            pass
        elif  button_selected == 0.22 :
            The_reff.reset_teams_buffer_for_game()
            screen = 6
        elif  button_selected == 0.23 :
            pass
        elif  button_selected == 0.24 :
            if The_reff.game_type != "none":
                screen = 4 # zpet na zapas pokud nebyl ukoncen
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
            screen = 9

    ## tlacitka zacinajici indexem 4 => screen 4 hra
    if  button_selected > 4 and  button_selected < 5:
        if  button_selected == 4.10 :
            for no_of_ingamers in range (2 , len(list_of_ingamers)):
                list_of_ingamers[no_of_ingamers].game_status = "pause"
            screen = 4
        if  button_selected == 4.20 :
            pass

    ## tlacitka zacinajici indexem 5 => screen 5 team management
    if  button_selected > 5 and  button_selected < 6 and screen_ID == 5:
        if  button_selected == 5.10 :
            The_reff.delete_player_from_slot()
            screen = 5
        if  button_selected == 5.20 :
            The_reff.copy_player_from_slot()
            screen = 5
        if  button_selected == 5.30 :
            The_reff.paste_player_from_other_slot()
            screen = 5
        if  button_selected == 5.40 :
            pass
        if  button_selected == 5.50 :
            The_reff.save_team_from_teammngmt_table()
            screen = 5

    ## tlacitka zacinajici indexem 6 => screen 6 vyber teamu do hry
    if  button_selected > 6 and  button_selected < 7 and screen_ID == 6:
        if  button_selected == 6.10 :
            The_reff.set_teams_type_for_game("H/AI")
        if  button_selected == 6.20 :
            #The_reff.set_teams_type_for_game("AI/H")
            pass
        if  button_selected == 6.30 :
            #The_reff.set_teams_type_for_game("AI/AI")
            pass
        if  button_selected == 6.40 :
            #hra lze zacit pouze s 2 teamy
            if  The_reff.count_selected_teams() == 2:
                The_reff.start_match (The_game_window,The_field,list_of_ingamers,True)
                screen = 4
        if  button_selected == 6.50 :#reset  pro reff ze muze zacit nova hra

            The_reff.set_game_status_to_self("none")
            print(The_reff.game_type)
            The_reff.set_game_status_to_players(list_of_ingamers)


    ## tlacitka zacinajici indexem 7 => screen 7 , vyber teamu do treningu
    if  button_selected > 7 and  button_selected < 8 and screen_ID == 7:
        start_training_check = [False,"empty"]

        if  button_selected == 7.10 :
            The_reff.copy_player_from_slot() #ulozi hrace do bufferu
            screen = 7

        # trening h/h
        if  button_selected == 7.20 :
            The_reff.set_teams_type_for_game("H/H")
            start_training_check = list_of_ingamers[0].start_training()
            The_reff.set_teams_type_for_game("H/H")

        # trening h/AI
        if  button_selected == 7.30 :
            #start_training_check = list_of_ingamers[0].start_training()
            #The_reff.set_teams_type_for_game("H/AI")
            pass
        # trening AI/AI
        if  button_selected == 7.40 :
            #start_training_check = list_of_ingamers[0].start_training()
            #The_reff.set_teams_type_for_game("AI/AI")
            pass
        # vyhodnoceni
        if start_training_check[0] == True:
            # prvni team je trenovany
            The_reff.start_match(The_game_window,The_field,list_of_ingamers,True)
            for ingamers_loop in range (2,len(list_of_ingamers)):
                # nastavi selected trenovaneho hrace
                if list_of_ingamers[ingamers_loop].ID == start_training_check[1]:
                    list_of_ingamers[ingamers_loop].set_selected(True)
                    list_of_ingamers[ingamers_loop].team_coach.active_trening = True
                    list_of_ingamers[ingamers_loop].team_coach.reset_training_arrays()
            screen = 8

    ## zobrazeni schovaneho menu
    if  button_selected > 9 and  button_selected < 10 and screen_ID == 9:
        if  button_selected == 9.10:
            screen = 3

    # vraci novou obrazovku dle menu nebo tlacitek                                                                                       # spustit hru
    return screen

# -------------------------------------------SCREENS---------------------------------------------------

# teams selection pro hru
def draw_teams_for_game(The_game_window,The_field,The_reff,list_of_ingamers):
    # hodnoty musi by ulozeny v 'window' aby slo vypocitat polohu mysi => spustit metodu/funkci

    lines = 13  # pocet zobrazenych radku
    column_width = 1.5 * The_game_window.mngmt_column_width
    teams_on_page = The_game_window.mngmt_teams_on_page + 2   # (+2) hostujici teamy
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
        note_1 = MenuFont.render('VOLBA HRY', 1, grey)
        note_2 = MenuFont.render('Teamy do hry ', 1, grey)
        table_headngs = ["team","trenovano" ,"trening" ,"prum skills" , "zapasu", "vyher", "vybrano",]
    else:
        page_heading = WelcomeFont.render('Choose teams for game', 1, grey)
        note_1 = MenuFont.render('Game settings:', 1, grey)
        note_2 = MenuFont.render('Games for the game:', 1, grey)
        table_headngs = ["Teams","note_a" ,"note_b" ,"note_c" , "note_d", "note_e", "selected"]

    # vypise pouze pokud jsou oba teamy vybrane
    if  The_reff.teams_for_game[0] == " " or  The_reff.teams_for_game[1] == " " :
        teams_chosen = WelcomeFont.render(  "_ vs _ "  , 1, grey)
    else:
        teams_chosen = WelcomeFont.render( The_reff.teams_for_game[0]  + " vs " + The_reff.teams_for_game[1]  , 1, grey)

    The_game_window.surface.blit(page_heading,( table_left  ,  0.1 * The_game_window.menu_line_spacing ))
    The_game_window.surface.blit(note_1,( table_left  , The_field.field_bl_window[1] +  2* The_game_window.menu_line_spacing ))
    The_game_window.surface.blit(note_2,( table_left + 2* column_width  , The_field.field_bl_window[1] +  2* The_game_window.menu_line_spacing ))
    The_game_window.surface.blit(teams_chosen,( table_left +( 2 *column_width ) , The_field.field_bl_window[1] +   The_game_window.menu_line_spacing *4 )) # 4 radku odsazeni

    ## Vykresleni tabulky
    # Rect(left, top, width, height)
    pygame.draw.rect(The_game_window.surface, red, ( table_left, table_top, \
                                                    columns * column_width, \
                                                    text_ratio * lines * The_game_window.menu_line_spacing),1)

    # radky
    shift = 0
    for row_loop in range (0,lines):
        shift = shift + text_ratio * The_game_window.menu_line_spacing
        pygame.draw.lines(The_game_window.surface, grey_lines, True,((table_left, table_top + shift), \
                                                                        (table_right, table_top + shift)), 1)

    # sloupce
    shift = 0
    for colmn_loop in range (0,columns):
        table_headngs_rendered = MenuFont.render(table_headngs[colmn_loop], 1, grey)
        The_game_window.surface.blit(table_headngs_rendered,( table_left + shift  + column_width/4  , table_top    )) # posun 1/4 sirka boxu
        shift = shift + column_width
        pygame.draw.lines(The_game_window.surface, grey_lines, True,((table_left + shift, table_top), \
                                                                     (table_left + shift, table_bottom )), 1)

    column_teams_shift =  text_ratio * The_game_window.menu_line_spacing
    player_line_shift = 0
    leter_shift_from_boarder = 5 #odsazeni od hran tabulky
    font_diference = 1   #rozdil mezi fontem a linkou

    # tisk teamu a hracu
    # domaci teamy 10 slotu , + 2 sloty hoste   => 12, jina barva pro vybrany team
    for teams_loop in range (0,12):
        team_name = The_reff.loaded_teams_xml[teams_loop][0][0]
        if team_name != "n":  # n prvni char z "none"

            color_team = grey
            if The_reff.loaded_teams_xml[teams_loop][0][2] == "selected":
                color_team = green
            if The_reff.loaded_teams_xml[teams_loop][0][1] == "updated":
                color_team = red

            team_details = MenuFont.render( team_name, 1, color_team)
            The_game_window.surface.blit(team_details,( table_left  + leter_shift_from_boarder , \
                                                table_top +  player_line_shift + column_teams_shift ))

            player_line_shift = player_line_shift +  2 * The_game_window.menu_line_spacing   # *3 team ma jen jmeno a musi se posunout 3 linie dolus

        column_teams_shift = column_teams_shift + text_ratio * The_game_window.menu_line_spacing
        player_line_shift = 0



def draw_team_managemet(The_game_window,The_field,The_reff,list_of_ingamers,screen_ID):
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
        if screen_ID == 5:
            screen_headeing = WelcomeFont.render('Team management', 1, grey)
        else:
            screen_headeing = WelcomeFont.render('Team trening', 1, grey)
    else:
        if screen_ID == 5:
            screen_headeing = WelcomeFont.render('Team management', 1, grey)
        else:
            screen_headeing = WelcomeFont.render('Team training', 1, grey)

    The_game_window.surface.blit(screen_headeing,( table_left  ,  0.1 * The_game_window.menu_line_spacing ))

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

    # zvyrazneni oznaceneho slotu pro vyber , 0.99  0.98 jsou pomery tabulky abe se barvy neprekryvaly
    if The_reff.selected_slot_team_management[0] >= 0:
        pygame.draw.rect(The_game_window.surface, green, (table_left + The_reff.selected_slot_team_management[0] * column_width, \
                                                          table_top + The_reff.selected_slot_team_management[1] * text_ratio * The_game_window.menu_line_spacing , \
                                                          column_width * 0.99, \
                                                          text_ratio  * The_game_window.menu_line_spacing *0.99), 1)


    # team management screen slot kopiruje , training screen slot jen zvirazni
    if screen_ID == 5:
        color_second_selection = red
    else:
        color_second_selection = green

    if The_reff.selected_slot_team_management_buffer[0] >= 0:
        pygame.draw.rect(The_game_window.surface, color_second_selection, (table_left + The_reff.selected_slot_team_management_buffer[0] * column_width, \
                                                                        table_top + The_reff.selected_slot_team_management_buffer[1] * text_ratio * The_game_window.menu_line_spacing , \
                                                                        column_width * 0.98, \
                                                                        text_ratio  * The_game_window.menu_line_spacing *0.98), 1)


    ## Vykresleni tabulky
    column_teams_shift = 0
    player_line_shift = 0
    leter_shift_from_boarder = 5 # odsazeni od hran tabulky
    font_diference = 1           # rozdil mezi fontem a linkou

    for teams_loop in range (0,10):

        # zvirazni team s neulozenou zmenou
        team_color = grey
        if The_reff.loaded_teams_xml[teams_loop] != "none" and The_reff.loaded_teams_xml[teams_loop][0][1] != "original" :
            team_color = red

        players_data =  The_reff.loaded_teams_xml[teams_loop]
        for players_loop in range (0,6):  # 1 nazev teamu +  5 hracu  => 6 radku
            if players_data[0] != "n":  # n prvni char z "none"

                # >1 players
                if players_loop >= 1:
                    for player_details in range (0,3 ):                       # !!!! PRIZPUSOBIT OPODLE POCTU DETAILS NA HRACE
                        # ID se nezobrazuje
                        if player_details !=1:
                            test = MenuFont.render( players_data[players_loop][player_details]   , 1, team_color)
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




# print team management tlacitka
def f_print_teammngmt_buttons(The_game_window):
    for loop in range (0,6):
        button_shift = 15 # prvni 15 je tlacitek menu
        draw_other_buttons(The_game_window,button_shift + loop)

# print vyber teamu  pro hru tlacitka
def f_print_teams_for_game_buttons (The_game_window):
    for loop in range (0,5):
        button_shift = 26 #
        draw_other_buttons(The_game_window,button_shift + loop)

# tisk score, reff details pri hre
def f_print_score(score,The_game_window,The_field):
    show_score = WelcomeFont.render(str(score), 1, grey)
    The_game_window.surface.blit(show_score,(The_field.field_bl_window [0],  The_field.field_bl_window[1] + The_game_window.menu_line_spacing ))
    for loop in range (0,3):
        button_shift = 20
        draw_other_buttons(The_game_window,button_shift + loop)

# print trening tlacitka
def f_print_trening_buttons(The_game_window):
    for loop in range (0,4):
        button_shift = 30 #
        draw_other_buttons(The_game_window,button_shift + loop)

# print hodnoty z treningu - pocet uskutecnenych  a planovanych 'runs'
def f_print_trening_progress(The_game_window,The_field,The_coach_A,The_coach_B):

    if The_coach_A.active_trening == True:
        trening_progress = len (The_coach_A.data_labels)
        max_trening_progress = The_coach_B.trening_sesion_total_runs
    else:
        trening_progress = len (The_coach_B.data_labels)
        max_trening_progress = The_coach_B.trening_sesion_total_runs

    show_trening_progress = MenuFont.render(str(max_trening_progress), 1, grey)
    The_game_window.surface.blit(show_trening_progress,(The_field.field_bl_window [0], \
                                 The_field.field_bl_window[1] + The_game_window.menu_line_spacing ))

    show_max_trening_progress = MenuFont.render(str(trening_progress), 1, grey)
    The_game_window.surface.blit(show_max_trening_progress,(The_field.field_bl_window [0], \
                                 The_field.field_bl_window[1] + 2 * The_game_window.menu_line_spacing ))



# tisk detailu hrace pri hre
def f_print_player_details(The_game_window,The_field,player,list_of_ingamers):
    shift_vertikal = 0
    shift_horisontal = 200                                                                                               #nejak lip definovat  hodnotu
    list_of_tags = ["angle: ","ball angle: ","ball distance(cntr-cntr)","velocity: ","site: "]
    list_of_data =[str(round(player.path_target)), \
                   str(round(player.calculate_angle_to_other_object(list_of_ingamers[1].position))), \
                   str(round(pythagoras_distance (player.position,list_of_ingamers[1].position))), \
                   str(player.velocity), \
                   player.field_site ]

    for data_index in range (0,len(list_of_data)):
        data = MenuFont.render(  list_of_tags[data_index] + list_of_data[data_index]   , 1, grey)
        The_game_window.surface.blit(data,(The_field.field_bl_window [0] + shift_horisontal, \
                                            The_field.field_bl_window[1] + The_game_window.menu_line_spacing + shift_vertikal ))
        shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing

'''
#test prints                                                                                            #testy souradnic
def print_test_x(The_game_window):
    xx = MenuFont.render( "XX"  , 1, red)
    The_game_window.surface.blit(xx,(300, 650 ))
    #print("xx")
'''


# vizualizace keras.modelu                                                                                          # pouzita pri testovani asi nebude v hre uzita
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
            The_game_window.surface.blit(data_print,(The_field.field_bl_window [0] + x_shift, \
                                                    The_field.field_bl_window[1] + The_game_window.menu_line_spacing + shift_vertikal ))
            shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing

        x_shift = x_shift + 100
        shift_vertikal = 0


# tisk nastaveni/hodnot balonu (uzito pro kontrolu metod )                                                                        # pouzita pri testovani asi nebude v hre uzita
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
        welcome = WelcomeFont.render('Flatball vitejte', 1, grey)
    else:
        welcome = WelcomeFont.render('Flatball welcome', 1, grey)

    The_game_window.surface.blit(welcome,(The_game_window.window_width * 0.4 , The_game_window.window_height * 0.3))


# pomocna funkce, pythagorovo pravidlo
def pythagoras_distance (location_1,location_2):                                                                            #stejna funkce v 2 modulech Zkontroluj
    ingamer_adjescent =  abs (location_1[0]  -  location_2[0])
    ingamer_opposite =  abs (location_1[1] -  location_2[1])
    ingamer_hypotensue = sqrt(ingamer_adjescent **2 + ingamer_opposite **2)

    return ingamer_hypotensue

# napoveda

def f_print_help(The_game_window):

    if The_game_window.language == "CZ":
        help_heading = WelcomeFont.render('Napoveda', 1, grey)
    else:
        help_heading = WelcomeFont.render('Game guide', 1, grey)
    The_game_window.surface.blit(help_heading,( The_game_window.window_width * 0.4 , 0.5 * The_game_window.menu_line_spacing ))

    if The_game_window.language == "CZ":
        help_text =['FLATBALL', \
                    '  ', \
                    '  ', \
                    'TEAM MANAGEMENT', \
                    '  hra ma ulozen jeden vytvoreny team  ' \
                    '  hrac můze byt kopirovan do noveho teamu, jakmile je 5 hracu v teamu zmena musi byt ulozena' , \
                    '  a to oznacenim jmena teamu a tlacitkem ulozit zmeny', \
                    '  v pripade kopirovani hrace do prazdneho teamu se novy team vytvori automaticky' , \
                    '  ', \
                    'Trening ', \
                    '  trenovany hrac je oznacen a potvrzen  (team A) ' , \
                    '  pote musi byt oznacen tym proti kteremu se bude trenovat ( team B )' , \
                    '  prozatim jen manualni trening je funkcni ( H / H)' ,
                    '  prave tlacitko mysi vytvori nove rozestaveni pro trening , klavesa -p- ukonci trening  ' , \
                    '  trening ma vliv na hrace pouze po dostazeni 5000 akci, kdy je trening vyhodnocen pote se muze v treningu pokracovat' , \
                    '  pocet akci je vyobrazen pod hrsitem' , \
                    '  kotrola hrace pri hre je vysvetlena nize' , \
                    '  ', \
                    'Potvrzeni teamu do hry   ', \
                    '  teamy jsou vytvoreny v  -team management- mohou byt vybrany do zapasu   ', \
                    '  cervene oznacene teamy nejsou uplne rozhodci je bude ignorovat     ', \
                    '  oznaceny hrac je ovladan  mysi ktera urcuje smer a klavesou -w- se potvrdi krok, mezernikem je proveden kop do mice ' , \
                    '   ', \
                    '  ', \
                    '  ']

    else:
        help_text =['FLATBALL', \
                    '  ', \
                    '  ', \
                    'TEAM MANAGEMENT', \
                    '  default created one non trained team ,user can copy players to new slots or later to created teams ' \
                    '  change has to be saved, save can be done if selected team and team has 5 players' , \
                    '  user needs cleck on player .use copy button than select new slot and select paste button ', \
                    '  new team is automaticaly generated if player is paste to non team slot' , \
                    '  ', \
                    'Training ', \
                    '  user has to select a player (his team is team A) ' , \
                    '  than need select team (will be team B for the training match)' , \
                    '  it is posible to select own team as opossite team (should be working fine ) ' ,
                    '  for now only non automised training is available ( H / H)' ,
                    '  left mouse selection will create new match situation , key -p- will end training  ' , \
                    '  training will affect a player if 5000 runs is hit than training can continue or be end' , \
                    '  for player control guide see part -match- below ' , \
                    '  ', \
                    'Teams confirmation for game  ', \
                    '  teams created and saved in -team management- are available for game selection   ', \
                    '  if teams is displayed red than team update  was not saved or doesnt have 5 players      ', \
                    '  MATCH  for now is available only at mod human vs AI ', \
                    '  AI players are non selectable , team of user is controled by AI but one of the player can be selected ' , \
                    '  selected player can be controlled by user: mouse gives direction of move, -w- key makes a step ,-space- kicks a ball if owned ' , \
                    '   ', \
                    '  ', \
                    '  ']



    for loop_help_print in range (0,len(help_text)):
        help_line = help_text[loop_help_print]
        help_line_rendered = MenuFont.render( help_line, 1, grey)
        The_game_window.surface.blit(help_line_rendered,( The_game_window.game_menu_x_start +100  , 3 * The_game_window.menu_line_spacing + loop_help_print * The_game_window.menu_line_spacing  ))



# icona pro zobrazeni menu
def draw_menu_icon(The_game_window):
    for loop_menu_icon in range (1,4):
        icon_line_rendered = WelcomeFont.render( "-", 1, grey)
        The_game_window.surface.blit(icon_line_rendered,( The_game_window.game_menu_x_start , -15 + 6 * loop_menu_icon   ))





#
