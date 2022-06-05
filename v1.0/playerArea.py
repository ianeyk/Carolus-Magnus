import pygame
import math
from cache import Cache
from courtSection import CourtSection

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

        self.court_sections = []
        section_spacing = 1.1
        for color_id, cube_count in enumerate(self.cube_counts):
            section_x = self.x + (color_id - 2) * CourtSection.size[0] * section_spacing
            section_y = self.y + PlayerArea.size[1] / 2 - CourtSection.size[1] - PlayerArea.small_offset_from_edges
            self.court_sections.append(CourtSection(section_x, section_y, color_id, cube_count))

    def draw(self, group = None):
        if not group:
            if len(self.groups()) > 0:
                group = self.groups()[0]
            else:
                group = pygame.sprite.Group()
        self.add(group)
        self.draw_court(group)
        self.cache.draw_cubes(group)
        return group

    def draw_court(self, group):
        for court_section in self.court_sections:
            court_section.draw(group)
        return group

    def select_cube(self, which_cube):
        return self.cache.select_cube(which_cube)

    def add_to_court(self, which_cube):
        color_id = self.cache_list[which_cube] # color id of the selected cube
        court_section = self.court_sections[color_id]
        new_xy = court_section.coords_of_cube(court_section.cube_locs()[court_section.num_cubes])
        court_section.num_cubes += 1
        updated_rects = self.cache.cube_list[which_cube].update_pos(new_xy)
        updated_rects.extend(self.select_cube(which_cube))
        return updated_rects
        # return self.select_cube(which_cube)
        # return court_section.rect