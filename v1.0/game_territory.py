from game_player import GamePlayer
from cube_set import CubeSet

class GameTerritory():
    def __init__(self, starting_cube):
        self.size = 1
        self.cubes = CubeSet()
        self.cubes.add_cube(starting_cube)
        self.castles = 0
        self.owner = None

    def __repr__(self) -> str:
        # return f"GameTerritory with size {self.size} and {self.castles} {GamePlayer.team_dict[self.owner]} castles"
        return f"GameTerritory <{self.cubes}>"