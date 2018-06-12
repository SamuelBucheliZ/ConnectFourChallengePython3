import numpy as np
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # disable logging for now
from keras import Sequential
from keras.engine import InputLayer
from keras.layers import Dense

NUMBER_OF_COLUMNS = 7
NUMBER_OF_ROWS = 6


def create_model():
    model = Sequential()
    model.add(InputLayer(batch_input_shape=(1, NUMBER_OF_ROWS * NUMBER_OF_COLUMNS)))
    model.add(Dense(10, activation='sigmoid'))
    model.add(Dense(NUMBER_OF_COLUMNS, activation='linear'))
    model.compile(loss='mse', optimizer='adam', metrics=['mae'])
    return model


def game_state_to_vec(game_state):
    board = game_state.board()
    board_vec = np.zeros((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS))
    my_color = game_state.get_current_player_color()
    for row in range(game_state.get_number_of_rows()):
        for column in range(game_state.get_number_of_columns()):
            if board[row][column] == my_color:
                board_vec.itemset((row, column), 1)
            elif board[row][column] != 0:
                board_vec.itemset((row, column), -1)
    return board_vec.reshape(-1, NUMBER_OF_ROWS * NUMBER_OF_COLUMNS)


def reshape_qvalues(qvalues_vec):
    return qvalues_vec.reshape(-1, NUMBER_OF_COLUMNS)
