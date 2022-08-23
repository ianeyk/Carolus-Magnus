from typing import List
from game_player import GamePlayer

class GameState():
    def __init__(self, nPlayers, whose_turn, players: List[GamePlayer], court_control_list, territories, king):
        self.nPlayers = nPlayers
        # self.whose_turn = whose_turn
        self.whose_turn = 0
        self.players = players
        self.court_control_list = court_control_list
        self.territories = territories
        self.king = king

    def __repr__(self) -> str:
        return \
f"""GameState <court: {self.players[self.whose_turn].court},
cache: {self.players[self.whose_turn].cache},
territories: {self.territories}>"""













