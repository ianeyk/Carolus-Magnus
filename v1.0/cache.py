import pygame
from cube import Cube
from enum import Enum


class Cache():
    class Placement(Enum):
        CACHE = 0
        COURT = 1
        TERRITORY = 2

    spacing = 1.5

    def __init__(self, x, y, size, cache_list):
        self.x = x
        self.y = y
        self.cache_list = cache_list # list of 7 color_ids
        self.size = size
        self.cube_list = [] # list of cube objects for highlighting purposes
        self.cube_placements = []


        locs = self.cube_locs(7, Cache.spacing)

        for loc, color_id in zip(locs, self.cache_list):
            cube = Cube(self.x + loc[0], self.y + loc[1], color_id)
            self.cube_list.append(cube)
            self.cube_placements.append(Cache.Placement.CACHE)

    def draw_cubes(self, group = None):
        if not group:
            if len(self.cube_list[0].groups()) > 0:
                group = self.cube_list[0].groups()[0]
            else:
                group = pygame.sprite.Group()
        # if not group:
        #     group = pygame.sprite.Group()
        for cube in self.cube_list:
            cube.add(group)
        return group

    def cube_locs(self, nCubes, spacing = 1.5):
        # jitter_range = (-0.4, 0.2)
        locs = []
        for pos in range(nCubes):
            locs.append(((pos - nCubes // 2) * Cube.size * spacing, Cube.size / 2))
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