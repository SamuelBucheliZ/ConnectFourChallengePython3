def play(player):
    player.register()
    while True:
        game_state = player.one_step()
        if game_state.is_finished():
            break
    print_winner(game_state)


def train(player, training_policy):
    player.register()
    while True:
        game_state = player.one_step()
        if game_state.has_error():
            break
        reward = get_reward(game_state, player)
        training_policy.fit(reward, game_state)
        if game_state.is_finished():
            break
    training_policy.decay()
    print_winner(game_state)


def get_reward(game_state, player):
    reward = 0
    if game_state.is_finished():
        if game_state.get_winner() == player.get_id():
            reward = 1
        else:
            reward = -1
    return reward


def print_winner(game_state):
    if game_state.has_error():
        print(game_state)
    elif game_state.is_draw():
        print("It's a draw")
    else:
        print(game_state.get_winner() + " won")