class GameCubeActions():
    def __init__(self, cube_actions, king_movement):
        self.cube_actions = cube_actions
        self.king_movement = king_movement

    def check(self):
        assert(len(self.cube_actions == 3))
        assert(self.king_movement >= 1 and self.king_movement <= 5)