import pygame

class Cube(pygame.sprite.Sprite):
    default_pngs = {
        0:"./sprites/cubes/green_cube1.png",
        1:"./sprites/cubes/red_cube1.png",
        2:"./sprites/cubes/blue_cube1.png",
        3:"./sprites/cubes/yellow_cube1.png",
        4:"./sprites/cubes/pink_cube1.png"
    }
    cache_pngs = {
        0:"./sprites/cache_cubes/green_cube2.png",
        1:"./sprites/cache_cubes/red_cube2.png",
        2:"./sprites/cache_cubes/blue_cube2.png",
        3:"./sprites/cache_cubes/yellow_cube2.png",
        4:"./sprites/cache_cubes/pink_cube2.png"
    }
    size = 15 # 13.4 # 12 # 17
    highlight_scale_factor = 1.5

    def __init__(self, x, y, color_id, png_path = None):
        pygame.sprite.Sprite.__init__(self) # Call the parent class (Sprite) constructor
        self.x = x
        self.y = y
        self.color_id = color_id
        self.highlighted = False

        if not png_path:
            png_path = Cube.default_pngs[color_id]
        self.png_image = pygame.image.load(png_path)
        self.image = self.get_image()
        self.rect = self.get_rect()
        # self.image = pygame.transform.smoothscale(png_image, (Cube.size, Cube.size))
        # self.rect = (x - Cube.size / 2, y - Cube.size / 2, Cube.size, Cube.size)

    def get_image(self):
        size = Cube.size * Cube.highlight_scale_factor if self.highlighted else Cube.size
        return pygame.transform.smoothscale(self.png_image, (int(size), int(size)))

    def get_rect(self):
        size = Cube.size * Cube.highlight_scale_factor if self.highlighted else Cube.size
        return (self.x - size / 2, self.y - size / 2, size, size)

    def highlight(self):
        self.highlighted = True
        self.rect = self.get_rect() # happens AFTER self.highlighted, so as to capture the larger highlighted updated rect
        self.image = self.get_image()
        return [self.rect] # has to be a list for antiquated reasons #TODO: make this not have to be a list

    def un_highlight(self):
        prev_rect = self.get_rect() # happens BEFORE self.highlighted, so as to capture the larger highlighted updated rect
        self.highlighted = False
        self.rect = self.get_rect()
        self.image = self.get_image()
        return [prev_rect]

    def update_pos(self, new_xy):
        prev_rect = self.get_rect()
        self.x = new_xy[0]
        self.y = new_xy[1]
        self.rect = self.get_rect()
        return [prev_rect, self.rect]