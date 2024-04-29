import f_menu
from f_menu import *


# -------------------------------------------SCREENS---------------------------------------------------

def draw_teams_for_game(The_game_window,The_field,The_reff):
    shift_from_menu = The_game_window.mngmt_shift_from_menu
    table_line_spacing = int(1.8 * The_game_window.menu_line_spacing)
    column_width = 1* The_game_window.mngmt_column_width
    lines = 12
    columns = 10

    table_top = The_game_window.heading_shift
    table_left = shift_from_menu + The_game_window.game_menu_x_end
    table_bottom = table_top + lines * table_line_spacing
    table_right = table_left + columns * column_width

    team_shift_y = 6 * table_line_spacing  #  lines nazev teamu + 5*hrac = 6
    draw_columns = True

    header = get_scaled_font('MENU_FONT_HEADING', The_game_window.resolution_ratio).render('Teams for game', 1, GREY)
    The_game_window.surface.blit(header,(table_left, 0.1 * The_game_window.menu_line_spacing))
    headings = f_teams_for_game_headings_text_raw(The_game_window.language)

    #spodni linka tabulky
    pygame.draw.lines(The_game_window.surface, GREY_LINES, True, \
                        ((table_right, table_bottom), (table_left, table_bottom)), 2)

    for teams_loop in range (0,2):
        draw_columns = True
        team_name = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render("Team " + The_reff.teams_for_game[teams_loop][0][0] + "    *"  \
                                    + The_reff.teams_for_game[teams_loop + 2] + "*", 1, GREY)
        The_game_window.surface.blit(team_name,(table_left , table_top + teams_loop * team_shift_y))

        pygame.draw.lines(The_game_window.surface, GREY_LINES, True, \
                                ((table_right, table_top + teams_loop * team_shift_y), (table_left, table_top + teams_loop * team_shift_y)), 2)

        # rows
        for player_loop in range (0,5):  # 0 nazev teamu +  5 hracu  => 6 radku
            pygame.draw.lines(The_game_window.surface, GREY_LINES, True, \
                                ((table_left, (player_loop+1) * table_line_spacing + table_top + teams_loop * team_shift_y ), \
                                 (table_right,(player_loop+1) * table_line_spacing + table_top + teams_loop * team_shift_y )), 1)

            #The_game_window.surface.blit(player, (table_left, (player_loop + 1) * table_line_spacing + table_top + teams_loop * team_shift_y))
            # jmeno, "trenovano" ,"trening" ,"skills" , "zapasu", "vyher"
            players = The_reff.teams_for_game[teams_loop] [1:]
            team_details =  10 * [" "]
            team_details[0] = players[player_loop][0]
            team_details[1] = TreningType_text(int(players[player_loop][7]),The_game_window.language)
            team_details[2] = "  " + str(players[player_loop][4])
            team_details[3] = "  " +str(players[player_loop][3])
            team_details[4] = "  " +str(players[player_loop][9])
            # columns
            new_shift = 0
            for player_column in range (0,columns ):
                name_shift = 1 if player_column == 1 else 0
                if draw_columns == True:
                    pygame.draw.lines(The_game_window.surface, GREY_LINES, True, \
                                        ((table_left + (name_shift + player_column) * column_width, table_top), \
                                         (table_left + (name_shift + player_column) * column_width, table_bottom)), 1)

                    column_title = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render(headings[player_column], 1, GREY)
                    The_game_window.surface.blit(column_title,(4 +player_column * column_width + table_left, table_top + teams_loop * team_shift_y))

                if player_column ==1:
                    new_shift =1

                player_details = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render(  team_details[player_column], 1, GREY)
                The_game_window.surface.blit(player_details,(4+ ( player_column+new_shift  )* column_width + table_left,  \
                                                             table_top + (player_loop+1 )   * table_line_spacing + teams_loop * team_shift_y))

            draw_columns = False
            pygame.draw.lines(The_game_window.surface, GREY_LINES, True,((table_right, table_top), \
                                                                         (table_right, table_bottom)), 2)



# teams selection pro hru  MOZNA UZIT PRO STATS???
def draw_stats(The_game_window,The_reff):
    list_of_ingamers = The_reff.list_of_ingamers
    lines = 21  # pocet zobrazenych radku
    column_width = int (1.42 * The_game_window.mngmt_column_width)
    table_line_spacing = int (1.2 * The_game_window.menu_line_spacing)
    columns = 7
    text_ratio = The_game_window.selection_game_text_ratio
    shift_from_menu = The_game_window.mngmt_shift_from_menu

    # hranice tabulky teamu
    table_top = The_game_window.heading_shift
    table_left = shift_from_menu + The_game_window.game_menu_x_end
    table_bottom = table_top +  lines * table_line_spacing
    table_right = table_left + columns * column_width

    text = f_stats_text(The_game_window.language,The_game_window.resolution_ratio)

    The_game_window.surface.blit(text[0], (table_left, 0.1 * The_game_window.menu_line_spacing ))

    ## Vykresleni tabulky
    # Rect(left, top, width, height)
    pygame.draw.rect(The_game_window.surface, GREY, ( table_left, table_top,columns * column_width, lines * table_line_spacing), 1)

    # radky
    shift = 0
    for row_loop in range (0,lines):
        shift = shift + table_line_spacing
        pygame.draw.lines(The_game_window.surface, GREY_LINES, True,((table_left, table_top + shift), (table_right, table_top + shift)), 1)

    # sloupce
    shift = 0
    for colmn_loop in range (0, columns):
        table_headngs_rendered = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render(text[1][colmn_loop], 1, GREY)
        The_game_window.surface.blit(table_headngs_rendered, (table_left + shift  , table_top)) # posun 1/4 sirka boxu
        shift = shift + column_width
        pygame.draw.lines(The_game_window.surface, GREY_LINES, True,((table_left + shift, table_top), (table_left + shift, table_bottom)), 1)

    column_teams_shift =  table_line_spacing
    player_line_shift = 0
    leter_shift_from_boarder = 5    # odsazeni od hran tabulky
    font_diference = 1              # mezera mezi pismem a linkou

    all_teams = The_reff.coach_team_A.loaded_teams_xml + The_reff.coach_team_B.loaded_teams_xml

    # domaci teamy 10 slotu , + 2 sloty hoste   => 12, jina barva pro vybrany team
    for teams_loop in range (0,len(all_teams)):
        team_details = [" "," "," "," "," "," "]
        if all_teams[teams_loop] != SavingType.empty_team_slot.value :  # n prvni char z "none"
            team_color = GREY_LINES
            if all_teams[teams_loop][0][1] != "original" :
                team_color = RED
            else:
                team_details[0] =  TreningType_text(int(The_reff.coach_team_A.check_team_training_type(all_teams,teams_loop)),The_game_window.language)
                team_details[1] = str(The_reff.coach_team_A.team_trenings_summary(all_teams,teams_loop))
                team_details[2] =  str(The_reff.coach_team_A.team_skills_averadge(all_teams,teams_loop))
                team_details[5] =   "         Y" if(all_teams[teams_loop][0][2] == "selected")  else "         N"
                for print_loop in range (0,6):
                    team_details_rendered = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render( team_details[print_loop] , 1, team_color)
                    The_game_window.surface.blit(team_details_rendered,  \
                                (table_left + leter_shift_from_boarder + (1 + print_loop) * column_width, table_top + player_line_shift + column_teams_shift))
            team_name = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render(all_teams[teams_loop][0][0], 1, team_color)
        else:
            team_name = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render( "  --  ", 1, GREY)
        The_game_window.surface.blit(team_name, (table_left + leter_shift_from_boarder, \
                                                table_top + player_line_shift + column_teams_shift))

        player_line_shift = player_line_shift +  table_line_spacing   # *3 team ma jen jmeno a musi se posunout 3 linie dolus

        column_teams_shift = column_teams_shift + table_line_spacing
        player_line_shift = 0

    start_pos_x = The_game_window.game_menu_x_end +The_game_window.mngmt_shift_from_menu
    start_pos_y =  The_game_window.heading_shift +(1+ The_game_window.team_detail_lines ) *  \
                        The_game_window.mngmt_text_ratio * The_game_window.menu_line_spacing + 3*The_game_window.menu_line_spacing

    text_info = f_stats_text_info (The_game_window.language, The_game_window.resolution_ratio)
    for print_loop in range (0,3):
        The_game_window.surface.blit(text_info[print_loop], (start_pos_x, start_pos_y +  (3 + print_loop) * The_game_window.menu_line_spacing))


#stejna funkce pro domaci i hostujici i training, definovano pomoci screen_ID
def draw_team_managemet(The_game_window,The_field,The_reff,screen_ID):
    list_of_ingamers = The_reff.list_of_ingamers
    lines = The_game_window.team_detail_lines
    column_width = The_game_window.mngmt_column_width       #int(1.052 * The_game_window.mngmt_column_width)
    teams_on_page = The_game_window.mngmt_teams_on_page
    text_ratio = The_game_window.mngmt_text_ratio
    shift_from_menu = The_game_window.mngmt_shift_from_menu

    # hranice tabulky teamu
    table_top = The_game_window.heading_shift
    table_left = shift_from_menu + The_game_window.game_menu_x_end
    table_bottom = table_top + text_ratio * lines * The_game_window.menu_line_spacing
    table_right = table_left + teams_on_page * column_width

    # texty
    screen_headeing = teammanagmnt_text_heading(The_game_window.language,screen_ID, The_game_window.resolution_ratio)
    secreen_details = teammanagmnt_text_buttons(The_game_window.language,screen_ID, The_game_window.resolution_ratio)

    coach = The_reff.coach_team_A
    if screen_ID == Screens.teammanagementaway.value:
        coach = The_reff.coach_team_B

    The_game_window.surface.blit(screen_headeing, (table_left,  0.1 * The_game_window.menu_line_spacing))
    The_game_window.surface.blit(secreen_details[0], (table_left,  21.5 * The_game_window.menu_line_spacing))
    if screen_ID != Screens.trening.value:
        The_game_window.surface.blit(secreen_details[1], (table_left + 8 * column_width, 21.5 * The_game_window.menu_line_spacing))
    if screen_ID == Screens.teammanagementaway.value:
        The_game_window.surface.blit(secreen_details[2], (table_left , 23 * The_game_window.menu_line_spacing ))
    if  screen_ID == Screens.trening.value:
        The_game_window.surface.blit(secreen_details[3], (table_left + 2 * column_width, 21.5 * The_game_window.menu_line_spacing))

    ## Vykresleni tabulky
    # Rect(left, top, width, height)
    pygame.draw.rect(The_game_window.surface, GREY, (table_left, table_top,  \
                                teams_on_page * column_width,text_ratio * lines * The_game_window.menu_line_spacing), 1)

    # line(surface, color, start_pos, end_pos, width)
    shift = 0
    for row_loop in range (0,lines):
        shift = shift + text_ratio * The_game_window.menu_line_spacing
        pygame.draw.lines(The_game_window.surface, GREY_LINES, True,((table_left ,table_top + shift ), \
                                                                        (table_right ,table_top + shift)), 1)

    shift = 0
    for row_loop in range (0,teams_on_page):
        shift = shift + column_width
        pygame.draw.lines(The_game_window.surface, GREY_LINES, True, ((table_left + shift, table_top), \
                                                                        (table_left + shift, table_bottom)), 1)

    # zvyrazneni oznaceneho slotu pro vyber , 0.99  0.98 jsou pomery tabulky abe se barvy neprekryvaly
    if coach.selected_slot_team_management[0] >= 0:
        pygame.draw.rect(The_game_window.surface, GREEN, (table_left + coach.selected_slot_team_management[0] * column_width, \
                                                          table_top + coach.selected_slot_team_management[1] * text_ratio * The_game_window.menu_line_spacing, \
                                                          column_width * 0.99, \
                                                          text_ratio  * The_game_window.menu_line_spacing * 0.99), 1)

    # team management screen slot kopiruje , training screen slot jen zvirazni
    if screen_ID == Screens.teammanagement.value:
        color_second_selection = BLUE #RED
    else:
        color_second_selection = BLUE #GREEN

    if coach.selected_slot_team_management_buffer[0] >= 0:
        pygame.draw.rect(The_game_window.surface, color_second_selection, \
                                    (table_left + coach.selected_slot_team_management_buffer[0] * column_width, \
                                     table_top + coach.selected_slot_team_management_buffer[1] * text_ratio * The_game_window.menu_line_spacing, \
                                     column_width * 0.98, \
                                     text_ratio  * The_game_window.menu_line_spacing * 0.98), 1)


    ## Vykresleni tabulky
    column_teams_shift = 0
    player_line_shift = 0
    leter_shift_from_boarder = 5 # odsazeni od hran tabulky
    font_diference = 1           # rozdil mezi fontem a linkou

    for teams_loop in range (0,10):

        # zvirazni team s neulozenou zmenou
        team_color = GREY
        if coach.loaded_teams_xml[teams_loop] != SavingType.empty_team_slot.value \
                and coach.loaded_teams_xml[teams_loop][0][1] != "original" :

            team_color = RED

        players_data =  coach.loaded_teams_xml[teams_loop]
        for players_loop in range (0,6):  # 1 nazev teamu +  5 hracu  => 6 radku
            if players_data == SavingType.empty_team_slot.value :
                break

            # != 0 pak players data
            if players_loop != 0:
                for player_details in range (0,4):      # !!!! PRIZPUSOBIT OPODLE POCTU DETAILS NA HRACE
                    # ID se nezobrazuje
                    if players_data[players_loop] != SavingType.empty_player_slot.value:
                        name_atring = players_data[players_loop][0]
                        space_index = name_atring.find(" ", 0, len(name_atring))
                        name = name_atring[0:space_index]
                        surname = name_atring[space_index:len(name_atring)]

                        if  player_details == 0:#name
                            data = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render(name, 1, team_color)
                        elif player_details == 2:#player_type
                            data = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render(surname, 1, team_color)
                        elif player_details == 3:#trening inputs
                            #data = MENU_FONT.render( players_data[players_loop][player_details], 1, team_color)
                            data = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render(player_type_text(float(players_data[players_loop][2])), 1, team_color)

                        if player_details!=1:# id se nevykresli
                            The_game_window.surface.blit(data, \
                                        (table_left + column_teams_shift + leter_shift_from_boarder, table_top +  player_line_shift))
                            player_line_shift = player_line_shift + The_game_window.menu_line_spacing

                    # prazdny slot
                    else:
                        if player_details!=1:# id se nevykresli
                            player_line_shift = player_line_shift + The_game_window.menu_line_spacing

            # 0 team data
            if players_loop ==0 :
                team_prefix = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render("Team ", 1, GREY)
                The_game_window.surface.blit(team_prefix,(table_left + column_teams_shift + leter_shift_from_boarder, table_top +  player_line_shift))

                team_name = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render(" " + coach.loaded_teams_xml[teams_loop][0][0], 1, GREY)
                The_game_window.surface.blit(team_name,(table_left + column_teams_shift + leter_shift_from_boarder, table_top +  player_line_shift + The_game_window.menu_line_spacing ))


                # vykresleni oznaceneho teamu se neprovede pri treningu
                if screen_ID != Screens.trening.value:
                    if coach.loaded_teams_xml[teams_loop][0][2] == "selected":

                        draw_green_tick([table_left + int(0.2*column_width)+column_teams_shift + leter_shift_from_boarder, \
                                         table_top + int(2.5*The_game_window.menu_line_spacing )],The_game_window)

                player_line_shift = player_line_shift +3* The_game_window.menu_line_spacing   # *3 team ma jen jmeno a musi se posunout 3 linie dolu

        column_teams_shift = column_teams_shift + column_width
        player_line_shift = 0


# print team management tlacitka
def f_print_teammngmt_buttons(The_game_window):
    counter = 0
    dims_taken = False
    button_location = [0,0]
    button_size = [0,0]
    MAIN_MENU_BUTTONS = The_game_window.number_buttons_main_menu
    for loop in range (MAIN_MENU_BUTTONS,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == Screens.teammanagement.value:
            draw_button_No(The_game_window, loop)
            if dims_taken == False:
                dims_taken = True
                button_location  = [The_game_window.buttons[loop].x_corner , The_game_window.buttons[loop].y_corner]
                button_size = The_game_window.buttons[loop].size   # lenght, high

    counter = 5
    counter2 = 8
    pygame.draw.rect(The_game_window.surface, GREY_LINES, ( button_location[0], button_location[1] -5, counter * button_size[0], 2 ),1)
    dot2 = pygame.draw.rect(The_game_window.surface, GREY_LINES,(button_location[0] + button_size[0] /4, button_location[1]  - 10, 10, 5),3)
    The_game_window.surface.fill(GREY_LINES,dot2)
    pygame.draw.rect(The_game_window.surface, GREY_LINES,(button_location[0] + counter2 * button_size[0],button_location[1] - 5, 2 * button_size[0] , 2 ),1)
    dot = pygame.draw.rect(The_game_window.surface, GREY_LINES,(button_location[0] + counter2 * button_size[0] + button_size[0] /4,button_location[1]- 10, 10, 5),3)
    The_game_window.surface.fill(GREY_LINES,dot)


# print team managementaway tlacitka
def f_print_teammngmtaway_buttons(The_game_window):
    number_buttons_main_menu = The_game_window.number_buttons_main_menu
    for loop in range (number_buttons_main_menu,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == Screens.teammanagementaway.value:
            draw_button_No(The_game_window, loop)
            button_location  = [The_game_window.buttons[loop].x_corner, The_game_window.buttons[loop].y_corner]
            button_size = The_game_window.buttons[loop].size   # lenght, high

    counter = 1
    counter2 = 8
    pygame.draw.rect(The_game_window.surface, GREY_LINES,(button_location[0] - counter2 * button_size[0],button_location[1] - 5, 5 * button_size[0], 2 ),1)
    dot2 = pygame.draw.rect(The_game_window.surface, GREY_LINES,(button_location[0] - counter2 * button_size[0] + button_size[0] /4,button_location[1]  - 10, 10, 5),3)
    The_game_window.surface.fill(GREY_LINES,dot2)
    pygame.draw.rect(The_game_window.surface, GREY_LINES,(button_location[0] ,  button_location[1] -5,  button_size[0], 2 ),1)
    dot = pygame.draw.rect(The_game_window.surface, GREY_LINES,(button_location[0] +  button_size[0] /4, button_location[1] - 10, 10, 5),3)
    The_game_window.surface.fill(GREY_LINES,dot)


def draw_ingame_header(The_game_window,The_reff):
    teamA = The_reff.teams_for_game[0][0][0]
    teamB = The_reff.teams_for_game[1][0][0]

    screen_headeing_raw = ingame_text_heading(The_game_window.language)
    screen_headeing = get_scaled_font('WELCOME_FONT', The_game_window.resolution_ratio).render(screen_headeing_raw + '  ' + teamA + ' x ' + teamB, 1, GREY)

    The_game_window.surface.blit(screen_headeing, ( int(1.5* The_game_window.mngmt_column_width ),  0.1 * The_game_window.menu_line_spacing))


# tisk score, reff details pri hre
def f_print_reff_ingame_lower_menu(score,The_game_window,The_field):
    right  = The_field.field_bl_corner[0] + The_field.field_width
    left   = The_field.field_bl_corner[0]
    midd   =  The_field.field_bl_corner[0] + int(The_field.field_width/2)

    #show_score = get_scaled_font("MENU_FONT" ,The_game_window.window_height).render(str(score[0])+ ' : '  + str(score[1]), 1, GREY)
    #The_game_window.surface.blit(show_score, (midd - 35 , 0.1 * The_game_window.menu_line_spacing))

    reff_header = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render("Reff MENU       score: "+str(score[0])+ ' x '  + str(score[1]), 1, GREY)
    The_game_window.surface.blit(reff_header,(The_field.field_bl_corner [0] , The_field.field_bl_corner[1] + The_game_window.menu_line_spacing ))

    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == Screens.ingame.value:
            draw_button_No(The_game_window, loop)


# print trening tlacitka
def f_print_trening_buttons(The_game_window):
    dims_taken = False
    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == Screens.trening.value:
            draw_button_No(The_game_window, loop)
            if dims_taken == False:
                dims_taken = True
                button_location  = [The_game_window.buttons[loop].x_corner , The_game_window.buttons[loop].y_corner ]
                button_size = The_game_window.buttons[loop].size   # lenght, high
    counter = 2
    counter2 = 4
    space_between_lines = 4

    pygame.draw.rect(The_game_window.surface, GREY_LINES, (button_location[0], button_location[1] -5, counter * button_size[0] - space_between_lines, 2 ),1)
    dot2 = pygame.draw.rect(The_game_window.surface, GREY_LINES, ( button_location[0] + button_size[0] /4,button_location[1]  - 10, 10, 5),3)
    The_game_window.surface.fill(GREY_LINES,dot2)

    pygame.draw.rect(The_game_window.surface, GREY_LINES, (button_location[0] + 2 * button_size[0] + space_between_lines , button_location[1] -5, 5.5 * button_size[0] , 2 ),1)
    dot = pygame.draw.rect(The_game_window.surface, GREY_LINES, (button_location[0] + 2 * button_size[0] + button_size[0] /4 , button_location[1]- 10, 10, 5),3)
    The_game_window.surface.fill(GREY_LINES,dot)


# trening manual
def f_print_treningman_buttons(The_game_window,lower_screen_ID):
    dims_taken = False
    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == Screens.treningmanual.value:
            draw_button_No(The_game_window, loop)
            if dims_taken == False:

                dims_taken = True

                if lower_screen_ID == Screens.trainingautomated.value :
                    button_shift = 2
                elif  lower_screen_ID == Screens.trainingoffscreen.value :
                    button_shift = 1
                else:
                    button_shift = 0

                start_button_location  = [The_game_window.buttons[loop].x_corner , The_game_window.buttons[loop].y_corner ]
                selected_button_location = The_game_window.buttons[loop].x_corner + button_shift * 2 * The_game_window.buttons[loop].size[0]
                button_size = The_game_window.buttons[loop].size   # lenght, high

    counter = 1
    pygame.draw.rect(The_game_window.surface, GREY_LINES, ( start_button_location[0]  , start_button_location[1] -5, 5.5 * button_size[0] , 2 ),1)
    dot = pygame.draw.rect(The_game_window.surface, GREY_LINES, ( selected_button_location + button_size[0] /4 , start_button_location[1]- 10, 10, 5),3)
    The_game_window.surface.fill(GREY_LINES,dot)


def f_draw_menu_button(The_game_window):                   #? pouziva se?
    index = len(The_game_window.buttons )- 1
    draw_button_No(The_game_window,index)


def f_print_edit_player_buttons(The_game_window):
    counter = 0
    dims_taken = False
    button_location = [0,0]
    button_size = [0,0]
    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == Screens.teammanagementedit.value:
            draw_button_No(The_game_window, loop)
            if dims_taken == False:
                dims_taken = True
                button_location  = [The_game_window.buttons[loop].x_corner , The_game_window.buttons[loop].y_corner ]
                button_size = The_game_window.buttons[loop].size   # lenght, high
            counter = counter + 1

    pygame.draw.rect(The_game_window.surface, GREY_LINES, ( button_location[0], button_location[1] -5, counter * button_size[0], 2 ),1)
    dot = pygame.draw.rect(The_game_window.surface, GREY_LINES, (button_location[0] + (counter - 2) * button_size[0] + button_size[0] /4, \
                                                                button_location[1]  - 10, 10, 5),3)
    The_game_window.surface.fill(GREY_LINES,dot)



def f_print_teams_for_game_buttons(The_game_window):

    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == Screens.teamsconfirmation.value:
            draw_button_No(The_game_window, loop)

    start_pos_x = The_game_window.game_menu_x_end +The_game_window.mngmt_shift_from_menu
    start_pos_y =  The_game_window.heading_shift +(1+ The_game_window.team_detail_lines ) *  \
                        The_game_window.mngmt_text_ratio * The_game_window.menu_line_spacing + 3*The_game_window.menu_line_spacing

    buton_width = int (The_game_window.mngmt_column_width)

    text_headings = f_teamsforgame_text (The_game_window.language, The_game_window.resolution_ratio)
    The_game_window.surface.blit(text_headings[0], (start_pos_x + 0 * buton_width +2, start_pos_y - int(1.5 * The_game_window.menu_line_spacing)))
    The_game_window.surface.blit(text_headings[1], (start_pos_x + 6 * buton_width +2, start_pos_y - int(1.5 * The_game_window.menu_line_spacing)))

    pygame.draw.rect(The_game_window.surface, GREY_LINES, ( start_pos_x  , start_pos_y -5, 6 * buton_width-2, 2 ),1)
    dot2 = pygame.draw.rect(The_game_window.surface, GREY_LINES,(start_pos_x + buton_width /4, start_pos_y  - 10, 10, 5),3)
    The_game_window.surface.fill(GREY_LINES,dot2)

    pygame.draw.rect(The_game_window.surface, GREY_LINES,(2+ start_pos_x + 6 * buton_width, start_pos_y - 5, 4 * buton_width , 2 ),1)
    dot = pygame.draw.rect(The_game_window.surface, GREY_LINES,(start_pos_x + 6 * buton_width + buton_width/4, start_pos_y- 10, 10, 5),3)
    The_game_window.surface.fill(GREY_LINES,dot)

    text_info = f_teamsforgame_text_info (The_game_window.language, The_game_window.resolution_ratio)
    for print_loop in range (0,3):
        The_game_window.surface.blit(text_info[print_loop], (start_pos_x, start_pos_y +  (3 + print_loop) * The_game_window.menu_line_spacing))



def f_print_create_player_buttons(The_game_window,coach_team_A):
    counter = counter2 = 0
    dims_taken =  False
    button_location = [0,0]
    button_size = button_size2 = [0,0]

    for loop in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == Screens.teammanagementcreate.value:
            draw_button_No(The_game_window, loop)
            if dims_taken == False:
                dims_taken = True
                button_location  = [The_game_window.buttons[loop].x_corner , The_game_window.buttons[loop].y_corner ]
                button_size = The_game_window.buttons[loop].size   # lenght, high
            counter = counter + 1

    # cisla vstupu pro vtvoreni hrace
    inner_counter_skill_buttons = 0
    for loop2 in range (16,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop2].number) == Screens.teammanagementcreateNo.value:
            draw_button_No(The_game_window, loop2)
            inner_counter_skill_buttons = inner_counter_skill_buttons + 1
            if coach_team_A.new_player_isREtrainingRawData == False and inner_counter_skill_buttons == 10:
                break

    pygame.draw.rect(The_game_window.surface, GREY_LINES, ( button_location[0], button_location[1] -5,int(5* The_game_window.mngmt_column_width), 2 ),1)
    dot = pygame.draw.rect(The_game_window.surface, GREY_LINES, \
                                        (button_location[0] + 4 * The_game_window.mngmt_column_width + The_game_window.mngmt_column_width /4 , \
                                         button_location[1]  - 10, 10, 5),3)

    The_game_window.surface.fill(GREY_LINES,dot)

    #sum vybranych skills
    skills_sums = coach_team_A.get_selected_truecount_Nos()
    skills_sums_rendered = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render(str(skills_sums), 1, GREY)
    The_game_window.surface.blit( skills_sums_rendered ,(int(The_game_window.game_menu_x_end + The_game_window.mngmt_shift_from_menu  \
                                                                + 1.4 * The_game_window.mngmt_column_width), \
                                                                 26 * The_game_window.menu_line_spacing))


def f_print_createPlr_details(The_game_window,trainig_code,is_player, isREtrainingRawData):
    shift_x = 0
    shift_y_original = 1 # 2 radky se vynechaji
    shift_y = 1

    text_skills = f_create_player_text_rawRE(The_game_window.language)
    if isREtrainingRawData == False:
        text_skills = f_create_player_text(The_game_window.language)

    #print (trainig_code)
    #The_game_window.surface.fill(BLACK,(The_game_window.game_menu_x_end,The_game_window.game_menu_y_end +5, 300,100))

    jump_over_tvo = False
    counter =0
    if isREtrainingRawData == True:
        jump_over_tvo = True
    #print(   'isREtrainingRawData'  , isREtrainingRawData )
    #print(   'trainig_code'  , trainig_code )
    texthedarer =  "HRAC osobnost" if(The_game_window.language ==  "CZ")  else "PLAYER personality"
    texthedarer_rendered= get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render(texthedarer, 1, GREY)
    The_game_window.surface.blit(texthedarer_rendered,(The_game_window.mngmt_shift_from_menu  + shift_x - 10, \
                                               The_game_window.game_menu_y_end + 2 ))

    for text_loop in range (0,len(text_skills)):

        a = trainig_code[text_loop]
        if jump_over_tvo and text_loop > 1:

            a = trainig_code[counter+ text_loop ]
            counter = counter + 1

        color_print = GREEN if (a == True or a == 'True') else RED
        skill_detail = get_scaled_font('CREATENO_FONT', The_game_window.resolution_ratio).render(text_skills[text_loop], 1, GREY)
        pygame.draw.circle(The_game_window.surface, color_print, (The_game_window.mngmt_shift_from_menu  + shift_x - 5 , \
                                                                      The_game_window.game_menu_y_end + int(0.5* The_game_window.menu_line_spacing) \
                                                                      + The_game_window.menu_line_spacing * shift_y), 2, 2)

        The_game_window.surface.blit(skill_detail,(The_game_window.mngmt_shift_from_menu  + shift_x, \
                                                       The_game_window.game_menu_y_end + The_game_window.menu_line_spacing * shift_y))


        shift_y = shift_y + 1
        if text_loop == 4 or text_loop == 9 :
            shift_x = shift_x + int(2 * The_game_window.mngmt_column_width)
            shift_y = shift_y_original


# print hodnoty z treningu - pocet uskutecnenych  a planovanych 'runs'
def f_print_trening_progress(The_game_window,The_field,coach_team_A,coach_team_B):

    if coach_team_A.active_trening == True:
        trening_progress = len (coach_team_A.data_labels)
        max_trening_progress = coach_team_A.trening_sesion_total_runs
    else:
        trening_progress = len (coach_team_B.data_labels)
        max_trening_progress = coach_team_B.trening_sesion_total_runs

    show_trening_progress = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render( 'PROGRESS:  ' + str(max_trening_progress) + ' / ' +  str(trening_progress), 1, GREY)
    The_game_window.surface.blit(show_trening_progress,(The_field.field_bl_corner [0], \
                                 The_field.field_bl_corner[1] + The_game_window.menu_line_spacing ))

def f_print_player_details_off_game(screen_ID,The_reff,The_game_window):

    coach = The_reff.coach_team_B if screen_ID == Screens.teammanagementaway.value else  The_reff.coach_team_A

    if  coach.selected_slot_team_management[1] > 0 :
        team = coach.selected_slot_team_management[0]
        player_index = coach.selected_slot_team_management[1]
        if coach.loaded_teams_xml[team] !=  SavingType.empty_team_slot.value and \
             coach.loaded_teams_xml[team][player_index] != SavingType.empty_player_slot.value:

            player_data = coach.loaded_teams_xml[team][player_index]
            shift_vertikal = The_game_window.game_menu_y_end + 1
            shift_horisontal = int(7 * The_game_window.mngmt_column_width)                                                                                               #nejak lip definovat  hodnotu
            list_of_tagscz =[ "HRAC info  ","ID: ","typ hrace: ","dovedbosti: ","trenovano: ","vyhrano: ","typ treningu: "]
            list_of_tagsen =[ "INFOEN: ","ID: ","typ hrace: ","dovedbosti: ","trenovano: ","vyhrano: ","typ treningu: "]
            list_of_tags  = list_of_tagscz if The_game_window.language == "CZ" else list_of_tagsen
            indextreningset= 5
            isREtrainingRawData = 8
            #[pl_name, pl_ID,pl_position(type),skills_level,trening_time,skills_set,pocet vyher,trening type,isREtrainingRawData]
            datatoprint = ['', player_data[1] , player_type_text(float(player_data[2]))  , player_data[3] ,  player_data[4] , player_data[6] ,   TreningType_text(int(player_data[7]),The_game_window.language) ]


            for data_index in range (0,7):

                data = get_scaled_font('CREATENO_FONT', The_game_window.resolution_ratio).render(  list_of_tags[data_index] + datatoprint[data_index], 1, GREY)
                if data_index == 0 :
                    data = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render(  list_of_tags[data_index] + datatoprint[data_index], 1, GREY)

                The_game_window.surface.blit(data,( shift_horisontal, shift_vertikal ))
                shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing

            # tisk skils set
            #f_print_createPlr_details(The_game_window,trainig_code,is_player,isREtrainingRawData)
            f_print_createPlr_details(The_game_window,player_data[indextreningset],True, player_data[isREtrainingRawData]   )


# tisk detailu hrace pri hre
def f_print_player_details_ingame(The_game_window,The_field,player,list_of_ingamers):
    shift_vertikal = 0
    shift_horisontal = 300

    if False:#testy                                                                                            #nejak lip definovat  hodnotu
        list_of_tags = ["plrangle: ","plr-ball angle: ","plr-ball distance(cntr-cntr)","velocity: ","site,team: ","sumskils: ","name: "]
        list_of_data =[str(round(player.path_target)), \
                       str(round(player.calculate_angle_to_other_object(list_of_ingamers[0].rect.center))), \
                       str(round(pythagoras_distance (player.rect.center,list_of_ingamers[0].rect.center))), \
                       str(player.velocity), \
                       player.field_site +" , "+ player.team , \
                       str(player.skills_level), \
                       player.name  ]

        for data_index in range (0,len(list_of_data)):
            data = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render(  list_of_tags[data_index] + list_of_data[data_index]   , 1, GREY)
            The_game_window.surface.blit(data,( 5 * The_game_window.mngmt_column_width  , The_game_window.game_menu_y_end  + shift_vertikal ))
            shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing


    if The_game_window.language == "CZ":
        list_of_tags2 = ['Hrac MENU',"jmeno:  ","pozice:  ",  "ID:      " , "sector: "]
    else: list_of_tags2 = ['Player MENU',"name:   ","pos.:   ",  "ID:     " , "sector: "]
    list_of_data2 =['', \
                    player.name, \
                    player_type_text(player.player_type), \
                   player.ID, \
                   str(calculate_sector(1,player.field_site,player.rect.center,[ The_field.field_width,The_field.field_height], The_field.field_bl_corner))]
    shift_vertikal = 0
    for data_index in range (0,len(list_of_data2)):
        data = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render(  list_of_tags2[data_index] + list_of_data2[data_index]   , 1, GREY)
        The_game_window.surface.blit(data,(5 * The_game_window.mngmt_column_width    , The_field.field_bl_corner[1] + The_game_window.menu_line_spacing   + shift_vertikal ))
        shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing




'''
#test prints                                                                                            #testy souradnic
def print_test_x(The_game_window):
    xx = MENU_FONT.render( "XX"  , 1, red)
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
                data_print = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render(  str(round(data[list_index][inner_list_index],4)  ) , 1, GREY)
            else:
                data_print = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render(  data[list_index][inner_list_index] , 1, GREY)
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
        data = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render(  list_of_tags[data_index] + list_of_data[data_index]   , 1, GREY)
        The_game_window.surface.blit(data,(The_field.field_bl_corner [0], The_field.field_bl_corner[1] + The_game_window.menu_line_spacing + shift_vertikal ))
        shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing


# tisk uvitaci plochy
def draw_weclome(The_game_window):
    welcomecz = get_scaled_font('WELCOME_FONT', The_game_window.resolution_ratio).render('Flatball vítejte', 1, GREY)
    welcomeuk = get_scaled_font('WELCOME_FONT', The_game_window.resolution_ratio).render('Flatball welcome', 1, GREY)

    The_game_window.surface.blit(welcomecz,(The_game_window.window_width * 0.4 , The_game_window.window_height * 0.3))
    The_game_window.surface.blit(welcomeuk,(The_game_window.window_width * 0.4 , The_game_window.window_height * 0.5))

def draw_trening_off_screen(The_game_window):
    if The_game_window.language == "CZ":
        welcome = get_scaled_font('WELCOME_FONT', The_game_window.resolution_ratio).render('trening', 1, GREY)
    else:
        welcome = get_scaled_font('WELCOME_FONT', The_game_window.resolution_ratio).render('trening', 1, GREY)

    The_game_window.surface.blit(welcome,(The_game_window.window_width * 0.4 , The_game_window.window_height * 0.3))


# tisk uvitaci plochy
def draw_teams_selection_error(The_game_window):
    if The_game_window.language == "CZ":
        error = get_scaled_font('WELCOME_FONT', The_game_window.resolution_ratio).render('Zkontrolujte vybrane teamy, flatball se hraje v 2 !', 1, GREY)
    else:
        error = get_scaled_font('WELCOME_FONT', The_game_window.resolution_ratio).render('Required 2 teams for the game!', 1, GREY)

    The_game_window.surface.blit(error,(The_game_window.game_menu_x_end +10 , The_game_window.window_height * 0.3))


# error  screen
def draw_error(The_game_window):
    if The_game_window.language == "CZ":
        error = get_scaled_font('WELCOME_FONT', The_game_window.resolution_ratio).render('Ooo, kde sou hraci? Treneři nevybrali teamy.', 1, GREY)
    else:
        error = get_scaled_font('WELCOME_FONT', The_game_window.resolution_ratio).render('D\'oh, where are the players?', 1, GREY)

    The_game_window.surface.blit(error,(The_game_window.window_width * 0.3 , The_game_window.window_height * 0.3))

# tisk paused game
def draw_paused_game(The_game_window):
    if The_game_window.language == "CZ":
        paused = get_scaled_font('WELCOME_FONT', The_game_window.resolution_ratio).render('Hra pozastavena', 1, GREY)
    else:
        paused = get_scaled_font('WELCOME_FONT', The_game_window.resolution_ratio).render('Game paused', 1, GREY)

    The_game_window.surface.blit(paused,(The_game_window.window_width * 0.4 , The_game_window.window_height * 0.3))


# pomocna funkce, pythagorovo pravidlo
def pythagoras_distance (location_1,location_2):                                                                            #stejna funkce v 2 modulech Zkontroluj
    ingamer_adjescent =  abs (location_1[0]  -  location_2[0])
    ingamer_opposite =  abs (location_1[1] -  location_2[1])
    ingamer_hypotensue = sqrt(ingamer_adjescent **2 + ingamer_opposite **2)
    return round(ingamer_hypotensue,4)

# napoveda

def f_print_help_trening(The_game_window):
    text =  f_help_trening_text(The_game_window.language,The_game_window.resolution_ratio)
    The_game_window.surface.blit(text[0],(The_game_window.game_menu_x_end + 50, The_game_window.menu_line_spacing))
    The_game_window.surface.blit(text[1],(The_game_window.game_menu_x_end + 50,2* The_game_window.menu_line_spacing))

def f_print_RE_trening_inprogress(The_game_window):
    text =  f_RE_trening_inprogress_text(The_game_window.language ,The_game_window.resolution_ratio)
    The_game_window.surface.blit(text,(The_game_window.game_menu_x_end, 20 * The_game_window.menu_line_spacing))

def f_print_RE_trening_done(The_game_window):
    text =  f_RE_trening_done_text(The_game_window.language,The_game_window.resolution_ratio)
    The_game_window.surface.blit(text,(The_game_window.game_menu_x_end, 30 * The_game_window.menu_line_spacing))

def f_print_RE_trening_started(The_game_window):
    text =  f_RE_trening_started_text(The_game_window.language,The_game_window.resolution_ratio)
    The_game_window.surface.blit(text,(The_game_window.game_menu_x_end, 30 * The_game_window.menu_line_spacing))

def f_print_message_in_lower_screen(text):
    The_game_window.surface.blit(text,(The_game_window.game_menu_x_end, 30 * The_game_window.menu_line_spacing))



def f_print_help(The_game_window):
    helpText="none"
    if The_game_window.language == "CZ":
        help_heading = get_scaled_font('MENU_FONT_HEADING', The_game_window.resolution_ratio).render('NAPOVEDA', 1, GREY)
    else:
        help_heading = get_scaled_font('MENU_FONT_HEADING', The_game_window.resolution_ratio).render('GAME GUIDE', 1, GREY)
    The_game_window.surface.blit(help_heading, (The_game_window.window_width * 0.4 , 0.5 * The_game_window.menu_line_spacing))

    helpText = f_help_text(The_game_window.language)                                                                                                                    #end line

    for loop_help_print in range (0,len(helpText)):
        help_line = helpText[loop_help_print]
        help_line_rendered = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render( help_line, 1, GREY)
        The_game_window.surface.blit(help_line_rendered,( The_game_window.game_menu_x_start + 50, \
                                                        1 * The_game_window.menu_line_spacing + loop_help_print * The_game_window.menu_line_spacing ))
'''
# icona pro zobrazeni menu
def draw_menu_icon(The_game_window):
    for loop_menu_icon in range (1,4):
        icon_line_rendered = WELCOME_FONT.render( "-", 1, GREY)
        The_game_window.surface.blit(icon_line_rendered,( The_game_window.game_menu_x_start , -15 + 6 * loop_menu_icon   ))
'''


def print_check_pin(The_game_window,errorCode):
    if errorCode == ErrorCodes.OK.value:
        return
    errorText = get_errormessage_by_errorcode(errorCode)
    positive_codes = [  ErrorCodes.plselectedfromslot.value, ErrorCodes.matchterminated.value ,ErrorCodes.trainingautomateddone.value  ]

    if   is_number_in_array(errorCode,positive_codes):
        color = GREY
        header_pin_text = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render('OK :)', 1, GREY)
    else:
        color = RED
        header_pin_text = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render('Ajajaj :(', 1, GREY)

    if The_game_window.language == "CZ":
        check_pin_text = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render(errorText[0], 1, color)
    else:
        check_pin_text = get_scaled_font('MENU_FONT', The_game_window.resolution_ratio).render(errorText[1], 1, color)

    The_game_window.surface.blit(header_pin_text,( The_game_window.game_menu_x_start , 20 * The_game_window.menu_line_spacing ))
    The_game_window.surface.blit(check_pin_text,( The_game_window.game_menu_x_start , 21 * The_game_window.menu_line_spacing ))


def draw_settings_windowAndGrafic(The_game_window):
    number_buttons_main_menu =   The_game_window.number_buttons_main_menu
    shift_from_menu = The_game_window.mngmt_shift_from_menu
    # hranice tabulky teamu
    table_left = shift_from_menu + The_game_window.game_menu_x_end

    # texty
    texts = windowAndGrafic_text_heading(The_game_window.language,The_game_window.resolution_ratio)
    screen_headeing = texts[0]
    secreen_details = texts[1]
    shift_y_from_top = The_game_window.menu_line_spacing * 4 -4
    The_game_window.surface.blit(screen_headeing, (table_left,  0.1 * The_game_window.menu_line_spacing))
    The_game_window.surface.blit(secreen_details[0], (table_left,  0 * The_game_window.menu_line_spacing  + shift_y_from_top))
    The_game_window.surface.blit(secreen_details[1], (table_left , 3 * The_game_window.menu_line_spacing  + shift_y_from_top))
    The_game_window.surface.blit(secreen_details[2], (table_left , 6 * The_game_window.menu_line_spacing  + shift_y_from_top ))

    for loop in range (number_buttons_main_menu,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == Screens.windowandgrafic.value:
            draw_button_No(The_game_window, loop)


def draw_settings_trening(The_game_window,The_reff):
    number_buttons_main_menu = The_game_window.number_buttons_main_menu
    shift_from_menu = The_game_window.mngmt_shift_from_menu
    # hranice tabulky teamu
    table_left = shift_from_menu + The_game_window.game_menu_x_end
    shift_y_from_top = The_game_window.menu_line_spacing * 4 -4
    # texty
    texts = settingstrening_text_heading(The_game_window.language,The_game_window.resolution_ratio)
    screen_headeing, secreen_details = texts

    The_game_window.surface.blit(screen_headeing, (table_left,  0.1 * The_game_window.menu_line_spacing))
    shift_y = 0
    for loop_print in range (0,len( secreen_details)):

        The_game_window.surface.blit(secreen_details[loop_print], (table_left, shift_y * The_game_window.menu_line_spacing  + shift_y_from_top  ))

        if loop_print == 2:
            shift_y  = shift_y + 4
        else:
            shift_y = shift_y + 3

    for loop in range (number_buttons_main_menu,len(The_game_window.buttons)):
        if trunc(The_game_window.buttons[loop].number) == Screens.settingstraining.value:                                                           #?? neni i v hlavnim neu??

            draw_button_No(The_game_window, loop)


#
#-------------------------------------------------------texty--------------------------------------------------------------

def f_stats_text (language, resolution_ratio):
    text = [0,0]
    if language == "CZ":
        text[0] = get_scaled_font('MENU_FONT_HEADING', resolution_ratio).render('Herní statistiky', 1, GREY)
        text[1] = ["  Team"," Trénovano" ,"Tréningů" ,"prum. skills", "prum. Zápasů", "prum. Výher", " Vybrán do hry" ] #,   "   trenovano" ,"trening" ,"prum skills" , "zapasu", "vyher", "vybrano"]
    else:
        text[0] = get_scaled_font('MENU_FONT_HEADING', resolution_ratio).render('Teams statistics', 1, GREY)
        text[1] = ["  Team"," Tren. type" ," Sum trenin." ,"avr. skills" , "avr.  Games", "avr.   Wins", " Is selected" ]
    return text

def f_teamsforgame_text (language, resolution_ratio):
    text = [0,0]
    if language == "CZ":
        text[0] = get_scaled_font('MENU_FONT', resolution_ratio).render('Nastaveni zapasu', 1, GREY)
        text[1] = get_scaled_font('MENU_FONT', resolution_ratio).render('Volby zapasu', 1, GREY)
    else:
        text[0] = get_scaled_font('MENU_FONT', resolution_ratio).render('Match settings ', 1, GREY)
        text[1] = get_scaled_font('MENU_FONT', resolution_ratio).render('Match runs', 1, GREY)
    return text

def f_teamsforgame_text_info (language, resolution_ratio):
    text = [0,0,0]
    if language == "CZ":
        text[0] = get_scaled_font('MENU_FONT', resolution_ratio).render('Nasta...................veni zapasu', 1, GREY)
        text[1] = get_scaled_font('MENU_FONT', resolution_ratio).render('Vol..................by zapasu', 1, GREY)
        text[2] = get_scaled_font('MENU_FONT', resolution_ratio).render('Vo   ................lby zapasu', 1, GREY)
    else:
        text[0] = get_scaled_font('MENU_FONT', resolution_ratio).render('Match.................. settings ', 1, GREY)
        text[1] = get_scaled_font('MENU_FONT', resolution_ratio).render('Mat..................ch runs', 1, GREY)
        text[2] = get_scaled_font('MENU_FONT', resolution_ratio).render('Mat..............ch runs', 1, GREY)
    return text

def f_stats_text_info (language, resolution_ratio):
    text = [0,0,0]
    if language == "CZ":
        text[0] = get_scaled_font('MENU_FONT', resolution_ratio).render('Nastfsfsfda...................veni zapasu', 1, GREY)
        text[1] = get_scaled_font('MENU_FONT', resolution_ratio).render('Vsfsdfsol..................by zapasu', 1, GREY)
        text[2] = get_scaled_font('MENU_FONT', resolution_ratio).render('Vo   ...sdfs.............lby zapasu', 1, GREY)
    else:
        text[0] = get_scaled_font('MENU_FONT', resolution_ratio).render('Masdfdddstch.................. settings ', 1, GREY)
        text[1] = get_scaled_font('MENU_FONT', resolution_ratio).render('Mat.fsfdsffsd.................ch runs', 1, GREY)
        text[2] = get_scaled_font('MENU_FONT', resolution_ratio).render('Mat.sfsdsfsf.............ch runs', 1, GREY)
    return text


def f_teams_for_game_headings_text_raw (language):
    if language == "CZ":
        text = [" "," " ," Trénovano" ," Tréningů" ,"  Skills" , "  Zápasů", "  Výher",  "note_a" ,"note_b" , "notec" ]
    else:
        text = [" "," " ," Trening " ,"Trenings" ,"Skills" , " Games", " Wins","note_a" ,"note_b"  , "notec"]
    return text

def teammanagmnt_text_heading (language,screen_ID, resolution_ratio):
    screen_headeing = "none"
    if language == "CZ":
        if screen_ID == Screens.teammanagement.value:
            screen_headeing = get_scaled_font('MENU_FONT_HEADING', resolution_ratio).render('Team management', 1, GREY)
        elif screen_ID == Screens.trening.value:
            screen_headeing = get_scaled_font('MENU_FONT_HEADING', resolution_ratio).render('Hráč trening', 1, GREY)
        elif screen_ID == Screens.teammanagementaway.value:
            screen_headeing = get_scaled_font('MENU_FONT_HEADING', resolution_ratio).render('Team management pro team hostů', 1, GREY)
    else:
        if screen_ID == Screens.teammanagement.value:
            screen_headeing = get_scaled_font('MENU_FONT_HEADING', resolution_ratio).render('Team management', 1, GREY)
        elif screen_ID == Screens.trening.value:
            screen_headeing = get_scaled_font('MENU_FONT_HEADING', resolution_ratio).render('Player training', 1, GREY)
        elif screen_ID == Screens.teammanagementaway.value:
            screen_headeing = get_scaled_font('MENU_FONT_HEADING', resolution_ratio).render('Team managemen guest team', 1, GREY)

    return  screen_headeing

def windowAndGrafic_text_heading (language, resolution_ratio):
    screen_headeing = ['x',['x','x','x']]
    if language == "CZ":
        screen_headeing[0] = get_scaled_font('MENU_FONT_HEADING', resolution_ratio).render('windowAndGrafic  cz', 1, GREY)
        screen_headeing[1][0] = get_scaled_font('MENU_FONT', resolution_ratio).render('Rozliseni', 1, GREY)
        screen_headeing[1][1] = get_scaled_font('MENU_FONT', resolution_ratio).render('Pixel art pro hrace', 1, GREY)
        screen_headeing[1][2] = get_scaled_font('MENU_FONT', resolution_ratio).render('Vizualizace automatizovaneho treningu', 1, GREY)
    else:
        screen_headeing[0] = get_scaled_font('MENU_FONT_HEADING', resolution_ratio).render('windowAndGrafic  en', 1, GREY)
        screen_headeing[1][0] = get_scaled_font('MENU_FONT', resolution_ratio).render('Resolution', 1, GREY)
        screen_headeing[1][1] = get_scaled_font('MENU_FONT', resolution_ratio).render('Pixel art for players', 1, GREY)
        screen_headeing[1][2] = get_scaled_font('MENU_FONT', resolution_ratio).render('rendering of automated treining', 1, GREY)
    return  screen_headeing

def settingstrening_text_heading (language, resolution_ratio):
    screen_headeing = ['x',['x','x','x','x','x','x']]
    if language == "CZ":
        screen_headeing[0] = get_scaled_font('MENU_FONT_HEADING', resolution_ratio).render('Nastavení tréningů a zápasu', 1, GREY)
        screen_headeing[1][0] = get_scaled_font('MENU_FONT', resolution_ratio).render('Počet kroků v manuálním treningu.', 1, GREY)
        screen_headeing[1][1] = get_scaled_font('MENU_FONT', resolution_ratio).render('Automayicke', 1, GREY)
        screen_headeing[1][2] = get_scaled_font('MENU_FONT', resolution_ratio).render('Počet kroků v jednotlivých treninzích a počet tréningů.', 1, GREY)
        screen_headeing[1][3] = get_scaled_font('MENU_FONT', resolution_ratio).render('Trénovaný x soupeřův team. Lze vypnout pohyb ostatních hráčů při tréningu. A to pro oba teamy zvlášť.', 1, GREY)
        screen_headeing[1][4] = get_scaled_font('MENU_FONT', resolution_ratio).render('Delka hry[min]', 1, GREY)
        screen_headeing[1][5] = get_scaled_font('MENU_FONT', resolution_ratio).render('Předprocesovaná data pro AI rozhodování', 1, GREY)
    else:
        screen_headeing[0] = get_scaled_font('MENU_FONT_HEADING', resolution_ratio).render('Ternings and game settings', 1, GREY)
        screen_headeing[1][0] = get_scaled_font('MENU_FONT', resolution_ratio).render('Number of steps for manual trening.', 1, GREY)
        screen_headeing[1][1] = get_scaled_font('MENU_FONT', resolution_ratio).render('??????', 1, GREY)
        screen_headeing[1][2] = get_scaled_font('MENU_FONT', resolution_ratio).render('Number of steps for each trening, number of trenings', 1, GREY)
        screen_headeing[1][3] = get_scaled_font('MENU_FONT', resolution_ratio).render('Trained  x the second team. For each team is option to diable team mates movenemt during training.', 1, GREY)
        screen_headeing[1][4] = get_scaled_font('MENU_FONT', resolution_ratio).render('Game time[min]', 1, GREY)
        screen_headeing[1][5] = get_scaled_font('MENU_FONT', resolution_ratio).render('Preprocessed data set for neural network input', 1, GREY)
    return  screen_headeing


def teammanagmnt_text_buttons (language,screen_ID, resolution_ratio):
    text = [ "none" ,  "none",  "none" ,  "none"  ]
    if language == "CZ":
        if True :                                                      # screen_ID == Screens.teammanagement.value:
            text[0] = get_scaled_font('MENU_FONT', resolution_ratio).render('HRAC', 1, GREY)
            text[1] = get_scaled_font('MENU_FONT', resolution_ratio).render('TEAM', 1, GREY)
            text[2] = get_scaled_font('MENU_FONT', resolution_ratio).render('Souperovy hráči zmněna nepovolena', 1, GREY)
            text[3] = get_scaled_font('MENU_FONT', resolution_ratio).render('TRENING', 1, GREY)
    else:
        if True :                                                        #screen_ID == Screens.teammanagement.value:
            text[0] = get_scaled_font('MENU_FONT', resolution_ratio).render('PLAYER', 1, GREY)
            text[1] = get_scaled_font('MENU_FONT', resolution_ratio).render('TEAM', 1, GREY)
            text[2] = get_scaled_font('MENU_FONT', resolution_ratio).render('Opponets team update not allowed ', 1, GREY)
            text[3] = get_scaled_font('MENU_FONT', resolution_ratio).render('TRENING', 1, GREY)
    return  text


def ingame_text_heading(language):
    if language == "CZ":
        text = 'Hra'
    else:
        text = 'Game'
    return text




def f_help_text(language):
    if language == "CZ":
        helpText =[' ', \
                    'TRENER   ', \
                    ' -Team management: ', \
                    '   Aplikace ma ulozen jeden vytvoreny (default) team. Z tohoto teamu můze byt hrac kopirovan do jineho ci noveho teamu. Hrac tez muze' , \
                    '   byt generovan zcela novy, v tomto pripade lze urcit jak dobry hrac bude (level). Jakmile je 5 hracu v teamu zmena musi byt ulozena. ',  \
                    '   Uzivatel oznaci team a v kombinaci s tlacitkem ulozit zmeny se team zapise.Pokud je zapis v poradku team zmeni barvu z cervene na bilou.',   \
                    '   V pripade kopirovani/vytvoreni hrace do prazdneho teamu, hra vytvori novy automaticky. Zkopirovani hraci ziskaji stejny  level i ',  \
                    '   natrenovane schopnosti od originalniho hrace po oznaceni teamu jej lze vybrat do utkani ',  \
                    ' -Stats: staistika hracu a teamu ', \
                    ' -Trening: ', \
                    '   Vzdy je trenovan pouze jeden hrac. Trenovany hrac musi byt uzivatelem oznacen a potvrzen, pote musi byt oznacen tym proti kteremu se bude ', \
                    '   trenovat. Lze vybrat v jake casti hriste bude trening probihat (brankar - 1. tretina hriste) ', \
                    '   MANUALNI trening znamena ze uzivatel sam trenuje fotbaloveho hrace(supervised). Zde jsou dve moznisti a) kde je pohyb ostatnich hracu ', \
                    '   vypnut b) hraci se pohybuji . Uzivatel muze vybrat jeden z 5 ukonu a to: pootocit hrace , udelat krok, kopnout do mice a nebo povtrdit ', \
                    '   /no action/, napr. pokud se trenuje brankar a mic je na druhe strane hriste neocekava se od brankare zadna akce. Uzivatel muze prepmnout ', \
                    '   na novou herni situaci aby trenink byl co nejvice efektivni. Trening ma vliv na hrace pouze po dostazeni celeho treningu (stav vyobrazen), ', \
                    '   pote je trening vyhodnocen .AUTOMATIZOVANY trening je plnne rizen pocitacem, v prubehu treningu je uzamcena obrazovka a tez vyobrazen prubeh.', \
                    '   Aby byl tento trening efektivni je zapotrebi alespon 1M akci, jeden trening ja nastaven na 10 opakovani pro 10k behu => 100000', \
                    '   poznamka: jedna akce/beh je mysleno jeden vyber z 5 moznych ukonu, pokud se hrac otoci udela krok a pote se znovu otoci vykonal 3 akce. ', \
                    '   ' , \
                    'ROZHODCI  ', \
                    ' -Potvrzeni teamu do hry: teamy jsou vybrany do zapasu v  /team management/, cervene oznacene teamy nejsou ulozene/uplne rozhodci je neuzna .', \
                    '  Lze vybrat ze dvou zapasu uzivatel proti Pc a nebo dva teamy ovladane pocitacem proti sobe. pote je spusten zapas.' , \
                    '  Pri prvni forme hry lze oznaci z kontrolovaneho teamu jakehokoli hrace ,oznaceny hrac je  ovladan  mysi ta urcuje smer, klavesa -w- je krok, ', \
                    '  mezernikem je proveden kop do mice, pokud je hra pozastaven lze se vratit z menu tlacitkem /Zpet na zapas /. Lze mit zapocatou poze jednu hru. ', \
                    ' -Nastaveni hriste  ', \
                    ' -Zpet na zapas   ' ]

    else:
        helpText =['FLATBALL', \
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

    return helpText


def teams_names (index):
    team = "null"
    list=["team1", "t2", "t3",  "t4" ,"t54", "ta" ,"tr", "tw" ,"uyy" , \
         "t74t" ,"t58t" ,"t4" ,"t75t" ,"tpt" ,"ttd" ,"dt" ]

    if index >=0 and index < len(list):
        team =  list[index]

    return team

def players_names (index):
    player_name = "Best Player"
    list=["Max Aarons","Rolando Aarons","Tammy Abraham","Che Adams","Adrián Mcdowel","Adrián Bernabé","Adrien Silva","Dan Adshead", \
        "Nathan Aké","Marc Albrighton","Toby Alderweireld","Aleix García","Trent Alexander-Arnold","Albian Ajeti","Pierre Aubameyang", \
        "Alisson Lee","Tom Allan","Dele Alli","Miguel Almirón","Steven Alzate","Daniel Amartey","Ethan Ampadu","Joseph Anang", \
        "André Gomes","Andreas Pereira","Michail Antonio","Stuart Armstrong","Arnau Puigmal","Daniel Arzani","Christian Atsu", \
        "Serge Aurier","Jordan Ayew","Ayoze Pérez","Abdul Rahman Baba","Daniel Bachmann","Eric Bailly","Leighton Baines", \
        "Fabián Balbuena","George Baldock","Folarin Balogun","Tudor Băluţă","Beni Baningime","Phil Bardsley","Ross Barkley","Ashley Barnes", \
        "Harvey Barnes","Chris Basham","Lewis Bate","Michy Batshuayi","Jack Bearne","Jan Bednarek","Ryan Bennett","Josh Benson", \
        "Nabil Bentaleb","Christian Benteke","Sander Berge","Steven Bergwijn","Bernardo Rosa","Bernardo Silva","Ryan Bertrand", \
        "Muhamed Bešić","Philip Billing","Yves Bissouma","Tolaji Bola","Yannick Bolasie","Willy Boly","Artur Boruc","Sofiane Boufal", \
        "Jarrod Bowen","Morgan Boyes","Robbie Brady","Jarrad Branthwaite","Claudio Bravo","Armando Broja","David Brooks","Josh Brownhill", \
        "Bruno Fernandes","Bruno Jordão","Emiliano Buendia","Dan Burn","Matt Butcher","David Button","Oskar Buur","Sam Byram", \
        "Willy Caballero","Gary Cahill","Jake Cain","Dominic Lewin","Leonardo Campana","Todd Cantwell","Étienne Capoue", \
        "Guido Carrillo","Andy Carroll","Scott Carson","Lewis Cass"]

    if index >=0 and index < len(list):
        player_name =  list[index]

    return player_name


def f_help_trening_text(language,resolution_ratio):
    if language == "CZ":
        textkeyboard = get_scaled_font('MENU_FONT', resolution_ratio).render('Klavesnice:  mezerník - kop do míče, w - krok,e -  bez akce, p - ukoncení tréningu, z - restart pozic na dvojstup   ', 1, GREY)
        textmouse = get_scaled_font('MENU_FONT', resolution_ratio).render('Myš:  pravé tlačítko - nova pozice hráče', 1, GREY)
    else:
        textkeyboard = get_scaled_font('MENU_FONT', resolution_ratio).render('Keyboard:  space - kick, w - step, e -  no action, p - terminate trening, z - restart positions to strat match standing', 1, GREY)
        textmouse = get_scaled_font('MENU_FONT', resolution_ratio).render('Mouse:  right click - new player position', 1, GREY)
    return  [textkeyboard ,textmouse ]

def f_creating_player_text(language,resolution_ratio):
    text = "null"
    return text
    if language == "CZ":
        text = get_scaled_font('MENU_FONT', resolution_ratio).render('generovani hrace', 1, GREY)
    else:
        text = get_scaled_font('MENU_FONT', resolution_ratio).render('player generating', 1, GREY)
    return  text


def f_RE_trening_inprogress_text(language,resolution_ratio):
    text = "null"
    if language == "CZ":
        text = get_scaled_font('MENU_FONT', resolution_ratio).render('trening ted´ probíha', 1, GREY)
    else:
        text = get_scaled_font('MENU_FONT', resolution_ratio).render('trening in progress', 1, GREY)

    return  text


def f_RE_trening_done_text(language,resolution_ratio):
    text = "null"
    if language == "CZ":
        text = get_scaled_font('MENU_FONT', resolution_ratio).render('trening hotov', 1, GREY)
    else:
        text = get_scaled_font('MENU_FONT', resolution_ratio).render('trening is done', 1, GREY)

    return  text

def f_RE_trening_started_text(language,resolution_ratio):
    text = "null"
    if language == "CZ":
        text = get_scaled_font('MENU_FONT', resolution_ratio).render('trening začal', 1, GREY)
    else:
        text = get_scaled_font('MENU_FONT', resolution_ratio).render('trening started', 1, GREY)

    return  text

def f_create_player_text(language):
    text = [0,0,0,0,0,0,0]
    if language == "CZ":
        text =["uhel pohledu", \
                "pozice v teamu", \
                "mujsector" , \
                "vzadlenost od míče" , \
                "uhel nejbl. spoluhrače" , \
                "vzdalensost nejbl. spoluhráče" , \
                "uhel nejbl. protihráče" , \
                "vzdalensost nejbl. protihráče" , \
                "je hrac nejbíže k míči" , \
                "uhel hrače k míči " ]
    else:
        text =["wiev angle" , \
                "position in team", \
                "sector" , \
                "distance to ball" , \
                "angle to closest team mate" , \
                "distance to closest team mate" , \
                "angle to closest 2.team plr." , \
                "distance to closest 2.team plr." , \
                "is player closets to ball" , \
                "angle to ball" ]

    return  text


def f_create_player_text_rawRE(language):
    text = [0,0,0,0,0,0,0]
    if language == "CZ":
        text =["uhel pohledu", \
             "pozice v teamu", \
             "pozice mice" , \
             "pozice spoluhrace č.1", \
             "pozice spoluhrace č.2", \
             "pozice spoluhrace č.3", \
             "pozice spoluhrace č.4", \
             "pozice spoluhrace č.5", \
             "pozice protihrace č.1", \
             "pozice protihrace č.2", \
             "pozice protihrace č.3", \
             "pozice protihrace č.4", \
             "pozice protihrace č.5"]
    else:
        text =["wiev angle" , \
             "position in team", \
             "coordinates team mate č.1", \
             "coordinates team mate č.2", \
             "coordinates team mate č.3", \
             "coordinates team mate  č.4", \
             "coordinates team mate č.5", \
             "coordinates 2.team plr. č.1", \
             "coordinates 2.team plr. č.2", \
             "coordinates 2.team plr. č.3", \
             "coordinates 2.team plr. č.4", \
             "coordinates 2.team plr. č.5"]

    return  text


    #----------------------------------------testy
def test_print_lines(The_game_window):
    text = MENU_FONT.render('A', 1, GREY)
    shift_y = 0
    for loop_print in range (0,30):
        The_game_window.surface.blit(text, (The_game_window.game_menu_x_end + 3, shift_y * The_game_window.menu_line_spacing    ))
        shift_y  = shift_y + 1
