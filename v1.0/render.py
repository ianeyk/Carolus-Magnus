import pygame
from random import randrange

from playerArea import PlayerArea
from territory import Territory
from map import Map
from game_state import GameState
from groups import Groups
from territory_hex import King

class Render(pygame.sprite.Sprite):

    pngs = {
        0: "./sprites/background1.png",
        1: "./sprites/background_your_turn.png"
    }

    def __init__(self, width: int, height: int, game_state: GameState) -> None:
        pygame.sprite.Sprite.__init__(self) # Call the parent class (Sprite) constructor

        self.width = width
        self.height = height
        self.game_state = game_state
        self.nPlayers = game_state.nPlayers

        self.set_image(0)
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

        self.king_loc = 0
        self.king_width = 35
        self.king = King((self.map.territories[self.king_loc].x, self.map.territories[self.king_loc].y), self.king_width)

    def set_image(self, i):
        png_image = pygame.image.load(self.pngs[i])
        self.image = pygame.transform.smoothscale(png_image, (self.width, self.height))

    def update_game_state(self, game_state: GameState) -> None:
        print("render is updating game state")
        for (player_area, game_player) in zip(self.player_areas, game_state.players):
            player_area.update(game_player)

        for color_id, controlling_player in enumerate(game_state.court_control_list):
            if controlling_player is not None:
                self.player_areas[controlling_player].show_control(color_id)

        self.map.update(game_state.territories)

        self.move_king(game_state.king)
        pass
    # def __init__(self, nPlayers, whose_turn, players, court_control_list, territories, king):

    def move_king(self, new_loc):
        self.king_loc = new_loc
        terr = self.map.territories[self.king_loc]
        coords = self.map.get_xy_by_angle_index(terr.outer_angle_index, terr.outer_radius - 60)
        self.king.move_center(coords)

    def draw(self, groups: Groups) -> None:
        self.add(groups.background_group)
        self.map.draw(groups)
        self.king.draw(groups.king)
        # self.terr.draw(group)
        for player_area in self.player_areas:
            player_area.draw(groups)