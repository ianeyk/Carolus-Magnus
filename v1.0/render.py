import pygame
from game import Game
from random import randrange, uniform

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
        player_area = (self.width / 4 * player_area_border, self.height / 2 * player_area_border)
        p0_center = (self.width * 1 / 8, self.height * 1 / 4)
        p1_center = (self.width * 1 / 8, self.height * 3 / 4)
        p2_center = (self.width * 7 / 8, self.height * 1 / 4)
        p3_center = (self.width * 7 / 8, self.height * 3 / 4)

        self.players = []
        for player_number, center in enumerate([p0_center, p1_center, p2_center, p3_center]):
            team = player_number % 2
            self.players.append(PlayerRender(self.win, center, player_area, team, player_number))

        # board area
        self.board_area = (self.width / 3, self.height / 3)
        self.board_center = (self.width / 2, self.height / 2)

        self.cube_width = 20
        self.cube_height = 20

    def update(self, game_state):
        self.game_state = game_state

        self.win.fill((225, 225, 200)) # background color
        for player in self.players:
            player.draw_player(self.game_state)
        self.draw_board()

        pygame.display.update()

    def draw_board(self):
        pass

class PlayerRender():
    def __init__(self, win, center, area, team, player_number):
        self.win = win
        self.center = center
        self.area = area
        self.team = team
        self.player_number = player_number

        self.active_cube_locs = []

    def parse_game_state(self, game_state):
        court_cubes = game_state.players[self.player_number].court.get_cubes()
        cache_cubes = game_state.players[self.player_number].cache.get_cubes()
        return court_cubes, cache_cubes

    def draw_player(self, game_state):
        # court_cubes, cache_cubes = self.parse_game_state(game_state)

        cube_size = 0.08
        def draw_court(court_cubes):
            gen_1 = CourtCubeGenerator(self.win, self.center, self.area, default_color=Render.pink)
            court_locs = []
            for color_id in range(5):
                court_gen = gen_1.new(CourtCubeGenerator, ((color_id - 2) / 2.4, 0.2), (1/5.2, 0.8), Render.cube_colors[color_id])
                # court_gen = gen_1.new_court_gen(((color_id - 2) / 2.4, 0.2), (1/5.2, 0.8), Render.cube_colors[color_id])
                court_gen.draw_background(fill = (140, 140, 140), border = (120, 120, 120))
                court_gen.draw_rect((0, 0.88), (0.8, 0.03))
                court_locs.append(court_gen.draw_court_cubes(court_cubes[color_id], cube_size))

        def draw_cache(cache_cubes):
            cache_gen = CacheCubeGenerator(self.win, self.center, self.area)
            return cache_gen.draw_cache_cubes(cache_cubes, cube_size)


        # court_cubes = self.game_state.players[player_num].court.get_cubes()
        court_cubes = []
        for color_id in range(5):
            court_cubes.append(randrange(0, 18))
        self.court_locs = draw_court(court_cubes)

        cache_color_ids = [randrange(0, 4) for cube in range(7)]
        sorted_cache_color_ids = sorted(cache_color_ids)

        cache_cubes = [Render.cube_colors[color_id] for color_id in sorted_cache_color_ids]
        self.cache_locs = draw_cache(cache_cubes)

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

    def new(self, sub_class, rel_center, rel_area, default_color = (255, 255, 255), factor = 1):
        new_center = self.convert_xy(rel_center)
        new_area = self.convert_area(rel_area)
        return sub_class(self.win, new_center, new_area, default_color, factor)

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

class CubeGenerator(RectangleGenerator):
    def relative_cube_locs(self):
        pass

    def draw_court_cubes(self, n, cube_size):
        pass

class CourtCubeGenerator(CubeGenerator):
    def relative_cube_locs(self, cube_size):
        spacing = 1.2
        for pos in range(9):
            yield (-cube_size * spacing, -(pos - 3 - 0.74) * cube_size * spacing * 2)
        for pos in range(9):
            yield ( cube_size * spacing, -(pos - 3 - 0.74) * cube_size * spacing * 2)

    def draw_court_cubes(self, n, cube_size):
        cube_gen = list(self.relative_cube_locs(cube_size))
        for cube in range(n):
            next_cube = next(cube_gen)
            print(next_cube)
            self.draw_cube(next_cube, cube_size)
        return cube_gen[n:n + 4] # return the next four cube positions in case someone decides to add four cubes to the court

class CacheCubeGenerator(CubeGenerator):
    def relative_cube_locs(self, n): # colors is a list of length 7 or 9
        offset_range = 0.04
        for pos in range(n):
            yield ((pos - n // 2) / n * 2 * 0.92 + uniform(-offset_range, offset_range),
                                             0.8 + uniform(-offset_range, offset_range))

    def draw_cache_cubes(self, colors, cube_size):
        cube_gen = list(self.relative_cube_locs(len(colors)))
        for color in colors:
            next_cube = next(cube_gen)
            print(next_cube)
            self.draw_cube(next_cube, cube_size, color = color)
        return cube_gen # return the locations of all the cache cubes

def main():
    width = 1280 - 0
    height = 720 - 100

    r = Render(width, height)
    r.update(0)



main()

pass