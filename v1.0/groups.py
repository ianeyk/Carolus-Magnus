import pygame

class Groups():
    def __init__(self, display) -> None:
        self.background_group = pygame.sprite.Group()
        self.cubes_group = pygame.sprite.Group()
        self.borders_group = pygame.sprite.Group()
        self.hex_group = pygame.sprite.Group()
        self.player_area_group = pygame.sprite.Group()
        self.castles = pygame.sprite.Group()
        self.king = pygame.sprite.Group()
        self.initiative_tokens = pygame.sprite.Group()
        self.court_section_group = pygame.sprite.Group()
        self.crown_group = pygame.sprite.Group()

        self.display = display

    def draw(self):
        # groups that are drawn first may be covered up by groups drawn later
        self.background_group.draw(self.display)
        self.borders_group.draw(self.display)
        self.hex_group.draw(self.display)
        self.player_area_group.draw(self.display)
        self.court_section_group.draw(self.display)
        self.crown_group.draw(self.display)
        self.initiative_tokens.draw(self.display)
        self.king.draw(self.display)
        self.castles.draw(self.display)
        self.cubes_group.draw(self.display)