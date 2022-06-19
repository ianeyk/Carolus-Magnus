import pygame
from selectable import Selectable

class Cube(Selectable):
    pngs = {
        0:"./sprites/cubes/green_cube1.png",
        1:"./sprites/cubes/red_cube1.png",
        2:"./sprites/cubes/blue_cube1.png",
        3:"./sprites/cubes/yellow_cube1.png",
        4:"./sprites/cubes/pink_cube1.png"
    }
    size = 15 # 13.4 # 12 # 17
    highlight_scale_factor = 1.5

class CacheCube(Cube):
    pngs = {
        0:"./sprites/cache_cubes/green_cube2.png",
        1:"./sprites/cache_cubes/red_cube2.png",
        2:"./sprites/cache_cubes/blue_cube2.png",
        3:"./sprites/cache_cubes/yellow_cube2.png",
        4:"./sprites/cache_cubes/pink_cube2.png"
    }