from api import ConnectFourClient
from play import KerasTrainingPolicy, LearningPlayer
from play import train, load_or_create_model, save_model

HOST = 'localhost'
PORT = 8080
NUMBER_OF_ITERATIONS = 1000
MODEL1_FILE = 'models/model1.h5'
MODEL2_FILE = 'models/model2.h5'


def main():
    host = HOST
    port = PORT
    client = ConnectFourClient(host, port)
    model1 = load_or_create_model(MODEL1_FILE)
    model2 = load_or_create_model(MODEL2_FILE)
    player1_training_policy = KerasTrainingPolicy(model1)
    player2_training_policy = KerasTrainingPolicy(model2)
    player1_id = 'player1'
    player1 = LearningPlayer(client, player1_id, player1_training_policy)
    player2_id = 'player2'
    player2 = LearningPlayer(client, player2_id, player2_training_policy)
    scoreboard = {player1_id: 0, player2_id: 0}
    for i in range(NUMBER_OF_ITERATIONS):
        winner = train([player1, player2])
        if winner:
            scoreboard[winner] += 1
        if i % 100 == 0:
            print(scoreboard)
    save_model(model1, MODEL1_FILE)
    save_model(model2, MODEL2_FILE)


if __name__ == '__main__':
    main()
