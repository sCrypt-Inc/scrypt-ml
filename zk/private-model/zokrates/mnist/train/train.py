#!/usr/bin/env python3

import json
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers


# Model / data parameters
num_pixels = 28 * 28
num_nodes_hl = 5
num_classes = 10

batch_size = 469
epochs = 50

# Load the data and split it between train and test sets.
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Reshape images to [784, 1] and scale them to the [0, 1] range.
x_train = x_train.reshape(x_train.shape[0], num_pixels).astype("float32") / 255
x_test = x_test.reshape(x_test.shape[0], num_pixels).astype("float32") / 255

# Model
model = keras.Sequential([ layers.Dense(num_nodes_hl, activation="relu" ),
                           layers.Dense(num_classes, activation="softmax" )
                          ]) 

model.compile(loss="sparse_categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)

#predictions = np.argmax(model.predict(x_test), axis=1)

# Get weights and biases of the model:
res = {
    'weights': [],
    'biases': []
}
for layer in model.layers:
    weights = layer.get_weights()[0]
    biases = layer.get_weights()[1]

    # Encode values as integers.
    # For float32, which have a max of 8 decimals, we can just scale the values by 10^8.
    weights = np.transpose((weights * 10**8).astype('uint64')).tolist()
    biases = (biases * 10**8).astype('uint64').tolist()

    for i, row in enumerate(weights):
        for j, val in enumerate(row):
            weights[i][j] = str(val)

    for i, val in enumerate(biases):
        biases[i] = str(val)
    
    res['weights'].append(weights)
    res['biases'].append(biases)


with open('res.json', 'w') as f:
    f.write(json.dumps(res))

# Also export some test examples.
res = {
    'examples': [],
    'labels': [] 
}

for i in range(10):
    example = np.around(x_test[i] * 10**8).astype('uint64').tolist()
    for i, val in enumerate(example):
        example[i] = str(val)
    label = str(int(y_test[i]))
    res['examples'].append(example)
    res['labels'].append(label)

with open('test_examples.json', 'w') as f:
    f.write(json.dumps(res))
    
