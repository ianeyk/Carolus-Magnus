import pygame
from enum import Enum
from playerArea import PlayerArea

class Player():
    class CubePlacement(Enum):
        CACHE = 0
        COURT = 1
        TERRITORY = 2

    def __init__(self, player_render: PlayerArea) -> None:
        self.selected_cube = None
        self.game_state = 0
        self.selected_cube = 0
        self.player_render = player_render
        self.cache_list = self.player_render.cache_list
        self.cache_size = len(self.cache_list)
        self.cube_placements = [Player.CubePlacement.CACHE for i in range(self.cache_size)]
        self.idx_list = self.generate_idx_list()
        self.search_mode = Player.CubePlacement.CACHE

    def select_cube(self, event:pygame.event.Event): # -> tuple[pygame.sprite.Group, list[any]]:

        print(event)
        action_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        if event.type != pygame.KEYDOWN or event.key not in action_keys:
            return None, None

        updated_rects = None

        if event.key == pygame.K_LEFT:
            updated_rects = self.player_render.select_cube(self.selected_cube)
            # bolt on a thing that says to go to the next cube of a different color
            self.selected_cube = self.left_cube()
            updated_rects = self.player_render.select_cube(self.selected_cube)

        elif event.key == pygame.K_RIGHT:
            self.selected_cube = self.right_cube(self.cache_list[self.selected_cube])
            updated_rects = self.player_render.select_cube(self.selected_cube)

        elif event.key == pygame.K_UP:
            if self.cube_placements[self.selected_cube] == self.CubePlacement.COURT:
                self.cube_placements[self.selected_cube] = self.CubePlacement.CACHE
                updated_rects = self.player_render.remove_from_court(self.selected_cube)

        elif event.key == pygame.K_DOWN:
            if self.cube_placements[self.selected_cube] == self.CubePlacement.CACHE:
                self.cube_placements[self.selected_cube] = self.CubePlacement.COURT
                updated_rects = self.player_render.add_to_court(self.selected_cube)

        return self.player_render.cache.draw_cubes(), updated_rects # returns a group

    def generate_idx_list(self):
        cache_list = self.player_render.cache_list
        # [0, 0, 1, 2, 4, 4, 4]
        idx_list = []
        # [0, 2, 3, 4]
        prev_color_id = -1 # magic bogus value
        for idx, color_id in enumerate(cache_list):
            if color_id != prev_color_id:
                idx_list.append(idx)
                prev_color_id = color_id
        return idx_list

        pass

    def right_cube(self, prev_color_id):
        # prev_color_id = self.cache_list[self.selected_cube]

        # for idx in wrap(list(range(len(self.cache_list))), self.selected_cube):
        #     if self.cache_list[idx] != prev_color_id or self.cube_placements[idx] != prev_placement:
        #         return idx
        # return 0 # else

        # then check the court
        for idx in list(range(self.selected_cube, len(self.cache_list))):
            if self.cache_list[idx] != prev_color_id and self.cube_placements[idx] == self.search_mode:
                return idx
        if self.search_mode == Player.CubePlacement.CACHE:
            self.search_mode = Player.CubePlacement.COURT
        elif self.search_mode == Player.CubePlacement.COURT:
            self.search_mode = Player.CubePlacement.TERRITORY
        elif self.search_mode == Player.CubePlacement.TERRITORY:
            self.search_mode = Player.CubePlacement.CACHE
            #TODO: if placement limit has been reached, don't let search_mode go back to cache

        self.selected_cube = 0
        return self.right_cube(-1)

        # return 0 # else

    # def right_search(self):
    #     prev_color_id = self.cache_list[self.selected_cube]
    #     prev_placement = self.cube_placements[self.selected_cube]

    def left_cube(self):
        prev_color_id = self.cache_list[self.selected_cube]
        prev_placement = self.cube_placements[self.selected_cube]

        for idx in wrap(list(range(len(self.cache_list)))[::-1], len(self.cache_list) - self.selected_cube - 1):
            if self.cache_list[idx] != prev_color_id or self.cube_placements[idx] != prev_placement:
                return idx
        return 0 # else
        # return self.idx_list[(self.idx_list.index(self.selected_cube) - 1) % len(self.idx_list)]

    def select_territory(self):
        total_territories = len(self.game_state.territories)
        self.selected_territory = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.selected_territory = (self.selected_territory + 1) % total_territories
            self.local_interface.select_terr(self.selected_territory)

        if keys[pygame.K_RIGHT]:
            self.selected_territory = (self.selected_territory + 1) % total_territories
            self.local_interface.select_terr(self.selected_territory)

        if keys[pygame.K_UP]:
            self.local_interface.undo_terr(self.selected_territory)
            self.select_territory()

        if keys[pygame.K_DOWN]:
            self.local_interface.add_to_terr(self.selected_territory)

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

def wrap(lst, idx):
    idx1 = (idx + 1) % len(lst)
    output = lst[idx1:]
    output.extend(lst[:idx1])
    return output

# def main():
#     a = [0, 1, 2, 3, 4, 5]
#     print(a)
#     b = wrap(a, 5)
#     print(b)

# main()