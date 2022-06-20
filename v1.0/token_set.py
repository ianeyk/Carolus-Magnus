from cube import Cube
from turn_token import WhiteToken, BlackToken, GreyToken, Token

class TokenSet(): # Turn Token

    spacing = 1.5

    def __init__(self, team, x, y, size, token_set):
        self.x = x
        self.y = y
        self.team = team
        self.token_set = token_set # list of 5 ordinal numbers
        self.nTokens = len(self.token_set)
        self.size = size
        self.prev_selected_token = 0

        self.token_type = [WhiteToken, BlackToken, GreyToken][team]

        self.token_locs = self.generate_token_locs()
        self.token_list = [] # list of cube objects for highlighting purposes
        for loc, ordinal_id in zip(self.token_locs, self.token_set):
            token = self.token_type(*loc, ordinal_id)
            self.token_list.append(token)

    def draw(self, group):
        for token in self.token_list:
            token.add(group)

    def generate_token_locs(self):
        locs = []
        for pos in range(self.nTokens):
            locs.append((self.x + (pos - self.nTokens // 2) * Token.size[0] * self.spacing, self.y + Token.size[1] / 2))
        return locs

    def select(self, which_token): # which_token is an index from 0 to 6, indicating which cube in the cache has been selected
        # updated_rects = self.deselect_all() # unhighlight all cubes
        updated_rects = self.token_list[self.prev_selected_token].un_highlight() # unhighlight the previous cube
        updated_rects.extend(self.token_list[which_token].highlight()) # then highlight the interesting cube
        self.prev_selected_token = which_token
        return updated_rects # returns the rect containing the highlighted cube, for pygame.display.update() in the main loop

    def deselect_all(self):
        updated_rects = []
        for other_cube in self.token_list:
            updated_rects.extend(other_cube.un_highlight())
        return updated_rects