from multiprocessing import Process

from api import ConnectFourClient
from play import KerasTrainingPolicy
from play import Player
from play import train

HOST = 'localhost'
PORT = 8080
NUMBER_OF_ITERATIONS = 50
MODEL1_FILE = 'models/model1.h5'
MODEL2_FILE = 'models/model2.h5'


def main():
    host = HOST
    port = PORT
    client = ConnectFourClient(host, port)
    player1_training_policy = KerasTrainingPolicy(MODEL1_FILE)
    player2_training_policy = KerasTrainingPolicy(MODEL2_FILE)
    player1 = Player(client, 'player1', player1_training_policy)
    player2 = Player(client, 'player2', player2_training_policy)
    for i in range(NUMBER_OF_ITERATIONS):
        process1 = Process(target=train, args=(player1, player1_training_policy))
        process2 = Process(target=train, args=(player2, player2_training_policy))
        process1.start()
        process2.start()
        process1.join()
        process2.join()


if __name__ == '__main__':
    main()
