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


