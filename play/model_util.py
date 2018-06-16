import os
from pathlib import Path

import numpy as np
from keras import Sequential
from keras.activations import sigmoid, linear
from keras.engine import InputLayer
from keras.layers import Dense
from keras.losses import mean_squared_error
from keras.metrics import mean_absolute_error
from keras.models import load_model
from keras.optimizers import adam

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # disable logging these warnings for now

NUMBER_OF_COLUMNS = 7
NUMBER_OF_ROWS = 6


def load_or_create_model(model_file):
    if Path(model_file).is_file():
        return load_model(model_file)
    else:
        return create_model()


def create_model():
    model = Sequential()
    model.add(InputLayer(batch_input_shape=(1, NUMBER_OF_ROWS * NUMBER_OF_COLUMNS), name='input'))
    model.add(Dense(NUMBER_OF_COLUMNS * NUMBER_OF_ROWS * 2, input_shape=(NUMBER_OF_ROWS * NUMBER_OF_COLUMNS,), activation=sigmoid, name='hidden1'))
    model.add(Dense(NUMBER_OF_COLUMNS*2, input_shape=(NUMBER_OF_COLUMNS * NUMBER_OF_ROWS * 2,), activation=sigmoid, name='hidden2'))
    model.add(Dense(NUMBER_OF_COLUMNS, input_shape=(NUMBER_OF_COLUMNS*2,), activation=linear, name='output'))
    model.compile(loss=mean_squared_error, optimizer=adam(), metrics=[mean_absolute_error])
    return model


def save_model(model, filename):
    model.save(filename)


def read_model(filename):
    return load_model(filename)


def game_state_to_vec(game_state):
    board = game_state.board()
    board_vec = np.zeros((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS), dtype=int)
    my_color = game_state.get_current_player_color()
    for row in range(game_state.get_number_of_rows()):
        for column in range(game_state.get_number_of_columns()):
            if board[row][column] == my_color:
                board_vec.itemset((row, column), 1)
            elif board[row][column] != 'EMPTY':
                board_vec.itemset((row, column), -1)
    return board_vec.reshape(-1, NUMBER_OF_ROWS * NUMBER_OF_COLUMNS)


def reshape_qvalues(qvalues_vec):
    return qvalues_vec.reshape(-1, NUMBER_OF_COLUMNS)


def create_index_mask(size, indices):
    indices_array = np.array(indices)
    mask_array = np.zeros(size, dtype=bool)
    mask_array[indices_array] = True
    return mask_array
