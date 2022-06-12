import pygame
from random import randrange

from playerArea import PlayerArea
from territory import Territory
from map import Map

class Render(pygame.sprite.Sprite):

    def __init__(self, width, height, game_state):
        pygame.sprite.Sprite.__init__(self) # Call the parent class (Sprite) constructor

        self.width = width
        self.height = height
        self.game_state = game_state

        png_image = pygame.image.load("./sprites/background1.png")
        self.image = pygame.transform.smoothscale(png_image, (width, height))
        self.rect = (0, 0, *PlayerArea.size)

        # initialize player boards
        p0_center = (self.width * 1 / 8, self.height * 1 / 4)
        p1_center = (self.width * 1 / 8, self.height * 3 / 4)
        p2_center = (self.width * 7 / 8, self.height * 1 / 4)
        p3_center = (self.width * 7 / 8, self.height * 3 / 4)

        self.players = []
        for player_number, center in enumerate([p0_center, p1_center, p2_center, p3_center]):
            team = player_number % 2
            cube_counts = [randrange(0, 18) for i in range(5)]
            cache_list = sorted([randrange(0, 4) for i in range(7)])
            self.players.append(PlayerArea(*center, team, cube_counts, cache_list))

        self.map = Map(self.width / 2, self.height / 2, [0] * 15)
        self.terr = Territory(self.width / 2, self.height / 2, 0, 4)

    def draw(self):
        group = pygame.sprite.Group()
        self.add(group)
        self.map.draw(group)
        self.terr.draw(group)
        for player in self.players:
            player.draw(group)
        return group
pass