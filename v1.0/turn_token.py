from selectable import Selectable

class Token(Selectable):
    size = (30, 30)
    highlight_scale_factor = 1.5

class WhiteToken(Token):
    pngs = {
        -1: "./sprites/tokens/white_token_exhausted0.png",
        0:"./sprites/tokens/white_token01.png",
        1:"./sprites/tokens/white_token02.png",
        2:"./sprites/tokens/white_token03.png",
        3:"./sprites/tokens/white_token04.png",
        4:"./sprites/tokens/white_token05.png",
    }

class BlackToken(Token):
    pngs = {
        -1: "./sprites/tokens/black_token_exhausted0.png",
        0:"./sprites/tokens/black_token01.png",
        1:"./sprites/tokens/black_token02.png",
        2:"./sprites/tokens/black_token03.png",
        3:"./sprites/tokens/black_token04.png",
        4:"./sprites/tokens/black_token05.png",
    }

class GreyToken(Token):
   pngs = {
        -1: "./sprites/tokens/grey_token_exhausted0.png",
        0:"./sprites/tokens/grey_token01.png",
        1:"./sprites/tokens/grey_token02.png",
        2:"./sprites/tokens/grey_token03.png",
        3:"./sprites/tokens/grey_token04.png",
        4:"./sprites/tokens/grey_token05.png",
    }