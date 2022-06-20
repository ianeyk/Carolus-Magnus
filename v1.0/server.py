import socket
from _thread import *
import pickle
from player import Player
from game import Game

server = "192.168.32.30"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

game = Game(nPlayers = 4)
game_state = game.get_game_state()

def threaded_client(conn):
    conn.sendall(pickle.dumps(game_state))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if not data:
                print("Disconnected")
                break
            else:
                game.handle_game_state_update(data)
                game_state = game.get_game_state()
                print("Received: ", data)
                print("Sending : ", game_state)

            conn.sendall(pickle.dumps(reply))

        except:
            break
    print("Lost connection")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, conn)