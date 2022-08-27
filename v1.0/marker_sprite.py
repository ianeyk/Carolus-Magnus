import pygame

class MarkerSprite(pygame.sprite.Sprite):

    pngs = {
        0: "./sprites/hexes/topographic-map-tile01.png"
    }

    def __init__(self, coords, width, height_factor = 1, png_id = 0, visible = True):
        pygame.sprite.Sprite.__init__(self)
        self.coords = coords
        self.width = width
        self.height = self.width * height_factor
        self.png_id = png_id
        self.visible = visible

        self.set_image()

    def draw(self, group):
        if self.visible:
            self.add(group)
        else:
            self.kill()

    def set_image(self):
        png_image = pygame.image.load(self.pngs[self.png_id])
        self.image = pygame.transform.smoothscale(png_image, (self.width, self.height))
        self.rect = self.image.get_rect(center = self.coords)

    def move_center(self, coords):
        self.coords = coords
        self.rect = self.image.get_rect(center = self.coords)

class Crown(MarkerSprite):
    pngs = {
        0: "./sprites/crowns/green_crown1.png",
        1: "./sprites/crowns/red_crown1.png",
        2: "./sprites/crowns/blue_crown1.png",
        3: "./sprites/crowns/yellow_crown1.png",
        4: "./sprites/crowns/pink_crown1.png"
    }