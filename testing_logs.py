
import support_functions
from support_functions import *


def player_trening_info_log(player,action,run_to_save):
    print("cooridnates ",player.rect.center," path_target " ,player.path_target ," action ",action ," run_to_save " ,run_to_save)


def player_toBall_info_log(player,The_ball):
    distanceToBall = pythagoras_distance(player.rect.center, The_ball.rect.center) - player.radius - The_ball.radius
    print("distanceToBall ",distanceToBall  )



def print_all_buttons(buttons):
    for loop in range (0,len(buttons)):
        print ("number ", buttons[loop].number,"        name ", buttons[loop].name)





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
