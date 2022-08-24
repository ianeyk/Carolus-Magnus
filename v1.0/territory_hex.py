import pygame
import math
import random

class TerritoryHex(pygame.sprite.Sprite):

    pngs = {
        0: "./sprites/hexes/topographic-map-tile01.png",
        1: "./sprites/hexes/topographic-map-tile02.png",
        2: "./sprites/hexes/topographic-map-tile03.png",
        3: "./sprites/hexes/topographic-map-tile04.png",
        4: "./sprites/hexes/topographic-map-tile05.png",
        5: "./sprites/hexes/sand-dune-map-tile06.png",
    }

    def __init__(self, coords, hex_diameter, background_style = 0):
        pygame.sprite.Sprite.__init__(self)
        self.coords = coords
        self.diameter = hex_diameter
        self.background_style = background_style
        self.background_rotation = 0 if background_style == 5 else random.randrange(0, 6)

        png_image = pygame.image.load(self.pngs[self.background_style]) #TODO: randomly select from textured pngs
        self.set_image(png_image)

    def clear(self):
        self.kill()

    def draw(self, group):
        self.add(group)

    def set_image(self, image, size = None):
        self.image = pygame.transform.smoothscale(image, (self.diameter, self.diameter))
        self.image = pygame.transform.rotate(self.image, self.background_rotation * 60)
        # self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))

        self.rect = self.image.get_rect(center = self.coords)

    def get_cube_slots(self):
        cube_coords = []
        for i in range(3):
            theta = 2 * math.pi / 3 * i # - math.pi / 6
            cube_coords.append((
                self.coords[0] + math.cos(theta) * self.diameter / 2,
                self.coords[1] + math.sin(theta) * self.diameter / 2
            ))
        return cube_coords