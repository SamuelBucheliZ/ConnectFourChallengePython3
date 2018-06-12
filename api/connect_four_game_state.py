import json


class GameState(object):

    def __init__(self, json):
        self._json = json

    def get_current_player(self):
        return self._json['currentPlayer']

    def is_draw(self):
        return self._json.get('draw', False)

    def get_winner(self):
        return self._json.get('winner', None)

    def board(self):
        return self._json['board']

    def has_error(self):
        return 'error' in self._json

    def get_current_player_color(self):
        current_player = self.get_current_player()
        for player in self._json['players']:
            if player['playerId'] == current_player:
                return player['disc']

    def is_finished(self):
        return self.has_error() or self.get_winner() or self.is_draw()

    def get_number_of_rows(self):
        return len(self.board())

    def get_number_of_columns(self):
        return len(self.board()[0])

    def get_full_columns(self):
        return self._get_columns(lambda c: self._is_full(c))

    def get_possible_columns(self):
        return self._get_columns(lambda c: not self._is_full(c))

    def _get_columns(self, predicate):
        number_of_columns = self.get_number_of_columns()
        column_indices = []
        for i in range(number_of_columns):
            column = self._get_column(i)
            if predicate(column):
                column_indices.append(i)
        return column_indices

    def _get_column(self, i):
        board = self.board()

        column = []
        for row in board:
            column.append(row[i])

        return column

    def _is_full(self, column):
        return 'EMPTY' not in column

    # def columns(self):
    #     return len(self.board()[0])
    #
    # def rows(self):
    #     return len(self.board())
    #
    # def shape(self):
    #     return self.rows(), self.columns()
    #
    # def possible_columns(self):
    #     c = self.columns()
    #     out = []
    #     for i in range(c):
    #         if self.free_space_column(i) < c:
    #             out.append(i)
    #     return out
    #
    # def state_column(self, n):
    #     board = self.board()
    #
    #     columns = []
    #     for row in board:
    #         columns.append(row[n])
    #
    #     return columns
    #
    # def free_space_column(self, n):
    #     column = self.state_column(n)
    #     free_space = 0
    #     for c in column:
    #         if c == 'EMPTY':
    #             free_space += 1
    #
    #     return free_space
    #
    # def state_row(self, n):
    #     board = self.board()
    #     return board[n]

    def __str__(self):
        return json.dumps(self._json)

