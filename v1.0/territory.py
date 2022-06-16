import pygame
import math
import random
from cube import Cube

class Territory(pygame.sprite.Sprite):
    pngs = {
        0: "./sprites/hexes/ruleBookTileA.png",
    }
    highlighted_pngs = {
        0: "./sprites/hexes/tileA_highlight1.png"
    }

    spacing = 1.2
    side_length = Cube.size * spacing * 1.8
    cube_dist = side_length * 2 / 3

    size = (3 * side_length * math.sqrt(3), side_length * 3.5)
    # small_offset_from_edges = 18
    # large_offset_from_edges = 24

    def __init__(self, x, y, angle, starting_cube, terr_type = 0):
        pygame.sprite.Sprite.__init__(self) # Call the parent class (Sprite) constructor

        self.x = x
        self.y = y
        self.angle = -angle + math.pi
        self.terr_type = terr_type
        self.cube_list = [starting_cube]
        self.placement_order = list(range(24))
        # random.shuffle(self.placement_order)
        self.permanent_cubes = 1 #TODO: update the number of permanent_cubes at the start of each round based on the game state
        self.temp_cube_list = []
        self.len_of_list = len(self.temp_cube_list)

        png_image = pygame.image.load(Territory.pngs[self.terr_type])
        self.set_image(png_image)

        self.cubes = []
        for loc, color_id in enumerate(self.cube_list):
            self.cubes.append(Cube(*self.coords_of_cube(self.placement_order[loc]), color_id))

    def coords_of_cube(self, loc):
        assert(loc <= 24) # fails for more cubes on one hex
        which_hex = loc // 6
        intra_hex_loc = loc % 6
        un_rotated = self.intra_hex_coords(*self.hex_coords(which_hex), intra_hex_loc) # returns x, y coordinates of the cube location
        rotated = un_rotated
        return rotated
        # return (self.x + loc[0], self.y + loc[1] + Territory.cube_vertical_offset)

    def intra_hex_coords(self, center_x, center_y, pos): # pos starts at the top and moves clockwise
        radius = Cube.size * Territory.spacing
        cube_angle = math.pi - math.pi / 6 + math.pi * 2 / 6 * pos - self.angle
        intra_hex_x = center_x + radius * math.cos(cube_angle)
        intra_hex_y = center_y + radius * math.sin(cube_angle)
        return intra_hex_x, intra_hex_y

    def hex_coords(self, which_hex):
        if self.terr_type == 0:
            if which_hex in [0, 1, 2]:
                hex_x = self.x + (which_hex - 1) * Territory.side_length * math.sqrt(3)
                hex_y = self.y + 0.75 * Territory.side_length
            else:
                hex_x = self.x - Territory.side_length * math.sqrt(3) / 2
                hex_y = self.y - 0.75 * Territory.side_length
        rotated = (self.x + (hex_x - self.x) *  math.cos(self.angle) + (hex_y - self.y) * math.sin(self.angle),
                   self.y + (hex_x - self.x) * -math.sin(self.angle) + (hex_y - self.y) * math.cos(self.angle))
        return rotated

    def draw(self, group):
        self.add(group)
        self.draw_cubes(group)

    def draw_cubes(self, group):
        for cube in self.cubes:
            cube.add(group)

    def set_image(self, image, size = None):
        if not size:
            size = Territory.size
        self.image = pygame.transform.smoothscale(image, size)
        self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))

        self.rect = self.image.get_rect(center = (self.x, self.y))
        # self.rect = (x - Territory.size[0] / 2, y - Territory.size[1] / 2, *Territory.size)


    def highlight(self):
        highlighted_image = pygame.image.load(Territory.highlighted_pngs[self.terr_type])
        scale_factor = 1.1
        self.set_image(highlighted_image, size = (Territory.size[0] * scale_factor, Territory.size[1] * scale_factor))

        new_rect = self.image.get_rect(center = (self.x, self.y))
        return (new_rect.x, new_rect.y, new_rect.w, new_rect.h)

    def un_highlight(self):
        # store the large rect for updated_rect purposes
        prev_rect = self.image.get_rect(center = (self.x, self.y))

        png_image = pygame.image.load(Territory.pngs[self.terr_type])
        self.set_image(png_image)
        return (prev_rect.x, prev_rect.y, prev_rect.w, prev_rect.h)

    def add_cube(self, cube_id, color_id):
        print("adding cube")


        for idx, existing_color_id in enumerate(self.temp_cube_list):
            if existing_color_id is None: # search for empty slots first before appending to the end
                self.temp_cube_list[idx] = cube_id
                new_idx = self.permanent_cubes + idx
                self.cube_list[new_idx] = color_id
                print(self.temp_cube_list)
                # print("cube_list:", self.cube_list, "; adding to index", idx, ", which is cube position", self.placement_order[idx])
                return self.coords_of_cube(self.placement_order[new_idx])

        self.temp_cube_list.append(cube_id)
        self.cube_list.append(color_id)
        print(self.temp_cube_list)
        # print("cube_list:", self.cube_list, "; adding to index", len(self.cube_list) - 1, ", which is cube position", self.placement_order[len(self.cube_list) - 1])
        return self.coords_of_cube(self.placement_order[self.permanent_cubes + len(self.temp_cube_list) - 1])

    def remove_cube(self, cube_id):
        print(id(self))
        idx = self.temp_cube_list.index(cube_id)
        self.temp_cube_list[idx] = None
        self.cube_list[self.permanent_cubes + idx] = None
        print(self.temp_cube_list)



    # def add_cube(self, color_id):
    #     print("adding cube")

    #     for idx, existing_color_id in enumerate(self.cube_list):
    #         if existing_color_id is None: # search for empty slots first before appending to the end
    #             self.cube_list[idx] = color_id
    #             print("cube_list:", self.cube_list, "; adding to index", idx, ", which is cube position", self.placement_order[idx])
    #             return self.coords_of_cube(self.placement_order[idx])

    #     self.cube_list.append(color_id)
    #     print("cube_list:", self.cube_list, "; adding to index", len(self.cube_list) - 1, ", which is cube position", self.placement_order[len(self.cube_list) - 1])
    #     return self.coords_of_cube(self.placement_order[len(self.cube_list) - 1])


    # def remove_cube(self, expected_color_id):
    #     # print("cube_list:", self.cube_list)
    #     for idx, color_id in enumerate(self.cube_list[::-1]):
    #         if color_id == expected_color_id:
    #             self.cube_list[len(self.cube_list) - 1 - idx] = None
    #             print("subtracting cube at index", len(self.cube_list) - 1 - idx, ", which is cube position", self.placement_order[len(self.cube_list) - 1 - idx])
    #             print("CUBE_LIST:", self.cube_list)
    #             return
    #     raise IndexError(f"No cubes of color {expected_color_id} in this territory")