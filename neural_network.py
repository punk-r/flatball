
'''
import f_menu
from f_menu import *
import f_clases
from f_clases import *
'''
import math
import os.path                  # pro ukladani soboru
from os import path
import random
# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
import numpy as np
import copy

def sigmoid(x):
    # kontrola pro velka cisla
    if x > 500 :
        x = 100
    if x < -500:
        x = -500

    calculated =  1 / (1 + math.exp(-x))
    return calculated


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
    for loop in range (0,len(data_list)):
        data_list[loop]= data_list[loop].replace("'", "")

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
    # zkontroluje path pokud neexistuje vytvori novy model
    if os.path.isfile("model.h5"):
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

    input_biases  = values_list[0][1]
    hiden_layer_weights = values_list[1][0]
    hiden_layer_biases  = values_list[1][1]
    raw_hiden_layer_calculated = [0,0,0,0]
    raw_output_calculated = [0,0,0,0,0]
    hiden_layer_calculated = [0,0,0,0]
    output_calculated = [0,0,0,0,0]
    counter = 0

    '''
    input           ----->                hiddne_layer                        ------->       output

    values        i_weights         H = siqm(sum values*i_weights)                   softmax (sum H * h_weights)

    '''

    raw_hiden_layer_calculated =  np.matmul(input_values,input_weights)
    #print (raw_hiden_layer_calculated)
    for sigmoid_loop in range(0,len(raw_hiden_layer_calculated)):
        #print(raw_hiden_layer_calculated[sigmoid_loop])
        hiden_layer_calculated[sigmoid_loop] = sigmoid(  raw_hiden_layer_calculated[sigmoid_loop] + input_biases[sigmoid_loop] )
        #print(hiden_layer_calculated[sigmoid_loop])

    #print (hiden_layer_calculated)
    raw_output_calculated    =  np.matmul(hiden_layer_calculated,hiden_layer_weights)
    #print (raw_output_calculated)
    for softmax_loop in range(0,len(raw_output_calculated)):
        raw_output_calculated[softmax_loop] = raw_output_calculated[softmax_loop] +  hiden_layer_biases[softmax_loop]
    softmax(output_calculated )

    # bez zapoctenych bias
    return [raw_hiden_layer_calculated , hiden_layer_calculated,raw_output_calculated , output_calculated ]




def save_model_special_format(model ) :
    model_values_list = read_model_values(model)
    in_weights_list = model_values_list[0]
    h_weights_list = model_values_list[1]
    out_weights_list = model_values_list[2]

    for loop1 in range (0,len(model_values_list)):
        print("")
        for loop2 in range (0,len(model_values_list[loop1])):
            for loop3 in range (0,len(model_values_list[loop1][loop2])):
                if loop2 == 0:
                    for loop4 in range (0,len(model_values_list[loop1][loop2][loop3])):
                        print (model_values_list[loop1][loop2][loop3][loop4])
                if loop2 != 0:
                    print (model_values_list[loop1][loop2][loop3])










def learn_from_random_data():

    train_data=[]
    train_labels = []
    set =[0,0,0]
    label=[0]


    for loop1 in range (0,10):
        for loop in range (0,10000):
            set[0] = random.randint( 0,359 ) # path
            set[1] = random.randint( 0,359 ) # uhel k mici
            set[2] = random.randint( -10,20 ) # delka


            # maly uhel,ball blizko kop
            if set[2] > -1 and set[2] < 3 :  #if  True:       # set[0] > 160  or set[0] < 200  :
                label[0] = 3

            # maly uhel,ball daleko krok   velky uhel pootocit
            else:
                if abs (set[1]-set[0]) > 21:
                    label[0] = 0

                if set[2] > 3 and abs (set[1]-set[0]) < 21  :
                    label[0] = 2

            # mic a hrac maji overlap
            if  set[2] < 0:
                label[0] = 2





            train_labels.append(label.copy())
            train_data.append(set.copy())

        print ("10k")


        if False:
            file_name_testing = 'trainingtest10k.txt'
            with open(file_name_testing, 'w') as f:
                for write_loop in range (0,len(train_labels)):
                    f.write( str(train_data[write_loop])  +  str(train_labels[write_loop]) )
                    f.write( '\n')


    train_model(train_data,train_labels,train_data,train_labels)





#--------------------------------------------------------------------------------

#save_model_special_format("model.h5" )

#calculate_live_model([1,2,3],read_model_values ("model.h5")  )

#train_model(train_data,train_labels,test_data,test_labels)

#calculate_live_model([10,10,10],read_model_values("model.h5"))

'''
model = load_model("model.h5")

prediction = model.predict([[ 170, 170 ,27 ]])


action = np.argmax(prediction[0])
biggest = -100
for find_bigges_loop in range (0,len(prediction[0])):
    if prediction[0][find_bigges_loop] > biggest:
        biggest = prediction[0][find_bigges_loop]

print (prediction[0])
print (prediction)
print (action)
print (biggest)


'''


if __name__ == "__main__":
    learn_from_random_data()



# a
