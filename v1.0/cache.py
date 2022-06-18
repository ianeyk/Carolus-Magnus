import pygame
from cube import Cube

class Cache():

    spacing = 1.5

    def __init__(self, x, y, size, cache_list):
        self.x = x
        self.y = y
        self.cache_list = cache_list # list of 7 color_ids
        self.nCubes = len(self.cache_list)
        self.size = size

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
        updated_rects = self.deselect_all() # unhighlight all cubes
        updated_rects.extend(self.cube_list[which_cube].highlight()) # then highlight the interesting cube
        return updated_rects # returns the rect containing the highlighted cube, for pygame.display.update() in the main loop

    def deselect_all(self):
        updated_rects = []
        for other_cube in self.cube_list:
            updated_rect = other_cube.un_highlight()
            updated_rects.extend(updated_rect)
        return updated_rects