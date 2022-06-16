import time
import pygame
from network import Network
from player import Player
from render import Render

width = 1280
# height = 720

def on_quit():
    pass

def main():

    # initialize the display
    # width = 1000
    height = 500
    pygame.display.init()
    pygame.display.set_caption("Client")
    # screen = pygame.Surface((width, height))
    display = pygame.display.set_mode((width, height))

    pygame.event.set_blocked(None)
    pygame.event.set_allowed(pygame.KEYDOWN)
    pygame.event.set_allowed(pygame.QUIT)
    pygame.event.get()

    run = True
    # n = Network()
    # p = n.getP()
    clock = pygame.time.Clock()


    r = Render(width, height, 0)
    p1_render = r.players[0]
    p1 = Player(p1_render, r.map)
    updated_rects = p1_render.select_cube(0)
    r.draw().draw(display)
    pygame.display.flip()
    i = 0
    j = 0
    k = 0
    while run:
        clock.tick(30)
        # p2 = n.send(p)

        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            run = False
            on_quit()
            pygame.quit()

        group, updated_rects = p1.select(event)
        if group:
            group.draw(display)
        if updated_rects:
            pygame.display.update(updated_rects)
            pygame.display.flip()

# def main():
#     width = 1280
#     height = 720
#     r = Render(width, height, 0)
#     r.players[0].cache.select_cube(2)
#     r.draw()
#     pygame.display.flip()

main()