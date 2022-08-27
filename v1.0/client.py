from re import L
from sys import set_coroutine_origin_tracking_depth
import time
import pygame
from _thread import *
from network import Network
from player import Player
from render import Render
from groups import Groups

class Client():
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.action_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN]

        self.network = Network()
        self.game_state = self.network.get_initial_game_state()

        # game_state = setup_network()
        self.player_number = self.network.get_player_num()
        self.I_know_its_my_turn = False

        self.r = Render(width, height, self.game_state)
        self.p1_render = self.r.player_areas[self.player_number]
        # self.p1 = Player(self.p1_render, self.r.map)
        self.p1 = Player(self.player_number, self.r)

        self.display = self.setup_display(self.width, self.height)
        self.clock = pygame.time.Clock()
        # self.group = pygame.sprite.Group()
        self.groups = Groups(self.display)

        self.setup_events()
        self.waiting_thread_running = False

        self.r.update_game_state(self.game_state)
        self.p1.reset_player_area(self.r)
        self.reset_turn()

        start_new_thread(self.waiting_pattern, ())
        pass # breakpoint


# def setup_network():
#     n = Network()
#     game_state = n.getP()
#     return game_state

    def setup_events(self):
        pygame.event.set_blocked(None)
        pygame.event.set_allowed(pygame.KEYDOWN)
        pygame.event.set_allowed(pygame.QUIT)
        pygame.event.get()

    def setup_display(self, width, height):
        pygame.display.init()
        pygame.display.set_caption("Client " + str(self.player_number))
        display = pygame.display.set_mode((width, height))
        return display

    def flip_display(self):
        self.r.draw(self.groups) # draw the initial board
        self.groups.draw()
        pygame.display.flip()

    def on_quit(self):
        print("Player quit. Ending session")

    def reset_turn(self):
        if self.game_state.whose_turn == self.player_number:
            updated_rects = self.p1_render.select_cube(0)
            self.r.set_image(1)
        else:
            self.r.set_image(0)
        self.flip_display()

    def main(self):
        run = True
        self.flip_display()
        while run:
            # wait for keydown events
            self.clock.tick(30)
            event = pygame.event.poll()
            # print(event)

            if event.type == pygame.QUIT:
                run = False
                self.on_quit()
                pygame.quit()


            # Trying something new: this thread is now the only way of getting a new game_state
            if self.game_state.whose_turn != self.player_number:
                continue

            if event.type != pygame.KEYDOWN or event.key not in self.action_keys:
                continue

            # a keydown even has occurred!
            # action pattern
            game_cube_actions = self.p1.select(event)
            if game_cube_actions is not None: # turn is over
                print("==============  My turn is over.  =========================")
                print("Prior to submitting Action, it was player", self.game_state.whose_turn, "'s turn. ==========")
                self.network.send(game_cube_actions) # transmits the client-side Actions and receives an updated game_state from the server
                continue # self.reset_turn() already includes a call to self.flip_display()

            self.flip_display()

    def waiting_pattern(self):
        while True:
            print("Prior to this loop, it was", self.game_state.whose_turn, "'s turn.")
            print("trying to receive pickle")
            self.game_state = self.network.receive_pickle() # hopefully this is asynchronous
            print("pickle received!!!!")
            print("It is now", self.game_state.whose_turn, "'s turn.")

            self.r.update_game_state(self.game_state)
            self.p1.reset_player_area(self.r)
            self.reset_turn()
            self.flip_display()

def main():
    width = 1280
    height = 720
    # width = 1000
    # height = 500

    print("creating client")
    client = Client(width, height)
    print("running main")
    client.main()

main()