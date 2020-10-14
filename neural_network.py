
'''
import f_menu
from f_menu import *
import f_clases
from f_clases import *
'''
import os.path                  # pro ukladani soboru
from os import path

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

import numpy as np


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
            keras.layers.Dense(3, input_shape=(3,)),
            keras.layers.Dense(4,activation="relu"),
            keras.layers.Dense(5,activation="softmax")
            ])


    model.compile(optimizer="adam",loss='sparse_categorical_crossentropy',metrics=["accuracy"])
    model.fit(train_data,train_labels,epochs=5)

    test_loss , test_acc = model.evaluate(test_data,test_labels )
    print ("tttestesd",test_acc)
    #print (model)

    prediction = model.predict(test_data)
    #print("vysledek",np.argmax(prediction[5]))

    model.save("model.h5")

def load_model(new_model):
    model = keras.models.load_model(new_model)
    return model



#train_model(train_data,train_labels,test_data,test_labels)
