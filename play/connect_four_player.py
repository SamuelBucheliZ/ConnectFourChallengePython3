import time


class Player(object):

    def __init__(self, client, player_id, policy, polling_interval=0.1):
        self._client = client
        self._player_id = player_id
        self._policy = policy
        self._polling_interval = polling_interval
        self._game_id = None

    def register(self):
        game_id = self._client.register_player(self._player_id)
        self._game_id = game_id

    def get_id(self):
        return self._player_id

    def wait_until_game_ready(self):
        return self._wait(lambda g: not g.has_error())

    def wait_for_turn(self):
        return self._wait(lambda g: g.get_current_player() == self._player_id or g.is_finished())

    def _wait(self, predicate):
        while True:
            game_state = self._get_game_state()
            if predicate(game_state):
                return game_state
            time.sleep(self._polling_interval)

    def one_step(self, game_state):
        column = self._policy.pick_column(game_state)
        return self._client.drop_disc(self._game_id, self._player_id, column)

    def _get_game_state(self):
        return self._client.get_game_state(self._game_id)
