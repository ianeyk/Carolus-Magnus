import pygame
import math
import random
from collections import Counter
from cube import Cube
from game_territory import GameTerritory
from territory_hex import TerritoryHex

class Territory(pygame.sprite.Sprite):
    pngs = {
        0: "./sprites/hexes/ruleBookTileA.png", # TODO: build tiles out of individual hexes using function
    }
    highlighted_pngs = {
        0: "./sprites/hexes/tileA_highlight1.png" # TODO: build tiles out of individual hexes using function
    }

    spacing = 1.2
    side_length = Cube.size[0] * spacing * 1.8
    cube_dist = side_length * 2 / 3
    size = (3 * side_length * math.sqrt(3), side_length * 3.5)

    def __init__(self, x, y, angle, terr_type = 0, terr_size = 1):
        pygame.sprite.Sprite.__init__(self) # Call the parent class (Sprite) constructor

        self.x = x
        self.y = y
        self.angle = -angle + math.pi
        self.terr_type = terr_type
        self.cube_list = []
        self.placement_order = list(range(24))
        random.shuffle(self.placement_order)
        self.temp_cube_list = [None] * 7 #TODO: change based on the number of players

        self.hex_diameter = 30 # two times the side length
        self.terr_size = terr_size # number of territories that have been merged together; multiply by 4 to get the number of hexes
        self.coords_of_hexes = [] # auto-generation of hex patterns
        self.hex_coord_list = self.get_all_hex_coords()
        self.hex_sprites = []
        self.expand_hexes()

        png_image = pygame.image.load(Territory.pngs[self.terr_type])
        self.set_image(png_image)
        self.can_draw = True # set to False if the territory disappears because of merging

        self.cubes = []
        for loc, color_id in enumerate(self.cube_list):
            self.cubes.append(Cube(*self.coords_of_cube(self.placement_order[loc]), color_id))

    # def __init__(self, starting_cube):
    #     self.size = 1
    #     self.cubes = CubeSet()
    #     self.cubes.add_cube(starting_cube)
    #     self.castles = 0
    #     self.owner = None

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
        self.kill()
        for cube in self.cubes:
            cube.kill()
        self.can_draw = False

    def coords_of_cube(self, loc):
        assert(loc <= 24) # fails for more cubes on one hex
        which_hex = loc // 6
        intra_hex_loc = loc % 6
        rotated_coords = self.intra_hex_coords(*self.hex_coords(which_hex), intra_hex_loc) # returns x, y coordinates of the cube location
        return rotated_coords

    def intra_hex_coords(self, center_x, center_y, pos): # pos starts at the top and moves clockwise
        radius = Cube.size[0] * Territory.spacing
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
        if self.can_draw:
            # self.add(group)
            self.draw_hexes(group)
            self.draw_cubes(group)

    def draw_cubes(self, group):
        for cube in self.cubes:
            cube.add(group)

    def draw_hexes(self, group):
        for hex_sprite in self.hex_sprites:
            hex_sprite.add(group)

    def set_image(self, image, size = None):
        if not size:
            size = Territory.size
        self.image = pygame.transform.smoothscale(image, size)
        self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))

        self.rect = self.image.get_rect(center = (self.x, self.y))

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
        return prev_rect


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
        return self.coords_of_cube(self.placement_order[idx])

    def remove_cube(self, cube_id):
        idx = self.temp_cube_list[cube_id]
        self.cube_list[idx] = None
        self.temp_cube_list[cube_id] = None
        # print(self.temp_cube_list)

    def remove_all_temp_cubes(self):
        for cube_id, cube_list_idx in enumerate(self.temp_cube_list):
            if cube_list_idx is not None:
                self.remove_cube(cube_id)

    def expand_hexes(self):
        # total number of hexes to create
        prev_n_hexes = len(self.coords_of_hexes)
        n_hexes = self.terr_size * 4

        if n_hexes <= prev_n_hexes:
            return

        self.coords_of_hexes = self.hex_coord_list[:n_hexes]
        for i in range(prev_n_hexes, n_hexes):
            self.add_hex_sprite(self.hex_coord_list[i])

    def add_hex_sprite(self, coords):
        self.hex_sprites.append(TerritoryHex(coords, self.hex_diameter))

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
            one_sixth_hex_coord_x = (n_rings - cos60 * i) * self.hex_diameter
            one_sixth_hex_coord_y = (sin60 * i) * self.hex_diameter
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