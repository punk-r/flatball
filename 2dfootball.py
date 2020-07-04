import pygame
import sys
import math
import random

import os.path
from os import path

#pygame modul
pygame.init()
from pygame.locals import *

clock = pygame.time.Clock()

import f_menu
from f_menu import *
import f_clases
from f_clases import *


# testovani
debug_mode = 0

The_game_window = game_window()
pygame.display.set_caption(" Flatball ")

The_field = game_field()
The_field.set_field(The_game_window)


The_ball = ball([300,400])
The_ball.draw_ingamer(The_game_window)
The_player_no_1 = player ([300,200])

The_player_no_2 = player ([500,100])

was_clicked = 0
position_clicked = [0,0]
game_menu_active = 1
game_menu_x_start = 5
game_menu_x_end = 200
menu_line_spacing = 20
heading_shift = 30
game_menu_selcection = 'A'
screen_ID = 1


draw_main_menu(The_game_window,menu_line_spacing,heading_shift)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            was_clicked = 1
            position_clicked = pygame.mouse.get_pos()

        if event.type == MOUSEMOTION:
            position_over = pygame.mouse.get_pos()
            over_x = position_over[0]
            over_y = position_over[1]
            if The_player_no_1.selected_b == 1:
                The_player_no_1.set_path_target(position_over)

            if The_player_no_2.selected_b == 1:
                The_player_no_2.set_path_target(position_over)

    if was_clicked == 1 and game_menu_active == 1:
        if position_clicked[0] < game_menu_x_end:

            #prvni radek krom main menu ,krok zpet  v v menu
            if position_clicked[1] > heading_shift and position_clicked[1] < heading_shift + menu_line_spacing :
                # zpet v menu
                if game_menu_selcection != 'A':
                    game_menu_selcection = game_menu_selcection[:-1]
                else:
                    game_menu_selcection = 'AA'

            if position_clicked[1] > heading_shift + menu_line_spacing:
                # 65 je A ascii
                line_selected = math.floor( (position_clicked[1] - heading_shift) / menu_line_spacing )
                game_menu_selcection = game_menu_selcection  +   chr(  65 + line_selected)


            screen_ID = f_choose_scree_from_selection(game_menu_selcection)
            if screen_ID == 2:
                game_menu_active = 0

            was_clicked = 0


    The_game_window.surface.fill(black)


    if screen_ID == 1:                                                              # dat do menu knihovny?
        draw_weclome(The_game_window)
    elif screen_ID == 2 :
        draw_5aside_field (game_window,game_field)

    choose_menu_from_selection(The_game_window,The_field,game_menu_selcection)
    The_ball.draw_ingamer(The_game_window)
    The_ball.is_selected(position_clicked)


    The_player_no_1.draw_player(The_game_window)
    The_player_no_1.is_selected(position_clicked)

    The_player_no_2.draw_player(The_game_window)
    The_player_no_2.is_selected(position_clicked)





    #print('clicked',position_clicked)
    pygame.display.update()
    clock.tick(60)


'''
#---------------------------------------------------------- HRA -----------------------------------------------------------------------

# inicializace rozhodciho & inicializace hraci desky
the_referee = class_referee()

# rozhodci vytvori novou hru, ma prehled o cele hre a to i o desce samotne
the_referee.start_game()

# posun osy x pro menu pod hraci deskou
Mneu_below_board_shift = 270
#PI=math.pi

# pocitadlo pro historii strran tahu, jedna strana obsahuje 10 tahu
moves_archive_page = 1

# test zobrazeni menu,  1 => pri spusteni se vzdy nejdrive ukaze napoveda
help_on_screen = 0
was_clicked = 1

# je li both_values_for_move = 2 hra pokracuje kontrolou tahu,jinak ceka na dvoje souradnice pro tah
both_values_for_move = 0
#coordinates_given = 0
position_clicked = [0,0]
position_over = [0,0]
new_locations =[0,0]
AI_palyer = 0
# nelze provest tah po vyhre nebo remize ,uzivatel muze ulozit hru a resetvovat pro novou => prevence pro tah po ukonceni hry
game_continue_staus = 1

# radky v menu
line_spacing = 25

# volane nove vlakno
second_tread_called = 0

# tisk zprav od rozhodciho, prvni spusteni hry
print_message= MenuFont.render('Hra zacala', 1, grey)
screen.blit(print_message,(Mneu_below_board_shift + 440,570 ))

# ram hraci desky ,uzito pro vypocty mista kliku mysi, menu => nastaveni hry nebo hraci deska => tah kameny
# frame_h_w =[vyska ,sirka obdelniku]
frame_h_w = frame_coordinates (x_board_site,y_board_site,beta,alfa,x_field,y_field)
frame_corners = ( x_field, y_inverted(window_height,y_field),x_field + frame_h_w[1] ,y_inverted(window_height, y_field + frame_h_w[0] ))

# nekonecna smycka pro zobrazeni okna pygame
while 1:

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            was_clicked = 1
            position_clicked = pygame.mouse.get_pos()
        if event.type == MOUSEMOTION:
            position_over = pygame.mouse.get_pos()
            over_x = position_over[0]
            over_y = position_over[1]

            pygame.mouse.set_cursor(*pygame.cursors.arrow)

            # zmena kursoru nad tlacitkami
            if over_x < 180:
                if (over_y > 22 * line_spacing and over_y < 25 * line_spacing)  or  \
                    ((over_y > 8 * line_spacing and over_y < 10 * line_spacing) and (over_x < 50  or over_x > 110))  or  \
                    (over_y > 3 * line_spacing and over_y < 4 * line_spacing)  or  \
                    (over_y > 5 * line_spacing and over_y < 6 * line_spacing) :

                    pygame.mouse.set_cursor(*pygame.cursors.tri_left)


    # hra ocekava vstup od hrace
    if was_clicked:


        if debug_mode == 1:
            print ('   FFFFIRSTTT')
            print ('the_referee.w_AI_level',the_referee.w_AI_level)
            print ('the_referee.b_AI_level',the_referee.b_AI_level)
            print ('the_referee.w_player_type',the_referee.w_player_type)
            print ('the_referee.b_player_type',the_referee.b_player_type)

        #reset
        was_clicked = 0
        move_decision = [0,0]
        new_location_index_format= [-1,-1,-1,-1]

        # hrac je obsuha PC ,(If No.1)
        if (the_referee.playing_team == 1 and the_referee.w_player_type == 1) or \
            (the_referee.playing_team == 0 and the_referee.b_player_type == 1):

            #                                                                                                                #zjednosist vyber napsat funkci s argumentem souradnic od mysi a vraci jaka akce se ma provest

            # pozice mysi je na urovni desky => hodnoty pro vypocet tahu , nelze provadet tah pri zobrazene napovede
            if click_on_board(position_clicked,frame_corners) == 1 and help_on_screen == 0 and second_tread_called == 0:

                # reset predesle zpravy
                print_message =MenuFont.render( ' ', 1, grey)

                new_locations[both_values_for_move] = position_clicked

                # pro kontrolu tahu jsou potreba 2 pozice ,pozdeji kontrola tahu pri both_values_for_move = 2
                both_values_for_move = both_values_for_move + 1

                if both_values_for_move == 1:
                    #print vybrano 'z' pozice
                    print_message = MenuFont.render( "Vybrana figurka pro tah,dokoncete tah: ", 1, grey)
                else:
                    print_message = MenuFont.render( "Tah vybran: ", 1, grey)                                                 # print probehne rychle ,lze vudet pouze pri debuging  .#oddelat??zkontrolj


                if debug_mode == 1:
                    print("both_values_for_move  kolikaty klik? :" , both_values_for_move)
                    test13 = MenuFont.render( ' ', 1, white)
                    test16 = myFont.render(str(position_clicked), 1, green)
                    screen.blit(test16, position_clicked)
                    pygame.display.update()


            # pozice mysi je na urovni menu, volani metod/funkci pro nastaveni hry
            else:

                # ----------------- NASTAVENI    -----------------------------------------------

                # nelze menit nastaveni pri napovede na obrazovce
                if help_on_screen==0:

                    # cerveny(bily) team
                    if position_clicked[1] > 70 and position_clicked[1] < 105:
                        if position_clicked[0] < 85 and position_clicked[0] > 0 and the_referee.check_game_status() == 6 :
                            the_referee.swap_player_type(1)
                        if position_clicked[0] < 135 and position_clicked[0] > 95:
                            the_referee.change_AI_level(1,1)
                        elif position_clicked[0] < 170 and position_clicked[0] > 135:
                            the_referee.change_AI_level(1,2)

                    # modry(cerny) team
                    if position_clicked[1] > 125 and position_clicked[1] < 150:
                        if position_clicked[0] < 85 and position_clicked[0] > 0 and the_referee.check_game_status() == 6 :
                            the_referee.swap_player_type(0)
                        if position_clicked[0] < 135 and position_clicked[0] > 95:
                            the_referee.change_AI_level(0,1)
                        elif position_clicked[0] < 170 and position_clicked[0] > 135:
                            the_referee.change_AI_level(0,2)

                    #test nastaveni hry
                    if debug_mode == 1:
                        test13 = myFont.render(str(position_clicked), 1, red)
                        screen.blit(test13,position_clicked)
                        f_print_game_summary(the_referee.game_summary())

                    # nastaveni strany zobrazovani tahu
                    if position_clicked[1]  > 200 and position_clicked[1] < 225:
                        if position_clicked[0] > 0 and position_clicked[0] < 40:
                            if moves_archive_page != 1:
                                moves_archive_page = moves_archive_page - 1
                        elif  position_clicked[0] > 120 and position_clicked[0] < 160:
                            # maximum ulozeni je 100 tahu,10 stran
                            if moves_archive_page < the_referee.archive_size /10:
                                moves_archive_page = moves_archive_page + 1


                    # zobrazeni predchoziho nebo dalsiho tahu,v pripade ze tahy jsou v archivu, argument metody:  0 -predchozi   /  1- nasledujici
                    if position_clicked[1] > 225 and position_clicked[1]<  250:
                        if  the_referee.w_player_type == 1 and the_referee.b_player_type == 1:
                            # predchozi tah
                            if position_clicked[0] > 0 and position_clicked[0] < 40 and the_referee.moveNo > 1:
                                the_referee.query_board_from_archive (0)
                                print_message = MenuFont.render('!! Ulozene tahy mohou byt prepsany !!', 1, grey)

                            # dalsi tah
                            elif  position_clicked[0] > 120 and position_clicked[0] < 160:
                                if the_referee.moveNo < the_referee.archive_size:
                                    the_referee.query_board_from_archive (1)

                                    print_message = MenuFont.render('!! Ulozene tahy mohou byt prepsany !!', 1, grey)
                        else:
                            print_message = MenuFont.render('Team(y) nemohou byt nastaveny na AI.', 1, red)



                    # ulozeni / nahrani hry
                    if position_clicked[1] > 575 and position_clicked[1]<  595 :

                        # ulozit hru
                        if position_clicked[0] > 5 and position_clicked[0] < 85:

                            # lze ulozit pouze neprobihajici hru => oba hraci musi by nastaveni na obsluhu PCs
                            if the_referee.w_player_type == 1 and the_referee.b_player_type == 1 :
                                save_game(the_referee.moves_archive_array)
                                print_message = MenuFont.render('Hra ulozena', 1, grey)
                            else:
                                print_message = MenuFont.render('Nelze ulozit hru,pri nastavenem AI.', 1, red)


                        # nahrat hru
                        elif  position_clicked[0] > 105 and position_clicked[0] < 185:
                            if the_referee.w_player_type == 1 and the_referee.b_player_type == 1 :
                                # podminka zda soubor existuje,kdyz ano zkontroluj obsah a nacti
                                if os.path.isfile('evade.txt'):
                                    test_of_file = load_game(len(the_referee.moves_archive_array),the_referee)                      #opravit ne uplne jede....!!!!!
                                    print_message = MenuFont.render(test_of_file, 1, grey)
                                    if test_of_file =='OK':
                                        #the_referee.board.board_cells =  the_referee.moves_archive_array[0] [2]
                                        #the_referee.playing_team = 1
                                        the_referee.moveNo = 2
                                        the_referee.query_board_from_archive(0)
                                        print_message = MenuFont.render('Hra nahrana, !tahy mohou byt prepsany!', 1, grey)
                                        #print_message = MenuFont.render(test_of_file , 1, grey)

                                else:
                                    print_message = MenuFont.render('Soubor v adresari neexistuje.', 1, red)
                            else:
                                print_message = MenuFont.render('Nelze nahrat hru,pri nastavenem AI.', 1, red)



                    # reset hry
                    if position_clicked[1] > 595 and position_clicked[1]<  620:
                        # ulozeni
                        if position_clicked[0] > 5 and position_clicked[0] < 185:
                            the_referee.restart_game()
                            game_continue_staus = 1
                            print_message = MenuFont.render('Hra resetovana', 1, grey)

                    # ----------------- KONEC NASTAVENI    --------------------------------------


                # napoveda, zobrazeni a vynuti
                if position_clicked[1] > 555 and position_clicked[1]<  575:
                    if help_on_screen == 0:
                        if position_clicked[0] > 5 and position_clicked[0] < 190:
                            help_on_screen = 1
                    else:
                        if position_clicked[0] > 5 and position_clicked[0] < 190:
                            help_on_screen = 0


                if debug_mode == 1:
                    print('hhelp_on_screenn',help_on_screen)
                    print('the_referee.moveNo',the_referee.moveNo)
                    #print('moves_archive_page',moves_archive_page)
                    #print('the_referee..ge',the_referee.board.board_cells)

                    for lllloop in range(0,4):
                        print ('archhive',the_referee.moves_archive_array[lllloop])
                    print('')

                    #print(the_referee.moves_archive_array)

        # AI hrac ,(If No.1)
        else:
            if debug_mode == 1:
                print ('ai pocita')
                print ('the_referee.w_AI_level',the_referee.w_AI_level)
                print ('the_referee.b_AI_level',the_referee.b_AI_level)
                print ('the_referee.w_player_type',the_referee.w_player_type)
                print ('the_referee.b_player_type',the_referee.b_player_type)





            if second_tread_called == 0 :
                print_message= MenuFont.render('', 1, white)
                print_message_from_pc= MenuFont.render('Zprava od PC :Pocitam', 1, white)
                screen.blit(print_message_from_pc,(Mneu_below_board_shift + 440,590 ))
                sprint_message = MenuFont.render( 'PC - Pocitam.', 1, white)
                pygame.display.update()
                AI_palyer = 1
                accual_level = 0
                new_location_index_format =  [0,0,0,0]
                buffer = [0,0,0,0]

            # zjisti level AI hrajiciho teamu
            if the_referee.playing_team == 1:
                accual_level = the_referee.w_AI_level
            else:
                accual_level = the_referee.b_AI_level


            # spusti funkci odpovidajici levelu a kontroluje konec hry, ocekavan reset od uzivatele nebo ulozeni dohrane hry
            if the_referee.check_game_status() == 6:
                if accual_level == 1 :
                    new_location_index_format = f_PCplayerLevel1()
                else:
                    new_location_index_format = f_PCplayerLevel2(the_referee)

            # spusti funkci odpovidajici levelu a kontroluje konec hry, ocekavan reset od uzivatele nebo ulozeni dohrane hry
            # s implementaci AI volanem v druhem vlakne
            if the_referee.check_game_status() == 6 and second_tread_called == 0 :
                if accual_level == 1 :
                    second_tread_called = 1
                    #print('ttttesestt in loooop' )
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(f_PCplayerLevel1)
                        new_location_index_format = future.result()
                else:
                    second_tread_called = 1
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(f_PCplayerLevel23 , the_referee)
                        new_location_index_format = future.result()

            if  new_location_index_format != [0,0,0,0]:
                if new_location_index_format != [-1,-1,-1,-1] :
                    #print('passssss' )
                    both_values_for_move = 2
                else:
                    second_tread_called = 0


        #print('new_location_index_format:::',new_location_index_format )
        # kontrola tahu se provede pouze jsouli zadany 2 pozice (z lokace ,do lokace)
        if both_values_for_move == 2:
            #print('ttttesestt' ,new_location_index_format )


            if AI_palyer == 0:
                if second_tread_called == 0 :
                    new_location_index_format = calculate_index_from_pixels (screen,new_locations,x_board_site,y_board_site,beta,alfa,x_field,y_field,window_height)
            else:
                #reset predesleho potahu
                AI_palyer = 0

            # reset multivlakna
            second_tread_called = 0

            # reset predchoziho tahu
            both_values_for_move = 0

            # e -error hodnota uzivatel vybral souradnice mimo hraci desku,oblast ramu-obdelnik (snazzsi vypocet) ve kterem je hraci desky je klikatelna pro tah
            if new_location_index_format[0] !='e':

                # chek_stone_move vrati 1 kdyz je tah ok,0 kdyz neni,druhy prvek urci duvod neuznani tahu
                move_decision = the_referee.chek_stone_move(new_location_index_format)
                message_to_user = choose_move_error(move_decision)
                print_message = MenuFont.render( message_to_user, 1, grey)
                #print('move_decision move_decision move_decision',message_to_user )
            else:
                print_message = MenuFont.render( 'Tah je mimo hraci desku,opakujte tah ', 1, grey)

            # ulozeni zmeny kamenu po tahu ,popripade zobrazi duvod neprovedeni tahu,prepne hrace
            if move_decision[0] == 1 and game_continue_staus == 1 :

                the_referee.confirm_stone_move(new_location_index_format)
                the_referee.archive_move(the_referee.playing_team,new_location_index_format)
                the_referee.increment_moveNo()


            # kontrola ukonceni hry
            status = the_referee.check_game_status()

            # hra ma omezeny pocet tahu
            if status == 6 and the_referee.moveNo == the_referee.archive_size:
                status = 3

            if status != 6:
                # uzivatel musi resetoat hru, prevence automatickeho reset hry ,uzivatel ma moznost si hru ulozit pote zvolit reset hry
                game_continue_staus = 0
                team_playing = "Konec hry"

                # po ukonceni hry se automayticky hraci prepnou na uzivatele PC
                the_referee.w_player_type = 1
                the_referee.b_player_type = 1

                if status == 1:
                    print_message = MenuFont.render( 'Cervene kameny vyhraly,zvolte reset hry', 1, white)
                elif status == 0:
                    print_message = MenuFont.render( 'Modre kameny vyhray,zvolte reset hry', 1, white)
                else:
                    print_message = MenuFont.render( 'Remiza,zvolte reset hry', 1, white)

                # the_referee.restart_game()


        # prekresleni
        screen.fill(black)

        # print playing team, kontrola pro dalsi loop                                                       ZKONTROLUJ
        if the_referee.playing_team == 1:
            team_playing = "Cerveni"
            if the_referee.w_player_type == 0:
                #print_message= MenuFont.render('Tah spocten,hra pokracuje.', 1, white)
                was_clicked =1
            else:
                was_clicked =0
        else:
            team_playing = "Modri"
            if the_referee.b_player_type == 0:
                #print_message= MenuFont.render('Tah spocten,hra pokracuje.', 1, white)
                was_clicked =1
            else:
                was_clicked =0

        if game_continue_staus == 0:
            team_playing = "Konec hry"


        menu_print_team_playing = MenuFont.render(team_playing , 1, grey)
        screen.blit(menu_print_team_playing,( Mneu_below_board_shift + 180,550 ))

        draw_menu(screen,the_referee,moves_archive_page,help_on_screen)

        # zobraz hraci desku / napovedu

        # mod - hra
        if help_on_screen == 0:

            # parametry funkce draw_field (x_board_site,y_board_site,beta,alfa,x_field,y_field,window_height,board)
            #   2x strana hraci desky
            #   2x uhly hraci desky ku ohranicujicimu ramu
            #   2x souradnice leveho dolniho rohu ohranicujiciho ramu
            #   vyska okna aplikace ,pro vypovet Y souradnice jako v klasicke soustave => pod osou x jsou zaporne hodnoty
            #   pole s kameny
            draw_field (x_board_site,y_board_site,beta,alfa,x_field,y_field,window_height,screen,the_referee.board.board_cells)

            # zprava od rozhodcih se ukazuje kdyz je napoveda zavrena
            screen.blit(print_message,(Mneu_below_board_shift + 440,570 ))
            #print_message =MenuFont.render( ' ', 1, grey)

        # mod - napoveda
        else:

            hide_below_board_menu = pygame.draw.rect(screen, black , (300 ,540 ,650, 100  )   ,  1)
            screen.fill(black,hide_below_board_menu)
            print_help_and_rules(screen)
            was_clicked = 0

        # ram okna,linie mezi menu a hraaci deskou
        pygame.draw.rect(screen, white , (0 ,0 ,window_width, window_height  )   ,  1)
        #pygame.draw.arc(screen, grey, [210,0,150,window_height], math.radians (130) ,  math.radians (250), 2)
        pygame.draw.lines(screen,  grey, True, ((200,55 ) , ( 200 ,620  )), 1)
        pygame.draw.lines(screen,  grey, True, ((5,45 ) , ( 245 ,45  )), 1)
        #pygame.draw.arc(screen, grey, [-95,610,400,200], math.radians (45) ,  math.radians (120), 2)

        if debug_mode ==1:
            screen.blit(test13,position_clicked)
            #reset
            test13 = MenuFont.render( ' ', 1, grey)

        pygame.display.update()
        #pygame.time.wait(1000)

'''
