from numpy import spacing
import pygame
from random import randrange, uniform

class Cube(pygame.sprite.Sprite):
    pngs = {
        0:"./sprites/green_cube1.png",
        1:"./sprites/red_cube1.png",
        2:"./sprites/blue_cube1.png",
        3:"./sprites/yellow_cube1.png",
        4:"./sprites/pink_cube1.png",
    }
    size = 20

    def __init__(self, x, y, color_id):
        pygame.sprite.Sprite.__init__(self) # Call the parent class (Sprite) constructor

        png_image = pygame.image.load(Cube.pngs[color_id])
        self.image = pygame.transform.smoothscale(png_image, (Cube.size, Cube.size))
        self.rect = (x - Cube.size / 2, y - Cube.size / 2, Cube.size, Cube.size)

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
    size = (2 * Cube.size * spacing + 10, 9 * Cube.size * spacing + cube_vertical_offset - 7)

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

    def __init__(self, x, y, size, cube_list):
        self.x = x
        self.y = y
        self.cube_list = cube_list
        self.size = size

    def draw_cubes(self, group):
        locs = self.cube_locs(7, Cache.spacing)

        for loc, color_id in zip(locs, self.cube_list):
            cube = Cube(self.x + loc[0], self.y + loc[1], color_id)
            cube.add(group)

    def cube_locs(self, nCubes, spacing = 1.5):
        # jitter_range = (-0.4, 0.2)
        locs = []
        for pos in range(nCubes):
            locs.append(((pos - nCubes // 2) * Cube.size * spacing, Cube.size / 2))
            # locs.append(((pos - nCubes // 2) * Cube.size * spacing + uniform(*jitter_range) * Cube.size, Cube.size / 2 + uniform(*jitter_range) * Cube.size))
        return locs

class Court(pygame.sprite.Sprite):
    pngs = {
        0: "./sprites/court_outline_white.png",
        1: "./sprites/court_outline_black.png",
        2: "./sprites/court_outline_gray.png"
    }
    size = (CourtSection.size[0] * 5 * CourtSection.spacing - 10, CourtSection.size[1] * 1.3 + 10)
    small_offset_from_edges = 18
    large_offset_from_edges = 24

    def __init__(self, x, y, team, cube_counts, cache_list):
        pygame.sprite.Sprite.__init__(self) # Call the parent class (Sprite) constructor

        self.x = x
        self.y = y
        self.team = team
        self.cube_counts = cube_counts
        self.cache_list = cache_list
        self.cache = Cache(x, y - Court.size[1] / 2 + Court.large_offset_from_edges, Court.size, cache_list)

        png_image = pygame.image.load(Court.pngs[team])
        self.image = pygame.transform.smoothscale(png_image, Court.size)
        print(Court.size)
        self.rect = (x - Court.size[0] / 2, y - Court.size[1] / 2, *Court.size)

    def draw(self):
        group = pygame.sprite.Group()
        self.add(group)
        self.draw_court(group)
        self.cache.draw_cubes(group)
        return group

    def draw_court(self, group):
        section_spacing = 1.1
        for color_id, cube_count in enumerate(self.cube_counts):
            section_x = self.x + (color_id - 2) * CourtSection.size[0] * section_spacing
            section_y = self.y + Court.size[1] / 2 - CourtSection.size[1] - Court.small_offset_from_edges
            court_section = CourtSection(section_x, section_y, color_id, cube_count)
            court_section.draw(group)
        return group

def main():
    width = 1280
    height = 720
    pygame.display.init()
    screen = pygame.Surface((width, height))
    # screen.init()
    d = pygame.display.set_mode((width, height))

    cube = Cube(1000, 150, 0)
    g = pygame.sprite.Group()
    cube.add(g)
    cube_counts = [randrange(0, 18) for color_id in range(5)]
    court = Court(250, 360, 0, cube_counts, [1, 2, 0, 0, 1, 4, 3])
    g2 = court.draw()
    g2.draw(d)
    g.draw(d)


    pygame.display.flip()

main()

pass