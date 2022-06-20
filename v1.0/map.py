import pygame
import math
from cache import Cache
from courtSection import CourtSection
from cube import Cube
from territory import Territory

class Map(pygame.sprite.Sprite):
    outer_radius = 270 # 300
    inner_radius = 270 # 300
    third_radius = 270 # 300
    ellipse_h_factor = 1
    ellipse_w_factor = 1

    def __init__(self, x, y, game_territories):

        self.x = x # center of the board
        self.y = y
        self.game_territories = game_territories # a subset of the game_state object
        self.territories = self.create_territories()
        self.selected_territory = 0

    def create_territories(self):
        territories = []
        for pos, territory in enumerate(self.game_territories):
            if (pos % 2) == 0:
                radius = Map.outer_radius
                if pos == len(self.game_territories) - 1:
                    radius = Map.third_radius
            else:
                radius = Map.inner_radius
            # assign positions around a circle
            angle = 2 * math.pi / len(self.game_territories) * pos - math.pi / 2
            terr_x = self.x + (radius * math.cos(angle)) * Map.ellipse_w_factor
            terr_y = self.y + (radius * math.sin(angle)) * Map.ellipse_h_factor
            territories.append(Territory(terr_x, terr_y, angle, 1))
        return territories

    # def update(self, territories):
#

    def draw(self, group):
        for territory in self.territories:
            territory.draw(group)
        return group

    def select_territory(self, which_terr):
        updated_rects = []
        # unhighlight the previously highlighted territory
        updated_rects.append(self.territories[self.selected_territory].un_highlight())
        # and highlight the new one
        self.selected_territory = which_terr
        updated_rects.append(self.territories[self.selected_territory].highlight())
        return updated_rects
        #TODO: make it return a rect to the two updated territories (unhighlighted and newly highlighted)

    def de_select_territory(self, which_terr):
        return self.territories[which_terr].un_highlight()

    def de_select_all(self):
        updated_rects = []
        for terr in self.territories:
            updated_rects.append(terr.un_highlight())
        return updated_rects

    # pass-through function
    def add_to_territory(self, which_terr, cube_id, color_id):
        return self.territories[which_terr].add_cube(cube_id, color_id)

    # pass-through function
    def remove_from_territory(self, which_terr, cube_id):
        return self.territories[which_terr].remove_cube(cube_id)