import pygame
from random import randrange

from playerArea import PlayerArea
from territory import Territory
from map import Map
from game_state import GameState

class Render(pygame.sprite.Sprite):

    def __init__(self, width: int, height: int, game_state: GameState) -> None:
        pygame.sprite.Sprite.__init__(self) # Call the parent class (Sprite) constructor

        self.width = width
        self.height = height
        self.game_state = game_state
        self.nPlayers = game_state.nPlayers

        png_image = pygame.image.load("./sprites/background1.png")
        self.image = pygame.transform.smoothscale(png_image, (width, height))
        self.rect = (0, 0, *PlayerArea.size)

        # initialize player boards
        p0_center = (self.width * 1 / 8, self.height * 1 / 4)
        p1_center = (self.width * 1 / 8, self.height * 3 / 4)
        p2_center = (self.width * 7 / 8, self.height * 1 / 4)
        p3_center = (self.width * 7 / 8, self.height * 3 / 4)

        self.player_areas = []
        for player_number, center in enumerate([p0_center, p1_center, p2_center, p3_center]):
            team = player_number % 2
            cube_counts = game_state.players[player_number].court.get_cubes()
            # cube_counts = [randrange(0, 18) for i in range(5)]
            cache_list = game_state.players[player_number].cache.get_cube_list()
            # cache_list = sorted([randrange(0, 4) for i in range(7)])
            self.player_areas.append(PlayerArea(*center, team, cube_counts, cache_list))

        self.map = Map(self.width / 2, self.height / 2, [0] * 15)
        # self.terr = Territory(self.width / 2, self.height / 2, 0, 4)

    def update_game_state(self, game_state: GameState) -> None:
        print("render is updating game state")
        for (player_area, game_player) in zip(self.player_areas, game_state.players):
            player_area.update(game_player)
        self.map.update(game_state.territories)
    # def __init__(self, nPlayers, whose_turn, players, court_control_list, territories, king):

    def draw(self, group: pygame.sprite.Group) -> None:
        self.add(group)
        self.map.draw(group)
        # self.terr.draw(group)
        for player_area in self.player_areas:
            player_area.draw(group)