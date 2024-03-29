import pygame
import math
from cube import Cube
from marker_sprite import Crown
from groups import Groups
from copy import copy

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
    size = (math.floor(2 * Cube.size[0] * spacing + 10), math.floor(9 * Cube.size[1] * spacing + cube_vertical_offset - 7))

    def __init__(self, x, y, color_id, num_cubes):
        pygame.sprite.Sprite.__init__(self) # Call the parent class (Sprite) constructor

        self.x = x
        self.y = y
        self.color_id = color_id
        self.num_cubes = num_cubes
        self.prev_cube_count = copy(self.num_cubes)

        self.crown_coords = (self.x, self.y)
        self.crown = Crown(self.crown_coords, 40, height_factor = 0.7, png_id = self.color_id, visible = False)

        png_image = pygame.image.load(CourtSection.pngs[color_id])
        self.image = pygame.transform.smoothscale(png_image, CourtSection.size)
        self.rect = (x - CourtSection.size[0] / 2, y, *CourtSection.size)
        self.locs = self.cube_locs(CourtSection.spacing)

        self.cube_list = []
        for loc in self.locs[0:self.num_cubes]:
            self.cube_list.append(Cube(*self.coords_of_cube(loc), self.color_id))

    def update(self, cube_count):
        for loc in self.locs[self.prev_cube_count:cube_count]:
            self.cube_list.append(Cube(*self.coords_of_cube(loc), self.color_id))
        self.num_cubes = cube_count
        self.prev_cube_count = cube_count

    def coords_of_cube(self, loc):
        return (self.x + loc[0], self.y + loc[1] + CourtSection.cube_vertical_offset)

    def draw(self, groups: Groups):
        self.add(groups.court_section_group)
        self.draw_cubes(groups.cubes_group)
        self.crown.draw(groups.crown_group)

    def draw_cubes(self, group):
        for cube in self.cube_list:
            cube.add(group)

    def cube_locs(self, spacing = 1.2):
        locs = []
        for pos in range(9):
            locs.append((-Cube.size[0] / 2 * spacing, pos * Cube.size[1] * spacing))
        for pos in range(9):
            locs.append(( Cube.size[0] / 2 * spacing, pos * Cube.size[1] * spacing))
        return locs

    def show_crown(self, val):
        self.crown.visible = val