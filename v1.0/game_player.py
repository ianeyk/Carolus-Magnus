from cube_set import CubeSet

class GamePlayer():
    team_dict = {0:"White", 1:"Black", 2:"Gray", None:"Neutral"}
    # dict_team = {v: k for k, v in team_dict.items()}

    def __init__(self, game, player_number, team, starting_initiative): # team is either 0, 1, or 2
        self.game = game
        self.player_number = player_number
        self.team = team
        self.initiative_tokens = {1, 2, 3, 4, 5}
        self.used_initiative_tokens = []
        self.current_initiative = starting_initiative

        # cube sets
        self.court = CubeSet() # exert control
        self.cache = CubeSet() # stored for deployment; start with 7 random cubes
        self.replenish_cache(7 if self.game.nPlayers in [2, 4] else 9)

    def __repr__(self):
        return f"GamePlayer {self.player_number}, team {GamePlayer.team_dict[self.team]}"

    def play_initiative(self, initiative):
        # check for valid initiative marker
        if initiative not in self.initiative_tokens:
            print("Tried to take an ititiative that you have already used or is out of range")
        if initiative in self.game.current_initiative_already_played_this_turn:
            print("Someone else has already played that initiative marker this turn")

        self.initiative_tokens.remove(initiative) # remove the initiative marker from play
        self.used_initiative_tokens.append(initiative) # and add it to the used stack
        self.game.current_initiative_already_played_this_turn.add(initiative)
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
