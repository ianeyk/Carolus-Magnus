import time
import pygame
from network import Network
from player import Player
from render import Render

width = 1280
height = 720
# width = 1000
# height = 500

action_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP_ENTER]

# def setup_network():
#     n = Network()
#     game_state = n.getP()
#     return game_state

def setup_events():
    pygame.event.set_blocked(None)
    pygame.event.set_allowed(pygame.KEYDOWN)
    pygame.event.set_allowed(pygame.QUIT)
    pygame.event.get()

def setup_display(width, height):
    pygame.display.init()
    pygame.display.set_caption("Client")
    display = pygame.display.set_mode((width, height))
    return display

def start_turn():
    if game_state.whose_turn == player_number:
        updated_rects = p1_render.select_cube(0)
    r.draw(group) # draw the initial board
    group.draw(display)
    pygame.display.flip()

def on_quit():
    print("Player quit. Ending session")

n = Network()
game_state = n.getP()

# game_state = setup_network()
player_number = 0

r = Render(width, height, game_state)
p1_render = r.players[player_number]
p1 = Player(p1_render, r.map)

display = setup_display(width, height)
clock = pygame.time.Clock()
group = pygame.sprite.Group()

def main():

    setup_events()

    run = True
    start_turn()
    while run:
        clock.tick(30)

        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            run = False
            on_quit()
            pygame.quit()

        if game_state.whose_turn != player_number:
            continue

        if event.type != pygame.KEYDOWN or event.key not in action_keys:
            continue

        if event.key == pygame.K_KP_ENTER:
            game_cube_actions = p1.return_actions()
            if game_cube_actions is not None:
                game_state = n.send(game_cube_actions)
                r.update_game_state(game_state)
                start_turn()
                continue
            else:
                print("Please take all required cube actions before pressing enter")

        updated_rects = p1.select(event)
        # p1.player_render.cache.draw_cubes(group)
        group.draw(display)
        # pygame.display.update(updated_rects)
        pygame.display.flip()


main()