import time
import pygame
from network import Network
from player import Player
from render import Render

class Client():
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.action_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN]

        self.network = Network()
        self.game_state = self.network.get_initial_game_state()

        # game_state = setup_network()
        self.player_number = self.network.get_player_num()

        self.r = Render(width, height, self.game_state)
        self.p1_render = self.r.player_areas[self.player_number]
        self.p1 = Player(self.p1_render, self.r.map)

        self.display = self.setup_display(self.width, self.height)
        self.clock = pygame.time.Clock()
        self.group = pygame.sprite.Group()

        self.setup_events()


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
        pygame.display.set_caption("Client")
        display = pygame.display.set_mode((width, height))
        return display

    def flip_display(self):
        if self.game_state.whose_turn == self.player_number:
            updated_rects = self.p1_render.select_cube(0)
        self.r.draw(self.group) # draw the initial board
        self.group.draw(self.display)
        pygame.display.flip()

    def on_quit(self):
        print("Player quit. Ending session")

    def main(self):
        run = True
        self.flip_display()
        while run:
            self.clock.tick(30)
            event = pygame.event.poll()
            # print(event)

            if event.type == pygame.QUIT:
                run = False
                self.on_quit()
                pygame.quit()

            # if self.game_state.whose_turn != self.player_number:
            #     continue

            if event.type != pygame.KEYDOWN or event.key not in self.action_keys:
                continue

            print("event: ", event, "with KEY", event.key)
            # print(event.key)

            if event.key == pygame.K_RETURN:
                game_cube_actions = self.p1.return_actions()
                if game_cube_actions is not None:
                    self.game_state = self.network.send(game_cube_actions)
                    print("Updating game state to", self.game_state)
                    self.r.update_game_state(self.game_state)
                    self.p1.reset_player_area(self.r.player_areas[self.player_number], self.r.map)
                    self.flip_display()
                    continue
                else:
                    print("Please take all required cube actions before pressing enter")

            updated_rects = self.p1.select(event)
            # p1.player_render.cache.draw_cubes(group)
            self.group.draw(self.display)
            # pygame.display.update(updated_rects)
            pygame.display.flip()

def main():
    width = 1280
    height = 720
    # width = 1000
    # height = 500

    client = Client(width, height)
    client.main()

main()