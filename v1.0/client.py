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

def on_quit():
    print("Player quit. Ending session")

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

def main():

    display = setup_display(width, height)
    setup_events()
    clock = pygame.time.Clock()
    group = pygame.sprite.Group()

    # n = Network()
    # p = n.getP()

    r = Render(width, height, 0)
    p1_render = r.players[0]
    p1 = Player(p1_render, r.map)
    updated_rects = p1_render.select_cube(0)
    r.draw(group) # draw the initial board
    group.draw(display)
    pygame.display.flip()


    run = True
    while run:
        clock.tick(30)
        # p2 = n.send(p)

        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            run = False
            on_quit()
            pygame.quit()

        if event.type != pygame.KEYDOWN or event.key not in action_keys:
            continue

        updated_rects = p1.select(event)
        # p1.player_render.cache.draw_cubes(group)
        group.draw(display)
        # pygame.display.update(updated_rects)
        pygame.display.flip()


main()