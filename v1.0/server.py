import socket
from _thread import *
import pickle
from player import Player
from game import Game

class Server():
    def __init__(self, server = "192.168.32.30", port = 5555) -> None:
        self.server = server
        self.port = port
        self.nPlayers = 4
        self.next_player_num = 0

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.bind((self.server, self.port))
        except socket.error as e:
            str(e)

        self.socket.listen(self.nPlayers)
        print("Waiting for a connection, Server Started")

        self.game = Game(self.nPlayers)

    def threaded_client(self, conn, player_num):
        self.conn = conn

        game_state = self.game.get_game_state()

        self.conn.send(str.encode(str(player_num)))
        self.conn.send(pickle.dumps(game_state))

        while True:
            try:
                action = pickle.loads(self.conn.recv(2048))
                print(action)

                if not action:
                    print("Disconnected")
                    break
                else:
                    self.game.handle_action(action)
                    game_state = self.game.get_game_state()
                    print("Received: ", action)
                    print("Sending : ", game_state)

                self.conn.send(pickle.dumps(game_state))

            except:
                break

        print("Lost connection")
        self.conn.close()

    def run_thread(self):
        while True:
            self.conn, addr = self.socket.accept()
            print("conn:", self.conn, "addr:", addr)
            print("Connected to:", addr)

            start_new_thread(self.threaded_client, (self.conn, self.next_player_num))
            self.next_player_num = 0
            # self.next_player_num += 1

def main():
    my_server = Server(server = "192.168.32.30", port = 5555)
    my_server.run_thread()

main()