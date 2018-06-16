CHECKPOINT_RATE = 10


def play(player):
    player.register()
    game_state = player.wait_until_game_ready()
    while not game_state.is_finished:
        game_state = player.wait_for_turn()
        game_state = player.one_step(game_state)
    get_winner(game_state)


def train(learning_players):
    assert len(learning_players) == 2
    for learning_player in learning_players:
        learning_player.register()

    game_state = learning_players[0].wait_until_game_ready()

    if learning_players[0].is_players_turn(game_state):
        current = 0
    else:
        current = 1

    for learning_player in learning_players:
        learning_player.game_started()

    while not game_state.is_finished():
        game_state = learning_players[current].make_one_step_and_learn(game_state)
        if game_state.has_error():
            break # TODO: Maybe throw exception?
        current = (current + 1) % 2

    for learning_player in learning_players:
        learning_player.game_finished()

    return get_winner(game_state)


def get_winner(game_state):
    if game_state.has_error():
        print(game_state)
        return None
    elif game_state.is_draw():
        print("It's a draw")
        return None
    else:
        # print(game_state.get_winner() + " won")
        return game_state.get_winner()
