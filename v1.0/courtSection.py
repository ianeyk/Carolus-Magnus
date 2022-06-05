import pygame
import math
from cube import Cube

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

        self.cube_list = []
        locs = self.cube_locs(CourtSection.spacing)

        for loc in locs[0:self.num_cubes]:
            self.cube_list.append(Cube(*self.coords_of_cube(loc), self.color_id))

    def coords_of_cube(self, loc):
        return (self.x + loc[0], self.y + loc[1] + CourtSection.cube_vertical_offset)

    def draw(self, group):
        self.add(group)
        self.draw_cubes(group)

    def draw_cubes(self, group):
        for cube in self.cube_list:
            cube.add(group)

    def cube_locs(self, spacing = 1.2):
        locs = []
        for pos in range(9):
            locs.append((-Cube.size / 2 * spacing, pos * Cube.size * spacing))
        for pos in range(9):
            locs.append(( Cube.size / 2 * spacing, pos * Cube.size * spacing))
        return locs
