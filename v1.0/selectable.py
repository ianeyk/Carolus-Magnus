import pygame

class Selectable(pygame.sprite.Sprite):
    # overwrite these variables
    default_pngs = {
        0:"./sprites/cubes/green_cube1.png",
        1:"./sprites/cubes/red_cube1.png",
        2:"./sprites/cubes/blue_cube1.png",
        3:"./sprites/cubes/yellow_cube1.png",
        4:"./sprites/cubes/pink_cube1.png"
    }
    size = 15
    highlight_scale_factor = 1.5

    def __init__(self, x, y, ordinal_id, png_path_dict = None):
        pygame.sprite.Sprite.__init__(self) # Call the parent class (Sprite) constructor
        self.x = x
        self.y = y
        self.ordinal_id = ordinal_id
        self.highlighted = False

        if not png_path_dict:
            png_path_dict = self.default_pngs
        self.png_image = pygame.image.load(png_path_dict[self.ordinal_id])
        self.image = self.get_image()
        self.rect = self.get_rect()

    def get_image(self):
        size = self.size * self.highlight_scale_factor if self.highlighted else self.size
        return pygame.transform.smoothscale(self.png_image, (int(size), int(size)))

    def get_rect(self):
        size = self.size * self.highlight_scale_factor if self.highlighted else self.size
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