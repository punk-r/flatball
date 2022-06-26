import tensorflow as tf
import numpy as np

from  tensorflow.keras import Sequential
from  tensorflow.keras.layers import Dense
from  tensorflow.keras.models import load_model
from  tensorflow.keras.optimizers import Adam
from gym import Env
from gym.spaces import Discrete, Box


#-from tf_agents.networks import q_network
#-from tf_agents.agents.dqn import dqn_agent

from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

import time

import neural_network
from neural_network import *


import pygame

import support_functions
from support_functions import *

import screens
from screens import *




##  ------DQN -----
##  soucet rewards za akci kterou provedeme



#---------------------  DQN KERAS AGENTS, Gym environment  ----

class TrainingEnvironment (Env):

    def __init__(self ):
        self.action_space = Discrete(5)
        self.observation_space = Box(low = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12]), \
                                      high= np.array([360,10,10,10,10,10,10,10,10,10,10,10,10]))
        self.state = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.episode_ended = False
        self.The_field = None
        self.list_of_ingamers=None
        self.trained_player=None

    def load_data (self, list_of_ingamers, trained_player, The_field,The_game_window,The_reff):
        self.The_field = The_field
        self.list_of_ingamers= list_of_ingamers
        self.trained_player= trained_player
        self.The_game_window= The_game_window
        self.The_reff = The_reff



    # action number from 0 to 4
    def step(self,action):



        list_of_ingamers = self.list_of_ingamers
        trained_player = self.trained_player
        The_field = self.The_field


        # self._state = trained_player.get_NN_data(The_field,list_of_ingamers)
        turn_angle = 22
        uhel = 10

        distance_old =  round(pythagoras_distance (trained_player.rect.center, list_of_ingamers[0].rect.center) -   \
                                                    trained_player.radius - list_of_ingamers[0].radius)

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
        elif action == 3 and list_of_ingamers[0].owner == trained_player:
            list_of_ingamers[0].speed = 200   #testovaci kop
        else:
            pass

        distance_new =  round(pythagoras_distance (trained_player.rect.center, list_of_ingamers[0].rect.center) -   \
                                                    trained_player.radius - list_of_ingamers[0].radius)

        self.state[0] =  trained_player.path_target

        if distance_new < distance_old:
            reward = 1.0

            if list_of_ingamers[0].owner == trained_player:
                reward = 10.0

        else:
            reward = -1.0


        done = True
        info = {}

        self.render()

        return self.state, reward, done, info

    def render(self):
        time.sleep(.05)
        #-print(  "-------------------------------------render  ")
        self.The_game_window.surface.fill(BLACK)

        self.list_of_ingamers[0].moving(self.The_field,self.The_reff)                                             # zastavi se pri paused game????
        #f_print_RE_trening_inprogress(self.The_game_window)
        draw_5aside_field (self.The_game_window,self.The_field,44)  # ENUM trainingautomated = 44
        for no_of_ingamers in range (0,len(self.list_of_ingamers)):
            self.list_of_ingamers[no_of_ingamers].draw_ingamer(self.The_game_window)


        pygame.display.flip()

    def reset(self):
        self.state = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12])
        return  self.state

    def close(self):
        self.state = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12])
        return  self.state




def build_agent_keras (model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit = 500, window_length = 1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy,  \
                    nb_actions=actions, nb_steps_warmup=10, target_model_update=1e-2)

    print(  "4---run build_agent_keras  ")
    return dqn


def run_RE_trening(model, actions, env,player_ID):
    print(  "3---run run_RE_trening  ")
    dqnAgent_created = build_agent_keras (model, actions)
    dqnAgent_created.compile(Adam(learning_rate=1e-3) , metrics=['mae'])
    print(  "4.5---run compile finished  ")
    dqnAgent_created.fit(env, nb_steps=5000, visualize=False, verbose=1 )

    print(  "5--model_name  ",   player_ID  )
    save_model_weights(dqnAgent_created,player_ID)
    print(  "5---run dqn.fit finished  ")




#---------------------  DQN TF AGENTS  ----





def build_Agent():
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









#---------------------  nasledujici funkce jsou pouze pro testy a kontrolu keras modelu  ----


'''

print(  "1---run  LERNING STARTEDD ")
The_RE_env =TrainingEnvironment()

#The_RE_env.load_data (The_reff.list_of_ingamers, The_reff.list_of_ingamers[ingamers_loop], The_field)
model = create_model_tf2(12)
print(  "2---model.summary -", model.summary())
actions = 5 # hrac muze udelat 5 akci
run_RE_trening(model, actions, The_RE_env)




def run_RE_trening_tf():
    q_net = q_network.QNetwork(train_env.observation_spec(), train_env.action_spec(), fc_layer_params=(100,))
    agent = dqn_agent.DqnAgent(train_env.time_step_spec(),train_env.action_spec(),q_network=q_net, \
                               optimizer=optimizer,td_errors_loss_fn=common.element_wise_squared_loss, \
                                train_step_counter=tf.Variable(0))


    return agent







print("----testy---------RE-----------")
The_RE = TrainingEnvironment()

print("----testy-- -The_RE._observation_space----------", The_RE._observation_space )
print(The_RE._observation_space.sample())
print("--")
print(The_RE._state)

print("----testy---------REwrd--2---------",The_RE.step(2,1,1,2))
print("----testy---------REwrd---3--------",The_RE.step(3,1,1,2))
print("----testy---------REwrd---1--------",The_RE.step(1,1,1,2))

----------------------------------------------------------------------------------




'''





#---------------------  nasledujici funkce jsou pouze pro testy a kontrolu keras modelu  ----------------------------------------

#--------------------------------------------------------------------------------
