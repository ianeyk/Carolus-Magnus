import socket
from _thread import *
import pickle
from player import Player
from game import Game

class Server():
    def __init__(self, server = "192.168.32.30", port = 5555) -> None:
        self.server = server
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.bind((self.server, self.port))
        except socket.error as e:
            str(e)

        self.socket.listen(2)
        print("Waiting for a connection, Server Started")

        self.game = Game(nPlayers = 4)

    def threaded_client(self, conn):
        self.conn = conn

        game_state = self.game.get_game_state()

        self.conn.sendall(pickle.dumps(game_state))
        reply = ""

        while True:
            try:
                action = pickle.loads(self.conn.recv(2048))

                if not action:
                    print("Disconnected")
                    break
                else:
                    self.game.handle_action(action)
                    game_state = self.game.get_game_state()
                    print("Received: ", action)
                    print("Sending : ", game_state)

                self.conn.sendall(pickle.dumps(reply))

            except:
                break
        print("Lost connection")
        self.conn.close()

    def run_thread(self):
        while True:
            self.conn, addr = self.socket.accept()
            print("conn:", self.conn, "addr:", addr)
            print("Connected to:", addr)

            start_new_thread(self.threaded_client, (self.conn, ))

def main():
    my_server = Server(server = "192.168.32.30", port = 5555)
    my_server.run_thread()

main()