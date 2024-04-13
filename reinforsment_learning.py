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

def f_print_RE_trening_repetition_sequence(The_game_window, trening_repetition_sequence):
    text_progress =  f_RE_trening_repetition_sequence()
    The_game_window.surface.blit(text_progress,(The_game_window.game_menu_x_end + 90 + 10 *trening_repetition_sequence, 2 * The_game_window.menu_line_spacing))
    The_game_window.surface.blit(MENU_FONT.render('I', 1, GREY),(The_game_window.game_menu_x_end + 90 + 0 *trening_repetition_sequence, 2 * The_game_window.menu_line_spacing))   #start point
    text_labels = f_RE_trening_repetition_sequence_percentage(The_game_window.language)
    The_game_window.surface.blit(text_labels,(The_game_window.game_menu_x_end ,  The_game_window.menu_line_spacing))
    The_game_window.surface.blit(MENU_FONT.render('I', 1, GREY),(The_game_window.game_menu_x_end + 180 + 0 *trening_repetition_sequence, 2 * The_game_window.menu_line_spacing))   #end point

def f_RE_trening_repetition_sequence():
    text = "null"
    text = MENU_FONT.render(' >', 1, GREY)
    return  text

def f_RE_trening_repetition_sequence_percentage(language):
    text = "null"
    if language == "CZ":
        text = MENU_FONT.render('trenovano 0% > > > 100%    OBRAZOVKA UZAMKNUTA', 1, GREY)
    else:
        text = MENU_FONT.render(' traned   0% > > > 100%    SCREEN LOCKED', 1, GREY)
    return  text





# tisk detailu hrace pri hre  MUSI BYT COPY Z CREENS PROCC NEJEDE ZJISTI
def f_print_player_details(The_game_window,The_field,player,list_of_ingamers):
    shift_vertikal = 0
    shift_horisontal = 300                                                                                              #nejak lip definovat  hodnotu
    list_of_tags = ["angle: ","ball angle: ","ball distance(cntr-cntr)","velocity: ","site,team: ","sumskils: ","name: "]
    list_of_data =[str(round(player.path_target)), \
                   str(round(player.calculate_angle_to_other_object(list_of_ingamers[1].rect.center))), \
                   str(round(pythagoras_distance (player.rect.center,list_of_ingamers[1].rect.center))), \
                   str(player.velocity), \
                   player.field_site +" , "+ player.team , \
                   str(player.skills_level), \
                   player.name ]

    for data_index in range (0,len(list_of_data)):
        data = MENU_FONT.render(  list_of_tags[data_index] + list_of_data[data_index]   , 1, GREY)
        The_game_window.surface.blit(data,(The_field.field_bl_corner [0] +200+ shift_horisontal, \
                                            The_game_window.game_menu_y_end  + shift_vertikal ))
        shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing

    list_of_tags2 = ["position: ",  "ID: ","sector: ","posix: " ,"posiy: " ,"feidx :","feidy :"]
    list_of_data2 =[player_type_text(int(player.player_type)) , \
                   player.ID, \
                   str(calculate_sector(1,player.field_site,player.rect.center,[ The_field.field_width,The_field.field_height], The_field.field_bl_corner)), \
                   str(player.rect.center[0]), \
                   str(player.rect.center[1]), \
                   str(The_field.field_width), \
                    str(The_field.field_height)]
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
        The_game_window.surface.blit(data,(The_field.field_bl_corner [0], The_field.field_bl_corner[1] + The_game_window.menu_line_spacing + shift_vertikal ))
        shift_vertikal = shift_vertikal + The_game_window.menu_line_spacing






#---------------------  DQN KERAS AGENTS, Gym environment  ----

class TrainingEnvironment (Env):

    def __init__(self ):
        self.action_space = Discrete(5)
        #self.observation_space = Box(low = np.array([-0.1 ,-0.1,-0.1,1,-1,5,6,7,8,9,1,1,11]),high= np.array([0.36,0.36,  5 ,5, 2,5,6,7,8,9,1,1,11]))
        #self.state = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.observation_space = Box(low = np.array([-0.1 ,-0.1,-0.1,1,-1]), \
                                      high= np.array([0.36,0.36,  5 ,5, 2]))
        self.state = np.array([0,0,0,0,0])
        self.episode_ended = False
        self.The_field = None
        self.list_of_ingamers=None
        self.trained_player=None
        self.do_render = False


    def load_data (self, list_of_ingamers, trained_player, The_field,The_game_window,The_reff, render):
        self.The_field = The_field
        self.list_of_ingamers= list_of_ingamers
        self.trained_player= trained_player
        self.The_game_window= The_game_window
        self.The_reff = The_reff
        self.do_render = render
        self.state = np.array( trained_player.get_NN_data(The_field,list_of_ingamers))

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
        distance_prev =   pythagoras_distance ((state_previouse[0],state_previouse[1]), (state_previouse[2],state_previouse[3]))
        distance_now =   pythagoras_distance ((self.state[0],self.state[1]), (self.state[2],self.state[3]))
        distance_prev_balltogoal =   The_field.field_bl_corner[0] - state_previouse[2]
        distance_now_balltogoal =  The_field.field_bl_corner[0] - self.state[2]


        if 1:

            #kope na branu soupere
            if list_of_ingamers[0].owner == trained_player and action == 3:
                reward = 4
                if  trained_player.path_target > 120 and  trained_player.path_target < 240:
                    reward = 6
                else:
                    reward = -2
                    #done = True

            if (distance_now < distance_prev ):
                reward = 2
            else:
                reward = -1

            if (distance_now_balltogoal > distance_prev_balltogoal ): # mic je cim dal vic od sve brany
                reward = 5


            isGoal = self.The_reff.goal_check(The_field ,the_ball  )
            if (isGoal == True   ):
                if original_score < self.The_reff.score[0]:
                    reward = 1000
                else:
                    reward = -1000

                done = True

            # mic daleko od brany a nehybese
            if self.trained_player.player_type == PlayerType.GK.value :
                #odejde od brany
                if trained_player.rect.center[0] >  The_field.field_bl_corner[0] + 100:
                    reward = -10
                else:
                    reward = 5

                if the_ball.speed == 0 and self.state[2] > The_field.field_bl_corner[0] +  self.The_field.field_width /8:

                    done = True

        info = {}

        if self.do_render == True:
            self.render()
            time.sleep(.01)

        return self.state, reward, done, info

    def render(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN :
                pass#self.episode_ended = True
        #-print(  "-------------------------------------render  ")
        self.The_game_window.surface.fill(BLACK)

        self.list_of_ingamers[0].moving(self.The_field,self.The_reff)                                             # zastavi se pri paused game????
        #f_print_RE_trening_inprogress(self.The_game_window)
        draw_5aside_field (self.The_game_window,self.The_field,44)  # ENUM trainingautomated = 44
        for no_of_ingamers in range (0,len(self.list_of_ingamers)):
            self.list_of_ingamers[no_of_ingamers].draw_ingamer(self.The_game_window)

        f_print_player_details(self.The_game_window,self.The_field,self.trained_player,self.list_of_ingamers)
        f_print_RE_trening_repetition_sequence(self.The_game_window, self.The_reff.coach_team_A.trening_repetition_sequence)
        f_print_ball_details(self.The_game_window, self.The_field, self.list_of_ingamers[0], self.list_of_ingamers)
        f_print_refff_details(self.The_game_window, self.The_field,self.The_reff)
        pygame.display.flip()

    def reset(self):                                                                           #jak gol reff resetovat hru movehrace pro novy game

        coach =  self.The_reff.coach_team_A
        if self.trained_player.player_type == PlayerType.GK.value :
            coach.move_players_for_new_training_run_GK (self.The_field,self.The_reff.list_of_ingamers,'noteam')
        else:
            coach.move_players_for_new_training_run (self.The_field,self.The_reff.list_of_ingamers)
        #coach.move_players_for_new_training_run (self.The_field,self.The_reff.list_of_ingamers)
        self.state = np.array( self.trained_player.get_NN_data(self.The_field,self.list_of_ingamers))
        return  self.state


def build_agent_keras (model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit = 500, window_length = 1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy,  \
                    nb_actions=actions, nb_steps_warmup=10, target_model_update=1e-2,batch_size=1)
    return dqn


def run_RE_trening(model, actions, env,player_ID,trening_runs):
    dqnAgent_created = build_agent_keras (model, actions)
    dqnAgent_created.compile(Adam(learning_rate=1e-3) , metrics=['mae'])
    dqnAgent_created.fit(env, nb_steps=trening_runs, visualize=False, verbose=1 )
    path = get_path_home_folder()
    model.save(path +  str(player_ID)  + ".h5")
    print('uulozen model ', player_ID)




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
