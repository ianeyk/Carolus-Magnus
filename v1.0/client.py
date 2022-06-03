import pygame
from network import Network
from player import Player
from testSurface import Render
import time

width = 1000
height = 600
# width = 1280
# height = 720
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

def main():
    run = True
    # n = Network()
    # p = n.getP()
    clock = pygame.time.Clock()


    r = Render(width, height, 0)
    p1 = Player()
    r.draw()
    pygame.display.flip()

    while run:
        clock.tick(1)
        # p2 = n.send(p)

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         run = False
        #         pygame.quit()

        # time.sleep(0.1)
        print(pygame.event.wait(100))
        if p1.select_cube():
            print("here")
            print(p1.selected_cube)
            updated_rects = r.players[0].cache.select_cube(p1.selected_cube)

            r.draw()
            pygame.display.update(updated_rects)

        # p.move()
        # redrawWindow(win, p, p2)

# def main():
#     width = 1280
#     height = 720
#     r = Render(width, height, 0)
#     r.players[0].cache.select_cube(2)
#     r.draw()
#     pygame.display.flip()

main()