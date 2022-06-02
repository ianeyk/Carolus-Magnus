import pygame

class GameState():
    def __init__(self):
        pass

class Render():

    green = (0, 230, 0)
    red = (230, 0, 0)
    blue = (0, 119, 234)
    yellow = (230, 230, 0)
    pink = (255, 167, 182)
    cube_colors = {0: green, 1: red, 2: blue, 3: yellow, 4: pink}

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Client")

        # drawing area sizes
        # player area
        self.player_area = (self.width / 4, self.height / 2)
        self.p0_center = (self.width * 1 / 8, self.height * 1 / 4)
        self.p1_center = (self.width * 1 / 8, self.height * 3 / 4)
        self.p2_center = (self.width * 7 / 8, self.height * 1 / 4)
        self.p3_center = (self.width * 7 / 8, self.height * 3 / 4)
        # board area
        self.board_area = (self.width / 3, self.height / 3)
        self.board_center = (self.width / 2, self.height / 2)

        self.cube_width = 20
        self.cube_height = 20

    def update(self, game_state):
        self.game_state = game_state

        self.win.fill((225, 225, 200)) # background color
        self.draw_player(self.p0_center, self.player_area, 0)
        self.draw_player(self.p1_center, self.player_area, 1)
        self.draw_player(self.p2_center, self.player_area, 0)
        self.draw_player(self.p3_center, self.player_area, 1)
        self.draw_board()

        pygame.display.update()

    def draw_player(self, mid, scale, player_num):

        def draw_background(fill, border):
            self.draw_rect(mid, scale, 0, 0, 1, 1, border, factor = 1)
            self.draw_rect(mid, scale, 0, 0, 1, 1, fill, factor = 0.95)

        draw_background((200, 200, 200), (10, 10, 10))
        for color_id in range(5):
            self.draw_cube(mid, scale, (color_id - 2) / 3, 1, color_id)
        self.draw_cube(mid, scale, 0, 0, 0)
        self.draw_cube(mid, scale, 1, 0, 0)
        self.draw_cube(mid, scale, -1, 0, 0)
        pass

    def draw_board(self):
        pass

    def draw_rect(self, center, area, x, y, width, height, color, factor = 0.9):
        """Pass in the given center and size of the region;
        this remaps the coordinates x and y to the scale of -1 to 1.
        Draws a rectangle centered on x, y in the local reference frame.
        The factor of 0.9 helps if you really don't want to exceed the bounds of your region.
        """
        rect = (center[0] + x * area[0] / 2 * factor - width * area[0] / 2 * factor,
                center[1] - y * area[1] / 2 * factor - height * area[0] / 2 * factor,
                width * area[0] * factor, height * area[1] * factor)
        pygame.draw.rect(self.win, color, rect)

    def draw_cube(self, center, area, x, y, color_id, factor = 0.9):
        rect = (center[0] - x * area[0] / 2 * factor - self.cube_width / 2,
            center[1] - y * area[1] / 2 * factor - self.cube_height / 2,
            self.cube_width, self.cube_height)
        pygame.draw.rect(self.win, Render.cube_colors[color_id], rect)

def main():
    width = 1280 - 0
    height = 720 - 100

    r = Render(width, height)
    r.update(0)

main()

pass