from numpy import spacing
import pygame
from random import randrange, uniform
import math

class Cube(pygame.sprite.Sprite):
    pngs = {
        0:"./sprites/green_cube1.png",
        1:"./sprites/red_cube1.png",
        2:"./sprites/blue_cube1.png",
        3:"./sprites/yellow_cube1.png",
        4:"./sprites/pink_cube1.png",
    }
    size = 17

    def __init__(self, x, y, color_id):
        pygame.sprite.Sprite.__init__(self) # Call the parent class (Sprite) constructor
        self.x = x
        self.y = y
        self.color_id = color_id

        self.png_image = pygame.image.load(Cube.pngs[color_id])
        self.image = self.get_image(Cube.size)
        self.rect = self.get_rect(Cube.size)
        # self.image = pygame.transform.smoothscale(png_image, (Cube.size, Cube.size))
        # self.rect = (x - Cube.size / 2, y - Cube.size / 2, Cube.size, Cube.size)

    def get_image(self, size):
        return pygame.transform.smoothscale(self.png_image, (math.floor(size), math.floor(size)))

    def get_rect(self, size):
        return (self.x - size / 2, self.y - size / 2, size, size)

    def highlight(self):
        self.rect = self.get_rect(Cube.size * 1.5)
        self.image = self.get_image(Cube.size * 1.5)
        return self.rect

    def un_highlight(self):
        prev_rect = self.rect
        self.rect = self.get_rect(Cube.size)
        self.image = self.get_image(Cube.size)
        return prev_rect

class CourtSection(pygame.sprite.Sprite):
    pngs = {
        0:"./sprites/green_court1.png",
        1:"./sprites/red_court1.png",
        2:"./sprites/blue_court1.png",
        3:"./sprites/yellow_court1.png",
        4:"./sprites/pink_court1.png",
    }
    cube_vertical_offset = 38
    spacing = 1.2
    size = (math.floor(2 * Cube.size * spacing + 10), math.floor(9 * Cube.size * spacing + cube_vertical_offset - 7))

    def __init__(self, x, y, color_id, num_cubes):
        pygame.sprite.Sprite.__init__(self) # Call the parent class (Sprite) constructor

        self.x = x
        self.y = y
        self.color_id = color_id
        self.num_cubes = num_cubes

        png_image = pygame.image.load(CourtSection.pngs[color_id])
        self.image = pygame.transform.smoothscale(png_image, CourtSection.size)
        self.rect = (x - CourtSection.size[0] / 2, y, *CourtSection.size)

    def draw(self, group):
        self.add(group)
        self.draw_cubes(group)

    def draw_cubes(self, group):
        locs = self.cube_locs(CourtSection.spacing)

        for loc in locs[0:self.num_cubes]:
            cube = Cube(self.x + loc[0], self.y + loc[1] + CourtSection.cube_vertical_offset, self.color_id)
            cube.add(group)

    def cube_locs(self, spacing = 1.2):
        locs = []
        for pos in range(9):
            locs.append((-Cube.size / 2 * spacing, pos * Cube.size * spacing))
        for pos in range(9):
            locs.append(( Cube.size / 2 * spacing, pos * Cube.size * spacing))
        return locs

class Cache():

    spacing = 1.5

    def __init__(self, x, y, size, cache_list):
        self.x = x
        self.y = y
        self.cache_list = cache_list # list of 7 color_ids
        self.size = size
        self.cube_list = [] # list of cube objects for highlighting purposes

        locs = self.cube_locs(7, Cache.spacing)

        for loc, color_id in zip(locs, self.cache_list):
            cube = Cube(self.x + loc[0], self.y + loc[1], color_id)
            self.cube_list.append(cube)

    def draw_cubes(self, group):
        for cube in self.cube_list:
            cube.add(group)

    def cube_locs(self, nCubes, spacing = 1.5):
        # jitter_range = (-0.4, 0.2)
        locs = []
        for pos in range(nCubes):
            locs.append(((pos - nCubes // 2) * Cube.size * spacing, Cube.size / 2))
            # locs.append(((pos - nCubes // 2) * Cube.size * spacing + uniform(*jitter_range) * Cube.size, Cube.size / 2 + uniform(*jitter_range) * Cube.size))
        return locs

    def select_cube(self, which_cube): # which_cube is an index from 0 to 6, indicating which cube in the cache has been selected
        updated_rects = self.deselect_all() # unhighlight all cubes
        print(self.cube_list[which_cube])
        updated_rect = self.cube_list[which_cube].highlight() # then highlight the interesting cube
        updated_rects.append(updated_rect)
        return updated_rects # returns the rect containing the highlighted cube, for pygame.display.update() in the main loop

    def deselect_all(self):
        updated_rects = []
        for other_cube in self.cube_list:
            updated_rect = other_cube.un_highlight()
            updated_rects.append(updated_rect)
        return updated_rects

class PlayerArea(pygame.sprite.Sprite):
    """Draws a complete Player Area, including the court and the cache."""
    pngs = {
        0: "./sprites/court_outline_white.png",
        1: "./sprites/court_outline_black.png",
        2: "./sprites/court_outline_gray.png"
    }
    size = (math.floor(CourtSection.size[0] * 5 * CourtSection.spacing - 10), math.floor(CourtSection.size[1] * 1.3 + 10))
    small_offset_from_edges = 18
    large_offset_from_edges = 24

    def __init__(self, x, y, team, cube_counts, cache_list):
        pygame.sprite.Sprite.__init__(self) # Call the parent class (Sprite) constructor

        self.x = x
        self.y = y
        self.team = team
        self.cube_counts = cube_counts
        self.cache_list = cache_list
        self.cache = Cache(x, y - PlayerArea.size[1] / 2 + PlayerArea.large_offset_from_edges, PlayerArea.size, cache_list)

        png_image = pygame.image.load(PlayerArea.pngs[team])
        self.image = pygame.transform.smoothscale(png_image, PlayerArea.size)
        self.rect = (x - PlayerArea.size[0] / 2, y - PlayerArea.size[1] / 2, *PlayerArea.size)

    def draw(self):
        if len(self.groups()) > 0:
            group = self.groups()[0]
        else:
            group = pygame.sprite.Group()
            self.add(group)
        self.draw_court(group)
        self.cache.draw_cubes(group)
        return group

    def draw_court(self, group):
        section_spacing = 1.1
        for color_id, cube_count in enumerate(self.cube_counts):
            section_x = self.x + (color_id - 2) * CourtSection.size[0] * section_spacing
            section_y = self.y + PlayerArea.size[1] / 2 - CourtSection.size[1] - PlayerArea.small_offset_from_edges
            court_section = CourtSection(section_x, section_y, color_id, cube_count)
            court_section.draw(group)
        return group

class Render(pygame.sprite.Sprite):

    def __init__(self, width, height, game_state):
        pygame.sprite.Sprite.__init__(self) # Call the parent class (Sprite) constructor

        self.width = width
        self.height = height
        self.game_state = game_state

        # initialize the display
        pygame.display.init()
        # screen = pygame.Surface((width, height))
        self.display = pygame.display.set_mode((width, height))

        png_image = pygame.image.load("./sprites/background1.png")
        self.image = pygame.transform.smoothscale(png_image, (width, height))
        self.rect = (0, 0, *PlayerArea.size)

        # initialize player boards
        p0_center = (self.width * 1 / 8, self.height * 1 / 4)
        p1_center = (self.width * 1 / 8, self.height * 3 / 4)
        p2_center = (self.width * 7 / 8, self.height * 1 / 4)
        p3_center = (self.width * 7 / 8, self.height * 3 / 4)

        self.players = []
        for player_number, center in enumerate([p0_center, p1_center, p2_center, p3_center]):
            team = player_number % 2
            cube_counts = [randrange(0, 18) for i in range(5)]
            cache_list = sorted([randrange(0, 4) for i in range(7)])
            self.players.append(PlayerArea(*center, team, cube_counts, cache_list))


    def draw(self):
        self.display.fill((255, 255, 255))
        background_group = pygame.sprite.Group()
        self.add(background_group)
        background_group.draw(self.display)
        for player in self.players:
            court_group = player.draw()
            court_group.draw(self.display)

# def main():
#     width = 1280
#     height = 720
#     r = Render(width, height, 0)
#     r.players[0].cache.select_cube(2)
#     r.draw()
#     pygame.display.flip()

# main()

pass