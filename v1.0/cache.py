import pygame
from cube import CacheCube, Cube

class Cache():

    spacing = 1.5

    def __init__(self, x, y, size, cache_list):
        self.x = x
        self.y = y
        self.cache_list = cache_list # list of 7 color_ids
        self.size = size
        self.prev_selected_cube = 0
        self.generate_cubes()

    def update(self, cache_list):
        self.clear_cubes()
        self.cache_list = cache_list
        self.generate_cubes()

    def generate_cubes(self):
        self.nCubes = len(self.cache_list)
        self.cube_locs = self.generate_cube_locs()
        self.cube_list = [] # list of cube objects for highlighting purposes
        for loc, color_id in zip(self.cube_locs, self.cache_list):
            cube = CacheCube(*loc, color_id)
            self.cube_list.append(cube)

    def draw_cubes(self, group):
        for cube in self.cube_list:
            cube.add(group)

    def clear_cubes(self):
        for cube in self.cube_list:
            cube.kill()

    def generate_cube_locs(self):
        # jitter_range = (-0.4, 0.2)
        locs = []
        for pos in range(self.nCubes):
            locs.append((self.x + (pos - self.nCubes // 2) * Cube.size[0] * Cache.spacing, self.y + Cube.size[1] / 2))
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