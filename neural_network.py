
'''
import f_menu
from f_menu import *
import f_clases
from f_clases import *
'''
import math
import os.path                  # pro ukladani soboru
from os import path

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
import numpy as np


def sigmoid(x):
  return 1 / (1 + math.exp(-x))


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()



def load_data(file_name):
    data_list=[]
    file = open(file_name, 'r')
    for line in file:
        line=line.replace("'", "")
        data_list.append(  line.strip() )

    file.close()
    return data_list

'''
train_data = load_data('training.txt')
train_labels = load_data('traininglabels.txt')


print ("train_data"  ,train_data )
print ("train_labels"  ,train_labels )


test_data = load_data('testing.txt')
test_labels = load_data('testinglabels.txt')

test_data = load_data('training.txt')
test_labels = load_data('traininglabels.txt')
'''




def train_model(train_data,train_labels,test_data,test_labels):
    #print (train_data)
    #print(train_labels)

    # existuje model?
    if os.path.isfile("model.h5"):
        print('model loading')
        model = load_model("model.h5")

        model.compile(optimizer="adam",loss='sparse_categorical_crossentropy',metrics=["accuracy"])
        model.fit(train_data,train_labels,epochs=5)

        test_loss , test_acc = model.evaluate(test_data,test_labels )

    else:
        model = keras.Sequential([
            keras.layers.Dense(4, input_shape=(3,)),
            keras.layers.Dense(5,activation="relu"),
            keras.layers.Dense(5,activation="softmax")
            ])


    model.compile(optimizer="adam",loss='sparse_categorical_crossentropy',metrics=["accuracy"])
    model.fit(train_data,train_labels,epochs=5)

    #test_loss , test_acc = model.evaluate(test_data,test_labels )
    #print ("tttestesd",test_acc)
    #print (model)

    #prediction = model.predict(test_data)
    #print("vysledek",np.argmax(prediction[5]))

    model.save("model.h5")


def load_model(new_model):
    model = keras.models.load_model(new_model)
    return model



def print_model_values(model):
    # hodnoty modelu
    model = load_model(model)

    for layer in model.layers:
        weights = layer.get_weights() # list of numpy arrays
        print (weights)
        print ("")
    model.summary()

def read_model_values(model):
    model_values_list =[0,0,0]
    saving_index = 0
    model = load_model(model)
    for layer in model.layers:
        weights = layer.get_weights() # list of numpy arrays
        model_values_list [saving_index] = weights
        saving_index = saving_index + 1
    return model_values_list


def calculate_live_model(live_inputs,values_list):
    input_values = np.array(live_inputs)
    input_weights = values_list[0][0]
    '''
    print("")
    print("input_values " , input_values)
    print("")
    print("input_weights " , input_weights)
    print("")
    print( "input_weights[0] ",input_weights[0])
    print("")
    print( "input_weights[0][0] "  ,input_weights[0][0])
    print("")
    '''
    input_biases  = values_list[0][1]
    hiden_layer_weights = values_list[1][0]
    hiden_layer_biases  = values_list[1][1]
    raw_hiden_layer_calculated = [0,0,0,0]
    raw_output_calculated = [0,0,0,0,0]
    hiden_layer_calculated = [0,0,0,0]
    output_calculated = [0,0,0,0,0]
    counter = 0

    raw_hiden_layer_calculated =  np.matmul(input_values,input_weights)
    for sigmoid_loop in range(0,len(hiden_layer_calculated)):
        hiden_layer_calculated[sigmoid_loop] = sigmoid(  hiden_layer_calculated[sigmoid_loop]  )

    raw_output_calculated    =  np.matmul(hiden_layer_calculated,hiden_layer_weights)
    softmax(output_calculated )

    # bez zapoctenych bias
    return [raw_hiden_layer_calculated , hiden_layer_calculated,raw_output_calculated , output_calculated ]

#--------------------------------------------------------------------------------

#calculate_live_model([1,2,3],read_model_values ("model.h5")  )





#train_model(train_data,train_labels,test_data,test_labels)


'''
print ( read_model_values ("model.h5"))

print("")



print ( read_model_values ("model.h5")[0])
print("")

print ( read_model_values ("model.h5")[0][0])
print("")

print ( read_model_values ("model.h5")[0][1])
'''
