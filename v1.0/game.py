from random import shuffle
from actions import Opening, CubeAction, Action
from game_player import GamePlayer
from game_state import GameState
from game_territory import GameTerritory
from cube_set import CubeSet

class Game():
    # only implementing two-player mode
    def __init__(self, nPlayers): # nPlayers is 2, 3, or 4
        self.nPlayers = nPlayers
        self.current_initiative_already_played_this_turn = set()
        self.current_players_already_played_this_turn = set()
        self.whose_turn = 0 # starting player

        self.n_territories = 15

        self.cube_supply = self.initialize_cube_supply()
        self.territories = self.initialize_territories()
        self.king = 0 # marker for which territory the king is on

        self.court_list = []
        for color_id in range(5):
            self.court_list.append([0] * self.nPlayers) # create a list of five (one per color) lists of nPlayers
        self.court_control_list = [None] * 5 # no one owns any territories in the beginning
        self.players = self.initialize_players()

    def initialize_cube_supply(self):
        cube_supply = []
        for color_id in range(5):
            cube_supply.extend([color_id] * 50)
        shuffle(cube_supply)
        return cube_supply

    def initialize_territories(self):
        territories = []
        for territory in range(self.n_territories):
            territories.append(GameTerritory(self.cube_supply.pop()))
        return territories

    def initialize_players(self):
        players = []
        for player_number in range(self.nPlayers):
            team_num = player_number % self.nPlayers
            starting_initiative = player_number
            players.append(GamePlayer(self, player_number, team_num, starting_initiative))
        return players

    def verify_action(self, action: Action):
        pass

    def handle_action(self, action: Action):
        # perform cube actions: either add each cube to the court or add it to a territory
        self.verify_action(action)
        acting_player:GamePlayer = self.players[action.player]
        for cube_action in action.cube_actions:
            if cube_action.court:
                acting_player.add_to_court(cube_action.color_id)
            else:
                acting_player.add_to_territory(cube_action.color_id, cube_action.terr_id)
        acting_player.replenish_cache(len(action.cube_actions))

        # perform king action: advance the king marker and check territory control
        self.move_king(action.king) #TODO: uncomment this line
        # self.whose_turn = self.next_player()
        self.whose_turn = (self.whose_turn + 1) % 2
        print("Game says it's player", self.whose_turn, "'s turn.!!!")

    def next_player(self):
        initiatives = [player.current_initiative for player in self.players]
        while len(initiatives) > 0:
            next_player_candidate = initiatives.index(min(initiatives))
            if next_player_candidate not in self.current_players_already_played_this_turn:
                self.current_players_already_played_this_turn.add(next_player_candidate)
                return next_player_candidate
            # else
            initiatives.pop(next_player_candidate) # and repeat

        # when all players have played, reset the turn order:
        self.current_players_already_played_this_turn = set()

    def verify_opening(opening: Opening):
        pass

    def handle_opening(self, opening: Opening):
        self.verify_opening(opening)
        self.players[opening.player].play_initiative(opening.inititative)

    def move_king(self, num_spaces):
        print("moving king!")
        # check game end criterion
        n_existing_territories = 0
        for territory in self.territories:
            if territory is not None:
                n_existing_territories += 1
        if n_existing_territories <= 4:
            print("The game is over!")

        # advance the king num_spaces steps, counting only territories that are not None (have not been merged)
        for step in range(num_spaces):
            self.king = (self.king + 1) % self.n_territories # move at least once
            while self.territories[self.king] is None:
                self.king = (self.king + 1) % self.n_territories

        # evaluate the result of the king's move (may initiate a merge)
        self.check_territory_owner(self.king, True)

    def check_territory_owner(self, terr_id, king = False):
        """Takes in a territory ID and returns the team (0, 1, or 2) with the most cubes and castles.
            Also handles merging if the conditions arise.
        """
        terr = self.territories[terr_id]

        prev_owner = terr.owner # used to check if the ownership changed

        # add up all cubes for each team
        total_cubes = [0, 0, 0]
        for color_id in range(5):
            for player in self.players:
                if self.court_control_list[color_id] == player.player_number:
                    total_cubes[player.team] += terr.cubes.get_cube_count(color_id)

        # add points for castles
        if terr.owner:
            total_cubes[terr.owner] += terr.castles

        # indices of teams with most cubes and castles
        owners = [index for index, cubes in enumerate(total_cubes) if cubes == max(total_cubes)]
        if len(owners) == 1: # only if there is a single, undisputed owner
            terr.owner = owners[0] # the first (and only) element in the list

            if king: # an optional argument that will add a castle and check merging (use if the king is landing on this square)
                if terr.castles <= 0:
                    terr.castles = 1
                self.check_merge_criterion(terr_id)
                self.check_castle_count()
        # if more than one player tied for highest number of cubes, the ownership doesn't change

    def check_merge_criterion(self, terr_id):
        terr = self.territories[terr_id]
        left_terr_id = (terr_id - 1) % len(self.territories)
        left_terr = self.territories[left_terr_id]
        right_terr_id = (terr_id + 1) % len(self.territories)
        right_terr = self.territories[right_terr_id]

        if left_terr.owner == terr.owner and (left_terr.castles > 0 and terr.castles > 0):
            self.merge_territories(terr, left_terr)
            self.territories[left_terr_id] = None # remove it from the list

        if right_terr.owner == terr.owner and (right_terr.castles > 0 and terr.castles > 0):
            self.merge_territories(terr, right_terr)
            self.territories[right_terr_id] = None # remove it from the list

    def merge_territories(self, terr_1, terr_2): # terr_2 is to be removed; all pieces migrate to terr_1

        terr_1.cubes.add_cubeSet(terr_2.cubes)
        terr_1.castles += terr_2.castles
        terr_1.size += terr_2.size

    def check_castle_count(self):
        castle_counts = [0, 0, 0]
        for terr in self.territories:
            if terr is None:
                continue
            if terr.owner and terr.castles:
                castle_counts[terr.owner] += terr.castles
        if max(castle_counts) > 10:
            winner = GamePlayer.team_dict[castle_counts.index(max(castle_counts))]
            print(f"{winner} won the game!")
        return castle_counts

    def get_game_state(self): # create a GameState object and return it
        return GameState(self.nPlayers, self.whose_turn, self.players, self.court_control_list, self.territories, self.king)

def main():
    print("Hello World!")
    g = Game(2)
    p1 = g.players[1]
    print(p1)
    p1.add_to_territory(1, 0)
    p1.add_to_territory(1, 0)
    p1.add_to_territory(4, 2)
    p1.add_to_territory(4, 2)
    p1.add_to_court(4)
    p1.add_to_court(1)
    print(p1.court)
    print(g.territories[0])
    print(g.territories[0].cubes)
    g.move_king(0)
    print(g.territories[0])

    pass

# main()