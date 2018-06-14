from .connect_four_player import Player


class LearningPlayer():
    def __init__(self, client, player_id, training_policy):
        self._player = Player(client, player_id, training_policy)
        self._policy = training_policy

    def register(self):
        self._player.register()

    def wait_until_game_ready(self):
        return self._player.wait_until_game_ready()

    def is_players_turn(self, game_state):
        return game_state.get_current_player() == self._player.get_id()

    def make_one_step_and_learn(self, game_state):
        game_state = self._player.one_step(game_state)
        if game_state.has_error():
            return game_state
        reward = self._get_reward(game_state)
        self._policy.learn(reward, game_state)
        return game_state

    def game_started(self):
        self._policy.game_started()

    def game_finished(self):
        self._policy.game_finished()

    def _get_reward(self, game_state):
        reward = 0
        if game_state.is_finished():
            if game_state.get_winner() == self._player.get_id():
                reward = 1
            else:
                reward = -1
        return reward
