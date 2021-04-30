import pygame as pg
import pytmx
import numpy as np

from settings import window

def collide_hit_rect(sprite_one, sprite_two):
    '''
    Updated Collision checker based on a fixed square (Creates something like a hit box)
    '''

    return sprite_one.hit_rect.colliderect(sprite_two.rect)

def load_occupation_map(filename):
    return np.load(filename).tolist()


class Map:
    '''
    Reader and builder for txt file-based maps (UNUSED).
    '''

    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * window['TILESIZE']
        self.height = self.tileheight * window['TILESIZE']


class TiledMap:
    '''
    Map creation and rendering based on the pytmx package.
    '''
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)  # Loads the TMX file
        self.width = tm.width * tm.tilewidth  # Gets its dimension
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm  # Assign the data to a variable

    def render_map(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):  # Checking for layers
                for x, y, gid, in layer:  # Locating tile coordenates
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render_map(temp_surface)
        return temp_surface

class Camera:
    '''
    Player follower camera.
    '''
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(window['WIDTH'] / 2)
        y = -target.rect.centery + int(window['HEIGHT'] / 2)

        # Limiting scrolling to map size
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - window['WIDTH']), x)
        y = max(-(self.height - window['HEIGHT']), y)
        self.camera = pg.Rect(x, y, self.width, self.height)
