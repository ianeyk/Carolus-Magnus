import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.32.30"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player_num, self.game_state = self.connect()

    def get_player_num(self):
        return self.player_num

    def get_initial_game_state(self):
        return self.game_state

    def connect(self):
        try:
            self.client.connect(self.addr)
        except socket.error as e:
            print(e)
            assert(False) #TODO: Make this pythonic
        player_num = int(self.receive_str(256))
        game_state = self.receive_pickle(2048 * 256)
        return player_num, game_state

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return self.receive_pickle(bytes = 2048 * 256)
        except socket.error as e:
            print(e)

    def receive_str(self, bytes = 2048):
        try:
            received = self.client.recv(bytes)
            # print("Network received:", received)
            decoded = received.decode()
            print("Decoded a", decoded)
            return decoded
        except socket.error as e:
            print(e)

    def receive_pickle(self, bytes = 2048 * 256 * 4):
        try:
            received = self.client.recv(bytes)
            # print("Network received:", received)
            decoded = pickle.loads(received)
            print("Decoded a", decoded)
            return decoded
        except socket.error as e:
            print(e)