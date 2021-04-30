import pygame.image as pgi
import pygame as pg

import os

# define some colors (R, G, B)
colors = {
    'WHITE': (240, 240, 240),
    'BLACK': (15, 15, 15),
    'DARK_GREY': (50, 50, 50),
    'LIGHT_GREY': (100, 100, 100),
    'BLUE': (0, 0, 220),
    'GREEN': (0, 220, 0),
    'RED': (220, 0, 0),
    'YELLOW': (220, 220, 0)
}

# keep aspect ratio as 4:3
window = {
    'TITLE': "No title",
    'GAME_LOGO': pgi.load(os.path.join(os.path.dirname(__file__), 'Assets/Images/logo.png')),
    'WIDTH': 1024,
    'HEIGHT':  768,
    'TILESIZE': 32,
}
window.update({
    'GRIDWIDTH': window['WIDTH'] / window['TILESIZE'],
    'GRIDHEIGHT': window['HEIGHT'] / window['TILESIZE']
})


# game settings
options = {
    'FPS': 60,
    'PLAYER_SPEED': 475,
    'PLAYER_ROT_SPEED': 250,
    'PLAYER_IMG': 'Second Option.png',
    'PLAYER_HIT_RECT': pg.Rect(0, 0, 35, 35),
    'WALL_IMG': 'tile32.png',
    'AVLC_IMG': 'scroll-avlc.png',
    'MD_IMG': 'scroll-md.png',
    'CALC_IMG': 'scroll-calc.png',
    'PAPIRO': 'papiro.png',
    'PARTITURA': 'partitura.png',
    'SEMINIMA': 'seminima.png'
}

