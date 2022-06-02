import pygame

class Player():
    def __init__(self):
        self.selected_cube = None
        self.game_state = 0

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def select_cube(self):
        total_cubes = 7
        self.selected_cube = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.selected_cube = (self.selected_cube + 1) % total_cubes
            self.local_interface.select(self.selected_cube)

        if keys[pygame.K_RIGHT]:
            self.selected_cube = (self.selected_cube + 1) % total_cubes
            self.local_interface.select(self.selected_cube)

        if keys[pygame.K_UP]:
            self.local_interface.send_to_territory(self.selected_cube)
            self.select_territory()

        if keys[pygame.K_DOWN]:
            self.local_interface.send_to_court(self.selected_cube)

    def select_territory(self):
        total_territories = len(self.game_state.territories)
        self.selected_territory = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.selected_cube = (self.selected_cube + 1) % total_cubes
            self.local_interface.select(self.selected_cube)

        if keys[pygame.K_RIGHT]:
            self.selected_cube = (self.selected_cube + 1) % total_cubes
            self.local_interface.select(self.selected_cube)

        if keys[pygame.K_UP]:
            self.local_interface.send_to_territory(self.selected_cube)
            self.select_territory()

        if keys[pygame.K_DOWN]:
            self.local_interface.send_to_court(self.selected_cube)

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)