import pygame
import math
import random
from collections import Counter
from cube import Cube
from game_territory import GameTerritory
from territory_hex import TerritoryBorder, TerritoryHex

class Territory(pygame.sprite.Sprite):
    pngs = {
        0: "./sprites/hexes/ruleBookTileA.png", # TODO: build tiles out of individual hexes using function
    }
    highlighted_pngs = {
        0: "./sprites/hexes/tileA_highlight1.png" # TODO: build tiles out of individual hexes using function
    }

    # spacing = 1.2
    # side_length = Cube.size[0] * spacing * 1.8
    # cube_dist = side_length * 2 / 3
    # size = (3 * side_length * math.sqrt(3), side_length * 3.5)

    def __init__(self, x, y, angle, terr_type = 0, terr_size = 1):
        pygame.sprite.Sprite.__init__(self) # Call the parent class (Sprite) constructor

        self.x = x
        self.y = y
        self.angle = -angle + math.pi
        self.terr_type = terr_type
        self.cube_list = []
        self.terr_size = terr_size # number of territories that have been merged together; multiply by 4 to get the number of hexes
        self.hexes_per_unit_size = 4
        self.cubes_per_hex = 3
        self.max_num_cubes = terr_size * self.hexes_per_unit_size * self.cubes_per_hex
        self.placement_order = list(range(self.max_num_cubes))
        random.shuffle(self.placement_order)
        self.temp_cube_list = [None] * 7 #TODO: change based on the number of players


        self.hex_diameter = 38 # two times the side length
        self.hex_overlap_factor = 1.1 # coord radius gets divided by this number
        self.coords_of_hexes = [] # auto-generation of hex patterns
        self.hex_coord_list = self.get_all_hex_coords()
        self.hex_sprites = []
        self.border_sprites = []

        self.expand_hexes()
        self.all_cube_coords = self.get_all_cube_coords()

        self.empty_spaces_to_my_left = 0
        self.empty_spaces_to_my_right = 0

        # png_image = pygame.image.load(Territory.pngs[self.terr_type])
        # self.set_image(png_image)
        self.can_draw = True # set to False if the territory disappears because of merging

        self.cubes = []
        for loc, color_id in enumerate(self.cube_list):
            self.cubes.append(Cube(*self.coords_of_cube(loc), color_id))


    def update(self, new_terr: GameTerritory):
        print("territory is updating game state")
        self.remove_all_temp_cubes()
        # current_cube_set = Counter(self.cube_list)
        current_cube_set = Counter([c.ordinal_id for c in self.cubes])
        print("cube set object", current_cube_set)
        print("self.cubes is", self.cubes)
        new_cube_set = new_terr.cubes.get_cubes()
        for color_id in range(5):
            print("color is:", color_id)
            # print("current_cube_set is:", current_cube_set.get(color_id, 0))
            print("current_cube_set is:", current_cube_set.get(color_id, 0))
            print("new_cube_set is:", new_cube_set[color_id])
            while new_cube_set[color_id] > current_cube_set.get(color_id, 0): # default value of 0
                cube_coords = self.add_cube(6, color_id)
                self.cubes.append(Cube(*cube_coords, color_id))
                print("adding one more cube to this territory")
                new_cube_set[color_id] -= 1

        # reset the temp_cube tracking
        self.temp_cube_list = [None] * 7 #TODO: change based on the number of players # I think this should also be 3?

    def clear(self):
        # self.kill()
        for cube in self.cubes:
            cube.kill()
        for hex in self.hex_sprites:
            hex.clear()
        for border in self.border_sprites:
            border.clear()
        self.can_draw = False

    def coords_of_cube(self, loc): # takes care of shuffled placement order
        return self.all_cube_coords[self.placement_order[loc]]

    def get_all_cube_coords(self):
        coords = []
        for hex in self.hex_sprites:
            coords.extend(hex.get_cube_slots())
        return coords

    def draw(self, group):
        if self.can_draw:
            # self.add(group)
            self.draw_hexes(group)
            self.draw_cubes(group)

    def draw_cubes(self, group):
        for cube in self.cubes:
            cube.add(group)

    def draw_hexes(self, group):
        for border in self.border_sprites: # draw the borders first
            border.add(group)
        for hex in self.hex_sprites:
            hex.add(group)

    # def set_image(self, image, size = None):
    #     if not size:
    #         size = Territory.size
    #     self.image = pygame.transform.smoothscale(image, size)
    #     self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))

    #     self.rect = self.image.get_rect(center = (self.x, self.y))

    def highlight(self):
        for border in self.border_sprites:
            border.highlight()

    def un_highlight(self):
        for border in self.border_sprites:
            border.un_highlight()


    # Each Territory object contains two lists of cube locations.
    #
    # self.cube_list is a permanent list of the color_ids of the cubes being stored on the Territory. It is important to
    # store these permanently, so that the orders of the colors do not change each time the map is refreshed. The actual
    # cubes on the map are placed according to self.placement_order[idx], where idx is the index of the cube in self.cube_list.
    # When a cube is removed from the territory, the color_id at the index of the cube is replaced with None. When a new cube
    # is added to the territory, it searches for None elements in self.cube_list and fills those in first. If there are no
    # elements that are None, it appends the new cube's color_id to the end of self.cube_list.
    #
    # self.temp_cube_list is the list of cubes which have been added and may be updated on the current turn. The index is
    # based on the cube_id of the Cache cubes being placed. Therefore, self.temp_cube_list has 7 elements in a 2 or 4 player
    # game and 9 elements in a 3 player game, all initialized to None. When one of the Cache cubes is added, the element at
    # cube_id is set to the index in self.cube_list where the cube was placed (filling in Nones first, as described above).
    # This allows the locations of each added cube to be tracked and also for their new positions to be specified according to
    # self.placement_order[idx], where idx = self.temp_cube_list[cube_id].

    def add_cube(self, cube_id, color_id):
        found_empty_slot = False # initialize flag

        for idx, existing_color_id in enumerate(self.cube_list):
            if existing_color_id is None: # search for empty slots first before appending to the end
                found_empty_slot = True
                break # keeps the value of idx and uses it below

        if not found_empty_slot:
            idx = len(self.cube_list) # the index of the subsequently appended cube (to avoid an off by -1 error)
            self.cube_list.append(color_id) # needed to make the list one longer; will be redefined
        else:
            self.cube_list[idx] = color_id
        # in any case:
        self.temp_cube_list[cube_id] = idx
        # print(self.temp_cube_list)
        return self.coords_of_cube(idx)

    def remove_cube(self, cube_id):
        idx = self.temp_cube_list[cube_id]
        self.cube_list[idx] = None
        self.temp_cube_list[cube_id] = None
        # print(self.temp_cube_list)

    def remove_all_temp_cubes(self):
        for cube_id, cube_list_idx in enumerate(self.temp_cube_list):
            if cube_list_idx is not None:
                self.remove_cube(cube_id)

    def move_xy(self, x, y):
        self.x = x
        self.y = y
        for hex in self.hex_sprites:
            hex.move_center(x, y)
        for border in self.border_sprites:
            border.move_center(x, y)

        self.all_cube_coords = self.get_all_cube_coords()

        for idx, cube in enumerate(self.cubes):
            cube.update_pos(self.coords_of_cube(idx))


    def expand_hexes(self):
        # total number of hexes to create
        prev_n_hexes = len(self.coords_of_hexes)
        n_hexes = self.terr_size * self.hexes_per_unit_size

        if n_hexes <= prev_n_hexes:
            return

        self.coords_of_hexes = self.hex_coord_list[:n_hexes]
        for i in range(prev_n_hexes, n_hexes):
            self.add_hex_sprite(self.hex_coord_list[i])

    def add_hex_sprite(self, coords):
        self.border_sprites.append(TerritoryBorder(coords, self.hex_diameter * 1.2))
        self.hex_sprites.append(TerritoryHex(coords, self.hex_diameter, random.randrange(0, 6)))

    def how_many_rings(self, n_hexes):
        # number of concentric rings of hexes that will be required (center hex counts as ring #0)
        n_rings = 0
        while n_hexes > (n_rings * (n_rings + 1) / 2 * 6 + 1):
            n_rings += 1
        return n_rings

    def get_all_hex_coords_in_ring(self, n_rings):
        # compute the coordinates for hexes lying along the outermost ring; assume all inner rings have been filled
        if n_rings == 0:
            ring_hex_coords = [(self.x, self.y)]
            return ring_hex_coords
        # else:

        # avoid repeated sin and cosine calculations
        sin60 = math.sin(math.radians(60))
        cos60 = 1/2 # math.cos(60)

        ring_hex_coords = []
        for i in range(n_rings):
            one_sixth_hex_coord_x = (n_rings - cos60 * i) * self.hex_diameter / self.hex_overlap_factor
            one_sixth_hex_coord_y = (sin60 * i) * self.hex_diameter / self.hex_overlap_factor
            for j in range(6):
                theta = 2 * math.pi / 6 * j
                ring_hex_coords.append((
                    self.x + one_sixth_hex_coord_x * math.cos(theta)      + one_sixth_hex_coord_y * math.sin(theta),
                    self.y + one_sixth_hex_coord_x * math.sin(theta) * -1 + one_sixth_hex_coord_y * math.cos(theta)
                ))

        return ring_hex_coords

    def get_all_hex_coords(self):
        hex_coords_list = []
        for ring in range(self.how_many_rings(100) + 1): # will never reach this limit
            ring_coords_list = self.get_all_hex_coords_in_ring(ring)
            random.shuffle(ring_coords_list)
            hex_coords_list.extend(ring_coords_list)

        return hex_coords_list