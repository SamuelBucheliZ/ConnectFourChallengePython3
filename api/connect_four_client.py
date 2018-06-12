import requests
from urllib.parse import urljoin

from api.connect_four_game_state import GameState


class ConnectFourClient(object):
    ENDPOINT_GAME_STATE = '/api/v1/client/games/{game_id}'
    ENDPOINT_DROP_DISC = '/api/v1/client/games/{game_id}/column/{column}'
    ENDPOINT_REGISTER = '/api/v1/client/register'

    def __init__(self, host, port, scheme='http'):
        self._host = host
        self._port = port
        self._scheme = scheme

    def _get_url(self, endpoint):
        base = '{scheme}://{host}:{port}'.format(
            scheme=self._scheme,
            host=self._host,
            port=self._port
        )
        return urljoin(base, endpoint)

    def get_game_state(self, game_id):
        url = self._get_url(self.ENDPOINT_GAME_STATE.format(
            host=self._host,
            port=self._port,
            game_id=game_id
        ))
        response = requests.get(url)
        return GameState(response.json())

    def drop_disc(self, game_id, player_id, column):
        column_fixed = column + 1 # fix 1-based indexing used by server
        url = self._get_url(self.ENDPOINT_DROP_DISC.format(
            host=self._host,
            port=self._port,
            game_id=game_id,
            column=column_fixed
        ))
        params = {'playerId': player_id}
        response = requests.put(url, params=params)
        return GameState(response.json())

    def register_player(self, player_id):
        url = self._get_url(self.ENDPOINT_REGISTER.format(
            host=self._host,
            port=self._port
        ))
        params = {'playerId': player_id}
        response = requests.post(url, params=params)
        return response.json()
