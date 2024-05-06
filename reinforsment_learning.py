import tensorflow as tf
import numpy as np

from  tensorflow.keras import Sequential
from  tensorflow.keras.layers import Dense
from  tensorflow.keras.models import load_model
from  tensorflow.keras.optimizers import Adam
from gym import Env
from gym.spaces import Discrete, Box

from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

import time

import neural_network
from neural_network import *

import copy
import pygame

import support_functions
from support_functions import *

import screens
from screens import *

pygame.init()
from pygame.locals import *

##  ------DQN -----
##  soucet rewards za akci kterou provedeme

GREY = (192,192,192)
MENU_FONT = pygame.font.SysFont("Arial", 18)
MENU_FONT_HEADING = pygame.font.SysFont("Arial", 30)

def f_print_RE_trening_header(The_game_window, coach):

    all_headers_text_raw =  raw_RE_trening_header( The_game_window.language)

    text_data_rendered_header = MENU_FONT_HEADING.render(all_headers_text_raw[0] , 1, GREY)
    text_data_rendered_steps = MENU_FONT.render( all_headers_text_raw[1]  + str(coach.trening_repetition_sequence) + ' / '+ str(coach.trening_repetition_total) , 1, GREY)
    text_data_rendered_runs = MENU_FONT.render( all_headers_text_raw[2]   + str(coach.RE_trening_sesion_runs), 1, GREY)

    The_game_window.surface.blit(text_data_rendered_header,( The_game_window.mngmt_column_width, int(1.2* The_game_window.menu_line_spacing)))
    The_game_window.surface.blit(text_data_rendered_steps,(The_game_window.game_menu_x_end +   The_game_window.mngmt_column_width,  The_game_window.menu_line_spacing))
    The_game_window.surface.blit(text_data_rendered_runs,(The_game_window.game_menu_x_end +   The_game_window.mngmt_column_width,  2 *  The_game_window.menu_line_spacing))

def f_print_RE_trening_stop_button(The_game_window, button_size, button_color, training_progress_text):
    #button
    rectangle_details = [0  ,The_game_window.window_height - button_size[1] , button_size[0],button_size[1] ]
    button_background = pygame.draw.rect(The_game_window.surface, button_color, rectangle_details, 0, 5)

    The_game_window.surface.fill(button_color,( 0  ,The_game_window.window_height - button_size[1] , button_size[0],button_size[1]))
    The_game_window.surface.blit(MENU_FONT.render(training_progress_text, 1, BLACK),(   5,  The_game_window.window_height - button_size[1] ))


def raw_RE_trening_header(language):
    text = 3 * ["null"]
    if language == "CZ":
        text[0] = 'Progres :'
        text[1] = 'Pocet treningu: '
        text[2] = 'kroku v treningu:  '
    else:
        text[0] = 'Progres :'
        text[1] = 'Pocet treningu: '
        text[2] = 'kroku v treningu:  '
    return  text





# tisk detailu hrace pri hre  MUSI BYT COPY Z CREENS PROCC NEJEDE ZJISTI
def f_print_player_details_RE(The_game_window,The_field,player,list_of_ingamers):
    shift_vertikal = 0
    shift_horisontal = 300                                                                                              #nejak lip definovat  hodnotu
    list_of_tags = ["angle: ","ball angle: ","ball distance(cntr-cntr)","velocity: ","site,team: ","sumskils: ","name: "]
    list_of_data =[str(round(player.path_target)), \
                   str(round(player.calculate_angle_to_other_object(list_of_ingamers[0].rect.center))), \
                   str(round(pythagoras_distance (player.rect.center,list_of_ingamers[0].rect.center))), \
                   str(player.velocity), \
                   player.field_site +" , "+ player.team , \
                   str(player.skills_level), \
                   player.name ]

    for data_index in range (0,len(list_of_data)):
        data = MENU_FONT.render(  list_of_tags[data_index] + list_of_data[data_index]   , 1, GREY)
        The_game_window.surface.blit(data,(The_field.field_bl_corner [0] +200+ shift_horisontal, \
                                            The_game_window.game_menu_y_end  + shift_vertikal ))
        shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing

    list_of_tags2 = ["position: ",  "ID: ","sector: ","posplr: " ,"posball: " ,"feidx :","feidy :"]
    list_of_data2 =[player_type_text(int(player.player_type)) , \
                   player.ID, \
                   str(calculate_sector(1,player.field_site,player.rect.center,[ The_field.field_width,The_field.field_height], The_field.field_bl_corner)), \
                   str(player.rect.center), \
                   str(list_of_ingamers[0].rect.center), \
                    str(The_field.field_bl_corner[0]), \
                     str(The_field.field_bl_corner[1])]
    #print(str(calculate_sector(player.position,[ The_field.field_width,The_field.field_height])))
    #print(The_field.field_width,The_field.field_height)
    shift_vertikal = 0
    for data_index in range (0,len(list_of_data2)):
        data = MENU_FONT.render(  list_of_tags2[data_index] + list_of_data2[data_index]   , 1, GREY)
        The_game_window.surface.blit(data,(The_field.field_bl_corner [0] + 3*shift_horisontal  , \
                                            The_game_window.game_menu_y_end  + shift_vertikal ))
        shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing



# tisk nastaveni/hodnot balonu (uzito pro kontrolu metod )                                                                        # pouzita pri testovani asi nebude v hre uzita
def f_print_ball_details(The_game_window,The_field,ball,list_of_ingamers):
    shift_vertikal = 0
    list_of_tags = ["angle: ","owner: ","velocty: ","site: ", 'speed']
    list_of_data =[str(round(ball.path_target)), \
                   'aa', \
                   str(ball.velocity), \
                   str(ball.field_site), \
                   str(ball.speed) ]


    for data_index in range (0,len(list_of_data)):
        data = MENU_FONT.render(  list_of_tags[data_index] + list_of_data[data_index]   , 1, GREY)
        The_game_window.surface.blit(data,(The_field.field_bl_corner [0], The_field.field_bl_corner[1] + The_game_window.menu_line_spacing + shift_vertikal ))
        shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing


def f_print_refff_details(The_game_window,The_field,reff):
    shift_vertikal = 50
    list_of_tags = ['scoree:']
    list_of_data =[str(reff.score)]


    for data_index in range (0,len(list_of_data)):
        data = MENU_FONT.render(  list_of_tags[data_index] + list_of_data[data_index]   , 1, GREY)
        The_game_window.surface.blit(data,(The_field.field_bl_corner [0] + 100, The_field.field_bl_corner[1] + The_game_window.menu_line_spacing + shift_vertikal ))
        shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing






#---------------------  DQN KERAS AGENTS, Gym environment  ----

class TrainingEnvironment (Env):

    def __init__(self ):
        self.action_space = Discrete(5)
        #self.observation_space = Box(low = np.array([-0.1 ,-0.1,-0.1,1,-1,5,6,7,8,9,1,1,11]),high= np.array([0.36,0.36,  5 ,5, 2,5,6,7,8,9,1,1,11]))
        self.observation_space = 'null'
        self.state = np.array([0,0,0,0,0])
        #self.state = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.episode_ended = False
        self.The_field = None
        self.list_of_ingamers=None
        self.trained_player=None
        self.do_render = False
        self.button_size = [100,26]
        self.button_color = RED
        self.training_progress_text ='   STOP  '


    def load_data (self, list_of_ingamers, trained_player, trainedplayer_ingamers_index, The_field,The_game_window,The_reff, render):

        if trained_player.isREtrainingRawData == True :
            self.observation_space = Box(low = np.array([0,0.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]), \
                                         high= np.array([1,0.5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]))
        else:
            self.observation_space = Box(low = np.array([-0.1 ,-0.1,-0.1,1,-1, 0,0,0,0,0,0,0,0 ]), \
                                         high= np.array([0.36 ,0.36,  5 ,5, 2, 1,1,1,1,1,1,1,1 ]))

        self.The_field = The_field
        self.list_of_ingamers= list_of_ingamers
        self.trained_player= trained_player
        self.The_game_window= The_game_window
        self.The_reff = The_reff
        self.do_render = render
        self.state = np.array( trained_player.get_NN_data(The_field,list_of_ingamers))
        self.trainedplayer_ingamers_index = trainedplayer_ingamers_index

    def Xstep(self,action):
        info = {}
        return self.state, 2, False, info

    # action number from 0 to 4
    def step(self,action):
        reward = 0
        ball_index = 0
        done = False
        list_of_ingamers = self.list_of_ingamers
        trained_player = self.trained_player
        the_ball = self.list_of_ingamers[ball_index]
        The_field = self.The_field
        original_score = copy.deepcopy(self.The_reff.score[0])
        turn_angle = 22
        state_previouse = copy.deepcopy(self.state)
        '''
        # oprava pro uhly kdyz presahnou 360   /    0
        if action == 0:
            trained_player.turn_player_path_by_angle(turn_angle)
        elif action == 1:
            trained_player.turn_player_path_by_angle(-1 * turn_angle)
        elif action == 2:
            trained_player.move(The_field,list_of_ingamers)
        elif action == 3 and list_of_ingamers[ball_index].owner == trained_player:
            list_of_ingamers[ball_index].speed = 200   #testovaci kop
        else:
            pass
        '''

        # oprava pro uhly kdyz presahnou 360   /    0
        if action == 0:
            if (trained_player.path_target + turn_angle) >= 360:                                    #  opakovany kod jak u class hrace
                uhel = (trained_player.path_target + turn_angle) - 360
            else:
                 uhel =   (trained_player.path_target + turn_angle)
            trained_player.set_path_target(uhel)
        elif action == 1:
            if (trained_player.path_target - turn_angle) <= 0:
                uhel = (trained_player.path_target - turn_angle) + 359
            else:
                uhel = (trained_player.path_target - turn_angle)
            trained_player.set_path_target(uhel)
        elif action == 2:
            trained_player.move(The_field,list_of_ingamers)
        elif action == 3 and list_of_ingamers[ball_index].owner == trained_player:
            list_of_ingamers[ball_index].speed = 200   #testovaci kop
        else:
            pass




        #-aktualizace stavu
        self.state = np.array( trained_player.get_NN_data(self.The_field,self.list_of_ingamers))
        #print("self.state" ,   self.state )
        ##-- Vyhodnoceni
        #-neni brankar
        #if self.state[3] != PlayerType.GK.value:

        # raw data : player_angle,player_type pak vsechny ingamers xz pozice    summa 24 vstupu do NN------------------------------------------------------------------------
        if trained_player.isREtrainingRawData == True:
            #indexy, player + 1 je position y
            shift_in_skils = 2
            player_angle = 0
            player_type = 1
            trained_player_pos_x = self.trainedplayer_ingamers_index * 2 + shift_in_skils
            index_ball_pos_x = 2
            index_pl_1_pos_x = 4
            index_pl_2_pos_x = 6
            index_pl_3_pos_x = 8
            index_pl_4_pos_x = 10
            index_pl_5_pos_x = 12
            index_pl_6_pos_x = 14
            index_pl_7_pos_x = 16
            index_pl_8_pos_x = 18
            index_pl_9_pos_x = 20
            index_pl_10_pos_x = 22

            if trained_player.skills_set[player_type] == True   and  trained_player.skills_set[trained_player_pos_x] ==True:
                # je na svem dle playertype
                if self.state[player_type] == PlayerType.leftdefender.value  or self.state[player_type] == PlayerType.rightdefender.value:
                    if self.state[trained_player_pos_x] < 0.4:
                        reward = 3
                if self.state[player_type] == PlayerType.middfielder.value :
                    if self.state[trained_player_pos_x] > 0.3  and  self.state[trained_player_pos_x] < 0.8:
                        reward = 3
                if self.state[player_type] == PlayerType.striker.value :
                    if self.state[trained_player_pos_x] > 0.6 :
                        reward = 3
                if self.state[player_type] == PlayerType.GK.value :
                    #odejde od brany
                    # +1 je y posice desetina cisla jsou kde na hristi se nachazi  0.5 je pul hriste od sve brany
                    if self.state[trained_player_pos_x] > 0.2 or abs( self.state[trained_player_pos_x + 1] - 0.5 > 0.3 ):
                        reward = -5
                    else:
                        reward = 5

            if trained_player.skills_set[index_ball_pos_x] == True   and  trained_player.skills_set[trained_player_pos_x + shift_in_skils] ==True:
                distance_prev_plrtoball = abs( state_previouse[index_ball_pos_x] - state_previouse[trained_player_pos_x + shift_in_skils] )
                distance_now_plrtoball  = abs( self.state[index_ball_pos_x ] - self.state[trained_player_pos_x + shift_in_skils] )

                #distance k mici
                if (distance_now_plrtoball < distance_prev_plrtoball ):
                    reward = reward + 2


            if trained_player.skills_set[index_ball_pos_x] == True:
                distance_prev_balltogoal = state_previouse[index_ball_pos_x]
                distance_now_balltogoal =  self.state[index_ball_pos_x]

                # mic je cim dal vic od sve brany
                if (distance_now_balltogoal > distance_prev_balltogoal ):
                    reward = reward + 5

                # mic je na druhe strane hriste
                if (distance_now_balltogoal > 0.5 ):
                    reward = reward + 7



            isGoal = self.The_reff.goal_check(The_field ,the_ball  )
            if (isGoal == True   ):
                if self.state[index_ball_pos_x] < 0.5: # hodnoty normalizovany znamena ze mic je na sve pulce =>dostali gol
                    reward = -20
                else:
                    reward = 20
                done = True

        # NOT raw data---------------------------------------------------------------------------------------------------------------------------------------------------------------
        if trained_player.isREtrainingRawData == False:

            player_angle = 0
            player_type = 1
            player_sector = 2
            distance_playerball = 3
            angle_slosestteamplayer = 4
            distc_slosestteamplayer = 5
            angle_closestoposplayer = 6
            distc_closestoposplayer = 7
            is_player_closest_ball = 8
            to_ball_angle = 9

            distance_prev_plrtoball = state_previouse[distance_playerball]
            distance_now_plrtoball  =  self.state[distance_playerball ]

            # je na svem dle playertype
            if self.state[player_type] == PlayerType.leftdefender.value  or self.state[player_type] == PlayerType.rightdefender.value:
                if self.state[player_sector] < 0.1323:
                    reward = 3
            if self.state[player_type] == PlayerType.middfielder.value :
                if self.state[player_sector] > 0.1313  and  self.state[player_sector] < 0.2313:
                    reward = 3
            if self.state[player_type] == PlayerType.striker.value :
                if self.state[player_sector] > 0.2323 :
                    reward = 3
            if self.state[player_type] == PlayerType.GK.value :
                #odejde od brany,sectror vysvetlen viz funkce 'calculate_sector'
                if round(self.state[player_sector] ,3) != 0.121  :
                    reward = -5
                else:
                    reward = 5

            #distance k mici   , gk chce aby mic se vzdaloval
            if (distance_now_plrtoball < distance_prev_plrtoball ) and self.state[player_type] != PlayerType.GK.value :
                reward = reward + 2

            #distance k mici   , gk chce aby mic se vzdaloval
            if (distance_now_plrtoball > distance_prev_plrtoball ) and self.state[player_type] == PlayerType.GK.value :
                reward = reward + 2

            #uhel k mici
            if self.state[to_ball_angle] > 90    and  self.state[to_ball_angle]   <  270 :

                #+++dode;ej mic porad pred nim
                reward = reward + 2
            else:
                reward = reward - 3

            buffer_ball = copy.deepcopy( self.list_of_ingamers[0].rect.center[0])
            isGoal = self.The_reff.goal_check(The_field ,the_ball  )

            if (isGoal == True   ):
                print (' .goal_top')

                if buffer_ball <  self.The_field.field_bl_corner[0] + 20 :
                    reward = -20
                    print (' .goal_top  -200')
                else:
                    reward = 20
                    print (' .goal_top200')

                #time.sleep(.01)
                done = True


        info = {}

        if self.do_render == True:
            self.render()
            #time.sleep(.01)

        return self.state, reward, done, info

    def render(self):
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                self.The_game_window.resize_window([1280,720],The_field)

            if event.type == QUIT:
                #self.The_reff.pause_game()#The_game_window,The_field)
                self.The_reff.set_game_status_to_self("none")
                self.The_reff.set_game_status_to_players()
                sys.exit()

            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN :
                position_clicked = pygame.mouse.get_pos()
                print ('position_clicked' , position_clicked    )
                print ('position_clicked' , position_clicked    )
                if position_clicked[0] <    self.button_size[0] and position_clicked[1] >   self.The_game_window.window_height - self.button_size[1] :
                    self.The_reff.coach_team_A.exit_RE_trening  = True
                    self.button_color = GREEN
                    self.training_progress_text = 'packiging... '

                pass#self.episode_ended = True
        #-print(  "-------------------------------------render  ")

        self.The_game_window.surface.fill(BLACK)

        self.list_of_ingamers[0].moving(self.The_field,self.The_reff)                                             # zastavi se pri paused game????
        draw_5aside_field (self.The_game_window,self.The_field,44)  # ENUM trainingautomated = 44
        draw_field_sectors(self.The_game_window,self.The_field)

        self.The_game_window.draw_all_ingamers(self.list_of_ingamers)

        f_print_player_details_RE(self.The_game_window,self.The_field,self.trained_player,self.list_of_ingamers)
        f_print_ball_details(self.The_game_window, self.The_field, self.list_of_ingamers[0], self.list_of_ingamers)
        f_print_refff_details(self.The_game_window, self.The_field,self.The_reff)

        f_print_RE_trening_header(self.The_game_window, self.The_reff.coach_team_A)
        f_print_RE_trening_stop_button(self.The_game_window, self.button_size, self.button_color, self.training_progress_text)

        pygame.display.flip()

    def reset(self):                                                                           #jak gol reff resetovat hru movehrace pro novy game

        coach =  self.The_reff.coach_team_A
        if self.trained_player.player_type == PlayerType.GK.value :
            coach.move_players_for_new_training_run_GK (self.The_field,self.The_reff.list_of_ingamers,'team')
        else:
            coach.move_players_for_new_training_run (self.The_field,self.The_reff.list_of_ingamers)
        #coach.move_players_for_new_training_run (self.The_field,self.The_reff.list_of_ingamers)
        self.state = np.array( self.trained_player.get_NN_data(self.The_field,self.list_of_ingamers))

        return  self.state

def build_agent_keras (model, actions, trening_runs):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit = trening_runs, window_length = 1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy,  \
                    nb_actions=actions, nb_steps_warmup=10, target_model_update=1e-2,batch_size=1)
    return dqn


def run_RE_trening(model, actions, env,player_ID,trening_runs):
    print("2---model.summary -", model.summary())
    print("train_modelRE1" )
    dqnAgent_created = build_agent_keras (model, actions, trening_runs)
    dqnAgent_created.compile(Adam(learning_rate=1e-3) , metrics=['mae'])
    dqnAgent_created.fit(env, nb_steps=trening_runs, visualize=False, verbose=1 )
    path = get_path_home_folder()
    print("2---model.summary -", model.summary())
    print("train_modelRE2" )
    model.save(path +  str(player_ID)  + ".h5")

    #print('uulozen model ', player_ID)




#---------------------  DQN TF AGENTS  ----
def build_TF_DQNagent():
    q_net = q_network.QNetwork(
      train_env.observation_spec(),
      train_env.action_spec(),
      fc_layer_params=(100,))

    agent = dqn_agent.DqnAgent(
      train_env.time_step_spec(),
      train_env.action_spec(),
      q_network=q_net,
      optimizer=optimizer,
      td_errors_loss_fn=common.element_wise_squared_loss,
      train_step_counter=tf.Variable(0))

    agent.initialize()

    return agent

'''

def run_RE_trening_tf():
    q_net = q_network.QNetwork(train_env.observation_spec(), train_env.action_spec(), fc_layer_params=(100,))
    agent = dqn_agent.DqnAgent(train_env.time_step_spec(),train_env.action_spec(),q_network=q_net, \
                               optimizer=optimizer,td_errors_loss_fn=common.element_wise_squared_loss, \
                                train_step_counter=tf.Variable(0))


    return agent



def save_trainingXx():
    file_name_testing = 'training.txt'
    xx =[  [[8,1,8,5,4,5,6,7,8,9,1,1,11]],[[0,1,2,5,4,5,6,7,8,9,1,1,11]]  ]
    x = [1,0]
    with open(file_name_testing, 'w') as f:
        for write_loop in range (0,len(xx)):
            for write_inner_loop in range (0,13):
                f.write( str(xx[write_loop][0][write_inner_loop]))
                if write_inner_loop != 12:
                    f.write( ",")
            f.write( '\n')

'''




'''
#---------jede
dat = load_data("training.txt")
daat = load_datalabels("traininglabels.txt")
model = create_model_tf2(13)
print(dat)
print(daat)
#x =[   [ [[0,1,2,7,4,5,7,7,8,9,1,1,11]],[[0,1,2,5,4,5,6,7,8,9,1,1,11]]  ]]

model.fit([dat], daat)
'''
#---------------------  nasledujici funkce jsou pouze pro testy a kontrolu keras modelu  ----





'''
JEEEEDEEEEEE

def testmodel(new_shape):
    model = tf.keras.Sequential([
        #tf.keras.layers.Flatten(input_shape=(1,13)),
        #tf.keras.layers.Input(shape=(13, )),
        tf.keras.layers.Flatten(input_shape=(1,13)),
        tf.keras.layers.Dense(5,activation="relu"),
        tf.keras.layers.Dense(5,activation="softmax")
        ])

    model.compile(optimizer="adam",loss='sparse_categorical_crossentropy',metrics=["accuracy"])

    return model





xxx=  [[   [[0,1,2,5,4,5,6,7,8,9,1,1,11]],[[0,1,2,5,4,5,6,7,8,9,1,1,11]]  ]]
print(  "shap-", np.shape(xxx))
xmodel = testmodel(13)
print(  "2---model.summary -", xmodel.summary())
xmodel.fit( xxx   ,    [[1,0]] )
print(" predikt "  , xmodel.predict(    [[[[0,1,2,5,4,5,6,7,8,9,1,1,11]]]]     ))

The_RE_env =TrainingEnvironment()
print(  "2---observation_space -")

ymodel = testmodel(13)
print(  "2---model.summary -", ymodel.summary())

dqnAgent_created = build_agent_keras (ymodel, 5)
dqnAgent_created.compile(Adam(learning_rate=1e-3) , metrics=['mae'])
dqnAgent_created.fit(The_RE_env, nb_steps=10, visualize=False, verbose=1 )

'''
