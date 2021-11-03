import pygame
from math import sqrt, exp, floor, trunc, atan, cos, sin, radians, degrees
from enum import Enum

# barvy
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
DARK_BLUE = (0,0,128)
WHITE = (255,255,255)
BLACK = (0,0,0)
PINK = (255,200,200)
GREY = (192,192,192)
GREY_LINES = (102,102,102)
GREEN_FIELD =(0, 128, 43)
YELLOW_SELECTED_ITEMS = (255, 255, 153)
GREY_BUTTONS = (64,64,64)

debug_mode = 0
debug_mode2 = 0

# screen menum
class Screens(Enum):
    welcome = 0
    coach = 1
    teammanagement = 2
    teammanagementaway = 22
    teammanagementedit = 21
    teammanagementcreate = 23
    teammanagementcreateNo = 24
    stats = 3
    statsdetail = 31
    trening = 4
    intrening = 41
    treningmanual = 42
    trainingoffscreen = 43
    #reffingame = 5   pouzito???
    matchlenght = 6
    teamsconfirmation =7
    ingame = 71
    fieldsettings = 8
    backtogame = 9
    settings = 10
    language = 11
    windowsize = 12
    lab = 13
    labmodswitcher = 14
    help = 15
    error = 404

'''
Screens.ingame.value
'''

# game status menum
class GameStatus(Enum):
    nogame =  0
    playing = 1
    paused  = 2
    set = 3

# game type menum
class GameType(Enum):
    game =  0
    paused = 1
    mantraining = 3
    autotraining = 4

class SavingType(Enum):
    empty_team_slot =  0
    empty_player_slot = 1

class PlayerType(Enum):
    GK =  1
    leftdefender = 2
    rightdefender = 3
    middfielder = 4
    striker= 5

def player_type_text(No_type):
    #print("sss",No_type )
    type = "null"
    if No_type == 1:
        type =  "GK"
    elif No_type == 2:
        type =  "Right df"
    elif No_type == 3:
        type =  "Left df"
    elif No_type == 4:
        type =  "Midd"
    elif No_type == 5:
        type = "Striker"

    return type

#-----------------------------------------FUNKCE--------------------------------------------------------------

def calculate_sector(call_No,site,position_in,The_field_size,The_field_start):
    # na kolik casti se hriste deli
    ratio = 3
    # hrsite je v hre posunuto od souradnic [0,0] ,proto tento posun musime odcist
    player_position = [ position_in[0] - The_field_start[0] , position_in[1] - The_field_start[1] + The_field_size[1] ]
    feild_size =[ The_field_size[0] , The_field_size[1]]
    sector_size = [ int(The_field_size[0] / ratio) ,int (The_field_size[1] / ratio)]

    # vysledny format priklad: 12
    data = [0,0]
    data[0] = player_position[0]//sector_size[0]  if site == "left" else 2 - player_position[0]//sector_size[0]
    data[1] = player_position[1]//sector_size[1]  if site == "left" else 2 - player_position[1]//sector_size[1]

    # error controla
    for loop in range (0,2):
        if data[loop] < 0:
            data[loop] = str(0)
        elif data[loop] > ratio:
            data[loop] = str(ratio + 1)
        else:
            # + 1 ,zacina indexem 1 ne 0 jako pole
            data[loop] = str(data[loop]+1)

    new_field_size = [int(The_field_size[0] / ratio), int(The_field_size[1] / ratio)]
    new_position_in =[int( position_in[0] + player_position[0]//sector_size[0] * sector_size[0]), \
                       int(position_in[1] -((2- player_position[1]//sector_size[1]) * sector_size[1]))]
    new_field_start =[int(The_field_start[0] + player_position[0]//sector_size[0] * sector_size[0]), \
                      int( The_field_start[1] -((2- player_position[1]//sector_size[1]) * sector_size[1]))]

    # mezni podminka pro rekurzi
    if call_No == 0:
        sector = data[0] + data[1]
    else:
        sector = data[0] + data[1] + "." + calculate_sector(call_No - 1,site,position_in,new_field_size,new_field_start)
    return sector


def center_button_name(original_name):
    spaces_string = ""
    frame_lenght = 14
    original_name_lenght = len(original_name)
    shift = int( (frame_lenght - original_name_lenght ) / 2)

    if shift > 0 and len(original_name) > 3 :
        for loop in range (0,shift-1):
            spaces_string = spaces_string + " "

    corrected_name =  spaces_string  +   original_name

    return corrected_name


# vypocet vzdalenosti
def pythagoras_distance (location_1,location_2):
    ingamer_adjescent =  abs (location_1[0]  -  location_2[0])
    ingamer_opposite =  abs (location_1[1] -  location_2[1])
    ingamer_hypotensue = sqrt(ingamer_adjescent **2 + ingamer_opposite **2)
    return ingamer_hypotensue


# funkce vypocte zda souradnice oznaceni mysi jsou v oznacene plose-kruhu
def is_clikced_on_circle(x_limits,y_limits,position_clicked):                                     # zkontroluj opakovani kodu v metodach pro tlacitka
    test = False
    if x_limits[0] <  position_clicked[0] and x_limits[1] > position_clicked[0]:
        if  y_limits[0] <  position_clicked[1] and y_limits[1] > position_clicked[1]:
            test = True
    return test


# zona hriste pro trening hrace napr brankare ,utocnika
# EXTRA
def draw_trening_field (game_window,game_field):
    field_corners = [0,0,0,0]

    # hriste
    field = pygame.draw.rect(game_window.surface, GREEN_FIELD, \
                                (game_field.field_bl_corner[0], game_field.field_bl_corner[1] - game_field.field_height, \
                                 game_field.field_width, game_field.field_height), 1)
    # 2x brany
    pygame.draw.rect(game_window.surface, white, \
                        (game_field.field_bl_corner[0] - game_field.goals_width, \
                         game_field.field_bl_corner[1] - game_field.field_height/2 - game_field.goals_height /2 , \
                         game_field.goals_width, game_field.goals_height), 1)

                                                                                                                                # 2x brany  ??? chybi brana?????
# vykresleni hriste
def draw_5aside_field (game_window,game_field,screen_ID):
    field_corners = [0,0,0,0]

    # hriste
    field = pygame.draw.rect(game_window.surface, GREEN_FIELD, \
                                (game_field.field_bl_corner[0], game_field.field_bl_corner[1] - game_field.field_height, \
                                 game_field.field_width, game_field.field_height), 2)
    # 2x brany
    pygame.draw.rect(game_window.surface, BLUE, \
                        (game_field.field_bl_corner[0] - game_field.goals_width,\
                         game_field.field_bl_corner[1] - game_field.field_height/2 - game_field.goals_height/2, \
                         game_field.goals_width,game_field.goals_height), 1)

    pygame.draw.rect(game_window.surface, RED, \
                        (game_field.field_bl_corner[0] + game_field.field_width, \
                         game_field.field_bl_corner[1] - game_field.field_height/2 - game_field.goals_height/2, \
                         game_field.goals_width,game_field.goals_height), 1)


    if screen_ID == Screens.ingame.value:
        # pulici cara hriste
        pygame.draw.lines(game_window.surface, GREY_LINES, True, \
                            ((game_field.field_bl_corner[0] + game_field.field_width/2 ,field.top), \
                             (game_field.field_bl_corner[0] + game_field.field_width/2,field.bottom)), 1)

        # 2x stred hriste
        pygame.draw.circle(game_window.surface, GREY_LINES, \
                            (int(game_field.field_bl_corner[0] + game_field.field_width/2), \
                            int(field.top + game_field.field_height/2)), 6, 1)
        pygame.draw.circle(game_window.surface, GREY_LINES, \
                            (int(game_field.field_bl_corner[0] + game_field.field_width/2), \
                            int(field.top + game_field.field_height/2)), 50, 1)


def draw_field_sectors(game_window,game_field):
    # sektory hriste - orintace hracu v poli
    pygame.draw.rect(game_window.surface, DARK_BLUE, \
                        (game_field.field_bl_corner[0] + game_field.field_width/3, \
                         game_field.field_bl_corner[1] - game_field.field_height + 5, \
                         game_field.field_width /3  ,game_field.field_height - 10), 1)

    pygame.draw.rect(game_window.surface, DARK_BLUE, \
                        (game_field.field_bl_corner[0] + 5, \
                         game_field.field_bl_corner[1] - game_field.field_height * 2/3, \
                         game_field.field_width -10 ,game_field.field_height/3),  1)


def draw_field_subsectors(The_game_window,game_field):
    field_top = game_field.field_bl_corner[1] - game_field.field_height
    field_right = game_field.field_bl_corner[0] + game_field.field_width
    field_bottom = game_field.field_bl_corner[1]
    field_left = game_field.field_bl_corner[0]
    sub_width = game_field.field_width / 9
    sub_height = game_field.field_height / 9

    #cross stred hriste
    pygame.draw.lines(The_game_window.surface,  GREY, True,  \
                        ((game_field.field_bl_corner[0] + game_field.field_width/2, \
                         game_field.field_bl_corner[1] - game_field.field_height/2 + 10 ), \
                         (game_field.field_bl_corner[0] + game_field.field_width/2, game_field.field_bl_corner[1] - game_field.field_height/2 - 10)), 1)

    pygame.draw.lines(The_game_window.surface,  GREY, True, \
                        ((game_field.field_bl_corner[0] + game_field.field_width/2 + 10, \
                         game_field.field_bl_corner[1] - game_field.field_height/2) , \
                         (game_field.field_bl_corner[0] + game_field.field_width/2 - 10, game_field.field_bl_corner[1] - game_field.field_height/2)), 1)

    shift_x = 0
    for column_loop in range (0,8):
        shift_y = 0                                                                                                                                    #???uzito
        for row_loop in range (0,8):
                if row_loop !=2 and row_loop !=5 and column_loop !=2 and column_loop !=5 :
                    # subsektory hriste - orintace hracu v poli
                    pygame.draw.circle(The_game_window.surface, GREY_LINES, \
                                        (int(field_left + sub_width + row_loop * sub_width), \
                                         int(field_bottom - sub_height - column_loop * sub_height) ) ,1, 1)
                shift_x = shift_x + 1

def draw_trening_mini_filed(The_game_window):
    field_tl_corner = [0,0] # tl = top left corner
    field_tl_corner[0] = 20 + The_game_window.game_menu_x_end + 8*The_game_window.mngmt_column_width
    field_tl_corner[1] = The_game_window.heading_shift + 20*  The_game_window.menu_line_spacing
    minifield_width = 2*The_game_window.mngmt_column_width
    minifield_height = 12*  The_game_window.menu_line_spacing

    pygame.draw.rect(The_game_window.surface, GREEN_FIELD, \
                                    (field_tl_corner[0], \
                                    field_tl_corner[1], \
                                     minifield_width, minifield_height), 1)

    pygame.draw.rect(The_game_window.surface, WHITE, \
                                    (field_tl_corner[0] + 1/3*minifield_width , \
                                    field_tl_corner[1] + minifield_height -2  , \
                                    minifield_width/3, 5), 1)

    pygame.draw.circle(The_game_window.surface, GREY_LINES, \
                    (int(field_tl_corner[0] + minifield_width/2), \
                    int(field_tl_corner[1]+ minifield_height/2)), 2, 1)
    pygame.draw.circle(The_game_window.surface, GREY_LINES, \
                    (int(field_tl_corner[0] + minifield_width/2), \
                    int(field_tl_corner[1]+ minifield_height/2)), 15, 1)



def calculate_trening_area(sectors,The_field):  #vstup sektory hriste
    sectors_letters = sectors[0]
    sectors_numbers = sectors[1]

    vertical_max    = The_field.field_bl_corner [1]
    vertical_min    = The_field.field_bl_corner [1] - The_field.field_height
    horizontal_min  = The_field.field_bl_corner [0]
    horizontal_max  = The_field.field_bl_corner [0] + The_field.field_width

    '''
     9x sektoru
            1                   2               3
       _____________________________________________________
      |                                                     |
A     |                                                     |
      |b                                                    |
      |r                                                    |
B     |a                                                    |
      |n                                                    |
      |a                                                    |
C     |                                                     |
      |_(vmax)______________________________________________|

      kombinace:
      a b ab abc bc c   vs   1 2 12 123 23 3
      => 36 kombinaci
    '''
    check = 0
    min_y = vertical_min
    max_y = vertical_min #+ The_field.field_height/3
    for letters_loop in range (0,2):
        if sectors_letters[letters_loop] == True:
            max_y = max_y + The_field.field_height/3
            check = 1
        else:
            if check == 0:
                min_y = min_y + The_field.field_height/3
                max_y = max_y + The_field.field_height/3

    check = 0
    min_x = horizontal_min
    max_x = horizontal_min #+ The_field.field_width/3
    for numberes_loop in range (0,2):
        if sectors_numbers[numberes_loop] == True:
            max_x = max_x + The_field.field_width/3
            check = 1
        else:
            if check == 0:
                min_x = min_x + The_field.field_width/3
                max_x = max_x + The_field.field_width/3

    return [int(min_x),int( max_x),int( min_y), int(max_y)]


def draw_green_tick(position,The_game_window):
    x_point = position[0]
    y_point = position[1]
    side = The_game_window.menu_line_spacing

    pygame.draw.lines(The_game_window.surface, GREEN, True, \
                                    ((x_point + side/2, y_point), \
                                     (x_point + side,y_point - side)), 4)

    pygame.draw.lines(The_game_window.surface, GREEN, True, \
                                    ((int(x_point + side/3 ), int(y_point - side/3)), \
                                     (x_point + side/2, y_point)), 4)

if False:
    test1 = calculate_sector(1,"left",[30, 200],[1216, 503],[15, 568])
    test1 = calculate_sector(1,"left",[16, 200],[1216, 503],[15, 568])
    test1 = calculate_sector(1,"right",[45, 200],[1216, 503],[15, 568])
    test1 = calculate_sector(1,"right",[25, 200],[1216, 503],[15, 568])

if False:
    print("-----------------------------------")
    print( calculate_sector(1,"left",[  29   ,  15  ],[90, 30],[0, 30]) )
    print("[29,15],[90, 30],[0,30]")
    print("-----------------------------------")
    print( calculate_sector(1,"left",[  31   ,  15  ],[90, 30],[0, 30]) )
    print("[31,15],[90, 30],[0,30]")
    print("-----------------------------------")
    print( calculate_sector(1,"left",[ 75,25  ],[90, 30],[0, 30]) )
    print("[75,25],[90, 30],[0,30]")
    print("-----------------------------------")
    print(" ")
    print("  ---------------------------------- ")
    print(" I           I           I          I   10")
    print(" I        .  I       .   I          I   20")
    print(" I           I           I     .    I   30  ")
    print("  ---------------------------------- ")
    print("             30          60         90 ")
    print("       [0]      [1]        [2]        ")


    #test1 = calculate_sector(1,"left",[  10   ,  20  ],[90, 30],[0, 30])
    #test1 = calculate_sector(1,"right",[  60  ,  20],[90, 30],[0, 30])
    #test1 = calculate_sector(1,"right",[  20   ,  20  ],[90, 30],[0, 30])
