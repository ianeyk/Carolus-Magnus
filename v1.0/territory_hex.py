import pygame
import math
import random

class HexSprite(pygame.sprite.Sprite):

    pngs = {
        0: "./sprites/hexes/topographic-map-tile01.png"
    }

    def __init__(self, coords, hex_diameter, background_style = 0, background_rotation = 0):
        pygame.sprite.Sprite.__init__(self)
        self.coords = coords
        self.diameter = hex_diameter
        self.background_style = background_style
        self.background_rotation = background_rotation

        self.set_image()

    def clear(self):
        self.kill()

    def draw(self, group):
        self.add(group)

    def set_image(self):
        png_image = pygame.image.load(self.pngs[self.background_style])

        self.image = pygame.transform.smoothscale(png_image, (self.diameter, self.diameter))
        self.image = pygame.transform.rotate(self.image, self.background_rotation * 60)

        self.rect = self.image.get_rect(center = self.coords)

    def move_center(self, coords):
        self.coords = coords
        self.rect = self.image.get_rect(center = self.coords)

class TerritoryHex(HexSprite):

    pngs = {
        0: "./sprites/hexes/topographic-map-tile01.png",
        1: "./sprites/hexes/topographic-map-tile02.png",
        2: "./sprites/hexes/topographic-map-tile03.png",
        3: "./sprites/hexes/topographic-map-tile04.png",
        4: "./sprites/hexes/topographic-map-tile05.png",
        5: "./sprites/hexes/sand-dune-map-tile06.png",
    }

    def __init__(self, coords, hex_diameter, background_style = 0, background_rotation = 0):
        HexSprite.__init__(self, coords, hex_diameter, background_style, background_rotation)
        if self.background_style == 5:
            self.background_rotation = 0

        png_image = pygame.image.load(self.pngs[self.background_style])
        self.set_image()

    def get_cube_slots(self):
        cube_coords = []
        for i in range(3):
            theta = 2 * math.pi / 3 * i # - math.pi / 6
            cube_coords.append((
                self.coords[0] + math.cos(theta) * self.diameter / 2,
                self.coords[1] + math.sin(theta) * self.diameter / 2
            ))
        return cube_coords

class TerritoryBorder(HexSprite):

    pngs = {
        0: "./sprites/hexes/border_color_hex.png",
        1: "./sprites/hexes/selected_color_hex.png",
    }

    def highlight(self):
        self.background_style = 1
        self.set_image()

    def un_highlight(self):
        self.background_style = 0
        self.set_image()

class Castle(HexSprite):

    pngs = {
        0: "./sprites/castles/whiteCastle1.png",
        1: "./sprites/castles/blackCastle1.png",
        2: "./sprites/castles/greyCastle1.png",
    }

    def set_image(self):
        png_image = pygame.image.load(self.pngs[self.background_style])
        self.image = pygame.transform.smoothscale(png_image, (self.diameter, self.diameter))
        self.rect = self.image.get_rect(center = self.coords)

    def set_color(self, team_color):
        self.background_style = team_color
        self.set_image()


class King(HexSprite):

    pngs = {
        0: "./sprites/castles/king1.png",
        1: "./sprites/castles/king_highlighted.png",
    }

    def set_image(self):
        png_image = pygame.image.load(self.pngs[self.background_style])
        self.image = pygame.transform.smoothscale(png_image, (self.diameter, self.diameter * 3))
        self.rect = self.image.get_rect(center = self.coords)

    def highlight(self):
        self.background_style = 1
        self.set_image()

    def un_highlight(self):
        self.background_style = 0
        self.set_image()