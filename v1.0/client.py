import pygame
from network import Network
from player import Player
from testSurface import Render

width = 1280
height = 720

def main():

    # initialize the display
    # width = 1000
    # height = 600
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
    p1 = Player()
    updated_rects = r.players[0].select_cube(0)
    r.draw().draw(display)
    pygame.display.flip()

    while run:
        clock.tick(30)
        # p2 = n.send(p)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        for event in events:
            if p1.select_cube(event):
                print("here")
                print(p1.selected_cube)
                updated_rects = r.players[0].select_cube(p1.selected_cube)

                r.players[0].cache.draw_cubes().draw(display)
                pygame.display.update(updated_rects)

                if p1.down:
                    updated_rects = r.players[0].add_to_court(p1.selected_cube)
                    r.players[0].cache.draw_cubes().draw(display)
                    pygame.display.update(updated_rects)
                # pygame.display.flip()

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