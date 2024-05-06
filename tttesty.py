
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

from os.path import abspath
from os import getcwd


from numpy import exp
from numpy import max
import copy


import platform
from platform import system
import h5py


print ('ssssstatatatart')
xxx=  [[   [[0,1,1,1,0,0,0,1,1,0]],[[0,1,1,1,0,0,0,1,1,0]]  ]]
xxxx= [[0,1]]


train_model(xxx,xxxx,'0205203954')
train_model(xxx,xxxx,'original')
path = get_path_home_folder()

model0205203954 = load_model_from_5h(path +  '0205203954'  + ".h5")

print ( model0205203954.layers[1].get_weights()[0])
print ( model0205203954.layers[1].get_weights()[1])

##print(model0205203954.to_json())
