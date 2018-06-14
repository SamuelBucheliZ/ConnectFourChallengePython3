import random

import numpy as np

from .model_util import game_state_to_vec, reshape_qvalues, create_index_mask, read_model, create_model, save_model


class KerasTrainingPolicy(object):

    def __init__(self, model_file=None, exploration_rate=0.5, decay_factor=0.999, discounting_factor=0.95):
        self._model_file = model_file
        self._exploration_rate = exploration_rate
        self._decay_factor = decay_factor
        self._discounting_factor = discounting_factor
        self._model = None
        self._last_state_vec = None
        self._last_move = None

    def load_model(self):
        # model load needs to happen in child process, else troubles: https://github.com/keras-team/keras/issues/3181
        if self._model_file:
            self._model = read_model(self._model_file)
        else:
            self._model = create_model()

    def pick_column(self, game_state):
        game_state_vec = game_state_to_vec(game_state)
        self._last_state_vec = game_state_vec
        if random.random() < self._exploration_rate:
            next_move = random.choice(game_state.get_possible_columns())
        else:
            next_move = self._get_next_move_from_model(game_state, game_state_vec)
        self._last_move = next_move
        return next_move

    def _get_next_move_from_model(self, game_state, game_state_vec):
        qvalues = self._predict(game_state_vec)
        qvalues_length = len(qvalues)
        possible_columns_index_mask = create_index_mask(qvalues_length,
                                                        game_state.get_possible_columns())  # based on https://stackoverflow.com/questions/5761642/python-numpy-get-index-into-main-array-from-subset
        masked_qvalues = qvalues[possible_columns_index_mask]
        sublist_index = np.argmax(masked_qvalues)
        original_index_range = np.arange(qvalues_length)
        next_move = original_index_range[possible_columns_index_mask][sublist_index]
        return next_move

    def learn(self, reward, new_state):
        new_state_vec = game_state_to_vec(new_state)
        new_state_max_qvalue = np.max(self._predict(new_state_vec))
        last_state_qvalue_updated = reward + self._discounting_factor * new_state_max_qvalue
        updated_qvalues_vec = self._predict(self._last_state_vec)
        updated_qvalues_vec[self._last_move] = last_state_qvalue_updated
        self._fit(self._last_state_vec, updated_qvalues_vec)

    def decay_exploration_rate(self):
        self._exploration_rate = self._exploration_rate * self._decay_factor

    def checkpoint(self):
        if self._model_file:
            save_model(self._model, self._model_file) # TODO: Maybe add timestamp

    def _predict(self, state_vec):
        return self._model.predict(state_vec)[0]

    def _fit(self, state_vec, qvalues_vec):
        self._model.fit(state_vec, reshape_qvalues(qvalues_vec), epochs=1, verbose=0)
