import pygame
from enum import Enum
from playerArea import PlayerArea
from map import Map

class Player():
    # Enum for tracking what region the current cube is in on the board
    class CubeRegion(Enum):
        CACHE = 0
        COURT = 1
        TERRITORY = 2
        TERRITORY_HOLDING = 2

    # Enum for tracking whether the arrow keys are being used for selecting cubes from the Cache or Territories on the map
    class SelectionType(Enum):
        CUBES = 0
        TERRITORIES = 1

    def __init__(self, player_render: PlayerArea, player_map: Map) -> None:
        self.game_state = 0 #TODO: get game_state
        self.selected_territory = 0
        self.map = player_map
        self.n_territories = len(self.map.territories)

        self.selection_mode = Player.SelectionType.CUBES
        self.selected_cube = 0
        self.player_render = player_render
        self.cache_list = self.player_render.cache_list
        self.cache_size = len(self.cache_list)
        self.terr_list = [None] * self.cache_size
        self.cube_placements = [Player.CubeRegion.CACHE for i in range(self.cache_size)] # all cubes start in the Cache
        self.search_mode = Player.CubeRegion.CACHE # used in self.right_cube()

    def select(self, event:pygame.event.Event):
        action_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        if event.type != pygame.KEYDOWN or event.key not in action_keys:
            return None

        if self.selection_mode == Player.SelectionType.CUBES:
            return self.select_cube(event)
        # else:
        return self.select_territory(event)

    def select_territory(self, event:pygame.event.Event): # -> tuple[pygame.sprite.Group, list[any]]:
        updated_rects = None

        if event.key == pygame.K_LEFT:
            self.selected_territory = (self.selected_territory - 1) % self.n_territories
            updated_rects = self.map.select_territory(self.selected_territory)

        elif event.key == pygame.K_RIGHT:
            self.selected_territory = (self.selected_territory + 1) % self.n_territories
            updated_rects = self.map.select_territory(self.selected_territory)

        elif event.key == pygame.K_UP:
            if self.cube_placements[self.selected_cube] == Player.CubeRegion.TERRITORY_HOLDING:
                self.cube_placements[self.selected_cube] = Player.CubeRegion.CACHE
                self.selection_mode = Player.SelectionType.CUBES
                self.map.de_select_territory(self.selected_territory)
                # self.selected_cube = self.right_cube(-1) # reset to the first cube in the cache
                self.return_to_cache()
                updated_rects = self.player_render.select_cube(self.selected_cube)

        elif event.key == pygame.K_DOWN:
            if self.cube_placements[self.selected_cube] == Player.CubeRegion.TERRITORY_HOLDING:
                self.cube_placements[self.selected_cube] = Player.CubeRegion.TERRITORY
                updated_rects = self.add_to_territory()
                self.selection_mode = Player.SelectionType.CUBES
                self.map.de_select_territory(self.selected_territory)
                self.selected_cube = self.right_cube(-1) # reset to the first cube in the cache
                if self.cube_placements[self.selected_cube] == Player.CubeRegion.TERRITORY:
                    self.selected_territory = self.terr_list[self.selected_cube]
                updated_rects = self.player_render.select_cube(self.selected_cube)

        return updated_rects # returns a group

    def add_to_territory(self):
        new_xy = self.map.add_to_territory(self.selected_territory, self.selected_cube, self.player_render.cache_list[self.selected_cube])
        updated_rects = self.move_selected_cube_to(new_xy)
        updated_rects.extend(self.player_render.select_cube(self.selected_cube))
        self.terr_list[self.selected_cube] = self.selected_territory
        return updated_rects

    def remove_from_territory(self):
        self.map.remove_from_territory(self.terr_list[self.selected_cube], self.selected_cube) # (self.selected_territory, self.selected_cube)
        self.terr_list[self.selected_cube] = None
        return self.move_to_holding()

    def return_to_cache(self):
        new_xy = self.player_render.cache.coords_of_cube(self.player_render.cache.cube_locs()[self.selected_cube])
        updated_rects = self.move_selected_cube_to(new_xy)
        updated_rects.extend(self.player_render.select_cube(self.selected_cube))
        self.terr_list[self.selected_cube] = None
        return updated_rects

    def move_selected_cube_to(self, new_xy):
        """Helper function to update the position of a selected cube, returning the rects at the old and new locations."""
        return self.player_render.cache.cube_list[self.selected_cube].update_pos(new_xy)

    def select_cube(self, event:pygame.event.Event): # -> tuple[pygame.sprite.Group, list[any]]:
        updated_rects = None

        if event.key == pygame.K_LEFT:
            # bolt on a thing that says to go to the next cube of a different color
            self.selected_cube = self.left_cube(self.cache_list[self.selected_cube])
            updated_rects = self.player_render.select_cube(self.selected_cube)

        elif event.key == pygame.K_RIGHT:
            self.selected_cube = self.right_cube(self.cache_list[self.selected_cube])
            updated_rects = self.player_render.select_cube(self.selected_cube)

        elif event.key == pygame.K_UP:
            if self.cube_placements[self.selected_cube] == Player.CubeRegion.COURT:
                self.cube_placements[self.selected_cube] = Player.CubeRegion.CACHE
                updated_rects = self.player_render.remove_from_court(self.selected_cube)
            elif self.cube_placements[self.selected_cube] == Player.CubeRegion.CACHE:
                self.cube_placements[self.selected_cube] = Player.CubeRegion.TERRITORY_HOLDING
                updated_rects = self.move_to_holding()
                updated_rects.extend(self.map.select_territory(self.selected_territory))
            elif self.cube_placements[self.selected_cube] == Player.CubeRegion.TERRITORY:
                self.cube_placements[self.selected_cube] = Player.CubeRegion.TERRITORY_HOLDING
                updated_rects = self.remove_from_territory()
                updated_rects.extend(self.map.select_territory(self.selected_territory))


        elif event.key == pygame.K_DOWN:
            if self.cube_placements[self.selected_cube] == Player.CubeRegion.CACHE:
                self.cube_placements[self.selected_cube] = Player.CubeRegion.COURT
                updated_rects = self.player_render.add_to_court(self.selected_cube)

        return updated_rects

    def move_to_holding(self):
        """Moves the currently selected cube to the holding location, which means the cube is being primed to be placed on a territory.
        A cube is moved to the holding position when it is selected to do so from the Cache (up arrow while selected in cache) or when
        it is removed from a territory (up arrow while on territory). While in holding, the selection mode is always TERRITORIES.
        While in holding, if the down arrow is pressed, it places the cube on the currently selected territory.
        While in holding, if the up arrow is pressed again, it returns the cube to the cache.
        """
        self.selection_mode = Player.SelectionType.TERRITORIES

        new_xy = self.player_render.territory_holding_location # predefined location of the cube in holding
        updated_rects = self.move_selected_cube_to(new_xy)
        updated_rects.extend(self.player_render.select_cube(self.selected_cube))
        return updated_rects

    def get_order_of_selection(self):
        # temp_selected_cube = self.selected_cube
        temp_selected_cube = 0
        selection_order = [temp_selected_cube]
        for i in range(self.cache_size): # could be a while loop but runs a maximum of 7 times
            temp_selected_cube = self._right_cube(temp_selected_cube, self.cache_list[temp_selected_cube])
            if temp_selected_cube in selection_order:
                break
            # else:
            selection_order.append(temp_selected_cube) # do not add it on the last round; it is now a cycle that works with %
        return selection_order

    def right_cube(self, temp = 0):
        selection_order = self.get_order_of_selection()
        temp_selected_cube = self.selected_cube
        for i in range(self.cache_size):
            if temp_selected_cube in selection_order:
                order_idx = selection_order.index(temp_selected_cube)
                break
            # else:
            temp_selected_cube = (temp_selected_cube + 1) % len(selection_order)
        return selection_order[(order_idx + 1) % len(selection_order)]
        # return selection_order[1]

    def left_cube(self, temp = 0):
        selection_order = self.get_order_of_selection()
        temp_selected_cube = self.selected_cube
        for i in range(self.cache_size):
            if temp_selected_cube in selection_order:
                order_idx = selection_order.index(temp_selected_cube)
                break
            # else:
            temp_selected_cube = (temp_selected_cube - 1) % len(selection_order)
        return selection_order[(order_idx - 1) % len(selection_order)]
        # return selection_order[-1]

    # underscored because it hides the inner workings
    def _right_cube(self, temp_selected_cube, prev_color_id = None):
        prev_terr_id = self.terr_list[temp_selected_cube]
        if not prev_color_id:
            prev_color_id = self.cache_list[temp_selected_cube]
        # then check the court
        if self.search_mode == Player.CubeRegion.COURT:
            range_to_search = range(temp_selected_cube, 0, -1)
        else:
            range_to_search = range(temp_selected_cube, len(self.cache_list), 1)
        for idx in range_to_search:
            if (self.cache_list[idx] != prev_color_id or self.terr_list[idx] != prev_terr_id) and \
            self.cube_placements[idx] == self.search_mode:
                return idx

        temp_selected_cube = self.right_search_mode()
        # temp_selected_cube = 0
        return self._right_cube(temp_selected_cube, -1) # recursion!!!

    def right_search_mode(self):
        if self.search_mode == Player.CubeRegion.CACHE:
            self.search_mode = Player.CubeRegion.COURT
            return self.cache_size - 1
        elif self.search_mode == Player.CubeRegion.COURT:
            self.search_mode = Player.CubeRegion.TERRITORY
            return 0
        elif self.search_mode == Player.CubeRegion.TERRITORY:
            self.search_mode = Player.CubeRegion.CACHE
            return 0
            #TODO: if placement limit has been reached, don't let search_mode go back to cache

    # def _left_cube(self, prev_color_id):
    #     for idx in list(range(0, self.selected_cube))[::-1]:
    #         if self.cache_list[idx] != prev_color_id and self.cube_placements[idx] == self.search_mode:
    #             return idx

    #     self.left_search_mode()
    #     self.selected_cube = len(self.cache_list)
    #     return self._left_cube(-1)

    # def left_search_mode(self):
    #     if self.search_mode == Player.CubeRegion.CACHE:
    #         self.search_mode = Player.CubeRegion.TERRITORY
    #     elif self.search_mode == Player.CubeRegion.TERRITORY:
    #         self.search_mode = Player.CubeRegion.COURT
    #     elif self.search_mode == Player.CubeRegion.COURT:
    #         self.search_mode = Player.CubeRegion.CACHE
    #         #TODO: if placement limit has been reached, don't let search_mode go back to cache