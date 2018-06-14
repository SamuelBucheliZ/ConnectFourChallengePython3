from multiprocessing import Process

from api import ConnectFourClient
from play import Player
from play import RandomPolicy
from play import KerasTrainingPolicy
from play import play, train, create_model, save_model, read_model


HOST = 'localhost'
PORT = 8080
NUMBER_OF_ITERATIONS = 10
MODEL_FILE = 'models/model.h5'


def main():
    host = HOST
    port = PORT
    client = ConnectFourClient(host, port)
    #model = create_model()
    model = read_model(MODEL_FILE)
    player1_training_policy = KerasTrainingPolicy(model)
    #player2_training_policy = KerasTrainingPolicy(model)
    player1 = Player(client, 'player1', player1_training_policy)
    player2 = Player(client, 'player2', RandomPolicy())
    for i in range(NUMBER_OF_ITERATIONS):
        process1 = Process(target=train, args=(player1, player1_training_policy))
        process2 = Process(target=play, args=(player2, ))
        process1.start()
        process2.start()
        process1.join()
        process2.join()
    save_model(model, MODEL_FILE)


if __name__ == '__main__':
    main()
