import f_menu
from f_menu import *


# -------------------------------------------SCREENS---------------------------------------------------

# teams selection pro hru
def draw_teams_for_game(The_game_window,The_field,The_reff):
    # hodnoty musi by ulozeny v 'window' aby slo vypocitat polohu mysi => spustit metodu/funkci
    list_of_ingamers = The_reff.list_of_ingamers
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
        page_heading = MenuFont_heading.render('vyberteam vitejte', 1, grey)
        note_1 = MenuFont.render('VOLBA HRY', 1, grey)
        note_2 = MenuFont.render('Teamy do hry ', 1, grey)
        table_headngs = ["team","trenovano" ,"trening" ,"prum skills" , "zapasu", "vyher", "vybrano",]
    else:
        page_heading = MenuFont_heading.render('Choose teams for game', 1, grey)
        note_1 = MenuFont.render('Game settings:', 1, grey)
        note_2 = MenuFont.render('Games for the game:', 1, grey)
        table_headngs = ["Teams","note_a" ,"note_b" ,"note_c" , "note_d", "note_e", "selected"]

    # vypise pouze pokud jsou oba teamy vybrane
    if  The_reff.teams_for_game[0] == " " or  The_reff.teams_for_game[1] == " " :
        teams_chosen = WelcomeFont.render(  "_ vs _ "  , 1, grey)
    else:
        teams_chosen = WelcomeFont.render( The_reff.teams_for_game[0]  + " vs " + The_reff.teams_for_game[1]  , 1, grey)

    The_game_window.surface.blit(page_heading,( table_left  ,  0.1 * The_game_window.menu_line_spacing ))
    The_game_window.surface.blit(note_1,( table_left  , The_game_window.game_menu_y_end +  2* The_game_window.menu_line_spacing ))
    The_game_window.surface.blit(note_2,( table_left + 2* column_width  , The_game_window.game_menu_y_end +  2* The_game_window.menu_line_spacing ))
    The_game_window.surface.blit(teams_chosen,( table_left +( 2 *column_width ) , The_game_window.game_menu_y_end +   The_game_window.menu_line_spacing *4 )) # 4 radku odsazeni

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

            team_details = MenuFont.render("TEAM " + team_name, 1, color_team)
            The_game_window.surface.blit(team_details,( table_left  + leter_shift_from_boarder , \
                                                table_top +  player_line_shift + column_teams_shift ))

            player_line_shift = player_line_shift +  2 * The_game_window.menu_line_spacing   # *3 team ma jen jmeno a musi se posunout 3 linie dolus

        column_teams_shift = column_teams_shift + text_ratio * The_game_window.menu_line_spacing
        player_line_shift = 0



def draw_team_managemet(The_game_window,The_field,The_reff,screen_ID):
    # hodnoty musi by ulozeny v 'window' aby slo vypocitat polohu mysi => spustit metodu/funkci
    list_of_ingamers = The_reff.list_of_ingamers
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
        if screen_ID == screens.teammanagement.value:
            screen_headeing = MenuFont_heading.render('Team management', 1, grey)
            coach = The_reff.coach_team_A
        elif screen_ID == screens.trening.value:
            screen_headeing = MenuFont_heading.render('Team trening', 1, grey)
        elif screen_ID == screens.teammanagementaway.value:
            screen_headeing = MenuFont_heading.render('Team managementaway', 1, grey)
            coach = The_reff.coach_team_B
    else:
        if screen_ID == screens.teammanagement.value:
            screen_headeing = MenuFont_heading.render('Team management', 1, grey)
            coach = The_reff.coach_team_A
        elif screen_ID == screens.trening.value:
            screen_headeing = MenuFont_heading.render('Team training', 1, grey)
        elif screen_ID == screens.teammanagementaway.value:
            screen_headeing = MenuFont_heading.render('Team managementaway', 1, grey)
            coach = The_reff.coach_team_B

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
    if coach.selected_slot_team_management[0] >= 0:
        pygame.draw.rect(The_game_window.surface, green, (table_left + coach.selected_slot_team_management[0] * column_width, \
                                                          table_top + coach.selected_slot_team_management[1] * text_ratio * The_game_window.menu_line_spacing , \
                                                          column_width * 0.99, \
                                                          text_ratio  * The_game_window.menu_line_spacing *0.99), 1)


    # team management screen slot kopiruje , training screen slot jen zvirazni
    if screen_ID == screens.teammanagement.value:
        color_second_selection = red
    else:
        color_second_selection = green

    if coach.selected_slot_team_management_buffer[0] >= 0:
        pygame.draw.rect(The_game_window.surface, color_second_selection, (table_left + coach.selected_slot_team_management_buffer[0] * column_width, \
                                                                        table_top + coach.selected_slot_team_management_buffer[1] * text_ratio * The_game_window.menu_line_spacing , \
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
        if coach.loaded_teams_xml[teams_loop] != "none" and coach.loaded_teams_xml[teams_loop][0][1] != "original" :
            team_color = red

        players_data =  coach.loaded_teams_xml[teams_loop]
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
                    team_name = MenuFont.render("Team " + coach.loaded_teams_xml[teams_loop][0][0], 1, grey)
                    The_game_window.surface.blit(team_name,( table_left + column_teams_shift + leter_shift_from_boarder , table_top +  player_line_shift  ))

                    if coach.loaded_teams_xml[teams_loop][0][2] == "selected":
                        is_selected = "OK"
                    else:
                        is_selected = "X"
                    is_selected_rendered = MenuFont.render(is_selected, 1, grey)
                    The_game_window.surface.blit(is_selected_rendered,( table_left + int(0.4*column_width)+column_teams_shift + leter_shift_from_boarder , table_top + 18*The_game_window.menu_line_spacing  ))
                    player_line_shift = player_line_shift +3* The_game_window.menu_line_spacing   # *3 team ma jen jmeno a musi se posunout 3 linie dolu

        column_teams_shift = column_teams_shift + column_width
        player_line_shift = 0




# print team management tlacitka
def f_print_teammngmt_buttons(The_game_window):
    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == screens.teammanagement.value:
            draw_button_No(The_game_window, loop)

# print team managementaway tlacitka
def f_print_teammngmtaway_buttons(The_game_window):
    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == screens.teammanagementaway.value:
            draw_button_No(The_game_window, loop)


# print vyber teamu  pro hru tlacitka
def f_print_teams_for_game_buttons (The_game_window):
    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == screens.teamsconfirmation.value:
            draw_button_No(The_game_window, loop)

# tisk score, reff details pri hre
def f_print_score(score,The_game_window,The_field):
    show_score = WelcomeFont.render(str(score), 1, grey)
    The_game_window.surface.blit(show_score,(The_field.field_bl_corner [0] + 0.92 * The_field.field_width / 2 ,  The_field.field_bl_corner[1] + The_game_window.menu_line_spacing ))
    reff_header = MenuFont.render("Reff menu:", 1, grey)
    The_game_window.surface.blit(reff_header,(The_field.field_bl_corner [0]  ,  The_field.field_bl_corner[1] + The_game_window.menu_line_spacing ))

    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == screens.ingame.value:
            draw_button_No(The_game_window, loop)

# print trening tlacitka
def f_print_trening_buttons(The_game_window):
    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == screens.trening.value:
            draw_button_No(The_game_window, loop)

# print zobraz  menu button
def f_print_dysplay_menu_buttons(The_game_window):
    index = len(The_game_window.buttons)  -1
    draw_button_No(The_game_window,index)

# print edit hrace
def f_print_edit_player_buttons(The_game_window):
    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == screens.teammanagementedit.value:
            draw_button_No(The_game_window, loop)



'''
#player je vstup ve tvaru [pl_name, pl_ID,pl_position,trening_type,trening_time]
def draw_edited_player_details (player,The_game_window):
    player_name = MenuFont.render(player[0], 1, grey)
    The_game_window.surface.blit(player_name,(The_game_window.game_menu_x_end + The_game_window.mngmt_shift_from_menu , \
                                              The_game_window.game_menu_y_end + The_game_window.menu_line_spacing ))



'''


# print hodnoty z treningu - pocet uskutecnenych  a planovanych 'runs'
def f_print_trening_progress(The_game_window,The_field,The_coach_A,The_coach_B):

    if The_coach_A.active_trening == True:
        trening_progress = len (The_coach_A.data_labels)
        max_trening_progress = The_coach_B.trening_sesion_total_runs
    else:
        trening_progress = len (The_coach_B.data_labels)
        max_trening_progress = The_coach_B.trening_sesion_total_runs

    show_trening_progress = MenuFont.render(str(max_trening_progress), 1, grey)
    The_game_window.surface.blit(show_trening_progress,(The_field.field_bl_corner [0], \
                                 The_field.field_bl_corner[1] + The_game_window.menu_line_spacing ))

    show_max_trening_progress = MenuFont.render(str(trening_progress), 1, grey)
    The_game_window.surface.blit(show_max_trening_progress,(The_field.field_bl_corner [0], \
                                 The_field.field_bl_corner[1] + 2 * The_game_window.menu_line_spacing ))



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
        The_game_window.surface.blit(data,(The_field.field_bl_corner [0] + shift_horisontal, \
                                            The_field.field_bl_corner[1] + The_game_window.menu_line_spacing + shift_vertikal ))
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
            The_game_window.surface.blit(data_print,(The_field.field_bl_corner [0] + x_shift, \
                                                    The_field.field_bl_corner[1] + The_game_window.menu_line_spacing + shift_vertikal ))
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
        The_game_window.surface.blit(data,(The_field.field_bl_corner [0], The_field.field_bl_corner[1] + The_game_window.menu_line_spacing + shift_vertikal ))
        shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing


# tisk uvitaci plochy
def draw_weclome(The_game_window):
    if The_game_window.language == "CZ":
        welcome = WelcomeFont.render('Flatball vitejte', 1, grey)
    else:
        welcome = WelcomeFont.render('Flatball welcome', 1, grey)

    The_game_window.surface.blit(welcome,(The_game_window.window_width * 0.4 , The_game_window.window_height * 0.3))

# tisk paused game
def draw_paused_game(The_game_window):
    if The_game_window.language == "CZ":
        paused = WelcomeFont.render('Hra pozastavena', 1, grey)
    else:
        paused = WelcomeFont.render('Game paused', 1, grey)

    The_game_window.surface.blit(paused,(The_game_window.window_width * 0.4 , The_game_window.window_height * 0.3))


# pomocna funkce, pythagorovo pravidlo
def pythagoras_distance (location_1,location_2):                                                                            #stejna funkce v 2 modulech Zkontroluj
    ingamer_adjescent =  abs (location_1[0]  -  location_2[0])
    ingamer_opposite =  abs (location_1[1] -  location_2[1])
    ingamer_hypotensue = sqrt(ingamer_adjescent **2 + ingamer_opposite **2)

    return ingamer_hypotensue

# napoveda

def f_print_help(The_game_window):

    if The_game_window.language == "CZ":
        help_heading = MenuFont_heading.render('NAPOVEDA', 1, grey)
    else:
        help_heading = MenuFont_heading.render('GAME GUIDE', 1, grey)
    The_game_window.surface.blit(help_heading,( The_game_window.window_width * 0.4 , 0.5 * The_game_window.menu_line_spacing ))

    if The_game_window.language == "CZ":                                                                                                                    #end line
        help_text =[' ', \
                    'TRENER   ', \
                    ' -Team management: hra ma ulozen jeden vytvoreny team hrac můze byt kopirovan do noveho teamu, jakmile je 5 hracu v teamu zmena musi  ', \
                    '   byt ulozena a to oznacenim jmena teamu a tlacitkem ulozit zmeny, v pripade kopirovani hrace do prazdneho  teamu se novy team vytvori automaticky', \
                    ' -Stats: staistika hracu a teamu ', \
                    ' -Trening: trenovany hrac je oznacen a potvrzen  (team A), pote musi byt oznacen tym proti kteremu se bude trenovat ( team B ), prozatim jen', \
                    '   manualni trening je funkcni ( H / H) prave tlacitko mysi vytvori nove rozestaveni pro trening , klavesa -p- ukonci trening', \
                    '   trening ma vliv na hrace pouze po dostazeni 5000 akci, kdy je trening vyhodnocen pote se muze v treningu pokracovat pocet akci', \
                    '   je vyobrazen pod hrsitem  kotrola hrace pri hre je vysvetlena nize', \
                    '   ' , \
                    'ROZHODCI  ', \
                    ' -Delka utkani  ', \
                    ' -Potvrzeni teamu do hry: teamy jsou vytvoreny v  -team management- mohou byt vybrany do zapasu, cervene oznacene teamy nejsou uplne ', \
                    '   rozhodci je bude ignorovat ,oznaceny hrac je  ovladan  mysi ta urcuje smer a klavesa -w-  je krok,mezernikem je proveden kop do mice  ', \
                    ' -Nastaveni hriste  ', \
                    ' -Zpet na zapas   ', \
                    'NASTAVENI  ', \
                    ' -lokalize  ', \
                    ' -velikost okna aplikace  ', \
                    'LAB MODE  ', \
                    ' -zapnout lab mode  ', \
                    ' -vypnout grafikku  ', \
                    'NAPOVDEA  ']

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
        The_game_window.surface.blit(help_line_rendered,( The_game_window.game_menu_x_start + 50  , 1 * The_game_window.menu_line_spacing + loop_help_print * The_game_window.menu_line_spacing  ))
'''
# icona pro zobrazeni menu
def draw_menu_icon(The_game_window):
    for loop_menu_icon in range (1,4):
        icon_line_rendered = WelcomeFont.render( "-", 1, grey)
        The_game_window.surface.blit(icon_line_rendered,( The_game_window.game_menu_x_start , -15 + 6 * loop_menu_icon   ))
'''




#
