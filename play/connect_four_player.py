import time


class Player(object):

    def __init__(self, client, player_id, policy, polling_interval=0.1):
        self._client = client
        self._player_id = player_id
        self._policy = policy
        self._polling_interval = polling_interval
        self._number_of_games = 0 # TODO: Add statistics
        self._number_of_wins = 0
        self._game_id = None

    def register(self):
        game_id = self._client.register_player(self._player_id)
        self._game_id = game_id

    def get_id(self):
        return self._player_id

    def one_step(self):
        while True:
            game_state = self._get_game_state()
            if game_state.get_current_player() == self._player_id:
                game_state = self._drop_disc(game_state)
                break
            if game_state.is_finished():
                break
            time.sleep(self._polling_interval)
        return game_state

    def _get_game_state(self):
        return self._client.get_game_state(self._game_id)

    def _drop_disc(self, game_state):
        column = self._policy.pick_column(game_state)
        return self._client.drop_disc(self._game_id, self._player_id, column)
