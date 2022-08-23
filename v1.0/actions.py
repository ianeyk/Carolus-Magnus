class Opening():
    def __init__(self, player: int, initiative: int):
        self.player = player
        self.inititative = initiative

    def __repr__(self) -> str:
        return f"Opening <Player {self.player} played {self.inititative}>"

class CubeAction():
    def __init__(self, color_id: int, court: bool = False, terr_id: int = 0):
        self.color_id = color_id
        self.court = court
        self.terr_id = terr_id

    def __repr__(self) -> str:
        if self.court:
            return f"CubeAction <Cube color {self.color_id} placed in court>"
        # else:
        return f"CubeAction <Cube color {self.color_id} placed on territory {self.terr_id}>"


class Action():
    def __init__(self, player: int, cube_actions: tuple[CubeAction, CubeAction, CubeAction], king: int):
        self.player = player
        self.cube_actions = cube_actions
        self.king = king

    def __repr__(self) -> str:
        return \
f"""Action <Player {self.player} made the following moves:
{self.cube_actions[0]},
{self.cube_actions[1]},
{self.cube_actions[2]},
King moved to {self.king}>"""

