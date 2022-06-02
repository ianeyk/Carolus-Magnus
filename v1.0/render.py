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
        player_area_border = 0.95
        self.player_area = (self.width / 4 * player_area_border, self.height / 2 * player_area_border)
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
        self.draw_player(self.p3_center, self.player_area, 1)
        self.draw_player(self.p2_center, self.player_area, 0)
        self.draw_player(self.p1_center, self.player_area, 1)
        self.draw_player(self.p0_center, self.player_area, 0)
        self.draw_board()

        pygame.display.update()

    def draw_player(self, center, area, player_num):

        def draw_court(court_cubes):
            gen_1 = CourtCubeGenerator(self.win, center, area, default_color=Render.pink)
            for color_id in range(5):
                court_gen = gen_1.new_court_gen(((color_id - 2) / 2.4, 0.2), (1/5.2, 0.8), Render.cube_colors[color_id])
                court_gen.draw_background(fill = (180, 180, 180), border = (120, 120, 120))
                court_gen.draw_court_cubes(court_cubes[color_id], 0.08)
                court_gen.draw_rect((0, 0.88), (1, 0.03))

        court_cubes = self.game_state.players[player_num].court.get_cubes()
        draw_court(court_cubes)

    def draw_board(self):
        pass

class ReferenceFrame():
    def __init__(self, center, area):
        self.center = center
        self.area = area

    def convert_xy(self, xy):
        x_out = self.center[0] + xy[0] * self.area[0] / 2
        y_out = self.center[1] + xy[1] * self.area[1] / 2
        return x_out, y_out

    def convert_area(self, wh):
        w_out = wh[0] * self.area[0]
        h_out = wh[1] * self.area[1]
        return w_out, h_out

class RectangleGenerator(ReferenceFrame):
    def __init__(self, win, center, area, default_color = (255, 255, 255), factor = 1):
        self.win = win
        self.center = center
        self.area = area
        self.default_color = default_color
        self.factor = factor

    def new_rect_gen(self, rel_center, rel_area, default_color = (255, 255, 255), factor = 1):
        new_center = self.convert_xy(rel_center)
        new_area = self.convert_area(rel_area)
        return RectangleGenerator(self.win, new_center, new_area, default_color, factor)

    def draw_rect(self, xy, wh, color = None, factor = None):
        if not color:
            color = self.default_color
        if not factor:
            factor = self.factor
        rect = (self.center[0] + xy[0] * self.area[0] / 2 * factor - wh[0] * self.area[0] / 2 * factor,
                self.center[1] - xy[1] * self.area[1] / 2 * factor - wh[1] * self.area[1] / 2 * factor,
                wh[0] * self.area[0] * factor, wh[1] * self.area[1] * factor)
        pygame.draw.rect(self.win, color, rect)

    def draw_cube(self, xy, cube_size, color = None, factor = None):
        if not color:
            color = self.default_color
        if not factor:
            factor = self.factor

        rect = (self.center[0] + xy[0] * self.area[1] / 2 * factor - cube_size * self.area[1] / 2 * factor,
                self.center[1] - xy[1] * self.area[1] / 2 * factor - cube_size * self.area[1] / 2 * factor,
                cube_size * self.area[1] * factor, cube_size * self.area[1] * factor) # onlyscale based on height
        pygame.draw.rect(self.win, color, rect)

    def draw_background(self, fill, border = None):
        if border:
            self.draw_rect((0, 0), (1, 1), color = border, factor = 1)
        self.draw_rect((0, 0), (1, 1), color = fill, factor = 0.94)

class CourtCubeGenerator(RectangleGenerator):
    def new_court_gen(self, rel_center, rel_area, default_color = (255, 255, 255), factor = 1):
        new_center = self.convert_xy(rel_center)
        new_area = self.convert_area(rel_area)
        return CourtCubeGenerator(self.win, new_center, new_area, default_color, factor)

    def relative_cube_locs(self, cube_size):
        spacing = 1.2
        for pos in range(9):
            yield (-cube_size * spacing, -(pos - 3 - 0.74) * cube_size * spacing * 2)
        for pos in range(9):
            yield ( cube_size * spacing, -(pos - 3 - 0.74) * cube_size * spacing * 2)

    def draw_court_cubes(self, n, cube_size):
        cube_gen = self.relative_cube_locs(cube_size)
        for cube in range(n):
            next_cube = next(cube_gen)
            print(next_cube)
            self.draw_cube(next_cube, cube_size)


def main():
    width = 1280 - 0
    height = 720 - 100

    r = Render(width, height)
    r.update(0)



main()

pass