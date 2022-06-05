import pygame

class Player():
    def __init__(self):
        self.selected_cube = None
        self.game_state = 0
        self.selected_cube = 0

    def select_cube(self):
        total_cubes = 7
        event = pygame.event.poll()
        print(event)
        if event.type != pygame.KEYDOWN:
            return False

        if event.key == pygame.K_LEFT:
            self.selected_cube = (self.selected_cube - 1) % total_cubes
            # self.local_interface.select_cube(self.selected_cube)
            self.down = False
            return True

        if event.key == pygame.K_RIGHT:
            self.selected_cube = (self.selected_cube + 1) % total_cubes
            # self.local_interface.select_cube(self.selected_cube)
            self.down = False
            return True

        if event.key == pygame.K_UP:
            # self.local_interface.send_to_territory(self.selected_cube)
            # self.select_territory()
            self.down = False
            return True

        if event.key == pygame.K_DOWN:
            # self.local_interface.send_to_court(self.selected_cube)
            self.down = True
            return True

        return False

    def select_territory(self):
        total_territories = len(self.game_state.territories)
        self.selected_territory = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.selected_territory = (self.selected_territory + 1) % total_territories
            self.local_interface.select_terr(self.selected_territory)

        if keys[pygame.K_RIGHT]:
            self.selected_territory = (self.selected_territory + 1) % total_territories
            self.local_interface.select_terr(self.selected_territory)

        if keys[pygame.K_UP]:
            self.local_interface.undo_terr(self.selected_territory)
            self.select_territory()

        if keys[pygame.K_DOWN]:
            self.local_interface.add_to_terr(self.selected_territory)

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

# class LocalInterface():
#     def __init__(self, court_cubes, cache_cubes)