import random


class RandomPolicy(object):

    def pick_column(self, game_state):
        next_move = random.choice(game_state.get_possible_columns())
        return next_move
