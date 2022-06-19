from selectable import Selectable

class WhiteToken(Selectable):
    pngs = {
        0:"./sprites/tokens/white_token01.png",
        1:"./sprites/tokens/white_token02.png",
        2:"./sprites/tokens/white_token03.png",
        3:"./sprites/tokens/white_token04.png",
        4:"./sprites/tokens/white_token05.png",
    }
    size = (30, 30)
    highlight_scale_factor = 1.5

class BlackToken(WhiteToken):
    pngs = {
        0:"./sprites/tokens/black_token01.png",
        1:"./sprites/tokens/black_token02.png",
        2:"./sprites/tokens/black_token03.png",
        3:"./sprites/tokens/black_token04.png",
        4:"./sprites/tokens/black_token05.png",
    }

class GreyToken(WhiteToken):
   pngs = {
        0:"./sprites/tokens/grey_token01.png",
        1:"./sprites/tokens/grey_token02.png",
        2:"./sprites/tokens/grey_token03.png",
        3:"./sprites/tokens/grey_token04.png",
        4:"./sprites/tokens/grey_token05.png",
    }