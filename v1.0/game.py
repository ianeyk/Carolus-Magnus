from random import shuffle

class Opening():
    def __init__(self, player: int, initiative: int):
        self.player = player
        self.inititative = initiative

class CubeAction():
    def __init__(self, color_id: int, court: bool = False, terr_id: int = 0):
        self.color_id = color_id
        self.court = court
        self.terr_id = terr_id

class Action():
    def __init__(self, player: int, cube_actions: tuple[CubeAction, CubeAction, CubeAction], king: int):
        self.player = player
        self.cube_actions = cube_actions
        self.king = king

class Game():
    # only implementing two-player mode
    def __init__(self, nPlayers): # nPlayers is 2, 3, or 4
        self.nPlayers = nPlayers
        self.current_initiative_already_played_this_turn = set()
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
        for territory in range(15):
            territories.append(Territory(self.cube_supply.pop()))
        return territories

    def initialize_players(self):
        players = []
        for player_number in range(self.nPlayers):
            color_num = player_number % self.nPlayers
            color = color_num
            starting_initiative = player_number
            players.append(Player(self, player_number, color, starting_initiative))
        return players

    def verify_action(self, action: Action):
        pass

    def handle_action(self, action: Action):
        # perform cube actions: either add each cube to the court or add it to a territory
        self.verify_action(action)
        for cube_action in action.cube_actions:
            if cube_action.court:
                self.players[action.player].add_to_court(cube_action.color_id)
            else:
                self.players[action.player].add_to_territory(cube_action.color_id, cube_action.terr_id)
        self.replenish_cache(len(action.cube_actions))

        # perform king action: advance the king marker and check territory control
        self.move_king(action.king)

    def verify_opeining(opening: Opening):
        pass

    def handle_opening(self, opening: Opening):
        self.verify_opening(opening)
        self.players[opening.player].play_initiative(opening.inititative)

    def move_king(self, num_spaces):
        self.king += num_spaces
        self.check_territory_owner(self.king)

    def check_territory_owner(self, terr_id, king = False):
        """
        takes in a territory ID and returns the team (0, 1, or 2) with the most cubes and castles
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
        if len(owners) == 1:
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
            self.territories.pop(left_terr_id) # remove it from the list
            if left_terr_id < terr_id: # reposition the king if needed
                self.king -= 1

        if right_terr.owner == terr.owner and (right_terr.castles > 0 and terr.castles > 0):
            self.merge_territories(terr, right_terr)
            self.territories.pop(right_terr_id) # remove it from the list
            if right_terr_id < terr_id: # reposition the king if needed
                self.king -= 1


    def merge_territories(self, terr_1, terr_2): # idx_1 and idx_2 are territory indices
        # terr_1 = self.territories[idx_1]
        # terr_2 = self.territories.pop(idx_2) # remove it from the list

        terr_1.cubes.add_cubeSet(terr_2.cubes)
        terr_1.castles += terr_2.castles
        terr_1.size += terr_2.size

    def check_castle_count(self):
        castle_counts = [0, 0, 0]
        for terr in self.territories:
            if terr.owner and terr.castles:
                castle_counts[terr.owner] += terr.castles
        if max(castle_counts) > 10:
            winner = Player.team_dict[castle_counts.index(max(castle_counts))]
            print(f"{winner} won the game!")
        return castle_counts


class Territory():
    def __init__(self, starting_cube):
        self.size = 1
        self.cubes = CubeSet()
        self.cubes.add_cube(starting_cube)
        self.castles = 0
        self.owner = None

    def __repr__(self) -> str:
        return f"Territory with size {self.size} and {self.castles} {Player.team_dict[self.owner]} castles"

class CubeSet():
    color_dict = {0:"green", 1:"red", 2:"blue", 3:"yellow", 4:"pink"}

    def __init__(self):
        self.cubes = [0, 0, 0, 0, 0]

    def add_cube(self, color_id):
        self.cubes[color_id] += 1

    def remove_cube(self, color_id):
        if self.cubes[color_id] <= 0:
            print("Tried to remove a cube when there are no cubes of that color")
        self.cubes[color_id] -= 1

    def get_cube_count(self, color_id):
        return self.cubes[color_id]

    def add_cubeSet(self, other):
        for color_id in range(5):
            self.cubes[color_id] += other.cubes[color_id]

    def __repr__(self):
        return f"<CubeSet with {self.cubes[0]} green, {self.cubes[1]} red, {self.cubes[2]} blue, {self.cubes[3]} yellow, {self.cubes[4]} pink>"

class Player():
    team_dict = {0:"White", 1:"Black", 2:"Gray", None:"Neutral"}
    # dict_team = {v: k for k, v in team_dict.items()}

    def __init__(self, game, player_number, team, starting_initiative): # team is either 0, 1, or 2
        self.game = game
        self.player_number = player_number
        self.team = team
        self.initiative_tokens = {1, 2, 3, 4, 5}
        self.used_initiative_tokens = set()
        self.current_initiative = starting_initiative

        # cube sets
        self.court = CubeSet() # exert control
        self.cache = CubeSet() # stored for deployment; start with 7 random cubes
        self.replenish_cache(7 if self.game.nPlayers in [2, 4] else 9)

    def __repr__(self):
        return f"Player {self.player_number}, team {Player.team_dict[self.team]}"

    def play_initiative(self, initiative):
        # check for valid initiative marker
        if initiative not in self.initiative_tokens:
            print("Tried to take an ititiative that you have already used or is out of range")
        if initiative in self.game.current_initiative_already_played_this_turn:
            print("Someone else has already played that initiative marker this turn")

        self.initiative_tokens -= {initiative} # remove the initiative marker from play
        self.used_initiative_tokens += {initiative} # and add it to the used stack
        self.game.current_initiative_already_played_this_turn += {initiative}
        self.turn_order = initiative

    def replenish_cache(self, n):
        for cube in range(n):
            color_id = self.game.cube_supply.pop()
            self.cache.add_cube(color_id)

    def add_to_court(self, color_id):
        # check ownership
        if self.court.get_cube_count(color_id) == max(self.game.court_list[color_id]):
            # you are now in control (after adding your cube)
            self.game.court_control_list[color_id] = self.player_number

        # add cube
        self.cache.remove_cube(color_id)
        self.court.add_cube(color_id)
        self.game.court_list[color_id][self.player_number] += 1
        return True

    def add_to_territory(self, color_id, terr_id):
        # place the cube in the territory
        self.cache.remove_cube(color_id)
        self.game.territories[terr_id].cubes.add_cube(color_id)


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
    g.check_territory_owner(0)
    print(g.territories[0])

    pass

main()