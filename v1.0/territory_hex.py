import pygame
import math

class TerritoryHex(pygame.sprite.Sprite):

    pngs = {
        0: "./sprites/hexes/singleTile01.png", # TODO: add textured pngs
    }

    def __init__(self, coords, hex_diameter):
        pygame.sprite.Sprite.__init__(self)
        self.coords = coords
        self.diameter = hex_diameter

        png_image = pygame.image.load(self.pngs[0]) #TODO: randomly select from textured pngs
        self.set_image(png_image)

    def clear(self):
        self.kill()

    def draw(self, group):
        self.add(group)

    def set_image(self, image, size = None):
        self.image = pygame.transform.smoothscale(image, (self.diameter, self.diameter))
        # self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))

        self.rect = self.image.get_rect(center = self.coords)