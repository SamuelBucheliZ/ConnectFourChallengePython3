from api import ConnectFourClient
from play import KerasTrainingPolicy
from play import LearningPlayer
from play import train2, load_or_create_model

HOST = 'localhost'
PORT = 8080
NUMBER_OF_ITERATIONS = 50
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
    player1 = LearningPlayer(client, 'player1', player1_training_policy)
    player2 = LearningPlayer(client, 'player2', player2_training_policy)
    for i in range(NUMBER_OF_ITERATIONS):
        train2([player1, player2])


if __name__ == '__main__':
    main()
