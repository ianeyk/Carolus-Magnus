import pygame

class Groups():
    def __init__(self, display) -> None:
        self.background_group = pygame.sprite.Group()
        self.cubes_group = pygame.sprite.Group()
        self.borders_group = pygame.sprite.Group()
        self.hex_group = pygame.sprite.Group()
        self.player_area_group = pygame.sprite.Group()

        self.display = display

    def draw(self):
        self.background_group.draw(self.display)
        self.borders_group.draw(self.display)
        self.hex_group.draw(self.display)
        self.player_area_group.draw(self.display)
        self.cubes_group.draw(self.display)