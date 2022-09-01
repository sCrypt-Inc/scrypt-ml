import json

import numpy as np
from tensorflow import keras

from scryptlib import (
        compile_contract, build_contract_class
        )

contract = 'testModel.scrypt' 

compiler_result = compile_contract(contract, debug=True)
desc = compiler_result.to_desc()

# Load desc instead:
#with open('./out/testModel.json', 'r') as f:
#    desc = json.load(f)

TestModel = build_contract_class(desc)
test_model = TestModel()

# Load MNIST data
num_classes = 10
num_pixels = 28 * 28

# Load the data and split it between train and test sets.
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Reshape images to [784, 1] and scale them to the [0, 1] range.
x_test = x_test.reshape(x_test.shape[0], num_pixels).astype("float32") / 255


def decimalize(image_arr):
    return np.around(image_arr * 10**8).astype('int64').tolist()


def test_predict_first_10():
    for i in range(10):
        parsed_input = decimalize(x_test[i])
        label = y_test[i]

        assert test_model.predict(parsed_input, label).verify()

