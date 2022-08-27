import socket
from _thread import *
from select import select
import pickle
from player import Player
from game import Game

class Server():
    def __init__(self, server = "192.168.32.30", port = 5555) -> None:
        self.server = server
        self.port = port
        self.nPlayers = 4
        self.next_player_num = 0

        self.updates_available_by_player = [True] * self.nPlayers

        self.connections_list = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.bind((self.server, self.port))
        except socket.error as e:
            print(e)

        self.socket.listen(self.nPlayers)
        print("Waiting for a connection, Server Started")

        self.game = Game(self.nPlayers)

    def set_game_state_update_available(self, all_but = None):
        for player_number in range(len(self.updates_available_by_player)):
            self.updates_available_by_player[player_number] = True

        if all_but is not None:
            self.updates_available_by_player[all_but] = False

    def threaded_client(self, conn, player_num):

        game_state = self.game.get_game_state()

        conn.send(str.encode(str(player_num)))
        conn.send(pickle.dumps(game_state))

        while True:

            print("START OF LOOP: waiting for player", player_num, "to send an action")

            try:
                select([conn], [], []) # wait until the socket `conn` is available for reading
                action = pickle.loads(conn.recv(2048 * 8))
            except Exception as e:
                print("error in connection was: (#1)")
                print(e)
                break

            print("player", player_num, "has sent action.")

            if not action:
                print("Disconnected")
                break

            print("~~~~~~~~~~~~~~  Updates are available, so sending a new game_state to Player", player_num, " ~~~~~~~~~~~~")
            print("^^^ sending that game_state's next player order is", game_state.whose_turn)

            self.game.handle_action(action) # first, handle the action!!!
            game_state = self.game.get_game_state()
            print(f"=-=-=-=-=-=-==-=-  setting game state update to be available! (End of Player {player_num}'s turn) -=-=-=-=-=--=-=-=-=-=-=-=")
            self.publish_game_state()

        print("Lost connection")
        conn.close()
        # assert(False) # crash so we can restart the server #TODO: take out this line when done debugging

    def publish_game_state(self):
        game_state = self.game.get_game_state()
        msg = pickle.dumps(game_state)

        print("sending message to all connections")
        for conn in self.connections_list:
            try:
                conn.send(msg)
            except Exception as e:
                print("error in connection was: (#2)")
                print(e)

    def run_thread(self):
        while True:
            conn, addr = self.socket.accept()
            print("conn:", conn, "addr:", addr)
            print("Connected to:", addr)

            conn.setblocking(False)
            self.connections_list.append(conn)

            start_new_thread(self.threaded_client, (conn, self.next_player_num))
            # self.next_player_num = 0
            # self.next_player_num += 1
            self.next_player_num = (self.next_player_num + 1) % 2

def main():
    # my_server = Server(server = "192.168.32.30", port = 5555) # this doesn't work while using a phone as hotspot!
    my_server = Server(server = "localhost", port = 5555)
    my_server.run_thread()

main()