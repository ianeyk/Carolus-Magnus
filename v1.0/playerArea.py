import pygame
import math
from cache import Cache
from courtSection import CourtSection
from token_set import TokenSet

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
        self.territory_holding_location = (x, y - PlayerArea.size[1] / 2 - PlayerArea.large_offset_from_edges)

        png_image = pygame.image.load(PlayerArea.pngs[team])
        self.image = pygame.transform.smoothscale(png_image, PlayerArea.size)
        self.rect = (x - PlayerArea.size[0] / 2, y - PlayerArea.size[1] / 2, *PlayerArea.size)

        self.token_set = TokenSet(self.team, x, y + PlayerArea.size[1] / 2 + PlayerArea.small_offset_from_edges, PlayerArea.size, list(range(5)))
        # self.token_set = TokenSet(self.team, 100, 100, PlayerArea.size, list(range(1, 5)))

        self.court_sections = []
        section_spacing = 1.1
        for color_id, cube_count in enumerate(self.cube_counts):
            section_x = self.x + (color_id - 2) * CourtSection.size[0] * section_spacing
            section_y = self.y + PlayerArea.size[1] / 2 - CourtSection.size[1] - PlayerArea.small_offset_from_edges
            self.court_sections.append(CourtSection(section_x, section_y, color_id, cube_count))

    def update(self, game_player):
        # update court
        self.cube_counts = game_player.court.get_cubes()
        for color_id, cube_count in enumerate(self.cube_counts):
            self.court_sections[color_id].update(cube_count)

        # update cache
        self.cache_list = game_player.cache.get_cubes()
        self.cache.update(self.cache_list)

    def draw(self, group):
        self.add(group)
        self.draw_court(group)
        self.cache.draw_cubes(group)
        self.token_set.draw(group)

    def draw_court(self, group):
        for court_section in self.court_sections:
            court_section.draw(group)

    def select_cube(self, which_cube):
        return self.cache.select_cube(which_cube)

    def select_token(self, which_token):
        return self.token_set.select(which_token)

    def add_to_court(self, which_cube):
        color_id = self.cache_list[which_cube] # color id of the selected cube
        court_section = self.court_sections[color_id]
        new_xy = court_section.coords_of_cube(court_section.cube_locs()[court_section.num_cubes])
        court_section.num_cubes += 1
        updated_rects = self.cache.cube_list[which_cube].update_pos(new_xy)
        updated_rects.extend(self.select_cube(which_cube))
        return updated_rects

    def remove_from_court(self, which_cube):
        color_id = self.cache_list[which_cube] # color id of the selected cube
        court_section = self.court_sections[color_id]
        new_xy = self.cache.cube_locs[which_cube]
        court_section.num_cubes -= 1
        updated_rects = self.cache.cube_list[which_cube].update_pos(new_xy)
        updated_rects.extend(self.select_cube(which_cube))
        return updated_rects