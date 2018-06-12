import random
import sys
import numpy as np

from .model_util import game_state_to_vec, reshape_qvalues


class KerasTrainingPolicy(object):

    def __init__(self, model, exploration_rate=0.5, decay_factor=0.999, discounting_factor=0.95):
        self._model = model
        self._exploration_rate = exploration_rate
        self._decay_factor = decay_factor
        self._discounting_factor = discounting_factor
        self._last_state = None
        self._last_move = None

    def pick_column(self, game_state):
        game_state_vec = game_state_to_vec(game_state)
        self._last_state = game_state_vec
        if random.random() < self._exploration_rate:
            next_move = random.choice(game_state.get_possible_columns())
        else:
            qvalues = self._model.predict(game_state_vec)
            for i in game_state.get_full_columns():
                qvalues.itemset((0, i), sys.float_info.min)
            next_move = np.argmax(qvalues)
        self._last_move = next_move
        return next_move

    def decay(self):
        self._exploration_rate = self._exploration_rate * self._decay_factor

    def fit(self, reward, new_state):
        new_state_vec = game_state_to_vec(new_state)
        new_state_max_qvalue = np.max(self._model.predict(new_state_vec))
        qvalues = reward + self._discounting_factor * new_state_max_qvalue
        old_state_vec = self._last_state
        qvalues_vec = self._model.predict(old_state_vec)[0]
        qvalues_vec[self._last_move] = qvalues
        self._model.fit(self._last_state, reshape_qvalues(qvalues_vec), epochs=1, verbose=0)

    def get_last_move(self):
        return self._last_move

    def get_last_state(self):
        return self._last_state
