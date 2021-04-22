# define some colors (R, G, B)
import pygame as pg

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 1024  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12

FPS = 60
TITLE = "O Monitorado"
Game_Logo = pg.image.load('labyrinth.png')
BGCOLOR = DARKGREY

TILESIZE = 32

GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

Wall_Img = 'tile32.png'

# Player Settings
PLAYER_SPEED = 500
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'Second Option.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
