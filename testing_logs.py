
import support_functions
from support_functions import *

import neural_network
from neural_network import *


def player_trening_info_log(player,action,run_to_save):
    print("cooridnates ",player.rect.center," path_target " ,player.path_target ," action ",action ," run_to_save " ,run_to_save)


def player_toBall_info_log(player,The_ball):
    distanceToBall = pythagoras_distance(player.rect.center, The_ball.rect.center) - player.radius - The_ball.radius
    print("distanceToBall ",distanceToBall  )



def print_all_buttons(buttons):
    for loop in range (0,len(buttons)):
        print ("number ", buttons[loop].number,"        name ", buttons[loop].name)



def print_players_summary(loaded_teams_xml ):
    for loop in range (0,2):
        for loop2 in range (1,6):
            path = get_path_home_folder()
            id = loaded_teams_xml [loop][loop2][1]
            model = load_model_from_5h(path +  id  + ".h5")
            print (  'id'   ,id   ,  'skilss                '    ,  loaded_teams_xml [loop][loop2][3]     )
            print (  'mmodel summ'   ,model.summary())


def print_all_indexes_from_menu_TESTING(list_in, repeat_level):
    for loop in range (0,len(list_in)):
        if ( (type(list_in[loop]) is list )   and repeat_level < 1) :
            print ("level " , repeat_level   , "index ", loop)
            print_all_indexes_from_menu_TESTING(list_in[loop], repeat_level + 1)
        else:
            print ("level " , repeat_level   , "index ", loop)
            print ( list_in[loop])

    print (" ----------------x--------------   ")




def TEST_button2( The_game_window,The_field,The_reff, position_clicked):
    if position_clicked[0] <    20 and position_clicked[1] >    The_game_window.window_height -20 :
        for loop in range (1,11):
            print ( loop,   '   plr  '  , The_reff.list_of_ingamers[loop].get_NN_data(The_field,The_reff.list_of_ingamers))
            print ( loop,   '   rewis  '  , The_reff.list_of_ingamers[loop].isREtrainingRawData)


def TEST_button1( The_game_window,The_field,The_reff, position_clicked):
    if position_clicked[0] <    20 and position_clicked[1] >    The_game_window.window_height -20 :
        The_reff.update_teams_game_stats()

#testy
#print("----testy-------------------------------")
#print ("The_game_window.window_height",The_game_window.window_height  )
#print ("The_game_window.width",The_game_window.window_width  )
if False:
    for btnloop in range (0,len(The_game_window.buttons)):
        print(vars(The_game_window.buttons[btnloop]))

    print ("The_game_window.menu_line_spacing ", The_game_window.menu_line_spacing)
    print ("The_game_window.window_height",The_game_window.window_height  )
if False:
    print("-fitrening  ",The_reff.coach_team_A.training_areas_player )
    print("-field_bl_corner ",The_field.field_bl_corner )
    print("--testy---------------------------------")
