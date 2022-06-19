import pygame
from cube import Cube

class Token(Cube):
    white_pngs = {
        0:"./sprites/tokens/white_token01.png",
        1:"./sprites/tokens/white_token02.png",
        2:"./sprites/tokens/white_token03.png",
        3:"./sprites/tokens/white_token04.png",
        4:"./sprites/tokens/white_token05.png",
    }
    black_pngs = {
        0:"./sprites/tokens/black_token01.png",
        1:"./sprites/tokens/black_token02.png",
        2:"./sprites/tokens/black_token03.png",
        3:"./sprites/tokens/black_token04.png",
        4:"./sprites/tokens/black_token05.png",
    }
    grey_pngs = {
        0:"./sprites/tokens/grey_token01.png",
        1:"./sprites/tokens/grey_token02.png",
        2:"./sprites/tokens/grey_token03.png",
        3:"./sprites/tokens/grey_token04.png",
        4:"./sprites/tokens/grey_token05.png",
    }
    size = 30
    highlight_scale_factor = 1.5

class TokenSet(): # Turn Token

    spacing = 1.5

    def __init__(self, x, y, size, cache_list):
        self.x = x
        self.y = y
        self.cache_list = cache_list # list of 7 color_ids
        self.nCubes = len(self.cache_list)
        self.size = size
        self.prev_selected_cube = 0

        self.cube_locs = self.generate_cube_locs()
        self.cube_list = [] # list of cube objects for highlighting purposes
        for loc, color_id in zip(self.cube_locs, self.cache_list):
            cube = Cube(*loc, color_id, png_path = Cube.cache_pngs[color_id])
            self.cube_list.append(cube)
            #TODO: give each cube that is generated as part of the cache a slightly different PNG (highlighted or such)

    def draw_cubes(self, group):
        for cube in self.cube_list:
            cube.add(group)

    def generate_cube_locs(self):
        # jitter_range = (-0.4, 0.2)
        locs = []
        for pos in range(self.nCubes):
            locs.append((self.x + (pos - self.nCubes // 2) * Cube.size * Cache.spacing, self.y + Cube.size / 2))
            # locs.append(((pos - nCubes // 2) * Cube.size * spacing + uniform(*jitter_range) * Cube.size, Cube.size / 2 + uniform(*jitter_range) * Cube.size))
        return locs

    def select_cube(self, which_cube): # which_cube is an index from 0 to 6, indicating which cube in the cache has been selected
        # updated_rects = self.deselect_all() # unhighlight all cubes
        updated_rects = self.cube_list[self.prev_selected_cube].un_highlight() # unhighlight the previous cube
        updated_rects.extend(self.cube_list[which_cube].highlight()) # then highlight the interesting cube
        self.prev_selected_cube = which_cube
        return updated_rects # returns the rect containing the highlighted cube, for pygame.display.update() in the main loop

    def deselect_all(self):
        updated_rects = []
        for other_cube in self.cube_list:
            updated_rects.extend(other_cube.un_highlight())
        return updated_rects