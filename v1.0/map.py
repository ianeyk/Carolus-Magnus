from email.headerregistry import Group
import pygame
import math
from cache import Cache
from courtSection import CourtSection
from cube import Cube
from territory import Territory
from game_state import GameState
from groups import Groups

class Map(pygame.sprite.Sprite):
    outer_radius = 270 # 300
    inner_radius = 270 # 300
    third_radius = 270 # 300
    ellipse_h_factor = 1.1
    ellipse_w_factor = 1.05

    def __init__(self, x, y, game_territories: GameState):

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
            territories.append(Territory(*self.get_xy_by_angle_index(pos), pos, self.outer_radius))
        return territories

    def get_angle_by_index(self, pos): # pos can either be an int or float
        angle = 2 * math.pi / len(self.game_territories) * pos - math.pi / 2
        return angle

    def get_xy_by_angle_index(self, pos, radius = None):
        if radius is None:
            radius = self.outer_radius
        angle = self.get_angle_by_index(pos)
        terr_x = self.x + (radius * math.cos(angle)) * Map.ellipse_w_factor
        terr_y = self.y + (radius * math.sin(angle)) * Map.ellipse_h_factor
        return (terr_x, terr_y)

    def update(self, new_territories): # : Optional[GameState] #TODO: look up correct typing for an object that can be either GameState or None
        print("map is updating game state")

        # initialize counters
        empty_terr_count = 0
        last_non_empty_idx = None

        for idx, new_terr in enumerate(new_territories):
            terr = self.territories[idx]
            if new_terr is None: # if a territory got merged
                terr.clear()
                empty_terr_count += 1
            else:
                terr.update(new_terr)

                if empty_terr_count > 0:
                    self.update_empty_spaces_left(idx, empty_terr_count)
                    if last_non_empty_idx is not None:
                        self.update_empty_spaces_right(last_non_empty_idx, empty_terr_count)

                empty_terr_count = 0
                last_non_empty_idx = idx

        # repeat the above code chunk until we find the first non-empty territory again
        for idx, (new_terr, terr) in enumerate(zip(new_territories, self.territories)):
            if new_terr is None: # if a territory got merged
                # terr.clear() # territory is already cleared
                empty_terr_count += 1
            else:
                terr.update(new_terr)

                if empty_terr_count > 0:
                    self.update_empty_spaces_left(idx, empty_terr_count)
                    if last_non_empty_idx is not None:
                        self.update_empty_spaces_right(last_non_empty_idx, empty_terr_count)

                break # break after finding the first non-empty territory for the second time

    def update_empty_spaces(self, which_terr):
        terr = self.territories[which_terr]
        displacement = terr.empty_spaces_to_my_right - terr.empty_spaces_to_my_left
        terr.outer_radius -= 5 * (terr.empty_spaces_to_my_right + terr.empty_spaces_to_my_left)
        terr.outer_angle_index = which_terr + displacement / 3
        terr.move_xy(*self.get_xy_by_angle_index(terr.outer_angle_index, terr.outer_radius))

    def update_empty_spaces_left(self, which_terr, new_left_val):
        if new_left_val > self.territories[which_terr].empty_spaces_to_my_left: # if it changed from the last time
            self.territories[which_terr].empty_spaces_to_my_left = new_left_val
            self.update_empty_spaces(which_terr)

    def update_empty_spaces_right(self, which_terr, new_right_val):
        if new_right_val > self.territories[which_terr].empty_spaces_to_my_right: # if it changed from the last time
            self.territories[which_terr].empty_spaces_to_my_right = new_right_val
            self.update_empty_spaces(which_terr)

    def draw(self, groups: Groups):
        for territory in self.territories:
            territory.draw(groups)

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