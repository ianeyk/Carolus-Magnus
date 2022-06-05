import pygame
import math

class Cube(pygame.sprite.Sprite):
    pngs = {
        0:"./sprites/green_cube1.png",
        1:"./sprites/red_cube1.png",
        2:"./sprites/blue_cube1.png",
        3:"./sprites/yellow_cube1.png",
        4:"./sprites/pink_cube1.png",
    }
    size = 17

    def __init__(self, x, y, color_id):
        pygame.sprite.Sprite.__init__(self) # Call the parent class (Sprite) constructor
        self.x = x
        self.y = y
        self.color_id = color_id
        self.highlighted = False

        self.png_image = pygame.image.load(Cube.pngs[color_id])
        self.image = self.get_image(Cube.size)
        self.rect = None # used to set self.prev_rect in the next function
        self.rect = self.get_rect(Cube.size)
        # self.image = pygame.transform.smoothscale(png_image, (Cube.size, Cube.size))
        # self.rect = (x - Cube.size / 2, y - Cube.size / 2, Cube.size, Cube.size)

    def get_image(self, size):
        return pygame.transform.smoothscale(self.png_image, (math.floor(size), math.floor(size)))

    def get_rect(self, size):
        self.prev_rect = self.rect
        return (self.x - size / 2, self.y - size / 2, size, size)

    def highlight(self):
        self.highlighted = True
        self.rect = self.get_rect(Cube.size * 1.5)
        self.image = self.get_image(Cube.size * 1.5)
        return [self.prev_rect, self.rect]

    def un_highlight(self):
        # prev_rect = self.rect
        self.highlighted = False
        self.rect = self.get_rect(Cube.size)
        self.image = self.get_image(Cube.size)
        return [self.prev_rect, self.rect]

    def update_pos(self, new_xy):
        self.x = new_xy[0]
        self.y = new_xy[1]
        self.rect = self.get_rect(Cube.size * 1.5 if self.highlighted else Cube.size)
        return [self.prev_rect, self.rect]