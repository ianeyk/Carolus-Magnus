class GameCubeAction():
    def __init__(self, color_id, cube_placement, terr_id = None):
        self.color_id = color_id
        self.cube_placement = cube_placement
        self.terr_id = terr_id


class GameCubeActions():
    def __init__(self, cube_actions, king_movement):
        self.cube_actions = cube_actions
        self.king_movement = king_movement

    def check(self):
        assert(len(self.cube_actions == 3))
        assert(self.king_movement >= 1 and self.king_movement <= 5)