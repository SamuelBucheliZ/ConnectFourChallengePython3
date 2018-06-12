from multiprocessing import Process

from api import ConnectFourClient
from play import Player
from play import RandomPolicy
from play import KerasTrainingPolicy
from play import play, train, create_model

NUMBER_OF_ITERATIONS = range(500)


def main():
    host = 'localhost'
    port = 8080
    client = ConnectFourClient(host, port)
    training_policy = KerasTrainingPolicy(create_model())
    player1 = Player(client, 'player1', training_policy)
    player2 = Player(client, 'player2', RandomPolicy())
    for i in NUMBER_OF_ITERATIONS:
        process1 = Process(target=train, args=(player1, training_policy))
        process2 = Process(target=play, args=(player2,))
        process1.start()
        process2.start()
        process1.join()
        process2.join()


if __name__ == '__main__':
    main()
