#!/usr/bin/env python3

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers


# Model / data parameters
num_classes = 10
num_pixels = 28 * 28

# Load the data and split it between train and test sets.
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Reshape images to [784, 1] and scale them to the [0, 1] range.
x_train = x_train.reshape(x_train.shape[0], num_pixels).astype("float32") / 255
#x_test = x_test.reshape(x_test.shape[0], num_pixels).astype("float32") / 255

# Model
model = keras.Sequential([ layers.Dense( 128, activation="relu" ),
                           layers.Dense( 10, activation="softmax" )
                          ]) 

batch_size = 469
epochs = 50

model.compile(loss="sparse_categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)


# Get weights and biases of the model:
weights_by_layer = []
biases_by_layer = []
for layer in model.layers:
    weights = layer.get_weights()[0]
    biases = layer.get_weights()[1]

    # Encode values as integers.
    # For float32, which have a max of 8? decimals, we can just scale the values by 10^8.
    weights = np.around(weights * 10**8).astype('int64')
    biases = np.around(biases * 10**8).astype('int64')
    
    weights_by_layer.append(weights.tolist())
    biases_by_layer.append(biases.tolist())

# Create an sCrypt lib with the resulting parameters.
with open('modelParams.scrypt', 'w') as f:
    f.write('''
    library ModelParams {{

        static const int N_INPUTS = 784;
        static const int N_NODES_HL = 128;
        static const int N_NODES_OUT = 10;
        
        int[N_INPUTS][N_NODES_HL] WEIGHTS_0 = {};

        int[N_NODES_HL][N_NODES_OUT] WEIGHTS_1 = {};
        
        int[N_NODES_HL] BIASES_0 = {};

        int[N_NODES_OUT] BIASES_1 = {};

    }}
    '''.format(weights_by_layer[0], weights_by_layer[1],
               biases_by_layer[0], biases_by_layer[1])
    )

