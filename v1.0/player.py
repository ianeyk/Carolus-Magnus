from numpy import place
import pygame
from enum import Enum
from playerArea import PlayerArea
from render import Render
from map import Map
from actions import CubeAction, Action
# from game_cube_actions import GameCubeAction, GameCubeActions

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
        TOKENS = 2
        KING = 3
        END_TURN = 4

    class TokenState(Enum):
        AVAILABLE = 0
        SELECTED = 1
        EXHAUSTED = 2

    def __init__(self, player_number, render: Render) -> None:
        self.player_number = player_number
        self.render = render
        self.player_render = self.render.player_areas[self.player_number]
        self.map = self.render.map

        self.game_state = 0 #TODO: get game_state
        self.selected_territory = 0
        self.prev_selected_territory = 0 # from when we were just selecting cubes, not the king
        self.n_territories = len(self.map.territories)

        self.selection_mode = Player.SelectionType.CUBES
        self.selected_cube = 0

        self.king_movements = 0
        self.king_movements_allowed = 3 # TODO: update based on which token was selected

        self.selected_token = 0
        self.nTokens = 5
        self.token_states = [Player.TokenState.AVAILABLE] * self.nTokens

        self.cache_list = self.player_render.cache_list
        self.cache_size = len(self.cache_list)
        self.terr_list = [None] * self.cache_size
        self.cube_placements = [Player.CubeRegion.CACHE] * self.cache_size # all cubes start in the Cache
        self.search_mode = Player.CubeRegion.CACHE # used in self.right_cube()

        self.nActions = 3
        self.cubes_placed = 0


    def reset_player_area(self, render: Render):
        self.render = render
        self.player_render = self.render.player_areas[self.player_number]
        self.map = self.render.map

        self.selected_territory = 0
        self.n_territories = len(self.map.territories)

        self.selection_mode = Player.SelectionType.CUBES
        self.selected_cube = 0

        self.cache_list = self.player_render.cache_list
        self.cache_size = len(self.cache_list)
        self.terr_list = [None] * self.cache_size
        self.cube_placements = [Player.CubeRegion.CACHE] * self.cache_size # all cubes start in the Cache
        self.search_mode = Player.CubeRegion.CACHE # used in self.right_cube()

        self.cubes_placed = 0
        self.king_movements = 0

    def check_king_movement(self):
        assert(self.king_movements <= self.king_movements_allowed) # this should never happen
        if self.king_movements < 1:
            return False
        # else:
        return True

    def check_actions(self):
        assert(self.cubes_placed <= self.nActions) # if this is not the case, then we messed up the turn control elsewhere
        # or someone is trying to cheat
        if self.cubes_placed < self.nActions: # if not enough actions have been taken yet, do not complete the turn
            return False

        correct_action_count = 0
        for color_id, placement, terr in zip(self.cache_list, self.cube_placements, self.terr_list):
            # only two places where cubes should be permanently deposited
            if placement in [Player.CubeRegion.COURT, Player.CubeRegion.TERRITORY]:
                correct_action_count += 1

        assert(correct_action_count <= self.nActions) # if this is not the case, then we messed up the turn control elsewhere
        # or someone is trying to cheat
        if correct_action_count < self.nActions: # if not enough actions have been taken yet, do not complete the turn
            return False

        # if all checks passed:
        return True

    def return_actions(self): # called when enter is pressed
        """Unpack all cube placement actions that have been taken over the course of the turn and add them to a
        GameCubeActions object for export to the server.

        self.return_actions() is called whenever ENTER is pressed during cube selection.
        It only makes sense to return the actions when self.cubes_placed == self.nActions; i.e. all three cube actions
        have been taken. self.return_actions() contains rigorous checking to make sure this is the case.
        If not, either raises an AssertionError or simply returns None.
        """
        assert(self.check_actions()) # at this point, it should be correct.
        # We have already thrown it back to the Player to redo if it's not correct, and this is the final inspection

        cube_actions = []
        for color_id, placement, terr in zip(self.cache_list, self.cube_placements, self.terr_list):
            if placement == Player.CubeRegion.COURT:
            # placement == Player.CubeRegion.TERRITORY:
                cube_actions.append(CubeAction(color_id, court = True, terr_id = None))
            elif placement == Player.CubeRegion.TERRITORY:
                cube_actions.append(CubeAction(color_id, court = False, terr_id = terr))

        assert(len(cube_actions) == self.nActions)

        actions_to_return = Action(self.player_render.team, cube_actions, king = self.king_movements)

        # self.selection_mode = Player.SelectionType.CUBES
        # self.selected_territory = 0 # reset for the start of next turn
        # self.king_movements = 0 # reset for the start of the next king phase
        return actions_to_return


    def select(self, event:pygame.event.Event):
        """Contains all the necessary commands to complete a single action on this player's main turn,
        including cube / territory selection, followed by king selection
        (distinguished from the initial, initiative-selection turn, which happens in a different order).

        Because all the events originate in the Client loop, this funtion is intended to be run inside
        a while loop in client.py. Each time a relevant event occurs in that while loop, this function is called.

        This function returns None as long as the turn is not over.
        When the turn is complete, it returns an Action object.
        """
        # discard unused actions
        action_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN]
        if event.type != pygame.KEYDOWN or event.key not in action_keys:
            return None

        if self.selection_mode == Player.SelectionType.TOKENS:
            self.select_token(event)
        elif self.selection_mode == Player.SelectionType.CUBES:
            self.select_cube(event)
        elif self.selection_mode == Player.SelectionType.TERRITORIES:
            self.select_territory(event)
        elif self.selection_mode == Player.SelectionType.KING:
            return self.select_king(event) # returns either None or an Actions object
        elif self.selection_mode == Player.SelectionType.END_TURN:
            print("Inside Player", self.player_number, ", we have reached the end of our turn and no longer wish to transmit.")
            # return self.return_actions()
            pass # don't return the actions a second time
        # else:
        return None

    def select_territory(self, event:pygame.event.Event): # -> tuple[pygame.sprite.Group, list[any]]:
        updated_rects = None

        if event.key == pygame.K_LEFT: # select left
            self.select_next_territory_left()
            # then
            updated_rects = self.map.select_territory(self.selected_territory)

        elif event.key == pygame.K_RIGHT: # select right
            self.select_next_territory_right()
            # then
            updated_rects = self.map.select_territory(self.selected_territory)

        elif event.key == pygame.K_UP: # return to cache
            if self.cube_placements[self.selected_cube] == Player.CubeRegion.TERRITORY_HOLDING:
                self.cube_placements[self.selected_cube] = Player.CubeRegion.CACHE
                updated_rects = self.return_to_cache()

        elif event.key == pygame.K_DOWN: # add to territory
            if self.cube_placements[self.selected_cube] == Player.CubeRegion.TERRITORY_HOLDING:
                self.cube_placements[self.selected_cube] = Player.CubeRegion.TERRITORY
                updated_rects = self.add_to_territory()
                self.cubes_placed += 1

        elif event.key == pygame.K_RETURN: # end turn selection with selected value
            if self.check_actions():
                self.selection_mode = Player.SelectionType.KING
                self.render.king.highlight()
                self.selected_territory = self.render.king_loc
            else:
                "Please finish all actions before pressing Enter. (#2)"

        # return updated_rects
        return None

    def start_selecting_king(self): # unused
        self.selected_territory = self.render.king_loc
        self.render.king.highlight()
        # self.king_movements = 0

    def select_king(self, event:pygame.event.Event):

        if event.key == pygame.K_LEFT: # select left
            if self.king_movements > 0:
                self.select_next_territory_left()
                self.render.move_king(self.selected_territory)
                self.king_movements -= 1

        elif event.key == pygame.K_RIGHT: # select right
            if self.king_movements < self.king_movements_allowed:
                self.select_next_territory_right()
                self.render.move_king(self.selected_territory)
                self.king_movements += 1

        elif event.key == pygame.K_UP: # return to cache
            self.render.king.un_highlight()
            self.selection_mode = Player.SelectionType.CUBES
            self.selected_territory = self.prev_selected_territory

        elif event.key == pygame.K_RETURN: # end turn selection with selected value
            if self.check_king_movement():
                self.render.king.un_highlight()
                self.selection_mode = Player.SelectionType.END_TURN
                return self.return_actions()
            else:
                print("Please move the King at least one space")


        return None

    def select_next_territory_left(self):
        self.selected_territory = (self.selected_territory - 1) % self.n_territories
        while self.map.territories[self.selected_territory].can_draw == False:
            self.selected_territory = (self.selected_territory - 1) % self.n_territories

    def select_next_territory_right(self):
        self.selected_territory = (self.selected_territory + 1) % self.n_territories
        while self.map.territories[self.selected_territory].can_draw == False:
            self.selected_territory = (self.selected_territory + 1) % self.n_territories

    def add_to_territory(self):
        """Adds the currently selected cube to the currently selected territory. Called when the down arrow is pressed
        during territory selection, when a cube is in the holding position.
        The next selection mode is CUBES, and the search mode resets to CACHE
        """
        # update self.terr_list
        self.terr_list[self.selected_cube] = self.selected_territory

        # add cube to territory
        color_id = self.player_render.cache_list[self.selected_cube]
        new_xy = self.map.add_to_territory(self.selected_territory, self.selected_cube, color_id) # returns the coordinates of the new cube
        updated_rects = self.move_selected_cube_to(new_xy)

        # deselect the territory and
        updated_rects.append(self.map.de_select_territory(self.selected_territory))

        # update selection mode
        self.selection_mode = Player.SelectionType.CUBES
        self.search_mode = Player.CubeRegion.CACHE

        return updated_rects

    def remove_from_territory(self):
        """Moves the currently selected cube from a territory to holding. Called when the up arrow is pressed during cube
        selection when the selected cube is on a territory.
        """
        # after going to holding, the selected and highlighted territory will be the territory where the cube just came from
        self.selected_territory = self.terr_list[self.selected_cube]
        self.map.remove_from_territory(self.terr_list[self.selected_cube], self.selected_cube) # (self.selected_territory, self.selected_cube)
        self.terr_list[self.selected_cube] = None
        return self.move_to_holding()

    def return_to_cache(self):
        """Moves the currently selected cube from the holding position to its original location in the Cache.
        The new selection mode is CUBES, and the search mode resets to CACHE.
        """
        # move the cube
        new_xy = self.player_render.cache.cube_locs[self.selected_cube]
        updated_rects = self.move_selected_cube_to(new_xy)

        # deselect the territory
        self.map.de_select_territory(self.selected_territory)
        self.terr_list[self.selected_cube] = None

        # reset the search mode
        self.selection_mode = Player.SelectionType.CUBES
        self.search_mode = Player.CubeRegion.CACHE

        return updated_rects

    def select_cube(self, event:pygame.event.Event): # -> tuple[pygame.sprite.Group, list[any]]:
        updated_rects = None

        if event.key == pygame.K_LEFT: # select left
            self.selected_cube = self.left_cube()
            updated_rects = self.player_render.select_cube(self.selected_cube)

        elif event.key == pygame.K_RIGHT: # select right
            self.selected_cube = self.right_cube()
            updated_rects = self.player_render.select_cube(self.selected_cube)

        elif event.key == pygame.K_UP:
            # if in COURT: remove from court
            if self.cube_placements[self.selected_cube] == Player.CubeRegion.COURT:
                self.cube_placements[self.selected_cube] = Player.CubeRegion.CACHE
                updated_rects = self.player_render.remove_from_court(self.selected_cube)
                self.cubes_placed -= 1

            # if in CACHE: move to holding
            elif self.cube_placements[self.selected_cube] == Player.CubeRegion.CACHE:
                self.cube_placements[self.selected_cube] = Player.CubeRegion.TERRITORY_HOLDING
                updated_rects = self.move_to_holding()

            # if in TERRITORY: remove from territory
            elif self.cube_placements[self.selected_cube] == Player.CubeRegion.TERRITORY:
                self.cube_placements[self.selected_cube] = Player.CubeRegion.TERRITORY_HOLDING
                updated_rects = self.remove_from_territory()
                self.cubes_placed -= 1

        elif event.key == pygame.K_DOWN: # add to court (adding to territories only happens in select_territory())
            if self.cube_placements[self.selected_cube] == Player.CubeRegion.CACHE:
                self.cube_placements[self.selected_cube] = Player.CubeRegion.COURT
                updated_rects = self.player_render.add_to_court(self.selected_cube)
                self.cubes_placed += 1

        elif event.key == pygame.K_RETURN: # end turn selection with selected value
            if self.check_actions():
                self.selection_mode = Player.SelectionType.KING
                self.selected_territory = self.render.king_loc
                self.render.king.highlight()
            else:
                "Please finish all actions before pressing Enter. (#1)"

        return updated_rects

    def move_to_holding(self):
        """Moves the currently selected cube to the holding location, which means the cube is being primed to be placed on a territory.
        A cube is moved to the holding position when it is selected to do so from the Cache (up arrow while selected in cache) or when
        it is removed from a territory (up arrow while on territory). While in holding, the selection mode is always TERRITORIES.
        While in holding, if the down arrow is pressed, it places the cube on the currently selected territory.
        While in holding, if the up arrow is pressed again, it returns the cube to the cache.
        """
        new_xy = self.player_render.territory_holding_location # predefined location of the cube in holding
        updated_rects = self.move_selected_cube_to(new_xy)

        # highlight the selected territory
        updated_rects.extend(self.map.select_territory(self.selected_territory))

        # start the selection process
        self.selection_mode = Player.SelectionType.TERRITORIES

        return updated_rects

    def move_selected_cube_to(self, new_xy):
        """Helper function to update the position of a selected cube, returning the rects at the old and new locations."""
        return self.player_render.cache.cube_list[self.selected_cube].update_pos(new_xy)


    def select_token(self, event:pygame.event.Event): # -> tuple[pygame.sprite.Group, list[any]]:
        updated_rects = None

        if event.key == pygame.K_LEFT: # select left
            for i in range(self.nTokens):
                self.selected_token = (self.selected_token - 1) % self.nTokens
                if self.token_states[self.selected_token] == Player.TokenState.AVAILABLE:
                    updated_rects = self.player_render.select_token(self.selected_token)
                    return updated_rects
            assert False, "Tried to select new cube when no cubes are AVAILABLE"

        elif event.key == pygame.K_RIGHT: # select right
            for i in range(self.nTokens):
                self.selected_token = (self.selected_token + 1) % self.nTokens
                if self.token_states[self.selected_token] == Player.TokenState.AVAILABLE:
                    updated_rects = self.player_render.select_token(self.selected_token)
                    return updated_rects
            assert False, "Tried to select new cube when no cubes are AVAILABLE"

        # elif event.key == pygame.K_UP: # return to cache
        #     if self.token_states[self.selected_token] == Player.TokenState.SELECTED:
        #         self.token_states[self.selected_token] = Player.TokenState.AVAILABLE
        #         self.player_render.token_set.token_list[self.selected_token].set_image(self.selected_token)
        #         updated_rects = self.player_render.select_token(self.selected_token)

        # elif event.key == pygame.K_DOWN: # add to territory
        #     if self.token_states[self.selected_token] == Player.TokenState.AVAILABLE:
        #         self.token_states[self.selected_token] = Player.TokenState.SELECTED
        #         self.player_render.token_set.token_list[self.selected_token].set_image(-1)
        #         updated_rects = self.player_render.select_token(self.selected_token)

        elif event.key == pygame.K_KP_ENTER: # end turn selection with selected value
            print(f"Selected token {self.selected_token}")
            return self.selected_token
            # self.selection_mode = Player.SelectionType.CUBES

        return updated_rects






# #################################################################################################### #
# Below lies the dark magic of cube selection. Beware, and don't touch anything shiny. (Bwaahaahaaaaa) #
# #################################################################################################### #

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
        if (self.cubes_placed >= self.nActions) and (self.search_mode == Player.CubeRegion.CACHE):
            self.search_mode = Player.CubeRegion.COURT
            temp_selected_cube = self.cache_size - 1

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
            if self.cubes_placed >= self.nActions:
                self.search_mode = Player.CubeRegion.COURT
                return self.cache_size - 1
            # else:
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